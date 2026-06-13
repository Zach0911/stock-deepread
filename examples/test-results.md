# stock-deepread 验证记录

日期：2026-06-13

## 已通过

```bash
python3 -m py_compile stock-deepread/scripts/*.py
python3 -m json.tool stock-deepread/examples/test-prompts.json
python3 -m json.tool stock-deepread/examples/sample-research-data.json
python3 stock-deepread/scripts/source_plan.py --company Tesla --market US --task earnings_call
python3 stock-deepread/scripts/source_plan.py --company 小米集团 --market HK --task earnings_report
python3 stock-deepread/scripts/source_plan.py --company 宁德时代 --market A-share --task annual_report
python3 stock-deepread/scripts/source_plan.py --company "港股 IPO candidate" --market HK --task ipo_prospectus
python3 stock-deepread/scripts/source_plan.py --company 阿里巴巴 --market multi-listed --task earnings_report --task earnings_call --task market_reaction
python3 stock-deepread/scripts/validate_sources.py stock-deepread/examples/sample-research-data.json
python3 stock-deepread/scripts/build_html_report.py stock-deepread/examples/sample-research-data.json stock-deepread/examples/sample-report.html
python3 stock-deepread/scripts/validate_html_report.py stock-deepread/examples/sample-report.html
python3 /Users/chaozhang/.codex/skills/.system/skill-creator/scripts/quick_validate.py stock-deepread
```

结果：

- JSON 示例语法正确。
- Python 脚本语法正确。
- Source plan 能按 US / HK / A-share / multi-listed 输出不同信源路由。
- 7 个默认示例案例均能生成 source plan：Tesla、NVIDIA、小米集团、宁德时代、港股 IPO、美团、阿里巴巴。
- 证据校验通过，D 级社媒没有独立支撑核心结论。
- 负例测试通过：核心结论仅由 D 级证据支撑时会被拒绝。
- 负例测试通过：D 级社媒驱动被标记为市场反应 primary driver 时会被拒绝。
- 样例 HTML 已生成到 `examples/sample-report.html`。
- HTML 必需区块、指标卡、核心发现和信源表校验通过。
- HTML 自包含 CSS、移动端媒体规则、信源链接、社媒边界说明均存在。
- 使用系统 Google Chrome + Playwright 完成桌面和移动端首屏渲染检查：
  - `examples/screenshots/sample-report-desktop.png`
  - `examples/screenshots/sample-report-mobile.png`
- Codex Skill 官方 quick_validate 通过。

## 浏览器渲染摘要

```json
{
  "title": "Tesla 财报与电话会深读样例",
  "sections": 11,
  "metrics": 4,
  "findings": 4,
  "sources": 5,
  "heroVisible": true,
  "desktopBytes": 210625,
  "mobileBytes": 82966
}
```

## 开源卫生

- 已清理 `stock-deepread` 目录内的 `.DS_Store`。
- 已清理测试产生的 `__pycache__` / `.pyc` 副产物。
