#!/usr/bin/env python3
"""Create a deterministic source plan for stock-deepread."""

from __future__ import annotations

import argparse
import json
from datetime import date


MARKET_ROUTES = {
    "US": {
        "official": [
            ("SEC EDGAR filing", "A", "10-K/10-Q/8-K/20-F/6-K/S-1/F-1"),
            ("Company investor relations", "A", "earnings release, presentation, webcast"),
            ("Earnings call transcript or webcast", "B", "prepared remarks and Q&A"),
        ],
        "market": [
            ("Stock price and volume", "C", "1D/5D/event-window move"),
            ("Benchmark and peers", "C", "Nasdaq, S&P 500, SOX, close peers"),
        ],
        "links": [
            "https://www.sec.gov/search-filings/edgar-application-programming-interfaces",
            "https://www.sec.gov/edgar/search/",
        ],
    },
    "HK": {
        "official": [
            ("HKEXnews announcement", "A", "results announcement, annual/interim report, prospectus"),
            ("Company investor relations", "A", "presentation, webcast, results deck"),
            ("Earnings call or results briefing", "B", "management tone and Q&A"),
        ],
        "market": [
            ("HK share price and turnover", "C", "event-window move"),
            ("Hang Seng/sector/peer comparison", "C", "relative market context"),
        ],
        "links": ["https://www.hkexnews.hk/index.htm"],
    },
    "A-share": {
        "official": [
            ("CNINFO/exchange disclosure", "A", "annual report, quarterly report, announcements"),
            ("Company investor relations", "A", "results briefing, activity records"),
            ("Exchange inquiry letters", "A", "regulatory pressure and clarifications"),
        ],
        "market": [
            ("A-share price and turnover", "C", "event-window move"),
            ("Sector index and northbound/financing context", "C", "relative market context"),
        ],
        "links": [
            "https://www.cninfo.com.cn/new/index",
            "https://www.sse.com.cn/disclosure/listedinfo/announcement/",
            "https://www.szse.cn/disclosure/listed/notice/",
        ],
    },
    "multi-listed": {
        "official": [
            ("Primary disclosure market", "A", "identify SEC/HKEX/A-share primary source"),
            ("All listing-market announcements", "A", "ADR/H-share/A-share mapping"),
            ("Company investor relations", "A", "earnings release and presentation"),
        ],
        "market": [
            ("Price by listing and trading session", "C", "US/HK/A-share reaction windows"),
            ("FX, liquidity, index and investor-base context", "C", "explain divergent moves"),
        ],
        "links": [
            "https://www.sec.gov/edgar/search/",
            "https://www.hkexnews.hk/index.htm",
            "https://www.cninfo.com.cn/new/index",
        ],
    },
}

TASK_EXTRAS = {
    "earnings_report": [
        ("Prior-period filing/release", "A", "change detection"),
        ("Public consensus or analyst-summary context", "C", "expectations check"),
    ],
    "earnings_call": [
        ("Call transcript/webcast replay", "B", "prepared remarks versus Q&A"),
        ("Previous call transcript", "B", "language change detection"),
    ],
    "annual_report": [
        ("Risk factors and MD&A", "A", "business/risk change detection"),
        ("Working-capital and cash-flow notes", "A", "financial quality"),
    ],
    "ipo_prospectus": [
        ("Prospectus/application proof", "A", "business model, financials, risks"),
        ("Peer filings", "C", "valuation and business-quality comparison"),
    ],
    "research_note": [
        ("Public rating/target-price changes", "C", "visible sell-side thesis"),
        ("Company filings/calls", "A", "assumption check against primary evidence"),
    ],
    "market_reaction": [
        ("Event-window price and volume", "C", "absolute move"),
        ("Benchmark/sector/peer move", "C", "relative move"),
        ("Social narrative sample", "D", "attention signal only"),
    ],
}


def normalize_market(value: str) -> str:
    aliases = {
        "us": "US",
        "usa": "US",
        "美股": "US",
        "hk": "HK",
        "hongkong": "HK",
        "港股": "HK",
        "cn": "A-share",
        "a": "A-share",
        "ashare": "A-share",
        "a-share": "A-share",
        "a股": "A-share",
        "multi": "multi-listed",
        "multi-listed": "multi-listed",
        "多地上市": "multi-listed",
    }
    key = value.strip().lower()
    return aliases.get(key, value)


def build_plan(company: str, market: str, tasks: list[str]) -> dict:
    market = normalize_market(market)
    route = MARKET_ROUTES.get(market)
    if route is None:
        raise SystemExit(f"Unsupported market: {market}. Use US, HK, A-share, or multi-listed.")

    required = []
    for name, grade, use in route["official"] + route["market"]:
        required.append({"source_type": name, "evidence_grade": grade, "used_for": use})

    for task in tasks:
        for name, grade, use in TASK_EXTRAS.get(task, []):
            item = {"source_type": name, "evidence_grade": grade, "used_for": use, "task": task}
            if item not in required:
                required.append(item)

    return {
        "company": company,
        "market": market,
        "tasks": tasks,
        "generated_on": date.today().isoformat(),
        "required_sources": required,
        "official_entry_points": route["links"],
        "hard_rules": [
            "Verify exact disclosure date and reporting period for latest requests.",
            "Use A/B/C evidence for core findings.",
            "Treat social media as D-grade narrative signal only.",
            "Do not claim paywalled research or transcript access unless actually obtained.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--company", required=True)
    parser.add_argument("--market", required=True, help="US, HK, A-share, or multi-listed")
    parser.add_argument(
        "--task",
        action="append",
        required=True,
        help="earnings_report, earnings_call, annual_report, ipo_prospectus, research_note, market_reaction",
    )
    parser.add_argument("--format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()

    plan = build_plan(args.company, args.market, args.task)
    if args.format == "json":
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return

    print(f"# Source Plan: {plan['company']} ({plan['market']})")
    print(f"Generated: {plan['generated_on']}\n")
    for source in plan["required_sources"]:
        print(f"- [{source['evidence_grade']}] {source['source_type']}: {source['used_for']}")


if __name__ == "__main__":
    main()
