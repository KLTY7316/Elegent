"""
安全帽智能检测系统 - 主入口
Helmet Detection System — Streamlit Frontend
"""
import streamlit as st
import sys
from pathlib import Path

# 确保 utils 可导入
sys.path.insert(0, str(Path(__file__).parent))

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
# 注入统一的全局样式（深色侧边栏 + 组件美化）
# ============================================================
from utils.styles import inject_common_styles
inject_common_styles()

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
