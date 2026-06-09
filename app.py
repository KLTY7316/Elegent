"""
安全帽智能检测系统 - 主入口
Helmet Detection System — Streamlit Frontend
"""
import streamlit as st

# ============================================================
# 页面全局配置（必须在第一个 st 命令之前）
# ============================================================
st.set_page_config(
    page_title="⛑️ 安全帽智能检测系统",
    page_icon="⛑️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 全局自定义 CSS —— 统一配色方案
# ============================================================
st.markdown("""
<style>
/* 全局字体 */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;600;700&display=swap');

/* 主色调变量 */
:root {
    --safe-green: #00C853;
    --danger-red: #FF1744;
    --warn-orange: #FF9100;
    --primary-blue: #2979FF;
    --bg-dark: #0F1923;
    --card-bg: #1A2736;
}

/* 隐藏 Streamlit 默认 hamburger menu */
#MainMenu {visibility: hidden;}

/* 侧边栏美化 */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F1923 0%, #1A2736 100%);
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #FFFFFF;
}

/* Metric 卡片美化 */
[data-testid="stMetricValue"] {
    font-size: 2rem;
    font-weight: 700;
}

/* 按钮美化 */
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

/* 文件上传区域美化 */
[data-testid="stFileUploader"] section {
    border: 2px dashed #2979FF !important;
    border-radius: 12px;
    background: #1A2736;
}

/* 页面标题 */
.main-header {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(90deg, #2979FF, #00E5FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# 侧边栏
# ============================================================
with st.sidebar:
    st.markdown("## ⛑️ 安全帽检测系统")
    st.markdown("---")
    st.markdown("### 📋 导航")
    st.info("使用左侧导航栏切换不同功能页面")

    st.markdown("---")
    st.markdown("### 📊 系统状态")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("模型", "YOLOv8", delta="就绪")
    with col2:
        st.metric("GPU", "可用", delta="正常")

    st.markdown("---")
    st.markdown("### ℹ️ 关于")
    st.caption("""
    **安全帽智能检测系统 v1.0**

    基于 YOLOv8 深度学习模型，
    实现施工场景安全帽佩戴检测。

    🤖 AI 驱动 · 🎯 实时检测 · 📊 智能分析
    """)

# ============================================================
# 首页内容
# ============================================================
st.markdown('<h1 class="main-header">⛑️ 安全帽智能检测系统</h1>', unsafe_allow_html=True)
st.markdown("---")

st.markdown("## 🎯 系统简介")
st.markdown("""
本系统基于 **YOLOv8** 深度学习模型，针对建筑施工场景实现：
- 📸 **图片检测** — 上传图片，自动识别安全帽佩戴情况
- 🎥 **视频检测** — 上传视频文件，逐帧分析安全帽佩戴
- 📹 **实时摄像头** — 接入摄像头，实时检测与预警
- 📊 **统计看板** — 可视化展示检测数据与趋势
- 🤖 **AI 报告** — 基于 LLM 自动生成安全分析报告
- 📁 **历史记录** — 浏览违规截图与检测历史
""")

# 首页统计卡片
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="今日检测", value="1,284", delta="↑ 12%")
with col2:
    st.metric(label="违规次数", value="37", delta="↓ 5%", delta_color="inverse")
with col3:
    st.metric(label="佩戴率", value="97.1%", delta="↑ 2.3%")
with col4:
    st.metric(label="在线时长", value="8h 32m", delta="运行中")

st.markdown("---")
st.markdown("### 🚀 快速开始")
st.info("👉 使用左侧导航栏选择功能页面，开始使用安全帽检测系统。第一周使用模拟数据演示，第二周将接入真实 YOLOv8 模型。")
