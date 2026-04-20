"""
Performance and energy reporting helpers.

This module is intentionally additive: it derives metrics from the existing
AST/IR pipeline, maintains persistent run history, and prepares chart datasets
for GUI rendering plus lightweight SVG exports for saved reports.
"""

from __future__ import annotations

from datetime import datetime
import json
import math
import os
from typing import Any, Dict, Iterable, List


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_DIR = os.path.join(ROOT_DIR, "results", "performance_energy")
HISTORY_FILE = os.path.join(REPORT_DIR, "history.json")
LOC_RANGE_POINTS = [20, 50, 100, 200, 500]
LOC_BUCKETS = [
    (20, "0-20 LOC"),
    (50, "20-50 LOC"),
    (100, "51-100 LOC"),
    (200, "101-200 LOC"),
    (500, "200-500 LOC"),
]
LOC_RANGE_LABELS = {
    20: "0-20",
    50: "20-50",
    100: "51-100",
    200: "101-200",
    500: "200-500",
}


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _non_empty_loc(source: str) -> int:
    return sum(1 for line in source.splitlines() if line.strip())


# ── Carbon & power constants ─────────────────────────────────────────────────
# Global average grid carbon intensity: 233 g CO₂ per kWh
# 1 kWh = 3 600 000 J  →  1 mJ = 233 / 3_600_000 µg CO₂  ≈ 6.472e-5 g CO₂/mJ
# We store in µg (micrograms) for readability at analysis-run scale.
_CARBON_UG_PER_MJ   = 233_000 / 3_600_000   # ≈ 0.06472 µg CO₂ per mJ
_CARBON_G_PER_KWH   = 233.0                  # reference: global avg kg CO₂ / kWh
_MJ_PER_KWH         = 3_600_000.0            # 1 kWh = 3 600 000 mJ
_UG_CO2_LED_PER_HOUR = 2_000.0               # typical 5 W LED: ~2 g CO₂/h = 2_000 000 µg/h → simplified


def _format_power(mw: float) -> str:
    return f"{mw:.4f} mW"


def _format_carbon(ug: float) -> str:
    """Human-readable carbon display: µg → mg → g as scale grows."""
    if ug < 1_000:
        return f"{ug:.4f} µg CO₂"
    if ug < 1_000_000:
        return f"{ug / 1000:.4f} mg CO₂"
    return f"{ug / 1_000_000:.6f} g CO₂"


def _carbon_context(ug: float) -> str:
    """Produce a friendly equivalence sentence for the carbon figure."""
    if ug <= 0:
        return "Negligible carbon footprint."
    # Compare against running a 5 W LED for 1 second (≈ 0.32 µg CO₂)
    led_one_second_ug = _CARBON_UG_PER_MJ * 5.0 * 1000 / 3600  # 5 W × 1 s → mJ → µg
    led_equiv = ug / led_one_second_ug if led_one_second_ug > 0 else 0
    # How many million runs equal 1 g CO₂?
    runs_per_gram = (1_000_000 / ug) if ug > 0 else 0
    parts = []
    if led_equiv >= 0.01:
        parts.append(f"≈ running a 5 W LED for {led_equiv:.3f} s")
    if runs_per_gram >= 1_000:
        parts.append(f"≈ {runs_per_gram:,.0f} such analyses equal 1 g CO₂")
    elif runs_per_gram >= 1:
        parts.append(f"≈ {runs_per_gram:,.1f} analyses equal 1 g CO₂")
    return "  |  ".join(parts) if parts else "Trace-level carbon footprint."


def _bucket_label(loc: int) -> str:
    for upper, label in LOC_BUCKETS:
        if loc <= upper:
            return label
    return LOC_BUCKETS[-1][1]


def _format_ms(value: float) -> str:
    return f"{value:.2f} ms"


def _format_energy(value: float) -> str:
    return f"{value:.3f} mJ"


def _format_delta(current: float, previous: float, suffix: str = "") -> str:
    delta = current - previous
    direction = "+" if delta >= 0 else ""
    return f"{direction}{delta:.3f}{suffix}"


