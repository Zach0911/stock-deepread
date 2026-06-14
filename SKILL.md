---
name: stock-deepread
description: Use when users ask to interpret listed-company filings, earnings reports, earnings calls, IPO prospectuses, analyst research, latest disclosures, stock moves, market reactions, or why a stock rose/fell for A-share, Hong Kong, U.S., or multi-listed public companies, especially when no source file or URL is provided.
---

# Stock Deepread

Stock Deepread creates source-backed deep reads of public-company disclosures and renders them as clear, evidence-graded HTML reports. Always build the source register before writing conclusions.

## Core Workflow

1. Identify the company, listing market, tickers, disclosure type, reporting period, and whether the user asks about price reaction.
2. Read `references/source-routing.md` and create a source plan before searching or analyzing.
3. Read `references/evidence-grading.md`; classify every source as A/B/C/D/E.
4. Read `references/disclosure-types.md` for the task type: annual/quarterly report, earnings call, IPO prospectus, research note, or market reaction.
5. Build a structured research object with company, task, sources, metrics, findings, supply chain, market reaction, scenarios, and report metadata.
6. Read `references/analysis-framework.md` before writing conclusions.
7. If the stock has moved or the user asks why it rose/fell, read `references/market-reaction.md`.
8. Read `references/html-report-spec.md` before generating the HTML report.
9. Validate sources and the rendered report before delivery.

## Hard Rules

- Do not write a core conclusion unless it is backed by an A/B/C source or explicitly marked as inference.
- Social media, forums, KOLs, X, Reddit, YouTube comments, Stocktwits, Snowball, Eastmoney Guba, Futu comments, and Xiaohongshu are D-grade narrative signals only. They cannot prove facts or stand alone as a buy/sell reason.
- For Chinese reports, translate all reader-visible English into Chinese. Keep only unavoidable identifiers such as ticker symbols, URLs, exchange codes, filing form names, and product names when translation would damage accuracy; explain them in Chinese on first use.
- For Chinese reports, render numeric content with Arabic numerals by default: amounts, percentages, dates, periods, ranks, counts, margins, prices, and changes should use forms like `221.9 亿美元`, `48%`, `2026 年第 2 季度`, not Chinese numeral prose.
- Do not pretend to have read paywalled or unavailable analyst research. State the limitation and use public summaries, rating changes, target-price changes, and company disclosures.
- Do not give unconditional buy/sell instructions or personalized position sizing without user constraints.
- When the user says "latest", verify the filing/release date and reporting period with current sources.
- If information cannot be refreshed, state that realtime verification is incomplete and lower conclusion confidence.

## Output Requirements

Default output is a single self-contained HTML report:

- key-data dashboard in the first viewport
- Chinese reader-visible labels, headings, table headers, captions, empty states, and summaries
- source register with evidence grades
- "what changed" findings
- financial bridge and operating metrics
- business-segment analysis
- supply-chain/upstream/downstream map
- earnings-call language and Q&A analysis when relevant
- market reaction attribution when price has moved
- research-note quality check when relevant
- Bull/Base/Bear scenarios and disconfirming evidence

For Chinese earnings/disclosure reports, use `examples/broadcom-latest-earnings-deepread.html` as the canonical standard for density, visual hierarchy, Arabic-numeral numeric formatting, evidence-register placement, and readable first-viewport dashboard. Use `examples/broadcom-latest-earnings-data.json` as the matching structured-data example.

Use `scripts/source_plan.py` to draft source plans, `scripts/validate_sources.py` to check research data, `scripts/build_html_report.py` to render reports from JSON, and `scripts/validate_html_report.py` to verify generated HTML.

## Resource Map

| File | Use |
|---|---|
| `references/source-routing.md` | Market-specific A/HK/US and multi-listing source routing |
| `references/evidence-grading.md` | Evidence grades, social-media boundary, research-note limits |
| `references/analysis-framework.md` | Deep-read framework, supply chain, financial translation |
| `references/market-reaction.md` | Stock rise/fall attribution framework |
| `references/html-report-spec.md` | HTML report structure, themes, validation rules |
| `references/disclosure-types.md` | Specific checklists for filings, calls, IPOs, and research notes |
| `assets/report-template.html` | Self-contained HTML report template |
| `examples/broadcom-latest-earnings-deepread.html` | Canonical Chinese HTML report example |
| `examples/broadcom-latest-earnings-data.json` | Canonical structured-data example for the Broadcom report |
| `scripts/*.py` | Source planning, source validation, report rendering, HTML validation |
