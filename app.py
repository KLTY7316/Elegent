"""
AI安全帽佩戴检测系统 - 主入口 (Dashboard 布局)
深空宇宙主题 + 极致磨砂玻璃拟态 (Glassmorphism)

布局结构：
1. 左侧固定垂直侧边导航栏
2. 顶部横向导航栏（日期选择、账号头像、通知、搜索）
3. 中间主区域：大卡片放安全帽实时检测画面 + 项目标题 + 检测任务列表
4. 右侧分多个小卡片：违规统计折线图、今日检测笔记、导出报告模块、文件存储模块
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(
    page_title="安全帽检测",
    page_icon="⛑️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.styles import inject_common_styles
inject_common_styles()

# ============================================================
# 侧边栏 —— 左侧固定垂直导航
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 24px 0 16px 0;">
        <div style="font-size:2.2rem; margin-bottom:8px; filter: drop-shadow(0 0 12px rgba(96,184,255,0.3));">⛑️</div>
        <h2 style="color:#60b8ff; font-size:1.2rem; margin:0; font-weight:700; letter-spacing:0.05em;">AI安全帽检测</h2>
        <p style="color:#8b9dc3; font-size:0.7rem; margin:6px 0 0 0; letter-spacing:0.08em;">智能佩戴识别监测系统</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(96,184,255,0.08); margin:12px 0;'>", unsafe_allow_html=True)

    # 导航菜单
    nav_items = [
        ("🏠", "首页", "./"),
        ("📸", "安全帽检测", "./图片检测"),
        ("🤖", "AI报告", "./AI报告"),
        ("📁", "历史记录", "./历史记录"),
        ("⚙️", "系统设置", "./统计看板"),
    ]

    for icon, label, href in nav_items:
        st.markdown(f"""
        <a href="{href}" style="display:flex; align-items:center; padding:12px 18px; margin:4px 10px;
           border-radius:14px; text-decoration:none; color:#8b9dc3; transition:all 0.25s;
           border:1px solid transparent;">
            <span style="margin-right:14px; font-size:1.1rem;">{icon}</span>
            <span style="font-size:0.85rem; letter-spacing:0.02em;">{label}</span>
        </a>
        """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(96,184,255,0.08); margin:12px 0;'>", unsafe_allow_html=True)

    # 系统状态
    st.markdown("""
    <div style="padding: 0 14px;">
        <p style="color:#60b8ff; font-size:0.7rem; margin-bottom:12px; font-weight:600; letter-spacing:0.08em; text-transform:uppercase;">系统状态</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("模型", "YOLOv8", delta="就绪")
    with col2:
        st.metric("状态", "运行中")

    st.markdown("<hr style='border-color:rgba(96,184,255,0.08); margin:12px 0;'>", unsafe_allow_html=True)

    # 退出登录
    st.markdown("""
    <div style="padding: 0 10px; margin-top:20px;">
        <a href="#" style="display:flex; align-items:center; padding:12px 18px;
           border-radius:14px; text-decoration:none; color:#ff4d4f; transition:all 0.25s;
           border:1px solid transparent;">
            <span style="margin-right:14px; font-size:1.1rem;">🚪</span>
            <span style="font-size:0.85rem;">退出登录</span>
        </a>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# 顶部横向导航栏
# ============================================================
st.markdown("""
<div class="top-nav" style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
    <div>
        <h1 style="color:#60b8ff; margin:0; font-size:1.6rem; font-weight:700; letter-spacing:-0.02em;">🏗️ AI安全帽佩戴检测</h1>
        <p style="color:#8b9dc3; margin:4px 0 0 0; font-size:0.8rem;">工地智能识别监测系统 Dashboard</p>
    </div>
    <div style="display:flex; align-items:center; gap:20px; flex-wrap:wrap;">
        <span style="color:#8b9dc3; font-size:0.85rem; cursor:pointer; padding:8px 12px; border-radius:10px; background:rgba(15,35,70,0.3);">📅 2026-06-18</span>
        <span style="color:#8b9dc3; font-size:0.85rem; cursor:pointer; padding:8px 12px; border-radius:10px; background:rgba(15,35,70,0.3);">🔍 搜索</span>
        <span style="color:#8b9dc3; font-size:0.85rem; cursor:pointer; padding:8px 12px; border-radius:10px; background:rgba(15,35,70,0.3); position:relative;" class="notification-dot">
            🔔 通知
        </span>
        <div style="display:flex; align-items:center; gap:10px; padding:6px 14px; border-radius:14px; background:rgba(15,35,70,0.3); border:1px solid rgba(96,184,255,0.1);">
            <span style="font-size:1.2rem;">👤</span>
            <div>
                <p style="color:#e6edf7; margin:0; font-size:0.8rem; font-weight:600;">管理员</p>
                <p style="color:#36d399; margin:0; font-size:0.7rem;"><span class="status-online" style="display:inline-block; width:6px; height:6px; background:#36d399; border-radius:50%; margin-right:4px;"></span>在线</p>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# 主区域：三列布局（左侧任务列表 | 中间实时画面 | 右侧统计卡片）
# ============================================================
left_col, center_col, right_col = st.columns([2, 4, 3])

# ---------- 左侧：检测任务列表 ----------
with left_col:
    st.markdown("""
    <div class="glass-card" style="padding:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
            <h3 style="color:#93c5fd; margin:0; font-size:1rem; font-weight:600;">📝 检测任务列表</h3>
            <span style="color:#8b9dc3; cursor:pointer; font-size:1.1rem;">⋮</span>
        </div>
    """, unsafe_allow_html=True)

    tasks = [
        {"name": "A区-基坑施工", "status": "检测中", "badge": "badge-green", "icon": "🟢"},
        {"name": "B区-脚手架作业", "status": "待检测", "badge": "badge-orange", "icon": "🟡"},
        {"name": "C区-材料堆放区", "status": "已完成", "badge": "badge-blue", "icon": "🔵"},
        {"name": "D区-塔吊下方", "status": "检测中", "badge": "badge-green", "icon": "🟢"},
        {"name": "E区-电梯井口", "status": "待检测", "badge": "badge-orange", "icon": "🟡"},
    ]

    for task in tasks:
        st.markdown(f"""
        <div style="background:rgba(15,35,70,0.3); border:1px solid rgba(96,184,255,0.06); border-radius:14px; padding:12px 14px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center; transition:all 0.2s;">
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="font-size:0.9rem;">{task['icon']}</span>
                <span style="color:#e6edf7; font-size:0.85rem;">{task['name']}</span>
            </div>
            <span class="badge {task['badge']}">{task['status']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style="text-align:center; margin-top:14px;">
            <a href="./图片检测" style="color:#60b8ff; text-decoration:none; font-size:0.8rem; font-weight:500;">+ 新建检测任务 →</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------- 中间：大卡片放安全帽实时检测画面 ----------
with center_col:
    st.markdown("""
    <div class="glass-card" style="padding:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
            <h3 style="color:#93c5fd; margin:0; font-size:1rem; font-weight:600;">📹 实时检测画面</h3>
            <div style="display:flex; gap:8px; align-items:center;">
                <span class="badge badge-green">● 实时检测中</span>
                <span style="color:#8b9dc3; cursor:pointer; font-size:1.1rem;">⋮</span>
            </div>
        </div>
        <div class="video-container" style="background:rgba(6,13,31,0.6); border-radius:20px; height:380px; display:flex; align-items:center; justify-content:center; border:1px solid rgba(96,184,255,0.1); position:relative; overflow:hidden;">
            <div style="text-align:center;">
                <p style="color:#8b9dc3; font-size:3.5rem; margin:0; opacity:0.6;">📷</p>
                <p style="color:#8b9dc3; font-size:0.95rem; margin-top:12px;">实时视频流监控画面</p>
                <p style="color:#60b8ff; font-size:0.8rem; margin-top:6px;">YOLO目标检测实时流</p>
                <div style="margin-top:20px; display:flex; gap:10px; justify-content:center;">
                    <span class="badge badge-green">🟢 已佩戴安全帽</span>
                    <span class="badge badge-red">🔴 未佩戴安全帽</span>
                </div>
            </div>
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:16px; align-items:center;">
            <span style="color:#8b9dc3; font-size:0.8rem;">📍 A区-基坑施工 | 摄像头 #CAM-001</span>
            <span style="color:#60b8ff; font-size:0.8rem;">置信度阈值: 0.65</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------- 右侧：多个小卡片 ----------
with right_col:
    # 卡片1：违规统计折线图
    st.markdown("""
    <div class="glass-card" style="padding:18px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
            <h3 style="color:#93c5fd; margin:0; font-size:0.95rem; font-weight:600;">📈 违规统计</h3>
            <span style="color:#8b9dc3; cursor:pointer; font-size:1.1rem;">⋮</span>
        </div>
        <div style="height:100px; display:flex; align-items:flex-end; justify-content:space-around; gap:4px; padding:0 4px;">
    """, unsafe_allow_html=True)

    # 简化折线柱状图
    weekly_data = [("一", 12), ("二", 8), ("三", 15), ("四", 6), ("五", 10), ("六", 4), ("日", 7)]
    max_v = max(v for _, v in weekly_data)
    for day, val in weekly_data:
        h = (val / max_v) * 80
        st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; flex:1;">
            <div style="width:100%; background:linear-gradient(180deg, rgba(255,77,79,0.5), rgba(255,77,79,0.15)); border-radius:3px 3px 0 0; height:{h}px; min-height:3px;"></div>
            <span style="color:#8b9dc3; font-size:0.55rem; margin-top:3px;">{day}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:10px; align-items:center;">
            <span style="color:#8b9dc3; font-size:0.7rem;">本周违规: <span style="color:#ff4d4f; font-weight:600;">62次</span></span>
            <span style="color:#36d399; font-size:0.7rem;">↓ 15%</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 卡片2：今日检测笔记
    st.markdown("""
    <div class="glass-card" style="padding:18px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
            <h3 style="color:#93c5fd; margin:0; font-size:0.95rem; font-weight:600;">📝 今日检测笔记</h3>
            <span style="color:#8b9dc3; cursor:pointer; font-size:1.1rem;">⋮</span>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:12px;">
            <div style="text-align:center; padding:10px; background:rgba(15,35,70,0.3); border-radius:12px;">
                <p style="color:#8b9dc3; font-size:0.65rem; margin:0; text-transform:uppercase; letter-spacing:0.05em;">检测人数</p>
                <p style="color:#e6edf7; font-size:1.4rem; font-weight:700; margin:4px 0;">1,284</p>
            </div>
            <div style="text-align:center; padding:10px; background:rgba(15,35,70,0.3); border-radius:12px;">
                <p style="color:#8b9dc3; font-size:0.65rem; margin:0; text-transform:uppercase; letter-spacing:0.05em;">违规人数</p>
                <p style="color:#ff4d4f; font-size:1.4rem; font-weight:700; margin:4px 0;">37</p>
            </div>
            <div style="text-align:center; padding:10px; background:rgba(15,35,70,0.3); border-radius:12px;">
                <p style="color:#8b9dc3; font-size:0.65rem; margin:0; text-transform:uppercase; letter-spacing:0.05em;">佩戴率</p>
                <p style="color:#36d399; font-size:1.4rem; font-weight:700; margin:4px 0;">97.1%</p>
            </div>
            <div style="text-align:center; padding:10px; background:rgba(15,35,70,0.3); border-radius:12px;">
                <p style="color:#8b9dc3; font-size:0.65rem; margin:0; text-transform:uppercase; letter-spacing:0.05em;">在线时长</p>
                <p style="color:#e6edf7; font-size:1.4rem; font-weight:700; margin:4px 0;">8h32m</p>
            </div>
        </div>
        <div style="margin-bottom:10px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <span style="color:#8b9dc3; font-size:0.7rem;">安全佩戴率</span>
                <span style="color:#36d399; font-size:0.7rem;">97.1%</span>
            </div>
            <div style="background:rgba(15,35,70,0.4); border-radius:10px; height:6px; overflow:hidden;">
                <div style="background:linear-gradient(90deg, #3690ff, #60b8ff); height:100%; width:97.1%; border-radius:10px;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 卡片3：导出报告模块
    st.markdown("""
    <div class="glass-card" style="padding:18px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
            <h3 style="color:#93c5fd; margin:0; font-size:0.95rem; font-weight:600;">📤 导出报告</h3>
            <span style="color:#8b9dc3; cursor:pointer; font-size:1.1rem;">⋮</span>
        </div>
        <p style="color:#a0aec0; font-size:0.8rem; margin-bottom:14px; line-height:1.5;">生成并下载安全检测报告，支持 AI 智能分析</p>
        <a href="./AI报告" style="display:block; text-align:center; background:linear-gradient(135deg, rgba(54,144,255,0.85), rgba(96,184,255,0.7)); color:white; padding:12px; border-radius:14px; text-decoration:none; font-size:0.85rem; font-weight:600; box-shadow:0 4px 16px rgba(54,144,255,0.25), inset 0 1px 0 rgba(255,255,255,0.15); transition:all 0.3s;">
            🤖 生成 AI 报告
        </a>
        <div style="display:flex; gap:8px; margin-top:10px;">
            <a href="./统计看板" style="flex:1; text-align:center; background:rgba(15,35,70,0.4); color:#93c5fd; padding:8px; border-radius:10px; text-decoration:none; font-size:0.75rem; border:1px solid rgba(96,184,255,0.1);">📊 统计报表</a>
            <a href="./历史记录" style="flex:1; text-align:center; background:rgba(15,35,70,0.4); color:#93c5fd; padding:8px; border-radius:10px; text-decoration:none; font-size:0.75rem; border:1px solid rgba(96,184,255,0.1);">📁 历史记录</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 卡片4：文件存储模块
    st.markdown("""
    <div class="glass-card" style="padding:18px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
            <h3 style="color:#93c5fd; margin:0; font-size:0.95rem; font-weight:600;">💾 文件存储</h3>
            <span style="color:#8b9dc3; cursor:pointer; font-size:1.1rem;">⋮</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; padding:10px; background:rgba(15,35,70,0.25); border-radius:12px;">
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="font-size:1.2rem;">📄</span>
                <span style="color:#a0aec0; font-size:0.8rem;">检测报告</span>
            </div>
            <span style="color:#60b8ff; font-size:0.85rem; font-weight:600;">12 个</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; padding:10px; background:rgba(15,35,70,0.25); border-radius:12px;">
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="font-size:1.2rem;">🖼️</span>
                <span style="color:#a0aec0; font-size:0.8rem;">违规截图</span>
            </div>
            <span style="color:#ff4d4f; font-size:0.85rem; font-weight:600;">37 张</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; padding:10px; background:rgba(15,35,70,0.25); border-radius:12px;">
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="font-size:1.2rem;">🎬</span>
                <span style="color:#a0aec0; font-size:0.8rem;">视频记录</span>
            </div>
            <span style="color:#60b8ff; font-size:0.85rem; font-weight:600;">8 个</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
