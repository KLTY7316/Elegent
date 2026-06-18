"""
共享样式模块 —— 深空宇宙主题 + 极致磨砂玻璃拟态 (Glassmorphism)
每个页面都应调用 inject_common_styles() 以保持视觉一致

色彩体系：
- 主色：深海藏蓝 #0a1628、暗靛蓝 #0f1535
- 辅色：冰青蓝 #60b8ff、浅雾霾蓝 #8b9dc3、淡天青渐变
- 整体低饱和暗调、深色模式 dark mode、冷色调商务科技配色、渐变柔光
- 安全绿 #36d399、违规红 #ff4d4f、警告橙 #fb923c
"""
import streamlit as st

COMMON_CSS = """
<style>
/* ============================================================
   深空宇宙背景 —— 地球远景 + 星空颗粒 + 朦胧深空氛围
   ============================================================ */
body, .stApp {
    background:
        radial-gradient(ellipse at 20% 80%, rgba(15, 40, 80, 0.4) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, rgba(10, 30, 60, 0.3) 0%, transparent 40%),
        linear-gradient(180deg, #060d1f 0%, #0a1628 25%, #0f1535 50%, #0a1628 75%, #060d1f 100%) !important;
    background-attachment: fixed !important;
    color: #e6edf7 !important;
}

/* 星空颗粒效果 —— 多层叠加 */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        radial-gradient(1px 1px at 20px 30px, rgba(255,255,255,0.2), transparent),
        radial-gradient(1px 1px at 40px 70px, rgba(255,255,255,0.12), transparent),
        radial-gradient(1px 1px at 90px 40px, rgba(96,184,255,0.15), transparent),
        radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.08), transparent),
        radial-gradient(1px 1px at 160px 20px, rgba(255,255,255,0.1), transparent),
        radial-gradient(2px 2px at 200px 100px, rgba(96,184,255,0.1), transparent),
        radial-gradient(1px 1px at 250px 50px, rgba(255,255,255,0.06), transparent),
        radial-gradient(1px 1px at 300px 150px, rgba(255,255,255,0.1), transparent),
        radial-gradient(1px 1px at 350px 90px, rgba(96,184,255,0.08), transparent),
        radial-gradient(1px 1px at 80px 180px, rgba(255,255,255,0.05), transparent);
    background-repeat: repeat;
    background-size: 400px 250px;
    pointer-events: none;
    z-index: 0;
}

/* ============================================================
   磨砂毛玻璃拟态卡片 —— 核心质感
   ============================================================ */
.glass-card {
    background: rgba(15, 35, 70, 0.25) !important;
    backdrop-filter: blur(24px) saturate(200%) !important;
    -webkit-backdrop-filter: blur(24px) saturate(200%) !important;
    border: 1px solid rgba(96, 184, 255, 0.15) !important;
    border-radius: 24px !important;
    box-shadow:
        0 4px 24px rgba(0, 0, 0, 0.4),
        0 1px 2px rgba(255, 255, 255, 0.05),
        inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    padding: 24px !important;
    margin-bottom: 20px !important;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 微弱内发光 —— 顶部光晕 */
.glass-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(96, 184, 255, 0.4), transparent);
}

/* 流体渐变底色 —— 角落微光 */
.glass-card::after {
    content: "";
    position: absolute;
    top: -50%; right: -50%;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(54, 144, 255, 0.06) 0%, transparent 70%);
    pointer-events: none;
    border-radius: 50%;
}

/* 卡片悬浮 —— 分层悬浮层级 + 柔和漫反射 */
.glass-card:hover {
    box-shadow:
        0 8px 40px rgba(0, 80, 200, 0.2),
        0 2px 4px rgba(255, 255, 255, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
    border-color: rgba(96, 184, 255, 0.25) !important;
    transform: translateY(-2px);
}

/* 扁平化 2.5D —— 轻微厚度感 */
.glass-card-3d {
    background: rgba(15, 35, 70, 0.3) !important;
    backdrop-filter: blur(24px) saturate(200%) !important;
    -webkit-backdrop-filter: blur(24px) saturate(200%) !important;
    border: 1px solid rgba(96, 184, 255, 0.18) !important;
    border-radius: 24px !important;
    box-shadow:
        0 2px 8px rgba(0, 0, 0, 0.3),
        0 8px 32px rgba(0, 0, 0, 0.2),
        inset 0 1px 0 rgba(255, 255, 255, 0.06),
        inset 0 -1px 0 rgba(0, 0, 0, 0.1) !important;
    padding: 24px !important;
    margin-bottom: 20px !important;
    position: relative;
    overflow: hidden;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card-3d::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(96, 184, 255, 0.5), transparent);
}

.glass-card-3d:hover {
    box-shadow:
        0 4px 16px rgba(0, 80, 200, 0.25),
        0 12px 48px rgba(0, 0, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
    border-color: rgba(96, 184, 255, 0.3) !important;
    transform: translateY(-3px);
}

/* ============================================================
   侧边栏 —— 深空主题 + 玻璃态
   ============================================================ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(8, 18, 40, 0.92) 0%, rgba(6, 13, 31, 0.88) 100%) !important;
    border-right: 1px solid rgba(96, 184, 255, 0.08) !important;
    backdrop-filter: blur(40px) saturate(180%) !important;
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
    color: #8b9dc3 !important;
}

[data-testid="stSidebar"] .stSidebarNavLink {
    color: #8b9dc3 !important;
    border-radius: 14px !important;
    padding: 12px 18px !important;
    margin: 4px 10px !important;
    transition: all 0.25s ease !important;
    border: 1px solid transparent !important;
}

[data-testid="stSidebar"] .stSidebarNavLink:hover {
    color: #e6edf7 !important;
    background: rgba(96, 184, 255, 0.08) !important;
    border-color: rgba(96, 184, 255, 0.15) !important;
}

[data-testid="stSidebar"] .stSidebarNavLink.active,
[data-testid="stSidebar"] .stSidebarNavLink[data-active="true"] {
    color: #ffffff !important;
    background: linear-gradient(135deg, rgba(54, 144, 255, 0.2), rgba(96, 184, 255, 0.12)) !important;
    border-left: 3px solid #60b8ff !important;
    border-color: rgba(96, 184, 255, 0.2) !important;
    box-shadow: 0 0 24px rgba(54, 144, 255, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
}

/* ============================================================
   主内容区标题 —— 渐变柔光
   ============================================================ */
.main-header {
    font-size: 2.4rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #60b8ff, #93c5fd, #c3dafe) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    text-shadow: 0 0 40px rgba(96, 184, 255, 0.2) !important;
    letter-spacing: -0.02em !important;
}

.sub-header {
    font-size: 1.1rem !important;
    font-weight: 500 !important;
    color: #8b9dc3 !important;
    letter-spacing: 0.02em !important;
}

/* ============================================================
   Metric 卡片 —— 玻璃态 + 渐变柔光数字
   ============================================================ */
[data-testid="stMetric"] {
    background: rgba(15, 35, 70, 0.2) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(96, 184, 255, 0.08) !important;
    border-radius: 20px !important;
    padding: 20px !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
    transition: all 0.3s ease;
}

[data-testid="stMetric"]:hover {
    box-shadow: 0 6px 24px rgba(0, 80, 200, 0.15) !important;
    border-color: rgba(96, 184, 255, 0.15) !important;
}

[data-testid="stMetricLabel"] {
    color: #8b9dc3 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}

[data-testid="stMetricValue"] {
    color: #e6edf7 !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    text-shadow: 0 0 20px rgba(96, 184, 255, 0.15) !important;
}

[data-testid="stMetricDelta"] {
    color: #36d399 !important;
}

/* ============================================================
   按钮 —— 渐变柔光发光
   ============================================================ */
.stButton > button {
    background: linear-gradient(135deg, rgba(54, 144, 255, 0.85), rgba(96, 184, 255, 0.7)) !important;
    color: white !important;
    border: 1px solid rgba(96, 184, 255, 0.35) !important;
    border-radius: 14px !important;
    font-weight: 600 !important;
    padding: 12px 28px !important;
    box-shadow:
        0 4px 16px rgba(54, 144, 255, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    letter-spacing: 0.02em !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow:
        0 8px 32px rgba(54, 144, 255, 0.35),
        inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    background: linear-gradient(135deg, rgba(54, 144, 255, 0.95), rgba(96, 184, 255, 0.8)) !important;
}

/* 次要按钮 */
.stButton > button[kind="secondary"] {
    background: rgba(15, 35, 70, 0.4) !important;
    border: 1px solid rgba(96, 184, 255, 0.2) !important;
    color: #93c5fd !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2) !important;
}

.stButton > button[kind="secondary"]:hover {
    background: rgba(15, 35, 70, 0.55) !important;
    border-color: rgba(96, 184, 255, 0.3) !important;
    box-shadow: 0 4px 16px rgba(0, 80, 200, 0.15) !important;
}

/* ============================================================
   文件上传区域
   ============================================================ */
[data-testid="stFileUploader"] section {
    background: rgba(15, 35, 70, 0.25) !important;
    backdrop-filter: blur(20px) !important;
    border: 2px dashed rgba(96, 184, 255, 0.2) !important;
    border-radius: 20px !important;
    transition: all 0.3s ease;
}

[data-testid="stFileUploader"] section:hover {
    border-color: rgba(96, 184, 255, 0.35) !important;
    background: rgba(15, 35, 70, 0.35) !important;
}

/* ============================================================
   输入框 / 选择框
   ============================================================ */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: rgba(15, 35, 70, 0.4) !important;
    border: 1px solid rgba(96, 184, 255, 0.12) !important;
    border-radius: 14px !important;
    color: #e6edf7 !important;
    transition: all 0.2s ease;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stSelectbox"] > div > div:focus {
    border-color: rgba(96, 184, 255, 0.3) !important;
    box-shadow: 0 0 0 3px rgba(54, 144, 255, 0.1) !important;
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
    background: rgba(15, 35, 70, 0.4) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(96, 184, 255, 0.12) !important;
    border-radius: 16px !important;
}

/* ============================================================
   分隔线
   ============================================================ */
hr {
    border-color: rgba(96, 184, 255, 0.06) !important;
}

/* ============================================================
   数据表格
   ============================================================ */
[data-testid="stDataFrame"] {
    background: rgba(15, 35, 70, 0.2) !important;
    border-radius: 20px !important;
    border: 1px solid rgba(96, 184, 255, 0.08) !important;
}

/* ============================================================
   进度条
   ============================================================ */
.stProgress > div > div {
    background: linear-gradient(90deg, #3690ff, #60b8ff, #93c5fd) !important;
    border-radius: 10px !important;
    box-shadow: 0 0 8px rgba(54, 144, 255, 0.3) !important;
}

/* ============================================================
   标签页
   ============================================================ */
[data-testid="stTabs"] button {
    background: transparent !important;
    color: #8b9dc3 !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.2s ease;
    padding: 12px 20px !important;
}

[data-testid="stTabs"] button:hover {
    color: #93c5fd !important;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    color: #60b8ff !important;
    border-bottom: 2px solid #60b8ff !important;
    text-shadow: 0 0 12px rgba(96, 184, 255, 0.3) !important;
}

/* ============================================================
   统一配色方案（安全=绿 违规=红 警告=橙）
   ============================================================ */
.text-safe { color: #36d399 !important; }
.text-violation { color: #ff4d4f !important; }
.text-warning { color: #fb923c !important; }
.bg-safe { background: rgba(54, 211, 153, 0.12) !important; }
.bg-violation { background: rgba(255, 77, 79, 0.12) !important; }
.bg-warning { background: rgba(251, 146, 60, 0.12) !important; }
.border-safe { border-color: rgba(54, 211, 153, 0.25) !important; }
.border-violation { border-color: rgba(255, 77, 79, 0.25) !important; }
.border-warning { border-color: rgba(251, 146, 60, 0.25) !important; }
.metric-safe [data-testid="stMetricValue"] { color: #36d399 !important; }
.metric-violation [data-testid="stMetricValue"] { color: #ff4d4f !important; }
.metric-warning [data-testid="stMetricValue"] { color: #fb923c !important; }

/* ============================================================
   在线状态指示器
   ============================================================ */
.status-online {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #36d399;
    border-radius: 50%;
    box-shadow: 0 0 10px rgba(54, 211, 153, 0.6);
    animation: pulse 2.5s infinite;
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(54, 211, 153, 0.7); }
    70% { box-shadow: 0 0 0 8px rgba(54, 211, 153, 0); }
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
    box-shadow: 0 0 8px rgba(255, 77, 79, 0.6);
}

/* ============================================================
   顶部导航栏样式
   ============================================================ */
.top-nav {
    background: rgba(8, 18, 40, 0.6) !important;
    backdrop-filter: blur(30px) saturate(180%) !important;
    border: 1px solid rgba(96, 184, 255, 0.1) !important;
    border-radius: 20px !important;
    padding: 16px 24px !important;
    margin-bottom: 24px !important;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3) !important;
}

/* ============================================================
   实时视频画面容器
   ============================================================ */
.video-container {
    background: rgba(6, 13, 31, 0.6) !important;
    border: 1px solid rgba(96, 184, 255, 0.12) !important;
    border-radius: 20px !important;
    overflow: hidden !important;
    box-shadow: inset 0 0 40px rgba(0, 0, 0, 0.3) !important;
}

/* ============================================================
   小标签/徽章
   ============================================================ */
.badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.02em;
}
.badge-blue {
    background: rgba(54, 144, 255, 0.15);
    color: #60b8ff;
    border: 1px solid rgba(54, 144, 255, 0.2);
}
.badge-green {
    background: rgba(54, 211, 153, 0.15);
    color: #36d399;
    border: 1px solid rgba(54, 211, 153, 0.2);
}
.badge-red {
    background: rgba(255, 77, 79, 0.15);
    color: #ff4d4f;
    border: 1px solid rgba(255, 77, 79, 0.2);
}
.badge-orange {
    background: rgba(251, 146, 60, 0.15);
    color: #fb923c;
    border: 1px solid rgba(251, 146, 60, 0.2);
}
</style>
"""


def inject_common_styles():
    """在页面中注入统一的深空宇宙 + Glassmorphism 样式"""
    st.markdown(COMMON_CSS, unsafe_allow_html=True)
