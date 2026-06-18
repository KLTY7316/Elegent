"""
图片检测页面 — 上传图片，展示真实检测结果
"""
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import sys
from pathlib import Path
from utils.history_manager import save_violation_screenshot

# 确保可以导入 utils
sys.path.insert(0, str(Path(__file__).parent.parent))

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

            # 违规截图自动保存
            saved = save_violation_screenshot(annotated, detections, source="图片检测")
            if saved:
                st.toast(f"🚨 违规截图已保存 ({saved['violation_count']}处违规)", icon="📸")

        # 在图片上画检测框
        annotated = image.copy()
        for det in detections:
            x1, y1, x2, y2 = det["bbox"]
            conf = det["confidence"]
            if det["class"] == "helmet":
                color = (0, 255, 0)  # 绿色 - 佩戴安全帽
                label = f"Helmet {conf:.0%}"
            else:
                color = (0, 0, 255)  # 红色 - 未佩戴
                label = f"NO Helmet {conf:.0%}"

            # 画框
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            # 画标签背景
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(annotated, (x1, y1 - th - 8), (x1 + tw + 4, y1), color, -1)
            cv2.putText(annotated, label, (x1 + 2, y1 - 4),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # 展示结果
        col_result, col_stats = st.columns([2, 1])

        with col_result:
            st.markdown("### 🔍 检测结果")
            annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
            st.image(annotated_rgb, width='stretch')

        with col_stats:
            st.markdown(f"""
            <div class="glass-card" style="padding:20px;">
                <h4 style="color:#93c5fd; margin:0 0 16px 0;">📊 检测统计</h4>
            """, unsafe_allow_html=True)
            st.metric("检测总人数", stats["total_persons"])
            safe_color = "metric-safe" if stats["helmet_count"] > 0 else ""
            st.markdown(f'<div class="{safe_color}">', unsafe_allow_html=True)
            st.metric("✅ 佩戴安全帽", stats["helmet_count"])
            st.markdown('</div>', unsafe_allow_html=True)
            vio_color = "metric-violation" if stats["no_helmet_count"] > 0 else ""
            st.markdown(f'<div class="{vio_color}">', unsafe_allow_html=True)
            st.metric("⚠️ 未佩戴", stats["no_helmet_count"])
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("#### 违规率")
            violation_rate = stats["violation_rate"]
            bar_color = "🟢" if violation_rate < 10 else "🟡" if violation_rate < 20 else "🔴"
            text_cls = "text-safe" if violation_rate < 10 else "text-warning" if violation_rate < 20 else "text-violation"
            st.progress(violation_rate / 100.0)
            st.markdown(f'<p class="{text_cls}" style="font-weight:700;">**{bar_color} {violation_rate}%**</p>', unsafe_allow_html=True)
            st.metric("平均置信度", f"{stats['avg_confidence']:.1%}")
            st.markdown('</div>', unsafe_allow_html=True)

        # 详细检测列表
        with st.expander("📋 检测详情", expanded=False):
            for i, det in enumerate(detections):
                icon = "✅" if det["class"] == "helmet" else "⚠️"
                col1, col2, col3 = st.columns([1, 2, 1])
                with col1:
                    st.markdown(f"**{icon} #{i+1}**")
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

    # 展示示例效果（用纯色模拟）
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📸\n\n**示例图片 1**\n\n基坑施工区域\n佩戴率: 95%")
    with col2:
        st.warning("📸\n\n**示例图片 2**\n\n脚手架作业区\n佩戴率: 78%")
    with col3:
        st.error("📸\n\n**示例图片 3**\n\n材料堆放区域\n佩戴率: 62%")
