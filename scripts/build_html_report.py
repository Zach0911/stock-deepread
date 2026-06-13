#!/usr/bin/env python3
"""Render stock-deepread research JSON to a single self-contained HTML file."""

from __future__ import annotations

import argparse
import html
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "report-template.html"


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def paragraph_list(items: list[str]) -> str:
    if not items:
        return '<p class="empty">Not applicable / unavailable.</p>'
    return "".join(f"<p>{esc(item)}</p>" for item in items)


def badge(text: str, grade: str | None = None) -> str:
    cls = f" badge grade-{esc(grade)}" if grade else " badge"
    return f'<span class="{cls.strip()}">{esc(text)}</span>'


def render_hero(data: dict) -> str:
    company = data.get("company", {})
    report = data.get("report", {})
    conclusion = data.get("conclusion", {})
    meta = [
        ("公司/代码", f"{company.get('name', '')} {company.get('ticker', '')}".strip()),
        ("市场", company.get("market", "")),
        ("期间", report.get("period", "")),
        ("生成日期", report.get("generated_at", date.today().isoformat())),
        ("披露日期", report.get("disclosure_date", "")),
        ("报告类型", ", ".join(report.get("disclosure_types", []))),
    ]
    meta_html = "".join(
        f'<div class="meta-item"><div class="meta-label">{esc(label)}</div><div class="meta-value">{esc(value or "Unavailable")}</div></div>'
        for label, value in meta
    )
    return f"""
        <div class="hero-card">
          <div>
            <div class="eyebrow">Stock Deepread / 股票深读</div>
            <h1>{esc(report.get("title") or company.get("name") or "Company Deepread")}</h1>
            <p class="lead">{esc(conclusion.get("summary", "Conclusion unavailable."))}</p>
          </div>
          <div class="hero-meta">{meta_html}</div>
        </div>
        <aside class="verdict">
          <div>
            <div class="label">One-line verdict</div>
            <div class="value">{esc(conclusion.get("verdict", "Watch / Need more evidence"))}</div>
          </div>
          <div><span class="confidence">Confidence: {esc(conclusion.get("confidence", "Medium"))}</span></div>
          <div>
            <div class="label">最大分歧</div>
            <p>{esc(conclusion.get("key_debate", "Unavailable"))}</p>
          </div>
          <div>
            <div class="label">下一催化</div>
            <p>{esc(conclusion.get("next_catalyst", "Unavailable"))}</p>
          </div>
          <div>
            <div class="label">最大证伪</div>
            <p>{esc(conclusion.get("main_disconfirming_evidence", "Unavailable"))}</p>
          </div>
        </aside>
    """


def render_metrics(data: dict) -> str:
    metrics = data.get("metrics", [])
    if not metrics:
        return '<div class="metric-card empty">Not applicable / unavailable.</div>'
    cards = []
    for metric in metrics:
        cards.append(
            f"""
            <div class="metric-card">
              <div class="metric-label">{esc(metric.get("label"))}</div>
              <div class="metric-value">{esc(metric.get("value"))}</div>
              <div class="metric-delta">{esc(metric.get("delta", ""))}</div>
              <div class="metric-source">{esc(metric.get("note", ""))}</div>
            </div>
            """
        )
    return "".join(cards)


def render_findings(data: dict) -> str:
    sources = {str(src.get("id")): src for src in data.get("sources", [])}
    cards = []
    for idx, finding in enumerate(data.get("findings", []), start=1):
        refs = []
        for ref in finding.get("supporting_sources", []):
            src = sources.get(str(ref), {})
            refs.append(badge(f"{ref} / {src.get('evidence_grade', '?')}", src.get("evidence_grade")))
        inference = badge("Inference", "E") if finding.get("inference") else ""
        cards.append(
            f"""
            <article class="finding" data-rank="{idx:02d}">
              <div class="finding-title">{esc(finding.get("title"))}</div>
              <div class="finding-body">{paragraph_list(finding.get("body", []))}</div>
              <div class="badges">{''.join(refs)}{inference}</div>
            </article>
            """
        )
    return "".join(cards) if cards else '<div class="finding empty">Not applicable / unavailable.</div>'


def render_table(rows: list[dict], columns: list[tuple[str, str]]) -> str:
    if not rows:
        return '<p class="empty">Not applicable / unavailable.</p>'
    head = "".join(f"<th>{esc(label)}</th>" for _, label in columns)
    body = []
    for row in rows:
        body.append("<tr>" + "".join(f"<td>{esc(row.get(key, ''))}</td>" for key, _ in columns) + "</tr>")
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def render_segments(data: dict) -> str:
    segments = data.get("segments", [])
    if not segments:
        return '<div class="mini-card empty">Not applicable / unavailable.</div>'
    return "".join(
        f"""
        <article class="mini-card">
          <div class="mini-kicker">{esc(seg.get("role", "Segment"))}</div>
          <div class="mini-title">{esc(seg.get("name"))}</div>
          <p>{esc(seg.get("change", ""))}</p>
          <p><strong>Watch:</strong> {esc(seg.get("watch_item", ""))}</p>
        </article>
        """
        for seg in segments
    )


