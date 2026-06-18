"""
统计看板页面 — Plotly 可视化
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.get_statistics import get_statistics

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="安全帽检测 - 统计看板",
    page_icon="⛑️",
    layout="wide",
)

from utils.styles import inject_common_styles
inject_common_styles()

st.markdown('<h1 class="main-header">📊 统计看板</h1>', unsafe_allow_html=True)
st.markdown("---")
st.caption("实时监控数据可视化，全面掌握安全帽佩戴情况")

# ============================================================
# 读取 session_state 检测历史
# ============================================================
history = st.session_state.get("detection_history", [])

if not history:
    st.warning("暂无检测数据。请先前往「图片检测」或「视频检测」页面进行检测，数据将自动汇总到此处。")
    st.stop()

# 聚合统计数据
total_detections = sum(h.get("total_persons", 0) for h in history)
total_helmet = sum(h.get("helmet_count", 0) for h in history)
total_no_helmet = sum(h.get("no_helmet_count", 0) for h in history)
avg_confidence = round(sum(h.get("avg_confidence", 0) for h in history) / max(len(history), 1), 1)
helmet_rate = round(total_helmet / max(total_detections, 1) * 100, 1)

# ============================================================
# 顶部统计卡片
# ============================================================
st.markdown("### 📈 今日概览")
col_s1, col_s2 = st.columns(2)

with col_s1:
    st.metric("📋 今日检测", f"{total_detections:,}")
    st.metric("✅ 佩戴人数", f"{total_helmet:,}")
    st.metric("📊 佩戴率", f"{helmet_rate}%")
with col_s2:
    st.metric("🚨 违规人数", f"{total_no_helmet:,}")
    st.metric("🎯 平均置信度", f"{avg_confidence}%")
    violation_rate = 100 - helmet_rate
    if violation_rate < 10:
        risk_text = "🟢 低风险"
        risk_color = "#00C853"
    elif violation_rate < 20:
        risk_text = "🟡 中风险"
        risk_color = "#FF9100"
    else:
        risk_text = "🔴 高风险"
        risk_color = "#FF1744"
    st.markdown(f"<p style='color:{risk_color};font-size:18px;font-weight:bold;'>{risk_text}</p>", unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# 图表区域
# ============================================================
# 构建 DataFrame（按日期聚合）
from collections import defaultdict
agg = defaultdict(lambda: {"total_detections": 0, "violations": 0, "helmet_count": 0})
for h in history:
    date = h.get("timestamp", "")[:5]  # mm-dd
    if not date:
        continue
    agg[date]["total_detections"] += h.get("total_persons", 0)
    agg[date]["violations"] += h.get("no_helmet_count", 0)
    agg[date]["helmet_count"] += h.get("helmet_count", 0)

history_list = []
for date in sorted(agg.keys()):
    d = agg[date]
    d["date"] = date
    d["violation_rate"] = round(d["violations"] / max(d["total_detections"], 1) * 100, 1)
    history_list.append(d)

df = pd.DataFrame(history_list)
if df.empty:
    df = pd.DataFrame(columns=["date", "total_detections", "violations", "helmet_count", "violation_rate"])

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("#### 🍩 安全帽佩戴分布")
    # 饼图
    fig_pie = go.Figure(data=[
        go.Pie(
            labels=["佩戴安全帽", "未佩戴安全帽"],
            values=[total_helmet, total_no_helmet],
            marker=dict(colors=["#00C853", "#FF1744"]),
            hole=0.6,
            textinfo="percent+label",
            textfont=dict(size=14),
        )
    ])
    fig_pie.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=20, b=20),
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_pie, width='stretch')

current_violation_rate = round(total_no_helmet / max(total_detections, 1) * 100, 1)

with col_chart2:
    st.markdown("#### ⚡ 违规率仪表盘")
    # 仪表盘
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=current_violation_rate,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "当前违规率 (%)"},
        number={"suffix": "%", "font": {"size": 48}},
        gauge={
            "axis": {"range": [0, 30], "tickwidth": 1},
            "bar": {"color": "#FF9100"},
            "steps": [
                {"range": [0, 5], "color": "#00C853"},
                {"range": [5, 10], "color": "#FFEB3B"},
                {"range": [10, 20], "color": "#FF9100"},
                {"range": [20, 30], "color": "#FF1744"},
            ],
            "threshold": {
                "line": {"color": "#FF1744", "width": 3},
                "thickness": 0.8,
                "value": 15,
            },
        },
    ))
    fig_gauge.update_layout(
        height=350,
        margin=dict(t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_gauge, width='stretch')

# 第二行图表
col_chart3, col_chart4 = st.columns(2)

with col_chart3:
    st.markdown("#### 📉 检测历史趋势（近7天）")
    # 折线图
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=df["date"],
        y=df["total_detections"],
        name="总检测数",
        mode="lines+markers",
        line=dict(color="#2979FF", width=3),
        marker=dict(size=8),
    ))
    fig_line.add_trace(go.Scatter(
        x=df["date"],
        y=df["violations"],
        name="违规次数",
        mode="lines+markers",
        line=dict(color="#FF1744", width=3),
        marker=dict(size=8),
        fill="tozeroy",
        fillcolor="rgba(255,23,68,0.1)",
    ))
    fig_line.update_layout(
        xaxis_title="日期",
        yaxis_title="人数",
        hovermode="x unified",
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        margin=dict(t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_line, width='stretch')

with col_chart4:
    st.markdown("#### 📊 各区域违规率")
    # 柱状图
    areas = ["A区-基坑", "B区-脚手架", "C区-材料区", "D区-塔吊", "E区-电梯井"]
    violation_rates = [2.1, 5.8, 3.2, 1.5, 7.3]
    colors = ["#00C853" if r < 5 else "#FF9100" if r < 8 else "#FF1744" for r in violation_rates]

    fig_bar = go.Figure(data=[
        go.Bar(
            x=areas,
            y=violation_rates,
            marker_color=colors,
            text=[f"{r}%" for r in violation_rates],
            textposition="auto",
        )
    ])
    fig_bar.update_layout(
        xaxis_title="施工区域",
        yaxis_title="违规率 (%)",
        yaxis=dict(range=[0, 15]),
        height=350,
        margin=dict(t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_bar, width='stretch')

# 第三行：违规率趋势
st.markdown("#### 📈 违规率变化趋势")
fig_rate = go.Figure()
fig_rate.add_trace(go.Scatter(
    x=df["date"],
    y=df["violation_rate"],
    name="违规率",
    mode="lines+markers+text",
    line=dict(color="#FF9100", width=3),
    marker=dict(size=10),
    text=[f"{r}%" for r in df["violation_rate"]],
    textposition="top center",
))
fig_rate.add_hline(y=10, line_dash="dash", line_color="#FF1744",
                   annotation_text="预警线 10%", annotation_position="top right")
fig_rate.update_layout(
    xaxis_title="日期",
    yaxis_title="违规率 (%)",
    height=300,
    margin=dict(t=20, b=20),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig_rate, width='stretch')

# ============================================================
# 实时刷新模拟
# ============================================================
st.markdown("---")
st.markdown("### 🔄 实时数据模拟")
if st.button("🔄 刷新数据", type="secondary"):
    st.rerun()
st.caption("数据每 30 秒自动刷新（模拟）")
