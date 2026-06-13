#!/usr/bin/env python3
"""Validate rendered stock-deepread HTML structure."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


REQUIRED_IDS = [
    "hero-summary",
    "key-metrics",
    "findings",
    "financial-bridge",
    "segments",
    "supply-chain",
    "call-language",
    "market-reaction",
    "research-notes",
    "scenarios",
    "source-register",
]


class SectionParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.current_id: str | None = None
        self.section_text: dict[str, list[str]] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_map = dict(attrs)
        element_id = attrs_map.get("id")
        if element_id:
            self.ids.add(element_id)
            if element_id in REQUIRED_IDS:
                self.current_id = element_id
                self.section_text.setdefault(element_id, [])

    def handle_endtag(self, tag: str) -> None:
        if tag in {"section", "header"}:
            self.current_id = None

    def handle_data(self, data: str) -> None:
        if self.current_id:
            text = data.strip()
            if text:
                self.section_text.setdefault(self.current_id, []).append(text)


def validate(path: Path) -> list[str]:
    html_text = path.read_text(encoding="utf-8")
    parser = SectionParser()
    parser.feed(html_text)
    errors: list[str] = []

    for section_id in REQUIRED_IDS:
        if section_id not in parser.ids:
            errors.append(f"missing required section id: {section_id}")
        elif not " ".join(parser.section_text.get(section_id, [])).strip():
            errors.append(f"section is empty: {section_id}")

    if "{{" in html_text or "}}" in html_text:
        errors.append("unresolved template placeholder found")
    if len(re.findall(r'class="metric-card', html_text)) < 2:
        errors.append("expected at least two metric cards")
    if len(re.findall(r'class="finding"', html_text)) < 3:
        errors.append("expected at least three findings")
    if len(re.findall(r'class="source-row"', html_text)) < 3:
        errors.append("expected at least three source rows")
    if '<style>' not in html_text or '</style>' not in html_text:
        errors.append("HTML must be self-contained with inline CSS")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html_report")
    args = parser.parse_args()
    errors = validate(Path(args.html_report))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
    print("OK: required report sections and core content are present")


if __name__ == "__main__":
    main()
