"""
图片检测页面 — 上传图片，展示真实检测结果
"""
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import sys
from pathlib import Path
from datetime import datetime

# 确保可以导入 utils
sys.path.insert(0, str(Path(__file__).parent.parent))

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="安全帽检测 - 图片检测",
    page_icon="⛑️",
    layout="wide",
)

from utils.styles import inject_common_styles
inject_common_styles()

# 懒加载真实模型
@st.cache_resource
def load_detector():
    from utils.detect import detect
    from utils.get_statistics import get_statistics
    return detect, get_statistics

st.markdown('<h1 class="main-header">📸 图片检测</h1>', unsafe_allow_html=True)
st.markdown("---")
st.caption("上传施工现场图片，AI 自动识别安全帽佩戴情况")

# ============================================================
# 上传区域
# ============================================================
col_upload, col_info = st.columns([2, 1])

with col_upload:
    uploaded_file = st.file_uploader(
        "📁 选择图片文件",
        type=["jpg", "jpeg", "png", "bmp", "webp"],
        help="支持 JPG / PNG / BMP / WebP 格式",
    )

with col_info:
    st.info("""
    ### 📋 使用说明
    1. 点击上传区域选择图片
    2. 系统自动进行安全帽检测
    3. 查看检测结果和统计信息
    4. 违规截图自动保存到 outputs/violations/

    **支持格式**: JPG, PNG, BMP, WebP
    **最大尺寸**: 20MB
    """)

# ============================================================
# 检测逻辑（真实模型）
# ============================================================
if uploaded_file is not None:
    # 读取图片
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image is not None:
        with st.spinner("🧠 YOLOv8 正在检测中..."):
            detect_fn, get_stats_fn = load_detector()
            detections = detect_fn(image)
            stats = get_stats_fn(detections)

        # 在图片上画检测框
        annotated = image.copy()
        violation_screenshots = []  # 收集违规截图
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            conf = det["confidence"]
            if det["class"] == "helmet":
                color = (0, 200, 0)  # 绿色 - 佩戴安全帽
                label = f"Helmet {conf:.0%}"
            else:
                color = (0, 0, 255)  # 红色 - 未佩戴
                label = f"NO Helmet {conf:.0%}"
                # 保存违规截图
                margin = 20
                h, w = image.shape[:2]
                vx1 = max(0, x1 - margin)
                vy1 = max(0, y1 - margin)
                vx2 = min(w, x2 + margin)
                vy2 = min(h, y2 + margin)
                violation_crop = image[vy1:vy2, vx1:vx2]
                violation_screenshots.append(violation_crop)

            # 画框
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 3)
            # 画标签背景
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            cv2.rectangle(annotated, (x1, y1 - th - 10), (x1 + tw + 8, y1), color, -1)
            cv2.putText(annotated, label, (x1 + 4, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # 保存违规截图到 outputs/violations/
        if violation_screenshots:
            violation_dir = Path("outputs/violations")
            violation_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            for idx, vimg in enumerate(violation_screenshots):
                save_path = violation_dir / f"violation_{timestamp}_{idx+1}.png"
                cv2.imwrite(str(save_path), vimg)

        # 展示结果
        col_result, col_stats = st.columns([2, 1])

        with col_result:
            st.markdown("### 🔍 检测结果")
            annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            st.image(annotated_rgb, width='stretch')

        with col_stats:
            st.markdown("### 📊 检测统计")
            # 卡片式布局
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.metric("👥 总人数", stats["total_persons"])
            with col_s2:
                st.metric("✅ 佩戴", stats["helmet_count"],
                          delta=f"{stats['helmet_count']}/{stats['total_persons']}")

            col_s3, col_s4 = st.columns(2)
            with col_s3:
                st.metric("🚨 违规", stats["no_helmet_count"],
                          delta_color="inverse")
            with col_s4:
                st.metric("📈 置信度", f"{stats['avg_confidence']:.1%}")

            # 违规率进度条
            st.markdown("#### 违规率")
            violation_rate = stats["violation_rate"]
            if violation_rate < 10:
                bar_color = "🟢 低风险"
                bar_color_hex = "#00C853"
            elif violation_rate < 20:
                bar_color = "🟡 中风险"
                bar_color_hex = "#FF9100"
            else:
                bar_color = "🔴 高风险"
                bar_color_hex = "#FF1744"

            st.progress(violation_rate / 100.0)
            st.markdown(f"<p style='color:{bar_color_hex};font-weight:700'>{bar_color} — {violation_rate}%</p>",
                        unsafe_allow_html=True)

            # 违规截图保存提示
            if violation_screenshots:
                st.error(f"⚠️ 已保存 {len(violation_screenshots)} 张违规截图到 outputs/violations/")

        # 详细检测列表
        with st.expander("📋 检测详情", expanded=False):
            for i, det in enumerate(detections):
                if det["class"] == "helmet":
                    icon = "✅"
                    row_color = "background-color:#00C85315"
                else:
                    icon = "🚨"
                    row_color = "background-color:#FF174415"
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    st.markdown(f"<div style='{row_color};padding:8px;border-radius:6px'><b>{icon} #{i+1}</b></div>",
                                unsafe_allow_html=True)
                with col2:
                    bbox_str = f"({det['bbox'][0]}, {det['bbox'][1]}) → ({det['bbox'][2]}, {det['bbox'][3]})"
                    st.text(f"位置: {bbox_str}")
                with col3:
                    st.markdown(f"置信度: **{det['confidence']:.1%}**")
                st.divider()

        # 保存到 session_state（供看板使用）
        if "detection_history" not in st.session_state:
            st.session_state.detection_history = []
        st.session_state.detection_history.append(stats)

    else:
        st.error("❌ 无法解析图片文件，请检查格式是否正确。")
else:
    # 没有上传图片时显示示例
    st.markdown("### 👇 上传图片开始检测")
    st.markdown("")

    # 展示示例效果
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("📸\n\n**示例图片 1**\n\n基坑施工区域\n佩戴率: 95%")
    with col2:
        st.warning("📸\n\n**示例图片 2**\n\n脚手架作业区\n佩戴率: 78%")
    with col3:
        st.error("📸\n\n**示例图片 3**\n\n材料堆放区域\n佩戴率: 62%")