def _load_history() -> Dict[str, Any]:
    if not os.path.exists(HISTORY_FILE):
        return {"version": 1, "runs": []}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as fh:
            payload = json.load(fh)
        if not isinstance(payload, dict):
            return {"version": 1, "runs": []}
        payload.setdefault("version", 1)
        payload.setdefault("runs", [])
        if not isinstance(payload["runs"], list):
            payload["runs"] = []
        return payload
    except Exception:
        return {"version": 1, "runs": []}


def _save_history(history: Dict[str, Any]) -> None:
    _ensure_dir(REPORT_DIR)
    with open(HISTORY_FILE, "w", encoding="utf-8") as fh:
        json.dump(history, fh, indent=2)


def _compute_useful_work_units(run: Dict[str, Any]) -> float:
    loc = max(_safe_float(run.get("loc")), 1.0)
    statements = max(_safe_float(run.get("statement_count")), 0.0)
    functions = max(_safe_float(run.get("function_count")), 0.0)
    tac = max(_safe_float(run.get("tac_instructions")), 0.0)
    cfg_blocks = max(_safe_float(run.get("cfg_blocks")), 0.0)
    loops = max(_safe_float(run.get("loops_detected")), 0.0)
    branches = max(_safe_float(run.get("branches_detected")), 0.0)
    complexity = max(_safe_float(run.get("cyclomatic_complexity")), 1.0)
    nesting = max(_safe_float(run.get("max_nesting_depth")), 0.0)
    errors = max(_safe_float(run.get("error_count")), 0.0)

    raw_work = (
        loc
        + 0.55 * statements
        + 2.5 * functions
        + 0.30 * tac
        + 0.45 * cfg_blocks
        + 0.25 * loops
        + 0.20 * branches
    )
    penalty = 1.0 + 0.045 * complexity + 0.05 * nesting + 0.08 * errors
    return raw_work / penalty


def _bounded_efficiency_score(total_useful_work: float, total_energy_mj: float) -> float:
    total_useful_work = max(total_useful_work, 0.0)
    total_energy_mj = max(total_energy_mj, 0.0)
    return round(100.0 * total_useful_work / (total_useful_work + 4.0 * total_energy_mj + 1e-9), 4)


