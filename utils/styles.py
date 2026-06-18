"""
共享样式模块 —— 深空宇宙主题 + 磨砂玻璃拟态 (Glassmorphism)
每个页面都应调用 inject_common_styles() 以保持视觉一致

色彩体系（精确规范）：
- 主色：深空深蓝 #0b203d、渐变高亮蓝 #3690ff
- 卡片底色：半透深蓝毛玻璃 rgba(20,45,80,0.35)
- 文字：浅灰白 #e6edf7、高亮文字冰蓝 #60b8ff
- 违规红色 #ff4d4f、合规绿色 #36d399
- 分割线：极浅半透蓝色
- 按钮：蓝渐变发光hover效果
- 整体背景：星空深蓝渐变底色
"""
import streamlit as st

# 全局共享 CSS —— 深空宇宙 + Glassmorphism 主题
COMMON_CSS = """
<style>
/* ============================================================
   深空宇宙背景
   ============================================================ */
body, .stApp {
    background: linear-gradient(135deg, #0a0e27 0%, #0f1535 30%, #0a1628 60%, #060d1f 100%) !important;
    background-attachment: fixed !important;
    color: #e6edf7 !important;
}

/* 星空颗粒效果 */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(1px 1px at 20px 30px, rgba(255,255,255,0.15), transparent),
        radial-gradient(1px 1px at 40px 70px, rgba(255,255,255,0.1), transparent),
        radial-gradient(1px 1px at 90px 40px, rgba(255,255,255,0.12), transparent),
        radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.08), transparent),
        radial-gradient(1px 1px at 160px 20px, rgba(255,255,255,0.1), transparent),
        radial-gradient(2px 2px at 200px 100px, rgba(100,180,255,0.08), transparent),
        radial-gradient(1px 1px at 250px 50px, rgba(255,255,255,0.06), transparent),
        radial-gradient(1px 1px at 300px 150px, rgba(255,255,255,0.1), transparent);
    background-repeat: repeat;
    background-size: 350px 200px;
    pointer-events: none;
    z-index: 0;
}

/* ============================================================
   磨砂玻璃拟态卡片 (Glassmorphism)
   ============================================================ */
.glass-card {
    background: rgba(20, 45, 80, 0.35) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
    border: 1px solid rgba(54, 144, 255, 0.12) !important;
    border-radius: 20px !important;
    box-shadow:
        0 8px 32px rgba(0, 0, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
    padding: 24px !important;
    margin-bottom: 20px !important;
    position: relative;
    overflow: hidden;
}

.glass-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(96, 184, 255, 0.3), transparent);
}

/* 卡片悬浮效果 */
.glass-card:hover {
    box-shadow:
        0 12px 40px rgba(0, 100, 255, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    border-color: rgba(54, 144, 255, 0.2) !important;
    transition: all 0.3s ease;
}

/* ============================================================
   侧边栏 —— 深空主题
   ============================================================ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(11, 32, 61, 0.95) 0%, rgba(8, 18, 40, 0.9) 100%) !important;
    border-right: 1px solid rgba(54, 144, 255, 0.1) !important;
    backdrop-filter: blur(30px) !important;
}

[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #e6edf7 !important;
    font-weight: 600 !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] label {
    color: #a0aec0 !important;
}

[data-testid="stSidebar"] .stSidebarNavLink {
    color: #8b9dc3 !important;
    border-radius: 12px !important;
    padding: 10px 16px !important;
    margin: 4px 8px !important;
    transition: all 0.2s ease !important;
}

[data-testid="stSidebar"] .stSidebarNavLink:hover {
    color: #e6edf7 !important;
    background: rgba(54, 144, 255, 0.1) !important;
}

[data-testid="stSidebar"] .stSidebarNavLink.active,
[data-testid="stSidebar"] .stSidebarNavLink[data-active="true"] {
    color: #ffffff !important;
    background: linear-gradient(135deg, rgba(54, 144, 255, 0.2), rgba(96, 184, 255, 0.15)) !important;
    border-left: 3px solid #3690ff !important;
    box-shadow: 0 0 20px rgba(54, 144, 255, 0.2) !important;
}

/* ============================================================
   主内容区标题
   ============================================================ */
.main-header {
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #60b8ff, #93c5fd, #c3dafe) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    text-shadow: 0 0 30px rgba(96, 184, 255, 0.3) !important;
}

/* ============================================================
   Metric 卡片
   ============================================================ */
[data-testid="stMetric"] {
    background: rgba(20, 45, 80, 0.35) !important;
    backdrop-filter: blur(15px) !important;
    border: 1px solid rgba(54, 144, 255, 0.1) !important;
    border-radius: 16px !important;
    padding: 16px !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
}

[data-testid="stMetricLabel"] {
    color: #8b9dc3 !important;
    font-size: 0.85rem !important;
}

[data-testid="stMetricValue"] {
    color: #e6edf7 !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
}

[data-testid="stMetricDelta"] {
    color: #36d399 !important;
}

/* ============================================================
   按钮
   ============================================================ */
.stButton > button {
    background: linear-gradient(135deg, rgba(54, 144, 255, 0.8), rgba(96, 184, 255, 0.7)) !important;
    color: white !important;
    border: 1px solid rgba(54, 144, 255, 0.3) !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 15px rgba(54, 144, 255, 0.3) !important;
    transition: all 0.3s ease !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(54, 144, 255, 0.4) !important;
    background: linear-gradient(135deg, rgba(54, 144, 255, 0.9), rgba(96, 184, 255, 0.8)) !important;
}

/* 次要按钮 */
.stButton > button[kind="secondary"] {
    background: rgba(20, 45, 80, 0.5) !important;
    border: 1px solid rgba(54, 144, 255, 0.2) !important;
    color: #93c5fd !important;
}

/* ============================================================
   文件上传区域
   ============================================================ */
[data-testid="stFileUploader"] section {
    background: rgba(20, 45, 80, 0.35) !important;
    backdrop-filter: blur(15px) !important;
    border: 2px dashed rgba(54, 144, 255, 0.25) !important;
    border-radius: 16px !important;
}

/* ============================================================
   输入框 / 选择框
   ============================================================ */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: rgba(20, 45, 80, 0.5) !important;
    border: 1px solid rgba(54, 144, 255, 0.15) !important;
    border-radius: 12px !important;
    color: #e6edf7 !important;
}

/* ============================================================
   隐藏默认元素
   ============================================================ */
#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}
header {visibility: hidden !important;}

/* ============================================================
   信息框 / 警告框
   ============================================================ */
[data-testid="stAlert"] {
    background: rgba(20, 45, 80, 0.5) !important;
    backdrop-filter: blur(15px) !important;
    border: 1px solid rgba(54, 144, 255, 0.15) !important;
    border-radius: 12px !important;
}

/* ============================================================
   分隔线
   ============================================================ */
hr {
    border-color: rgba(54, 144, 255, 0.1) !important;
}

/* ============================================================
   数据表格
   ============================================================ */
[data-testid="stDataFrame"] {
    background: rgba(20, 45, 80, 0.35) !important;
    border-radius: 16px !important;
    border: 1px solid rgba(54, 144, 255, 0.1) !important;
}

/* ============================================================
   进度条
   ============================================================ */
.stProgress > div > div {
    background: linear-gradient(90deg, #3690ff, #60b8ff) !important;
    border-radius: 10px !important;
}

/* ============================================================
   标签页
   ============================================================ */
[data-testid="stTabs"] button {
    background: transparent !important;
    color: #8b9dc3 !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    color: #3690ff !important;
    border-bottom: 2px solid #3690ff !important;
}

/* ============================================================
   违规标签（红色）
   ============================================================ */
.violation-badge {
    background: rgba(255, 77, 79, 0.2) !important;
    color: #ff4d4f !important;
    padding: 3px 10px !important;
    border-radius: 20px !important;
    font-size: 0.75rem !important;
    border: 1px solid rgba(255, 77, 79, 0.3) !important;
}

/* ============================================================
   合规标签（绿色）
   ============================================================ */
.compliant-badge {
    background: rgba(54, 211, 153, 0.2) !important;
    color: #36d399 !important;
    padding: 3px 10px !important;
    border-radius: 20px !important;
    font-size: 0.75rem !important;
    border: 1px solid rgba(54, 211, 153, 0.3) !important;
}

/* ============================================================
   在线状态指示器
   ============================================================ */
.status-online {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #36d399;
    border-radius: 50%;
    box-shadow: 0 0 8px rgba(54, 211, 153, 0.6);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(54, 211, 153, 0.7); }
    70% { box-shadow: 0 0 0 6px rgba(54, 211, 153, 0); }
    100% { box-shadow: 0 0 0 0 rgba(54, 211, 153, 0); }
}

/* ============================================================
   通知红点
   ============================================================ */
.notification-dot {
    position: relative;
}
.notification-dot::after {
    content: "";
    position: absolute;
    top: -2px;
    right: -2px;
    width: 8px;
    height: 8px;
    background: #ff4d4f;
    border-radius: 50%;
    box-shadow: 0 0 6px rgba(255, 77, 79, 0.6);
}

/* ============================================================
   统一配色方案（安全=绿 违规=红 警告=橙）
   ============================================================ */
.text-safe {
    color: #36d399 !important;
}
.text-violation {
    color: #ff4d4f !important;
}
.text-warning {
    color: #fb923c !important;
}
.bg-safe {
    background: rgba(54, 211, 153, 0.15) !important;
}
.bg-violation {
    background: rgba(255, 77, 79, 0.15) !important;
}
.bg-warning {
    background: rgba(251, 146, 60, 0.15) !important;
}
.border-safe {
    border-color: rgba(54, 211, 153, 0.3) !important;
}
.border-violation {
    border-color: rgba(255, 77, 79, 0.3) !important;
}
.border-warning {
    border-color: rgba(251, 146, 60, 0.3) !important;
}
.metric-safe [data-testid="stMetricValue"] {
    color: #36d399 !important;
}
.metric-violation [data-testid="stMetricValue"] {
    color: #ff4d4f !important;
}
.metric-warning [data-testid="stMetricValue"] {
    color: #fb923c !important;
}
</style>
"""


def inject_common_styles():
    """在页面中注入统一的深空宇宙 + Glassmorphism 样式"""
    st.markdown(COMMON_CSS, unsafe_allow_html=True)
