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

EMPTY_TEXT = "不适用或暂不可得。"
GRADE_LABELS = {
    "A": "1级证据",
    "B": "2级证据",
    "C": "3级证据",
    "D": "4级证据",
    "E": "5级证据",
}
MARKET_LABELS = {
    "US": "美股",
    "HK": "港股",
    "A-share": "A 股",
    "multi-listed": "多地上市",
}
DISCLOSURE_LABELS = {
    "earnings_report": "财报",
    "earnings_call": "电话会",
    "market_reaction": "市场反应",
    "annual_report": "年报",
    "ipo_prospectus": "上市文件",
    "research_note": "研报",
}


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def paragraph_list(items: list[str]) -> str:
    if not items:
        return f'<p class="empty">{EMPTY_TEXT}</p>'
    return "".join(f"<p>{esc(item)}</p>" for item in items)


def grade_label(grade: object) -> str:
    return GRADE_LABELS.get(str(grade), esc(grade))


def badge(text: str, grade: str | None = None) -> str:
    cls = f" badge grade-{esc(grade)}" if grade else " badge"
    return f'<span class="{cls.strip()}">{esc(text)}</span>'


def source_label(source_id: object) -> str:
    text = str(source_id or "")
    if text.upper().startswith("S") and text[1:].isdigit():
        return f"信源{text[1:]}"
    return text


def translated_market(value: object) -> str:
    return MARKET_LABELS.get(str(value), str(value or ""))


def translated_disclosure_types(values: list[str]) -> str:
    labels = [DISCLOSURE_LABELS.get(str(value), str(value)) for value in values]
    return "、".join(labels)


def render_hero(data: dict) -> str:
    company = data.get("company", {})
    report = data.get("report", {})
    conclusion = data.get("conclusion", {})
    company_label = company.get("display_name") or company.get("name", "")
    meta = [
        ("公司", company_label),
        ("市场", translated_market(company.get("market", ""))),
        ("期间", report.get("period", "")),
        ("生成日期", report.get("generated_at", date.today().isoformat())),
        ("披露日期", report.get("disclosure_date", "")),
        ("报告类型", translated_disclosure_types(report.get("disclosure_types", []))),
    ]
    meta_html = "".join(
        f'<div class="meta-item"><div class="meta-label">{esc(label)}</div><div class="meta-value">{esc(value or EMPTY_TEXT)}</div></div>'
        for label, value in meta
    )
    return f"""
        <div class="hero-card">
          <div>
            <div class="eyebrow">股票深读</div>
            <h1>{esc(report.get("title") or company_label or "公司深度解读")}</h1>
            <p class="lead">{esc(conclusion.get("summary", "结论暂不可得。"))}</p>
          </div>
          <div class="hero-meta">{meta_html}</div>
        </div>
        <aside class="verdict">
          <div>
            <div class="label">一句话结论</div>
            <div class="value">{esc(conclusion.get("verdict", "观察 / 等待更多证据"))}</div>
          </div>
          <div><span class="confidence">置信度：{esc(conclusion.get("confidence", "中等"))}</span></div>
          <div>
            <div class="label">最大分歧</div>
            <p>{esc(conclusion.get("key_debate", EMPTY_TEXT))}</p>
          </div>
          <div>
            <div class="label">下一催化</div>
            <p>{esc(conclusion.get("next_catalyst", EMPTY_TEXT))}</p>
          </div>
          <div>
            <div class="label">最大证伪</div>
            <p>{esc(conclusion.get("main_disconfirming_evidence", EMPTY_TEXT))}</p>
          </div>
        </aside>
    """


def render_metrics(data: dict) -> str:
    metrics = data.get("metrics", [])
    if not metrics:
        return f'<div class="metric-card empty">{EMPTY_TEXT}</div>'
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
            grade = src.get("evidence_grade", "?")
            refs.append(badge(f"{source_label(ref)} / {grade_label(grade)}", grade))
        inference = badge("推断", "E") if finding.get("inference") else ""
        cards.append(
            f"""
            <article class="finding" data-rank="{idx:02d}">
              <div class="finding-title">{esc(finding.get("title"))}</div>
              <div class="finding-body">{paragraph_list(finding.get("body", []))}</div>
              <div class="badges">{''.join(refs)}{inference}</div>
            </article>
            """
        )
    return "".join(cards) if cards else f'<div class="finding empty">{EMPTY_TEXT}</div>'


