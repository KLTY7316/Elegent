"""
历史记录页面 — 违规截图浏览与检测历史
"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.fake_data import fake_violation_records

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="历史记录 - 安全帽检测系统",
    page_icon="📁",
    layout="wide",
)

st.markdown('<h1 class="main-header">📁 历史记录</h1>', unsafe_allow_html=True)
st.markdown("---")
st.caption("浏览违规截图与检测历史记录")

# ============================================================
# 筛选器
# ============================================================
col_filter1, col_filter2, col_filter3, col_filter4 = st.columns(4)

with col_filter1:
    date_range = st.selectbox(
        "时间范围",
        ["全部", "今日", "近7天", "近30天"],
        index=0,
    )

with col_filter2:
    location_filter = st.selectbox(
        "施工区域",
        ["全部", "A区-基坑旁", "B区-脚手架", "C区-材料堆放区",
         "D区-塔吊下方", "E区-电梯井口"],
        index=0,
    )

with col_filter3:
    severity_filter = st.selectbox(
        "严重程度",
        ["全部", "高", "中", "低"],
        index=0,
    )

with col_filter4:
    status_filter = st.selectbox(
        "处理状态",
        ["全部", "已处理", "待处理", "处理中"],
        index=0,
    )

# ============================================================
# 统计概览
# ============================================================
st.markdown("### 📊 违规统计")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("总违规记录", "156", delta="本周 +12")
with col2:
    st.metric("已处理", "128", delta="处理率 82%")
with col3:
    st.metric("待处理", "22", delta_color="inverse")
with col4:
    st.metric("高危违规", "8", delta_color="inverse")

st.markdown("---")

# ============================================================
# 违规记录表格
# ============================================================
st.markdown("### 📋 违规记录列表")

records = fake_violation_records(count=20)
df = pd.DataFrame(records)

# 筛选
if date_range != "全部":
    pass  # TODO: 按日期筛选
if location_filter != "全部":
    df = df[df["location"] == location_filter]
if severity_filter != "全部":
    df = df[df["severity"] == severity_filter]
if status_filter != "全部":
    df = df[df["status"] == status_filter]

# 自定义样式
def color_status(val):
    if val == "已处理":
        return "background-color: #00C85320"
    elif val == "待处理":
        return "background-color: #FF174420"
    elif val == "处理中":
        return "background-color: #FF910020"
    return ""

def color_severity(val):
    if val == "高":
        return "color: #FF1744; font-weight: bold"
    elif val == "中":
        return "color: #FF9100; font-weight: bold"
    return "color: #00C853"

styled_df = df.style.format({"timestamp": lambda x: x}).map(color_status, subset=["status"])

st.dataframe(
    styled_df,
    width='stretch',
    height=500,
    hide_index=True,
    column_order=["id", "timestamp", "location", "violation_type", "severity", "status"],
)

# ============================================================
# 违规截图预览
# ============================================================
st.markdown("---")
st.markdown("### 🖼️ 违规截图预览")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("**VIO-1001**")
    st.markdown("📍 A区-基坑旁")
    st.markdown("🔴 高危")
    st.caption("2026-06-06 14:32:15")
    # 占位图
    st.markdown("> 📸 *[截图预览]*")

with col2:
    st.markdown("**VIO-1003**")
    st.markdown("📍 B区-脚手架")
    st.markdown("🟡 中危")
    st.caption("2026-06-06 11:20:08")
    st.markdown("> 📸 *[截图预览]*")

with col3:
    st.markdown("**VIO-1005**")
    st.markdown("📍 D区-塔吊下方")
    st.markdown("🔴 高危")
    st.caption("2026-06-05 16:45:33")
    st.markdown("> 📸 *[截图预览]*")

with col4:
    st.markdown("**VIO-1008**")
    st.markdown("📍 C区-材料堆放区")
    st.markdown("🟢 低危")
    st.caption("2026-06-05 09:12:47")
    st.markdown("> 📸 *[截图预览]*")

# ============================================================
# 操作按钮
# ============================================================
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📥 导出全部记录", key="export_all"):
        csv_path = Path("outputs/violations/violation_records.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        st.success(f"✅ 已导出到: {csv_path}")
with col2:
    if st.button("📥 导出筛选结果", key="export_filtered"):
        st.info("📋 已导出筛选后的记录")
with col3:
    if st.button("🗑️ 清除历史记录", key="clear_history"):
        st.warning("⚠️ 确认要清除所有历史记录吗？")
