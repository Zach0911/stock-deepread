# HTML Report Spec

Default output is a single self-contained HTML file with inline CSS and JS. It is a reading report, not a 16:9 slide deck.

## Design Direction

Use a "research terminal" style:

- high information density with clear hierarchy
- first viewport contains the conclusion and key metrics
- crisp tables, evidence badges, timeline, supply-chain map, and scenario grid
- restrained palette with theme accents
- no landing-page hero, no marketing copy, no generic purple gradient

This borrows from frontend-slides principles: single-file delivery, show-don't-tell visuals, distinctive design, and rendered verification.

## Required Sections

Use these section IDs so validation can check them:

- `hero-summary`
- `key-metrics`
- `findings`
- `financial-bridge`
- `segments`
- `supply-chain`
- `call-language`
- `market-reaction`
- `research-notes`
- `scenarios`
- `source-register`

If a section is not relevant, keep a short "not applicable / unavailable" card rather than silently omitting it.

## Themes

| Theme | Use |
|---|---|
| `classic-research` | General earnings, financials, diversified companies |
| `industrial-chain` | Auto, battery, manufacturing, energy, semiconductors, hardware |
| `consumer-ops` | Internet, consumer, local services, platform businesses |
| `tech-infrastructure` | AI, cloud, chips, data centers, enterprise software |

Default to `classic-research` unless the industry clearly maps to another theme.

## Mobile Rules

- Top summary becomes a single column.
- Metrics become two columns.
- Supply chain becomes a vertical ladder.
- Large tables can scroll horizontally.
- Source register can be dense but must remain readable.

## Validation

Before delivery, verify:

- required section IDs exist
- key metrics are non-empty
- at least three findings exist in full reports
- supply-chain section has at least three layers when a supply-chain thesis is present
- market reaction section exists when the user asks about stock movement
- source register exists
- each core finding has at least one source
- no obvious text overlap at desktop and mobile widths
