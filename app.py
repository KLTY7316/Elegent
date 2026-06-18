"""
工地安全帽智能识别监测系统 - 主入口 (Dashboard 布局)
深空宇宙主题 + 磨砂玻璃拟态 (Glassmorphism)

布局结构：
- 左侧：固定垂直侧边导航菜单
- 顶部栏：标题 + 日期 + 管理员 + 通知 + 搜索
- 左侧超大主卡片：实时AI视频监控画面（YOLO检测，绿框合规/红框违规）
- 右侧三层堆叠玻璃卡片：
  * 上层【今日数据统计面板】
  * 中层【安全帽违规告警记录】
  * 下层【月度违规趋势Activity图表】
- 底部技术架构图
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# ============================================================
# 页面全局配置
# ============================================================
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
    <div style="text-align:center; padding: 20px 0;">
        <div style="font-size:2rem; margin-bottom:8px;">⛑️</div>
        <h2 style="color:#60b8ff; font-size:1.3rem; margin:0; font-weight:700;">AI安全帽检测</h2>
        <p style="color:#8b9dc3; font-size:0.75rem; margin:5px 0 0 0;">工地智能识别监测系统</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 导航菜单
    st.markdown("""
    <div style="padding: 0 10px;">
        <p style="color:#60b8ff; font-size:0.75rem; margin-bottom:12px; font-weight:600;">📋 导航菜单</p>
    </div>
    """, unsafe_allow_html=True)

    nav_items = [
        ("🏠", "Dashboard首页总览", "./"),
        ("📹", "实时监控", "./实时摄像头"),
        ("🚨", "告警记录", "./历史记录"),
        ("📊", "统计报表", "./统计看板"),
        ("📷", "摄像头设备管理", "./图片检测"),
        ("⚙️", "系统设置", "./AI报告"),
    ]

    for icon, label, href in nav_items:
        st.markdown(f"""
        <a href="{href}" style="display:flex; align-items:center; padding:10px 16px; margin:4px 8px;
           border-radius:12px; text-decoration:none; color:#8b9dc3; transition:all 0.2s;">
            <span style="margin-right:12px; font-size:1.1rem;">{icon}</span>
            <span style="font-size:0.85rem;">{label}</span>
        </a>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 系统状态
    st.markdown("""
    <div style="padding: 0 10px;">
        <p style="color:#60b8ff; font-size:0.75rem; margin-bottom:12px; font-weight:600;">📊 系统状态</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("模型", "YOLOv8", delta="就绪")
    with col2:
        st.metric("GPU", "CPU", delta="运行中")

    st.markdown("---")

    # 退出登录
    st.markdown("""
    <div style="padding: 0 10px; margin-top:20px;">
        <a href="#" style="display:flex; align-items:center; padding:10px 16px;
           border-radius:12px; text-decoration:none; color:#ff4d4f; transition:all 0.2s;">
            <span style="margin-right:12px; font-size:1.1rem;">🚪</span>
            <span style="font-size:0.85rem;">退出登录</span>
        </a>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# 顶部导航栏
# ============================================================
header_col1, header_col2, header_col3, header_col4, header_col5 = st.columns([4, 2, 1, 1, 1])

with header_col1:
    st.markdown('<h1 class="main-header">🏗️ 工地安全帽智能识别监测系统</h1>', unsafe_allow_html=True)

with header_col2:
    st.markdown("""
    <div style="text-align:right; padding-top:14px;">
        <span style="color:#8b9dc3; font-size:0.85rem;">📅 2026-06-18</span>
    </div>
    """, unsafe_allow_html=True)

with header_col3:
    st.markdown("""
    <div style="text-align:right; padding-top:14px;">
        <span style="color:#8b9dc3; font-size:0.85rem; cursor:pointer;">🔍 搜索</span>
    </div>
    """, unsafe_allow_html=True)

with header_col4:
    st.markdown("""
    <div style="text-align:right; padding-top:14px;">
        <span style="color:#8b9dc3; font-size:0.85rem; cursor:pointer; position:relative;" class="notification-dot">
            🔔 通知
        </span>
    </div>
    """, unsafe_allow_html=True)

with header_col5:
    st.markdown("""
    <div style="text-align:right; padding-top:10px;">
        <div style="display:inline-flex; align-items:center; gap:8px;">
            <span style="color:#8b9dc3; font-size:0.85rem;">👤 管理员</span>
            <span style="background:rgba(52,211,153,0.2); color:#36d399; padding:4px 12px; border-radius:20px; font-size:0.75rem;">
                <span class="status-online" style="display:inline-block; width:6px; height:6px; background:#36d399; border-radius:50%; margin-right:4px;"></span>在线
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# 全局筛选按钮
# ============================================================
filter_col1, filter_col2, filter_col3, filter_col4, filter_col5 = st.columns([1, 1, 1, 1, 3])
with filter_col1:
    st.button("📅 今日", key="filter_today")
with filter_col2:
    st.button("📆 本周", key="filter_week")
with filter_col3:
    st.button("🗓️ 本月", key="filter_month")
with filter_col4:
    st.button("⚠️ 高优先级违规", key="filter_high_priority")
with filter_col5:
    st.markdown("""
    <div style="text-align:right;">
        <a href="./历史记录" style="display:inline-block; background:linear-gradient(135deg, rgba(255,77,79,0.8), rgba(255,120,120,0.7)); color:white; padding:8px 20px; border-radius:12px; text-decoration:none; font-size:0.85rem; font-weight:600; box-shadow:0 4px 15px rgba(255,77,79,0.3);">
            🚨 新增告警
        </a>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# ============================================================
# 主区域：左中大区域 + 右侧三层卡片
# ============================================================
left_main_col, right_stacked_col = st.columns([3, 2])

# ---------- 左侧超大主卡片：实时AI视频监控画面 ----------
with left_main_col:
    st.markdown("""
    <div class="glass-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
            <h3 style="color:#93c5fd; margin:0; font-size:1.1rem;">📹 实时AI视频监控画面</h3>
            <div style="display:flex; gap:8px; align-items:center;">
                <span style="background:rgba(54,211,153,0.2); color:#36d399; padding:3px 10px; border-radius:20px; font-size:0.75rem;">● 实时检测中</span>
                <span style="color:#8b9dc3; cursor:pointer; font-size:1.2rem;">⋮</span>
            </div>
        </div>
        <div style="background:rgba(10,15,35,0.6); border-radius:16px; height:400px; display:flex; align-items:center; justify-content:center; border:1px solid rgba(54,144,255,0.1); position:relative; overflow:hidden;">
            <div style="text-align:center;">
                <p style="color:#8b9dc3; font-size:3rem; margin:0;">📷</p>
                <p style="color:#8b9dc3; font-size:0.9rem; margin-top:10px;">实时视频流监控画面</p>
                <p style="color:#60b8ff; font-size:0.8rem; margin-top:5px;">YOLO目标检测实时流</p>
                <div style="margin-top:16px;">
                    <span style="display:inline-block; background:rgba(54,211,153,0.2); color:#36d399; padding:4px 12px; border-radius:20px; font-size:0.75rem; margin-right:8px;">🟢 已佩戴安全帽</span>
                    <span style="display:inline-block; background:rgba(255,77,79,0.2); color:#ff4d4f; padding:4px 12px; border-radius:20px; font-size:0.75rem;">🔴 未佩戴安全帽</span>
                </div>
            </div>
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:16px; align-items:center;">
            <span style="color:#8b9dc3; font-size:0.8rem;">📍 A区-基坑施工 | 摄像头 #CAM-001</span>
            <span style="color:#60b8ff; font-size:0.8rem;">置信度阈值: 0.65</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------- 右侧三层堆叠玻璃卡片 ----------
with right_stacked_col:
    # 上层【今日数据统计面板】
    st.markdown("""
    <div class="glass-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
            <h3 style="color:#93c5fd; margin:0; font-size:1rem;">📊 今日数据统计面板</h3>
            <span style="color:#8b9dc3; cursor:pointer; font-size:1.2rem;">⋮</span>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-bottom:16px;">
            <div style="text-align:center; padding:12px; background:rgba(20,45,80,0.3); border-radius:12px;">
                <p style="color:#8b9dc3; font-size:0.75rem; margin:0;">在岗检测总人数</p>
                <p style="color:#e6edf7; font-size:1.6rem; font-weight:700; margin:4px 0; text-shadow:0 0 20px rgba(96,184,255,0.3);">1,284</p>
            </div>
            <div style="text-align:center; padding:12px; background:rgba(20,45,80,0.3); border-radius:12px;">
                <p style="color:#8b9dc3; font-size:0.75rem; margin:0;">未佩戴违规总数</p>
                <p style="color:#ff4d4f; font-size:1.6rem; font-weight:700; margin:4px 0; text-shadow:0 0 20px rgba(255,77,79,0.3);">37</p>
            </div>
            <div style="text-align:center; padding:12px; background:rgba(20,45,80,0.3); border-radius:12px;">
                <p style="color:#8b9dc3; font-size:0.75rem; margin:0;">正常佩戴人数</p>
                <p style="color:#36d399; font-size:1.6rem; font-weight:700; margin:4px 0; text-shadow:0 0 20px rgba(54,211,153,0.3);">1,247</p>
            </div>
            <div style="text-align:center; padding:12px; background:rgba(20,45,80,0.3); border-radius:12px;">
                <p style="color:#8b9dc3; font-size:0.75rem; margin:0;">违规占比</p>
                <p style="color:#e6edf7; font-size:1.6rem; font-weight:700; margin:4px 0;">2.9%</p>
            </div>
        </div>
        <div style="margin-bottom:12px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                <span style="color:#8b9dc3; font-size:0.75rem;">违规占比进度</span>
                <span style="color:#ff4d4f; font-size:0.75rem;">2.9%</span>
            </div>
            <div style="background:rgba(20,45,80,0.5); border-radius:10px; height:8px; overflow:hidden;">
                <div style="background:linear-gradient(90deg, #3690ff, #60b8ff); height:100%; width:97.1%; border-radius:10px;"></div>
            </div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="color:#8b9dc3; font-size:0.75rem;">今日高危点位: <span style="color:#ff4d4f;">A区-基坑 (12次)</span></span>
            <span style="color:#8b9dc3; cursor:pointer; font-size:0.75rem;">查看详情 →</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 中层【安全帽违规告警记录】
    st.markdown("""
    <div class="glass-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
            <h3 style="color:#93c5fd; margin:0; font-size:1rem;">🚨 安全帽违规告警记录</h3>
            <div style="display:flex; gap:8px; align-items:center;">
                <span style="background:rgba(255,77,79,0.2); color:#ff4d4f; padding:2px 8px; border-radius:20px; font-size:0.7rem;">NEW +3</span>
                <span style="color:#8b9dc3; cursor:pointer; font-size:1.2rem;">⋮</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 告警记录表格
    alerts = [
        {"time": "14:32:15", "cam": "CAM-001", "type": "未佩戴安全帽", "status": "未处理", "status_color": "#ff4d4f"},
        {"time": "14:28:42", "cam": "CAM-003", "type": "未佩戴安全帽", "status": "已处理", "status_color": "#36d399"},
        {"time": "14:15:08", "cam": "CAM-002", "type": "未佩戴安全帽", "status": "未处理", "status_color": "#ff4d4f"},
        {"time": "13:52:33", "cam": "CAM-001", "type": "未佩戴安全帽", "status": "已处理", "status_color": "#36d399"},
    ]

    for alert in alerts:
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; padding:10px 0; border-bottom:1px solid rgba(54,144,255,0.08);">
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="width:36px; height:36px; background:rgba(255,77,79,0.15); border-radius:8px; display:flex; align-items:center; justify-content:center;">
                    <span style="font-size:0.9rem;">📷</span>
                </div>
                <div>
                    <p style="color:#e6edf7; font-size:0.8rem; margin:0;">{alert['type']}</p>
                    <p style="color:#8b9dc3; font-size:0.7rem; margin:0;">{alert['time']} | {alert['cam']}</p>
                </div>
            </div>
            <span style="background:rgba({",".join([str(int(alert['status_color'][i:i+2],16)) for i in (1,3,5)])},0.2); color:{alert['status_color']}; padding:2px 8px; border-radius:20px; font-size:0.7rem;">{alert['status']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div style="text-align:center; margin-top:12px;">
            <a href="./历史记录" style="color:#60b8ff; text-decoration:none; font-size:0.8rem;">查看全部记录 →</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 下层【月度违规趋势Activity图表】
    st.markdown("""
    <div class="glass-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
            <h3 style="color:#93c5fd; margin:0; font-size:1rem;">📈 月度违规趋势 Activity</h3>
            <span style="color:#8b9dc3; cursor:pointer; font-size:1.2rem;">⋮</span>
        </div>
        <div style="height:140px; display:flex; align-items:flex-end; justify-content:space-around; gap:6px; padding:0 8px;">
    """, unsafe_allow_html=True)

    # 月度数据柱状图（简化版）
    monthly_data = [
        ("1月", 45), ("2月", 38), ("3月", 52), ("4月", 41),
        ("5月", 35), ("6月", 29), ("7月", 33), ("8月", 40),
        ("9月", 48), ("10月", 55), ("11月", 42), ("12月", 37)
    ]
    max_val = max(v for _, v in monthly_data)

    for month, val in monthly_data:
        height_pct = (val / max_val) * 100
        st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; flex:1;">
            <div style="width:100%; background:linear-gradient(180deg, rgba(54,144,255,0.6), rgba(96,184,255,0.3)); border-radius:4px 4px 0 0; height:{height_pct * 0.8}px; min-height:4px;"></div>
            <span style="color:#8b9dc3; font-size:0.6rem; margin-top:4px;">{month}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:12px; align-items:center;">
            <span style="color:#8b9dc3; font-size:0.75rem;">年度违规总计: <span style="color:#e6edf7; font-weight:600;">495次</span></span>
            <a href="./统计看板" style="background:linear-gradient(135deg, rgba(54,144,255,0.8), rgba(96,184,255,0.7)); color:white; padding:6px 16px; border-radius:10px; text-decoration:none; font-size:0.75rem; font-weight:600;">📤 导出报表</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# 底部：技术架构图
# ============================================================
st.markdown("---")
st.markdown("""
<div class="glass-card">
    <h3 style="color:#93c5fd; margin:0 0 20px 0; font-size:1rem;">🏗️ 技术架构</h3>
    <div style="display:flex; justify-content:center; align-items:center; flex-wrap:wrap; gap:30px;">
        <div style="text-align:center;">
            <div style="background:rgba(54,144,255,0.15); width:70px; height:70px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto; border:1px solid rgba(54,144,255,0.3); box-shadow:0 0 20px rgba(54,144,255,0.2);">
                <span style="font-size:1.8rem;">📷</span>
            </div>
            <p style="color:#e6edf7; font-size:0.85rem; margin-top:10px; font-weight:600;">边缘计算设备</p>
            <p style="color:#8b9dc3; font-size:0.7rem;">摄像头 / 工控机</p>
        </div>
        <div style="display:flex; flex-direction:column; align-items:center; gap:4px;">
            <div style="color:#3690ff; font-size:1.2rem;">→</div>
            <div style="color:#3690ff; font-size:0.7rem;">RTSP流</div>
            <div style="color:#3690ff; font-size:1.2rem;">→</div>
        </div>
        <div style="text-align:center;">
            <div style="background:rgba(139,92,246,0.15); width:70px; height:70px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto; border:1px solid rgba(139,92,246,0.3); box-shadow:0 0 20px rgba(139,92,246,0.2);">
                <span style="font-size:1.8rem;">🧠</span>
            </div>
            <p style="color:#e6edf7; font-size:0.85rem; margin-top:10px; font-weight:600;">推理引擎</p>
            <p style="color:#8b9dc3; font-size:0.7rem;">YOLOv8 / SSD 检测</p>
        </div>
        <div style="display:flex; flex-direction:column; align-items:center; gap:4px;">
            <div style="color:#3690ff; font-size:1.2rem;">→</div>
            <div style="color:#3690ff; font-size:0.7rem;">REST API</div>
            <div style="color:#3690ff; font-size:1.2rem;">→</div>
        </div>
        <div style="text-align:center;">
            <div style="background:rgba(34,211,238,0.15); width:70px; height:70px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto; border:1px solid rgba(34,211,238,0.3); box-shadow:0 0 20px rgba(34,211,238,0.2);">
                <span style="font-size:1.8rem;">☁️</span>
            </div>
            <p style="color:#e6edf7; font-size:0.85rem; margin-top:10px; font-weight:600;">云端平台</p>
            <p style="color:#8b9dc3; font-size:0.7rem;">Streamlit 前端 / 数据库</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
