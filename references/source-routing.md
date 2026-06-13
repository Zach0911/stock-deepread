# Source Routing

Use this file before searching or analyzing. Build a source register with URL, date, source type, evidence grade, and usage.

## General Rules

- Primary company and regulator sources come first.
- Record the search date, filing/release date, and reporting period whenever the user asks for the "latest" disclosure.
- If the company is multi-listed, map all relevant tickers and identify the primary disclosure market.
- Separate disclosure sources from market-price sources, analyst summaries, news, and social narratives.

## U.S. Stocks

Priority order:

1. SEC EDGAR filings: 10-K, 10-Q, 8-K, 20-F, 6-K, S-1, F-1, DEF 14A.
2. SEC companyfacts/submissions when structured data helps.
3. Company Investor Relations: earnings release, shareholder letter, investor presentation, webcast, transcript.
4. Market data: stock price, volume, pre/post-market move, Nasdaq/S&P/SOX/peer comparison.
5. Analyst/public expectation context: public rating changes, media summaries, target-price changes.
6. Social narratives: X, Reddit, Stocktwits, YouTube comments. Grade D only.

Useful official entry points:

- SEC EDGAR APIs: https://www.sec.gov/search-filings/edgar-application-programming-interfaces
- SEC company search: https://www.sec.gov/edgar/search/

## Hong Kong Stocks

Priority order:

1. HKEXnews announcements: annual report, interim report, results announcement, quarterly update, prospectus, application proof.
2. Company IR: results presentation, webcast, transcript, investor day.
3. Market data: HK price, turnover, Hang Seng/sector/peer comparison, Southbound flow if available.
4. Analyst/public expectation context: public summaries, rating changes, news coverage.
5. Social narratives: Snowball, Futu comments, X, Xiaohongshu, YouTube. Grade D only.

Official entry point:

- HKEXnews: https://www.hkexnews.hk/index.htm

## A-Share Stocks

Priority order:

1. CNINFO and exchange disclosures: annual report, quarterly report, preliminary results, guidance, inquiry letters, investor-relation activity records, announcements.
2. Company IR or official website: results briefing, presentation, Q&A.
3. Market data: stock price, turnover, limit up/down, sector index, financing balance, Northbound flow, Dragon Tiger list if relevant.
4. Analyst/public expectation context: public research summaries, industry data, news.
5. Social narratives: Snowball, Eastmoney Guba, Tonghuashun comments, Xiaohongshu, WeChat articles. Grade D only.

Official entry points:

- CNINFO: https://www.cninfo.com.cn/new/index
- SSE listed-company announcements: https://www.sse.com.cn/disclosure/listedinfo/announcement/
- SZSE disclosure: https://www.szse.cn/disclosure/listed/notice/

## Multi-Listed Companies

Always include:

- listing map: ADR, H-share, A-share, primary ticker, currency, exchange
- primary disclosure source
- market reaction by trading session
- FX and liquidity caveats
- index inclusion and investor-base differences

Do not treat ADR and HK/A-share listings as unrelated companies.