def render_supply_chain(data: dict) -> str:
    chain = data.get("supply_chain", [])
    if not chain:
        return '<div class="chain-node empty">Not applicable / unavailable.</div>'
    return "".join(
        f"""
        <div class="chain-node">
          <div class="chain-layer">{esc(node.get("layer"))}</div>
          <div class="chain-title">{esc(node.get("title"))}</div>
          <p>{esc(node.get("evidence", ""))}</p>
          <div class="badges">{badge(node.get("grade", "C"), node.get("grade", "C"))}</div>
        </div>
        """
        for node in chain
    )


def render_call_language(data: dict) -> str:
    call = data.get("call_language", {})
    rows = call.get("items", [])
    return render_table(rows, [("area", "Area"), ("read", "Read"), ("evidence", "Evidence"), ("watch", "Watch")])


def render_market_reaction(data: dict) -> str:
    reaction = data.get("market_reaction", {})
    drivers = reaction.get("drivers", [])
    if not drivers and not reaction:
        return '<div class="panel empty">Not applicable / unavailable.</div>'
    driver_html = "".join(
        f"""
        <div class="driver">
          <div class="driver-name">{esc(driver.get("name"))}</div>
          <div>{esc(driver.get("read", ""))}</div>
          <div>{badge(driver.get("evidence_grade", "?"), driver.get("evidence_grade"))}</div>
        </div>
        """
        for driver in drivers
    )
    context_rows = reaction.get("price_context", [])
    context_html = render_table(context_rows, [("window", "Window"), ("move", "Move"), ("relative", "Relative"), ("note", "Note")])
    return f"""
      <div class="panel"><h3>价格上下文</h3>{context_html}</div>
      <div class="panel"><h3>驱动排序</h3><div class="driver-list">{driver_html or '<p class="empty">Unavailable.</p>'}</div></div>
    """


def render_research_notes(data: dict) -> str:
    notes = data.get("research_notes", {})
    if not notes:
        return '<p class="empty">Not applicable / unavailable.</p>'
    return paragraph_list(notes.get("summary", [])) + render_table(
        notes.get("checks", []),
        [("claim", "Visible claim"), ("support", "Support"), ("limit", "Limit / caveat")],
    )


def render_scenarios(data: dict) -> str:
    scenarios = data.get("scenarios", [])
    if not scenarios:
        return '<div class="scenario empty">Not applicable / unavailable.</div>'
    return "".join(
        f"""
        <article class="scenario">
          <h3>{esc(scenario.get("name"))}</h3>
          <p>{esc(scenario.get("thesis", ""))}</p>
          <p><strong>关键假设:</strong> {esc(scenario.get("assumptions", ""))}</p>
          <p><strong>证伪:</strong> {esc(scenario.get("disconfirming", ""))}</p>
        </article>
        """
        for scenario in scenarios
    )


def render_sources(data: dict) -> str:
    rows = []
    for src in data.get("sources", []):
        title = esc(src.get("title"))
        url = esc(src.get("url"))
        rows.append(
            f"""
            <div class="source-row">
              <div>{badge(src.get("evidence_grade", "?"), src.get("evidence_grade"))}</div>
              <div>
                <div class="source-title"><a href="{url}">{title}</a></div>
                <div class="source-meta">{esc(src.get("id"))} / {esc(src.get("source_type"))}</div>
              </div>
              <div class="source-meta">{esc(src.get("date"))}</div>
              <div>{esc(src.get("used_for"))}</div>
            </div>
            """
        )
    return "".join(rows) if rows else '<div class="source-row empty">No sources supplied.</div>'


def render(data: dict) -> str:
    template = TEMPLATE.read_text(encoding="utf-8")
    report = data.get("report", {})
    theme = report.get("theme", "classic-research")
    replacements = {
        "{{TITLE}}": esc(report.get("title", "Stock Deepread")),
        "{{THEME_CLASS}}": f"theme-{esc(theme)}",
        "{{HERO_SUMMARY}}": render_hero(data),
        "{{KEY_METRICS}}": render_metrics(data),
        "{{FINDINGS}}": render_findings(data),
        "{{FINANCIAL_BRIDGE}}": render_table(data.get("financial_bridge", []), [("metric", "Metric"), ("current", "Current"), ("prior", "Prior"), ("change", "Change"), ("read", "Read")]),
        "{{SEGMENTS}}": render_segments(data),
        "{{SUPPLY_CHAIN}}": render_supply_chain(data),
        "{{CALL_LANGUAGE}}": render_call_language(data),
        "{{MARKET_REACTION}}": render_market_reaction(data),
        "{{RESEARCH_NOTES}}": render_research_notes(data),
        "{{SCENARIOS}}": render_scenarios(data),
        "{{SOURCE_REGISTER}}": render_sources(data),
        "{{DISCLAIMER}}": esc(data.get("disclaimer", "仅用于公开信息研究辅助，不构成投资建议。")),
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    return template


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("research_json")
    parser.add_argument("output_html")
    args = parser.parse_args()

    data = json.loads(Path(args.research_json).read_text(encoding="utf-8"))
    html_text = render(data)
    out = Path(args.output_html)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_text, encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
