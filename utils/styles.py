"""
共享样式模块 —— 统一侧边栏深色主题 + 全局样式
每个页面都应调用 inject_common_styles() 以保持视觉一致
"""
import streamlit as st

# 全局共享 CSS
COMMON_CSS = """
<style>
/* ============================================================
   侧边栏深色主题 —— 强制覆盖 Streamlit 默认样式
   ============================================================ */

/* 侧边栏整体背景 */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F1923 0%, #1A2736 100%) !important;
    color: #FFFFFF !important;
}

/* 侧边栏内部所有文字默认白色 */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown span {
    color: #E0E0E0 !important;
}

/* 侧边栏标题 —— 亮白色加粗 */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* 侧边栏 caption 文字 */
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] [data-testid="stCaption"] {
    color: #B0BEC5 !important;
}

/* 侧边栏导航链接 —— 默认灰色，选中亮白 */
[data-testid="stSidebar"] .stSidebarNavLink {
    color: #90A4AE !important;
}
[data-testid="stSidebar"] .stSidebarNavLink:hover {
    color: #FFFFFF !important;
    background-color: rgba(41, 121, 255, 0.15) !important;
}
[data-testid="stSidebar"] .stSidebarNavLink.active,
[data-testid="stSidebar"] .stSidebarNavLink[data-active="true"] {
    color: #FFFFFF !important;
    background-color: rgba(41, 121, 255, 0.2) !important;
    border-left: 3px solid #2979FF !important;
}

/* 侧边栏 metric 卡片 */
[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
    color: #B0BEC5 !important;
}
[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 1.4rem;
    font-weight: 700;
}
[data-testid="stSidebar"] [data-testid="stMetricDelta"] {
    color: #00C853 !important;
}

/* 侧边栏 info/警告/成功 框 */
[data-testid="stSidebar"] [data-testid="stAlert"] {
    background-color: rgba(41, 121, 255, 0.15) !important;
    border-color: rgba(41, 121, 255, 0.3) !important;
}
[data-testid="stSidebar"] [data-testid="stAlert"] p,
[data-testid="stSidebar"] [data-testid="stAlert"] div {
    color: #E0E0E0 !important;
}

/* 侧边栏分隔线 */
[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.1) !important;
}

/* 侧边栏输入框/选择框 */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] select,
[data-testid="stSidebar"] .stSelectbox label {
    color: #E0E0E0 !important;
}

/* ============================================================
   隐藏 Streamlit 默认元素
   ============================================================ */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* ============================================================
   全局组件样式
   ============================================================ */

/* Metric 卡片 */
[data-testid="stMetricValue"] {
    font-size: 2rem;
    font-weight: 700;
}

/* 按钮 */
.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.2s;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

/* 文件上传区域 */
[data-testid="stFileUploader"] section {
    border: 2px dashed #2979FF !important;
    border-radius: 12px;
    background: #1A2736;
}

/* 页面标题渐变 */
.main-header {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(90deg, #2979FF, #00E5FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
"""


def inject_common_styles():
    """在页面中注入统一的深色侧边栏样式"""
    st.markdown(COMMON_CSS, unsafe_allow_html=True)
