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
from utils.fake_data import fake_history_data, fake_get_statistics, fake_detect

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="统计看板 - 安全帽检测系统",
    page_icon="📊",
    layout="wide",
)

from utils.styles import inject_common_styles
inject_common_styles()

st.markdown('<h1 class="main-header">📊 统计看板</h1>', unsafe_allow_html=True)
st.markdown("---")
st.caption("实时监控数据可视化，全面掌握安全帽佩戴情况")

# ============================================================
# 顶部统计卡片
# ============================================================
st.markdown("### 📈 今日概览")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("今日检测", "1,284", delta="↑ 12%")
with col2:
    st.metric("佩戴人数", "1,247", delta="↑ 8%")
with col3:
    st.metric("违规人数", "37", delta="↓ 5%", delta_color="inverse")
with col4:
    st.metric("佩戴率", "97.1%", delta="↑ 2.3%")
with col5:
    st.metric("平均置信度", "94.2%", delta="↑ 1.1%")

st.markdown("---")

# ============================================================
# 图表区域
# ============================================================
# 获取假数据
history = fake_history_data(days=7)
df = pd.DataFrame(history)

col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("#### 🍩 安全帽佩戴分布")
    # 饼图
    fig_pie = go.Figure(data=[
        go.Pie(
            labels=["佩戴安全帽", "未佩戴安全帽"],
            values=[1247, 37],
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

with col_chart2:
    st.markdown("#### ⚡ 违规率仪表盘")
    # 仪表盘
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=2.9,
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
