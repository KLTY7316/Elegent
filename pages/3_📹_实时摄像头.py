"""
实时摄像头检测页面
"""
import streamlit as st
import cv2
import numpy as np
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.fake_data import fake_detect, fake_get_statistics

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="实时摄像头 - 安全帽检测系统",
    page_icon="📹",
    layout="wide",
)

st.markdown('<h1 class="main-header">📹 实时摄像头检测</h1>', unsafe_allow_html=True)
st.markdown("---")
st.caption("接入摄像头，实时检测施工现场安全帽佩戴情况")

# ============================================================
# 控制面板
# ============================================================
col_ctrl, col_status = st.columns([1, 2])

with col_ctrl:
    st.markdown("### ⚙️ 控制面板")

    camera_source = st.selectbox(
        "摄像头来源",
        ["默认摄像头 (0)", "摄像头 (1)", "摄像头 (2)"],
        index=0,
    )
    camera_idx = int(camera_source.split("(")[1].split(")")[0])

    conf_threshold = st.slider("置信度阈值", 0.1, 1.0, 0.5)
    show_labels = st.toggle("显示标签", value=True)
    alert_sound = st.toggle("违规声音提醒", value=False)

    start_btn = st.button("🚀 开始检测", type="primary", key="start_camera")
    stop_btn = st.button("⏹️ 停止检测", key="stop_camera")

with col_status:
    st.markdown("### 📊 实时状态")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("FPS", "0")
    with col2:
        st.metric("检测人数", "0")
    with col3:
        st.metric("佩戴安全帽", "0")
    with col4:
        st.metric("违规人数", "0")

# ============================================================
# 摄像头检测逻辑
# ============================================================
if "camera_running" not in st.session_state:
    st.session_state.camera_running = False

if start_btn:
    st.session_state.camera_running = True
    st.toast("📹 摄像头已启动", icon="✅")

if stop_btn:
    st.session_state.camera_running = False
    st.toast("⏹️ 摄像头已停止", icon="⏹️")

if st.session_state.camera_running:
    cap = cv2.VideoCapture(camera_idx)

    if not cap.isOpened():
        st.error("❌ 无法打开摄像头。请检查摄像头是否连接正常，或是否有其他程序占用。")
        st.session_state.camera_running = False
    else:
        frame_placeholder = st.empty()
        stats_placeholder = st.empty()

        frame_count = 0
        start_time = time.time()
        fps_display = 0

        while st.session_state.camera_running:
            ret, frame = cap.read()
            if not ret:
                st.warning("⚠️ 摄像头读取失败，尝试重新连接...")
                time.sleep(1)
                continue

            frame_count += 1

            # 每 3 帧检测一次
            if frame_count % 3 == 0:
                detections = fake_detect(frame)
                stats = fake_get_statistics(detections)

                # 画检测框
                for det in detections:
                    x1, y1, x2, y2 = [int(v) for v in det["bbox"]]
                    color = (0, 255, 0) if det["class"] == "helmet" else (0, 0, 255)
                    label = det["label"] if show_labels else ""
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    if label:
                        cv2.putText(frame, label, (x1, y1 - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # 计算 FPS
                elapsed = time.time() - start_time
                if elapsed > 0:
                    fps_display = frame_count / elapsed

                # 显示画面
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_placeholder.image(frame_rgb, width='stretch')

                # 更新统计
                with stats_placeholder.container():
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("FPS", f"{fps_display:.1f}")
                    with col2:
                        st.metric("检测人数", stats["total_persons"])
                    with col3:
                        st.metric("佩戴安全帽", stats["helmet_count"])
                    with col4:
                        st.metric("违规人数", stats["no_helmet_count"])

            time.sleep(0.01)

        cap.release()
        st.info("📹 摄像头已停止。")
else:
    st.markdown("### 👇 点击「开始检测」启动摄像头")
    st.markdown("")

    # 预览占位
    col1, col2 = st.columns([2, 1])
    with col1:
        # 用灰色占位模拟摄像头画面
        placeholder_img = np.zeros((480, 640, 3), dtype=np.uint8)
        placeholder_img[:] = (30, 40, 50)
        cv2.putText(placeholder_img, "Camera Preview", (200, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (100, 100, 100), 2)
        cv2.putText(placeholder_img, "Click 'Start' to begin", (170, 290),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (80, 80, 80), 1)
        placeholder_rgb = cv2.cvtColor(placeholder_img, cv2.COLOR_BGR2RGB)
        st.image(placeholder_rgb, width='stretch')
    with col2:
        st.warning("""
        ### ⚠️ 注意事项
        - 确保摄像头已正确连接
        - 关闭其他占用摄像头的程序
        - 建议在光线充足的环境下使用
        - 检测过程中请勿关闭此页面
        """)
