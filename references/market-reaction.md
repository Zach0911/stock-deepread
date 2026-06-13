# Market Reaction

Use this when a stock has moved or the user asks why it rose/fell.

## Required Price Context

Prefer:

- 1D, 5D, since filing/release
- pre-market/post-market if relevant
- relative to benchmark index
- relative to sector ETF or close peers
- volume and turnover changes when available

Do not explain price action without comparing it to the market and peers.

## Driver Categories

Rank likely drivers with evidence grades:

| Driver | Questions |
|---|---|
| Fundamental surprise | Did revenue, margin, EPS, cash flow, or orders differ from expectations? |
| Guidance surprise | Did management raise/lower guidance or avoid guidance? |
| Demand/order signal | Did backlog, pipeline, deliveries, GMV, RPO, or utilization change? |
| Valuation/rates | Was the multiple already stretched? Did rates or sector multiples move? |
| Positioning/structure | Was the trade crowded? Any short interest, options gamma, unlock, buyback, liquidity effect? |
| Analyst revisions | Did public ratings/target prices/estimates change? |
| Social narrative | Did market attention shift? Grade D only. |
| Macro/sector beta | Did the whole market or industry move? |

## Output Shape

Write:

```text
This reaction looks more like [primary driver] + [secondary driver], not [excluded driver].
```

Then include:

- primary cause with evidence grade
- secondary cause with evidence grade
- possible but unconfirmed cause
- excluded cause and why
- what new data would change the attribution

## Social Narrative Rules

Social media may explain what investors are talking about, not what is true. Any D-grade signal must be phrased as:

- "market narrative"
- "attention signal"
- "claim to verify"
- "possible positioning/hype factor"

Never phrase a D-grade social item as confirmed orders, customers, margins, or guidance.
