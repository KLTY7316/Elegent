"""
视频检测页面 — 上传视频，逐帧检测
"""
import streamlit as st
import cv2
import numpy as np
import time
import sys
from pathlib import Path
from utils.history_manager import save_violation_screenshot

sys.path.insert(0, str(Path(__file__).parent.parent))


@st.cache_resource
def load_detector():
    from utils.detect import detect
    from utils.get_statistics import get_statistics
    return detect, get_statistics


detect_fn, get_stats_fn = load_detector()

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="安全帽检测",
    page_icon="⛑️",
    layout="wide",
)

from utils.styles import inject_common_styles
inject_common_styles()

st.markdown('<h1 class="main-header">🎥 视频检测</h1>', unsafe_allow_html=True)
st.markdown("---")
st.caption("上传施工监控视频，逐帧分析安全帽佩戴情况")

# ============================================================
# 上传区域
# ============================================================
col_upload, col_ctrl = st.columns([2, 1])

with col_upload:
    uploaded_file = st.file_uploader(
        "📁 选择视频文件",
        type=["mp4", "avi", "mov", "mkv"],
        help="支持 MP4 / AVI / MOV / MKV 格式",
    )

with col_ctrl:
    st.info("""
    ### 📋 使用说明
    1. 上传视频文件
    2. 点击"开始检测"按钮
    3. 系统逐帧分析并展示结果

    **注意**: 视频越大处理时间越长
    """)

    # 检测参数
    st.markdown("### ⚙️ 检测参数")
    skip_frames = st.slider("帧采样间隔", 1, 10, 3,
                            help="每隔 N 帧检测一次，值越大速度越快")
    conf_threshold = st.slider("置信度阈值", 0.1, 1.0, 0.5,
                               help="低于此阈值的检测结果将被过滤")

# ============================================================
# 检测逻辑
# ============================================================
if uploaded_file is not None:
    # 保存临时文件
    temp_path = f"temp_video.{uploaded_file.name.split('.')[-1]}"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.read())

    cap = cv2.VideoCapture(temp_path)
    if not cap.isOpened():
        st.error("❌ 无法打开视频文件，请检查格式。")
    else:
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / max(fps, 1)

        col_info1, col_info2, col_info3 = st.columns(3)
        with col_info1:
            st.metric("总帧数", f"{total_frames:,}")
        with col_info2:
            st.metric("帧率", f"{fps:.1f} FPS")
        with col_info3:
            st.metric("视频时长", f"{duration:.1f}s")

        # 开始检测按钮
        start_btn = st.button("🚀 开始检测", type="primary", key="start_video")

        if start_btn:
            placeholder = st.empty()
            progress_bar = st.progress(0)
            stats_placeholder = st.empty()

            frame_count = 0
            processed = 0
            all_stats = []

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame_count += 1

                # 按间隔采样
                if frame_count % skip_frames != 0:
                    continue

                # 真实模型检测
                detections = detect_fn(frame, conf_threshold=conf_threshold)
                stats = get_stats_fn(detections)
                all_stats.append(stats)

                # 违规截图自动保存（每帧，但通过计数限制频率）
                if stats["no_helmet_count"] > 0 and processed % max(skip_frames, 3) == 0:
                    save_violation_screenshot(frame, detections, source="视频检测")

                # 画检测框
                annotated = frame.copy()
                for det in detections:
                    x1, y1, x2, y2 = [int(v) for v in det["bbox"]]
                    color = (0, 255, 0) if det["class"] == "helmet" else (0, 0, 255)
                    conf = det["confidence"]
                    label = f"Helmet {conf:.0%}" if det["class"] == "helmet" else f"NO Helmet {conf:.0%}"
                    cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(annotated, label, (x1, y1 - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
                placeholder.image(annotated_rgb, width='stretch')

                # 更新进度
                progress = min(frame_count / total_frames, 1.0)
                progress_bar.progress(progress)

                # 更新统计
                with stats_placeholder.container():
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("已处理帧", processed)
                        with col2:
                            st.markdown('<div class="metric-safe">', unsafe_allow_html=True)
                            st.metric("佩戴安全帽", stats["helmet_count"])
                            st.markdown('</div>', unsafe_allow_html=True)
                        with col3:
                            st.markdown('<div class="metric-violation">', unsafe_allow_html=True)
                            st.metric("违规人数", stats["no_helmet_count"])
                            st.markdown('</div>', unsafe_allow_html=True)
                        with col4:
                            st.metric("检测人数", stats["total_persons"])

                processed += 1
                time.sleep(0.05)  # 控制播放速度

            cap.release()
            progress_bar.progress(1.0)
            st.success(f"✅ 视频检测完成！共处理 {processed} 帧。")

            # 汇总统计
            if all_stats:
                st.markdown("### 📊 视频检测汇总")
                total_persons = sum(s["total_persons"] for s in all_stats)
                total_violations = sum(s["no_helmet_count"] for s in all_stats)
                avg_rate = total_violations / max(total_persons, 1) * 100

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("总检测人数", total_persons)
                with col2:
                    st.metric("总违规次数", total_violations)
                with col3:
                    st.metric("平均违规率", f"{avg_rate:.1f}%")

else:
    st.markdown("### 👇 上传视频开始检测")
    st.markdown("")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🎥\n\n**监控录像 1**\n\n基坑区域\n时长: 5:32")
    with col2:
        st.info("🎥\n\n**监控录像 2**\n\n脚手架区域\n时长: 12:15")
    with col3:
        st.info("🎥\n\n**监控录像 3**\n\n出入口区域\n时长: 8:47")