def _refresh_history_metrics(history_runs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    cumulative_energy = 0.0
    refreshed: List[Dict[str, Any]] = []

    for idx, run in enumerate(history_runs, 1):
        item = dict(run)
        item["run_number"] = idx
        if "loc_bucket" not in item:
            item["loc_bucket"] = _bucket_label(_safe_int(item.get("loc")))

        useful_work = _compute_useful_work_units(item)
        item["useful_work_units"] = round(useful_work, 4)
        item["efficiency_score"] = _bounded_efficiency_score(
            useful_work,
            _safe_float(item.get("estimated_energy_mj")),
        )

        cumulative_energy += _safe_float(item.get("estimated_energy_mj"))
        item["cumulative_energy_mj"] = round(cumulative_energy, 4)
        refreshed.append(item)

    return refreshed


def _extract_hotspots(complexity: Dict[str, Any],
                      ir_program,
                      control_flow: Dict[str, Any],
                      diagnostics: Iterable[Any]) -> List[Dict[str, Any]]:
    hotspots: List[Dict[str, Any]] = []

    for fn in complexity.get("per_function", []):
        cc = _safe_int(fn.get("cyclomatic_complexity"))
        depth = _safe_int(fn.get("max_nesting_depth"))
        loc = max(_safe_int(fn.get("estimated_loc")), 1)
        stmts = _safe_int(fn.get("statement_count"))
        score = cc * 2.0 + depth * 2.6 + stmts * 0.35 + loc * 0.08
        reasons = [
            f"CC {cc}",
            f"Nesting {depth}",
            f"{stmts} statements",
            f"{loc} LOC",
        ]
        hotspots.append({
            "name": fn.get("name", "<function>"),
            "kind": "function",
            "line": _safe_int(fn.get("line")),
            "score": round(score, 3),
            "reasons": reasons,
        })

    if ir_program is not None:
        for cfg_name, cfg in ir_program.all_cfgs():
            for block_id, block in cfg.blocks.items():
                instr_count = len(getattr(block, "instrs", []))
                branch_bonus = max(len(getattr(block, "successors", [])) - 1, 0) * 2.0
                if instr_count <= 0:
                    continue
                line = 0
                for instr in getattr(block, "instrs", []):
                    if getattr(instr, "line", 0) > 0:
                        line = instr.line
                        break
                score = instr_count * 1.1 + branch_bonus
                if score < 4:
                    continue
                hotspots.append({
                    "name": f"{cfg_name}:{block_id}",
                    "kind": "block",
                    "line": line,
                    "score": round(score, 3),
                    "reasons": [
                        f"{instr_count} TAC instructions",
                        f"{len(getattr(block, 'successors', []))} outgoing edges",
                    ],
                })

    diag_counts: Dict[int, int] = {}
    for diag in diagnostics:
        line = _safe_int(getattr(diag, "line", 0))
        if line > 0:
            diag_counts[line] = diag_counts.get(line, 0) + 1

    for line, count in diag_counts.items():
        if count < 2:
            continue
        hotspots.append({
            "name": f"Line {line}",
            "kind": "diagnostic-cluster",
            "line": line,
            "score": round(count * 2.25, 3),
            "reasons": [f"{count} diagnostics overlap on this line"],
        })

    unreachable = control_flow.get("unreachable_block_ids", []) or []
    if unreachable:
        hotspots.append({
            "name": "Unreachable CFG blocks",
            "kind": "control-flow",
            "line": 0,
            "score": round(len(unreachable) * 2.8, 3),
            "reasons": [f"{len(unreachable)} unreachable blocks detected"],
        })

    hotspots.sort(key=lambda item: (-item["score"], item["line"] or 10**9, item["name"]))
    return hotspots[:5]


def _build_current_loc_projection(run_entry: Dict[str, Any]) -> List[Dict[str, Any]]:
    loc = max(_safe_int(run_entry["loc"]), 1)
    cc = _safe_float(run_entry.get("cyclomatic_complexity"), 1.0)
    loops = _safe_float(run_entry.get("loops_detected"), 0.0)
    branches = _safe_float(run_entry.get("branches_detected"), 0.0)
    errors = _safe_float(run_entry.get("error_count"), 0.0)
    base_energy = max(_safe_float(run_entry["estimated_energy_mj"]), 0.02)

    complexity_density = min(cc / loc, 1.5)
    control_density = min((loops + branches) / loc, 1.5)
    error_density = min(errors / loc, 1.5)

    points = []
    for bucket_loc in LOC_RANGE_POINTS:
        size_ratio = bucket_loc / loc
        growth = size_ratio
        projected = base_energy * growth
        projected *= 1.0 + complexity_density * 0.12
        projected *= 1.0 + control_density * 0.07
        projected *= 1.0 + error_density * 0.05
        points.append({
            "x": bucket_loc,
            "label": LOC_RANGE_LABELS.get(bucket_loc, str(bucket_loc)),
            "value": round(projected, 4),
        })
    return points


def _summarize_current(run_entry: Dict[str, Any], hotspots: List[Dict[str, Any]]) -> str:
    power_mw   = _safe_float(run_entry.get("power_mw"))
    carbon_ug  = _safe_float(run_entry.get("carbon_ug_co2"))
    lines = [
        "Current Code Performance & Energy Report",
        "",
        f"Language: {run_entry['language'].upper()}",
        f"Program: {run_entry['filepath']}",
        f"LOC: {run_entry['loc']} ({run_entry['loc_bucket']})",
        # ── Energy ─────────────────────────────────────────────────────────
        f"Estimated energy consumption: {_format_energy(run_entry['estimated_energy_mj'])}",
        f"Estimated power draw: {_format_power(power_mw)}",
        # ── Carbon ─────────────────────────────────────────────────────────
        f"Carbon emission (this run): {_format_carbon(carbon_ug)}",
        f"Carbon context: {_carbon_context(carbon_ug)}",
        # ── Timing ─────────────────────────────────────────────────────────
        f"Total analysis time: {_format_ms(run_entry['total_analysis_ms'])}",
        f"Parse time: {_format_ms(run_entry['parse_time_ms'])}",
        f"IR build time: {_format_ms(run_entry['ir_build_time_ms'])}",
        f"Analysis pass time: {_format_ms(run_entry['analysis_pass_ms'])}",
        f"Throughput: {run_entry['throughput_loc_per_s']:.2f} LOC/s",
        f"Efficiency score: {run_entry['efficiency_score']:.2f}",
        f"Useful work units: {run_entry['useful_work_units']:.2f}",
        f"CFG blocks / edges / TAC: {run_entry['cfg_blocks']} / {run_entry['cfg_edges']} / {run_entry['tac_instructions']}",
        f"Cyclomatic complexity: {run_entry['cyclomatic_complexity']} ({run_entry['complexity_rating']})",
        f"Max nesting depth: {run_entry['max_nesting_depth']}",
        f"Loops / branches / diagnostics: {run_entry['loops_detected']} / {run_entry['branches_detected']} / {run_entry['error_count']}",
        "",
        "Hotspots:",
    ]

    if hotspots:
        for item in hotspots:
            location = f"line {item['line']}" if item.get("line") else "global"
            lines.append(
                f"- {item['name']} [{item['kind']}] score {item['score']:.2f} at {location}: "
                + ", ".join(item["reasons"])
            )
    else:
        lines.append("- No dominant hotspots detected in the current run.")

    return "\n".join(lines)


def _summarize_cumulative(run_entry: Dict[str, Any],
                          history_runs: List[Dict[str, Any]]) -> str:
    total_runs    = len(history_runs)
    total_energy  = sum(_safe_float(item.get("estimated_energy_mj")) for item in history_runs)
    total_carbon  = sum(_safe_float(item.get("carbon_ug_co2"))        for item in history_runs)
    avg_energy    = total_energy / total_runs if total_runs else 0.0
    avg_carbon    = total_carbon / total_runs if total_runs else 0.0
    avg_power     = sum(_safe_float(item.get("power_mw")) for item in history_runs) / total_runs if total_runs else 0.0
    avg_runtime   = (
        sum(_safe_float(item.get("total_analysis_ms")) for item in history_runs) / total_runs
        if total_runs else 0.0
    )
    avg_efficiency = (
        sum(_safe_float(item.get("efficiency_score")) for item in history_runs) / total_runs
        if total_runs else 0.0
    )
    previous = history_runs[-2] if total_runs >= 2 else None

    lines = [
        "Cumulative Performance & Energy Report",
        "",
        f"Total analyzed runs: {total_runs}",
        f"Cumulative estimated energy: {_format_energy(total_energy)}",
        f"Cumulative carbon emission: {_format_carbon(total_carbon)}",
        f"Average carbon per run: {_format_carbon(avg_carbon)}",
        f"Average power draw per run: {_format_power(avg_power)}",
        f"Average energy per run: {_format_energy(avg_energy)}",
        f"Average analysis time: {_format_ms(avg_runtime)}",
        f"Average per-run efficiency score: {avg_efficiency:.2f}",
        f"Latest run bucket: {run_entry['loc_bucket']}",
    ]

    if previous:
        prev_carbon = _safe_float(previous.get("carbon_ug_co2"))
        cur_carbon  = _safe_float(run_entry.get("carbon_ug_co2"))
        lines.extend([
            "",
            "Comparison vs previous run:",
            f"- Energy delta: {_format_delta(run_entry['estimated_energy_mj'], _safe_float(previous.get('estimated_energy_mj')), ' mJ')}",
            f"- Carbon delta: {_format_delta(cur_carbon, prev_carbon, ' µg CO₂')}",
            f"- Runtime delta: {_format_delta(run_entry['total_analysis_ms'], _safe_float(previous.get('total_analysis_ms')), ' ms')}",
            f"- Efficiency delta: {_format_delta(run_entry['efficiency_score'], _safe_float(previous.get('efficiency_score')))}",
            f"- LOC delta: {_safe_int(run_entry['loc']) - _safe_int(previous.get('loc')):+d}",
        ])

    best = sorted(history_runs, key=lambda item: _safe_float(item.get("efficiency_score")), reverse=True)[:3]
    lines.extend(["", "Most efficient runs:"])
    for item in best:
        lines.append(
            f"- Run {item.get('run_number', '?')} | {item.get('filepath', '<input>')} | "
            f"{item.get('efficiency_score', 0):.2f} efficiency | "
            f"{item.get('loc', 0)} LOC | {_format_energy(_safe_float(item.get('estimated_energy_mj')))} | "
            f"{_format_carbon(_safe_float(item.get('carbon_ug_co2')))}"
        )

    return "\n".join(lines)


def _series_from_runs(history_runs: List[Dict[str, Any]], key: str, label: str) -> Dict[str, Any]:
    points = []
    for idx, run in enumerate(history_runs, 1):
        run_number = _safe_int(run.get("run_number"), idx)
        points.append({
            "x": run_number,
            "label": f"Run {run_number}",
            "value": round(_safe_float(run.get(key)), 4),
        })
    return {"label": label, "points": points}


def _loc_bucket_chart(history_runs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    buckets = {label: 0.0 for _, label in LOC_BUCKETS}
    counts = {label: 0 for _, label in LOC_BUCKETS}
    for run in history_runs:
        label = run.get("loc_bucket", _bucket_label(_safe_int(run.get("loc"))))
        buckets[label] = buckets.get(label, 0.0) + _safe_float(run.get("estimated_energy_mj"))
        counts[label] = counts.get(label, 0) + 1
    return [
        {
            "label": label,
            "value": round(buckets[label], 4),
            "count": counts[label],
        }
        for _, label in LOC_BUCKETS
    ]


def _current_loc_range_chart(run_entry: Dict[str, Any], projected_points: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "label": point["label"],
            "value": round(_safe_float(point.get("value")), 4),
        }
        for point in projected_points
    ]


def _svg_escape(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _write_svg(path: str, content: str) -> str:
    _ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return path


def _line_chart_svg(title: str,
                    series: List[Dict[str, Any]],
                    width: int = 860,
                    height: int = 320) -> str:
    if not series:
        series = [{"label": "Series", "points": []}]

    margin_left = 62
    margin_right = 24
    margin_top = 36
    margin_bottom = 52
    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom
    all_points = [point for item in series for point in item.get("points", [])]
    if not all_points:
        all_points = [{"x": 1, "label": "1", "value": 0.0}]
    min_x = min(point["x"] for point in all_points)
    max_x = max(point["x"] for point in all_points)
    max_y = max(point["value"] for point in all_points)
    max_y = max(max_y, 1.0)
    colors = ["#2563eb", "#d97706", "#15803d", "#dc2626"]

    def sx(x: float) -> float:
        span = max(max_x - min_x, 1)
        return margin_left + ((x - min_x) / span) * plot_w

    def sy(y: float) -> float:
        return margin_top + plot_h - (y / max_y) * plot_h

    y_grid = []
    for step in range(5):
        value = max_y * step / 4
        y = sy(value)
        y_grid.append(
            f'<line x1="{margin_left}" y1="{y:.2f}" x2="{width - margin_right}" y2="{y:.2f}" '
            f'stroke="#dbe4ee" stroke-width="1" />'
            f'<text x="10" y="{y + 4:.2f}" font-size="11" fill="#64748b">{value:.2f}</text>'
        )

    x_labels = []
    for point in series[0]["points"]:
        x = sx(point["x"])
        x_labels.append(
            f'<text x="{x:.2f}" y="{height - 20}" text-anchor="middle" font-size="11" fill="#64748b">'
            f'{_svg_escape(point["label"])}</text>'
        )

    poly_parts = []
    legends = []
    for idx, item in enumerate(series):
        color = colors[idx % len(colors)]
        points = item.get("points", [])
        coords = " ".join(f"{sx(p['x']):.2f},{sy(p['value']):.2f}" for p in points) or f"{margin_left},{sy(0):.2f}"
        poly_parts.append(
            f'<polyline fill="none" stroke="{color}" stroke-width="3" points="{coords}" />'
        )
        for p in points:
            poly_parts.append(
                f'<circle cx="{sx(p["x"]):.2f}" cy="{sy(p["value"]):.2f}" r="4.5" fill="{color}" />'
            )
        legends.append(
            f'<rect x="{margin_left + idx * 170}" y="12" width="14" height="14" fill="{color}" rx="2" />'
            f'<text x="{margin_left + idx * 170 + 22}" y="24" font-size="12" fill="#0f172a">{_svg_escape(item["label"])}</text>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="#ffffff"/>
<text x="{margin_left}" y="24" font-size="16" font-weight="700" fill="#0f172a">{_svg_escape(title)}</text>
{''.join(legends)}
{''.join(y_grid)}
<line x1="{margin_left}" y1="{margin_top + plot_h}" x2="{width - margin_right}" y2="{margin_top + plot_h}" stroke="#94a3b8" stroke-width="1.5"/>
<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_h}" stroke="#94a3b8" stroke-width="1.5"/>
{''.join(poly_parts)}
{''.join(x_labels)}
</svg>"""


def _bar_chart_svg(title: str,
                   items: List[Dict[str, Any]],
                   value_key: str = "value",
                   width: int = 860,
                   height: int = 320,
                   color: str = "#2563eb") -> str:
    margin_left = 62
    margin_right = 24
    margin_top = 36
    margin_bottom = 74
    plot_w = width - margin_left - margin_right
    plot_h = height - margin_top - margin_bottom
    if not items:
        items = [{"label": "None", value_key: 0.0}]
    max_y = max(_safe_float(item.get(value_key)) for item in items)
    max_y = max(max_y, 1.0)
    bar_gap = 16
    bar_w = max((plot_w - bar_gap * (len(items) + 1)) / max(len(items), 1), 18)

    bars = []
    labels = []
    for idx, item in enumerate(items):
        value = _safe_float(item.get(value_key))
        x = margin_left + bar_gap + idx * (bar_w + bar_gap)
        h = (value / max_y) * plot_h
        y = margin_top + plot_h - h
        bars.append(
            f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_w:.2f}" height="{h:.2f}" fill="{color}" rx="6" />'
            f'<text x="{x + bar_w / 2:.2f}" y="{y - 8:.2f}" text-anchor="middle" font-size="11" fill="#0f172a">{value:.2f}</text>'
        )
        labels.append(
            f'<text x="{x + bar_w / 2:.2f}" y="{height - 30}" text-anchor="middle" font-size="11" fill="#64748b">'
            f'{_svg_escape(item.get("label", ""))}</text>'
        )

    y_grid = []
    for step in range(5):
        value = max_y * step / 4
        y = margin_top + plot_h - (value / max_y) * plot_h
        y_grid.append(
            f'<line x1="{margin_left}" y1="{y:.2f}" x2="{width - margin_right}" y2="{y:.2f}" stroke="#dbe4ee" stroke-width="1" />'
            f'<text x="10" y="{y + 4:.2f}" font-size="11" fill="#64748b">{value:.2f}</text>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="#ffffff"/>
<text x="{margin_left}" y="24" font-size="16" font-weight="700" fill="#0f172a">{_svg_escape(title)}</text>
{''.join(y_grid)}
<line x1="{margin_left}" y1="{margin_top + plot_h}" x2="{width - margin_right}" y2="{margin_top + plot_h}" stroke="#94a3b8" stroke-width="1.5"/>
<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_h}" stroke="#94a3b8" stroke-width="1.5"/>
{''.join(bars)}
{''.join(labels)}
</svg>"""


def _export_svgs(current_summary: str,
                 cumulative_summary: str,
                 current_projection: List[Dict[str, Any]],
                 hotspots: List[Dict[str, Any]],
                 energy_series: Dict[str, Any],
                 loc_buckets: List[Dict[str, Any]]) -> Dict[str, str]:
    current_dir = os.path.join(REPORT_DIR, "current")
    cumulative_dir = os.path.join(REPORT_DIR, "cumulative")
    _ensure_dir(current_dir)
    _ensure_dir(cumulative_dir)

    summary_paths = {
        "current_summary": os.path.join(current_dir, "current_report_summary.txt"),
        "cumulative_summary": os.path.join(cumulative_dir, "cumulative_report_summary.txt"),
    }
    with open(summary_paths["current_summary"], "w", encoding="utf-8") as fh:
        fh.write(current_summary)
    with open(summary_paths["cumulative_summary"], "w", encoding="utf-8") as fh:
        fh.write(cumulative_summary)

    exports = {
        **summary_paths,
        "current_energy_loc_svg": _write_svg(
            os.path.join(current_dir, "energy_vs_loc.svg"),
            _bar_chart_svg(
                "Energy Consumption by LOC Range",
                current_projection,
                color="#2563eb",
            ),
        ),
        "current_hotspots_svg": _write_svg(
            os.path.join(current_dir, "hotspots.svg"),
            _bar_chart_svg(
                "Current Hotspot Scores",
                [{"label": item["name"], "value": item["score"]} for item in hotspots] or [{"label": "None", "value": 0.0}],
                color="#d97706",
            ),
        ),
        "cumulative_energy_trend_svg": _write_svg(
            os.path.join(cumulative_dir, "energy_trend.svg"),
            _line_chart_svg("Cumulative Energy vs Code Sample Number", [energy_series]),
        ),
        "cumulative_loc_ranges_svg": _write_svg(
            os.path.join(cumulative_dir, "loc_bucket_energy.svg"),
            _bar_chart_svg("Cumulative Energy by LOC Range", loc_buckets, color="#15803d"),
        ),
    }
    return exports


def build_reports(source: str,
                  language: str,
                  filepath: str,
                  ast_tree=None,
                  ir_program=None,
                  errors: Iterable[Any] | None = None,
                  timing_breakdown: Dict[str, float] | None = None,
                  persist: bool = True) -> Dict[str, Any]:
    from week_7.analysis_modules.complexity import ComplexityAnalyzer
    from week_7.analysis_modules.control_flow import ControlFlowAnalyzer

    diagnostics = list(errors or [])
    complexity = {}
    control_flow = {}

    if ast_tree is not None:
        try:
            complexity = ComplexityAnalyzer().analyze(ast_tree)
        except Exception:
            complexity = {}
        try:
            control_flow = ControlFlowAnalyzer().analyze(ast_tree)
        except Exception:
            control_flow = {}

    loc = _safe_int(complexity.get("estimated_loc")) or _non_empty_loc(source)
    statement_count = _safe_int(complexity.get("statement_count"), loc)
    function_count = _safe_int(complexity.get("function_count"))
    cc = max(_safe_int(complexity.get("cyclomatic_complexity"), 1), 1)
    max_depth = _safe_int(complexity.get("max_nesting_depth"))
    complexity_rating = complexity.get("complexity_rating", "unknown")

    cfg_blocks = 0
    cfg_edges = 0
    tac_instructions = 0
    if ir_program is not None:
        try:
            for _, cfg in ir_program.all_cfgs():
                cfg_blocks += len(cfg.blocks)
                cfg_edges += sum(len(block.successors) for block in cfg.blocks.values())
                tac_instructions += sum(len(block.instrs) for block in cfg.blocks.values())
        except Exception:
            pass

    loops = _safe_int(control_flow.get("summary", {}).get("loops_detected"))
    branches = _safe_int(control_flow.get("summary", {}).get("branches_detected"))
    unreachable = control_flow.get("unreachable_block_ids", []) or []

    timing_breakdown = timing_breakdown or {}
    parse_ms = max(_safe_float(timing_breakdown.get("parse_time_ms")), 0.01)
    ir_ms = max(_safe_float(timing_breakdown.get("ir_build_time_ms")), 0.0)
    analysis_ms = max(_safe_float(timing_breakdown.get("analysis_pass_ms")), 0.0)
    total_ms = max(_safe_float(timing_breakdown.get("total_analysis_ms"), parse_ms + ir_ms + analysis_ms), 0.01)

    error_count = len(diagnostics)
    throughput = loc / (total_ms / 1000.0) if total_ms > 0 else 0.0
    energy_mj = (
        0.038 * total_ms
        + 0.012 * tac_instructions
        + 0.18 * cc
        + 0.08 * branches
        + 0.11 * loops
        + 0.06 * error_count
        + 0.015 * statement_count
    )
    energy_mj = round(max(energy_mj, 0.02), 4)

    # ── Power & carbon ───────────────────────────────────────────────────────
    power_mw      = round(energy_mj / (total_ms / 1000.0), 6) if total_ms > 0 else 0.0
    carbon_ug_co2 = round(energy_mj * _CARBON_UG_PER_MJ, 6)

    useful_work_units = _compute_useful_work_units({
        "loc": loc,
        "statement_count": statement_count,
        "function_count": function_count,
        "tac_instructions": tac_instructions,
        "cfg_blocks": cfg_blocks,
        "loops_detected": loops,
        "branches_detected": branches,
        "cyclomatic_complexity": cc,
        "max_nesting_depth": max_depth,
        "error_count": error_count,
    })
    efficiency_score = _bounded_efficiency_score(useful_work_units, energy_mj)

    run_entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "filepath": filepath,
        "language": language,
        "loc": loc,
        "loc_bucket": _bucket_label(loc),
        "statement_count": statement_count,
        "function_count": function_count,
        "cyclomatic_complexity": cc,
        "max_nesting_depth": max_depth,
        "complexity_rating": complexity_rating,
        "cfg_blocks": cfg_blocks,
        "cfg_edges": cfg_edges,
        "tac_instructions": tac_instructions,
        "loops_detected": loops,
        "branches_detected": branches,
        "unreachable_blocks": len(unreachable),
        "error_count": error_count,
        "parse_time_ms": round(parse_ms, 4),
        "ir_build_time_ms": round(ir_ms, 4),
        "analysis_pass_ms": round(analysis_ms, 4),
        "total_analysis_ms": round(total_ms, 4),
        "estimated_energy_mj": energy_mj,
        "power_mw":            round(power_mw, 6),
        "carbon_ug_co2":       round(carbon_ug_co2, 6),
        "throughput_loc_per_s": round(throughput, 4),
        "useful_work_units": round(useful_work_units, 4),
        "efficiency_score": efficiency_score,
    }

    history = _load_history()
    if persist:
        history["runs"].append(run_entry)
    history["runs"] = _refresh_history_metrics(history["runs"])
    if persist:
        _save_history(history)
    history_runs = history["runs"]
    if history_runs:
        run_entry = history_runs[-1]

    hotspots = _extract_hotspots(complexity, ir_program, control_flow, diagnostics)
    current_projection = _build_current_loc_projection(run_entry)
    current_loc_range_bars = _current_loc_range_chart(run_entry, current_projection)
    current_summary = _summarize_current(run_entry, hotspots)
    cumulative_summary = _summarize_cumulative(run_entry, history_runs)

    energy_series = _series_from_runs(history_runs, "cumulative_energy_mj", "Cumulative energy (mJ)")
    loc_bucket_series = _loc_bucket_chart(history_runs)
    exports = _export_svgs(
        current_summary=current_summary,
        cumulative_summary=cumulative_summary,
        current_projection=current_loc_range_bars,
        hotspots=hotspots,
        energy_series=energy_series,
        loc_buckets=loc_bucket_series,
    )

    return {
        "history_path": HISTORY_FILE,
        "run": run_entry,
        "current": {
            "summary": current_summary,
            "hotspots": hotspots,
            "energy_loc_points": current_projection,
            "energy_loc_bars": current_loc_range_bars,
            "power_mw":      run_entry.get("power_mw", 0.0),
            "carbon_ug_co2": run_entry.get("carbon_ug_co2", 0.0),
            "exports": {
                "summary": exports["current_summary"],
                "energy_loc_svg": exports["current_energy_loc_svg"],
                "hotspots_svg": exports["current_hotspots_svg"],
            },
        },
        "cumulative": {
            "summary": cumulative_summary,
            "energy_trend": energy_series,
            "loc_bucket_energy": loc_bucket_series,
            "total_carbon_ug": sum(_safe_float(r.get("carbon_ug_co2")) for r in history_runs),
            "avg_power_mw":   sum(_safe_float(r.get("power_mw"))       for r in history_runs) / max(len(history_runs), 1),
            "exports": {
                "summary": exports["cumulative_summary"],
                "energy_trend_svg": exports["cumulative_energy_trend_svg"],
                "loc_bucket_svg": exports["cumulative_loc_ranges_svg"],
            },
        },
    }