def render_table(rows: list[dict], columns: list[tuple[str, str]]) -> str:
    if not rows:
        return f'<p class="empty">{EMPTY_TEXT}</p>'
    head = "".join(f"<th>{esc(label)}</th>" for _, label in columns)
    body = []
    for row in rows:
        body.append("<tr>" + "".join(f"<td>{esc(row.get(key, ''))}</td>" for key, _ in columns) + "</tr>")
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def render_segments(data: dict) -> str:
    segments = data.get("segments", [])
    if not segments:
        return f'<div class="mini-card empty">{EMPTY_TEXT}</div>'
    return "".join(
        f"""
        <article class="mini-card">
          <div class="mini-kicker">{esc(seg.get("role", "业务分部"))}</div>
          <div class="mini-title">{esc(seg.get("name"))}</div>
          <p>{esc(seg.get("change", ""))}</p>
          <p><strong>跟踪重点：</strong>{esc(seg.get("watch_item", ""))}</p>
        </article>
        """
        for seg in segments
    )


def render_supply_chain(data: dict) -> str:
    chain = data.get("supply_chain", [])
    if not chain:
        return f'<div class="chain-node empty">{EMPTY_TEXT}</div>'
    return "".join(
        f"""
        <div class="chain-node">
          <div class="chain-layer">{esc(node.get("layer"))}</div>
          <div class="chain-title">{esc(node.get("title"))}</div>
          <p>{esc(node.get("evidence", ""))}</p>
          <div class="badges">{badge(grade_label(node.get("grade", "C")), node.get("grade", "C"))}</div>
        </div>
        """
        for node in chain
    )


def render_call_language(data: dict) -> str:
    call = data.get("call_language", {})
    rows = call.get("items", [])
    return render_table(rows, [("area", "维度"), ("read", "解读"), ("evidence", "证据"), ("watch", "跟踪重点")])


def render_market_reaction(data: dict) -> str:
    reaction = data.get("market_reaction", {})
    drivers = reaction.get("drivers", [])
    if not drivers and not reaction:
        return f'<div class="panel empty">{EMPTY_TEXT}</div>'
    driver_html = "".join(
        f"""
        <div class="driver">
          <div class="driver-name">{esc(driver.get("name"))}</div>
          <div>{esc(driver.get("read", ""))}</div>
          <div>{badge(grade_label(driver.get("evidence_grade", "?")), driver.get("evidence_grade"))}</div>
        </div>
        """
        for driver in drivers
    )
    context_rows = reaction.get("price_context", [])
    context_html = render_table(context_rows, [("window", "观察窗口"), ("move", "涨跌幅"), ("relative", "相对表现"), ("note", "说明")])
    return f"""
      <div class="panel"><h3>价格上下文</h3>{context_html}</div>
      <div class="panel"><h3>驱动排序</h3><div class="driver-list">{driver_html or f'<p class="empty">{EMPTY_TEXT}</p>'}</div></div>
    """


def render_research_notes(data: dict) -> str:
    notes = data.get("research_notes", {})
    if not notes:
        return f'<p class="empty">{EMPTY_TEXT}</p>'
    return paragraph_list(notes.get("summary", [])) + render_table(
        notes.get("checks", []),
        [("claim", "公开观点"), ("support", "支撑证据"), ("limit", "限制与注意事项")],
    )


def render_scenarios(data: dict) -> str:
    scenarios = data.get("scenarios", [])
    if not scenarios:
        return f'<div class="scenario empty">{EMPTY_TEXT}</div>'
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
              <div>{badge(grade_label(src.get("evidence_grade", "?")), src.get("evidence_grade"))}</div>
              <div>
                <div class="source-title"><a href="{url}">{title}</a></div>
                <div class="source-meta">{esc(source_label(src.get("id")))} / {esc(src.get("source_type"))}</div>
              </div>
              <div class="source-meta">{esc(src.get("date"))}</div>
              <div>{esc(src.get("used_for"))}</div>
            </div>
            """
        )
    return "".join(rows) if rows else f'<div class="source-row empty">暂无信源。</div>'


def render(data: dict) -> str:
    template = TEMPLATE.read_text(encoding="utf-8")
    report = data.get("report", {})
    theme = report.get("theme", "classic-research")
    replacements = {
        "{{TITLE}}": esc(report.get("title", "股票深读")),
        "{{THEME_CLASS}}": f"theme-{esc(theme)}",
        "{{HERO_SUMMARY}}": render_hero(data),
        "{{KEY_METRICS}}": render_metrics(data),
        "{{FINDINGS}}": render_findings(data),
        "{{FINANCIAL_BRIDGE}}": render_table(data.get("financial_bridge", []), [("metric", "指标"), ("current", "本期"), ("prior", "前期"), ("change", "变化"), ("read", "解读")]),
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
