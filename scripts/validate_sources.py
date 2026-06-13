#!/usr/bin/env python3
"""Validate stock-deepread research JSON before rendering."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

VALID_GRADES = {"A", "B", "C", "D", "E"}
CORE_SAFE_GRADES = {"A", "B", "C"}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def source_map(data: dict) -> dict:
    return {str(src.get("id")): src for src in data.get("sources", []) if src.get("id") is not None}


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("sources must be a non-empty list")
        return errors

    seen_ids = set()
    for index, src in enumerate(sources, start=1):
        sid = str(src.get("id", "")).strip()
        if not sid:
            errors.append(f"source #{index} missing id")
        elif sid in seen_ids:
            errors.append(f"duplicate source id: {sid}")
        seen_ids.add(sid)

        for key in ("title", "url", "date", "source_type", "evidence_grade", "used_for"):
            if not str(src.get(key, "")).strip():
                errors.append(f"source {sid or index} missing {key}")
        grade = src.get("evidence_grade")
        if grade not in VALID_GRADES:
            errors.append(f"source {sid or index} has invalid evidence_grade: {grade}")
        if grade == "D":
            used_for = str(src.get("used_for", "")).lower()
            forbidden = ["revenue", "margin", "valuation", "buy", "sell", "order", "customer win", "guidance"]
            if any(word in used_for for word in forbidden):
                errors.append(f"source {sid or index} is D-grade but used_for looks factual/valuation-related")

    sources_by_id = source_map(data)
    for index, finding in enumerate(data.get("findings", []), start=1):
        title = finding.get("title", f"finding #{index}")
        refs = [str(ref) for ref in finding.get("supporting_sources", [])]
        if not refs:
            errors.append(f"finding '{title}' has no supporting_sources")
            continue
        missing = [ref for ref in refs if ref not in sources_by_id]
        if missing:
            errors.append(f"finding '{title}' references unknown sources: {', '.join(missing)}")
        if finding.get("core", True):
            grades = {sources_by_id[ref].get("evidence_grade") for ref in refs if ref in sources_by_id}
            if not grades.intersection(CORE_SAFE_GRADES):
                errors.append(f"core finding '{title}' is supported only by D/E evidence")

    market_reaction = data.get("market_reaction", {})
    for index, driver in enumerate(market_reaction.get("drivers", []), start=1):
        name = driver.get("name", f"driver #{index}")
        grade = driver.get("evidence_grade")
        if grade not in VALID_GRADES:
            errors.append(f"market driver '{name}' has invalid or missing evidence_grade")
        refs = [str(ref) for ref in driver.get("supporting_sources", [])]
        if refs:
            missing = [ref for ref in refs if ref not in sources_by_id]
            if missing:
                errors.append(f"market driver '{name}' references unknown sources: {', '.join(missing)}")
        if grade in {"D", "E"} and driver.get("primary"):
            errors.append(f"market driver '{name}' cannot be primary with D/E evidence")

    if data.get("sample_only") is not True and data.get("report", {}).get("latest_request"):
        if not data.get("report", {}).get("verified_latest_as_of"):
            errors.append("latest_request reports need verified_latest_as_of")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("research_json")
    args = parser.parse_args()
    data = load_json(Path(args.research_json))
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(f"OK: validated {len(data.get('sources', []))} sources and {len(data.get('findings', []))} findings")


if __name__ == "__main__":
    main()
