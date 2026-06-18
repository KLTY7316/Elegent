"""
危险区域检测页面 —— 多边形绘制 + 区域内违规检测
"""
import streamlit as st
import cv2
import numpy as np
import sys
from pathlib import Path
from utils.history_manager import save_violation_screenshot

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="安全帽检测",
    page_icon="⛑️",
    layout="wide",
)

from utils.styles import inject_common_styles
inject_common_styles()

# 懒加载检测器
@st.cache_resource
def load_zone_checker():
    from utils.zone_check import HelmetZoneChecker
    return HelmetZoneChecker(model_path='models/best.pt', zone_polygon=[])

st.markdown('<h1 class="main-header">🚨 危险区域检测</h1>', unsafe_allow_html=True)
st.markdown("---")
st.caption("在图片上绘制危险区域多边形，检测区域内未佩戴安全帽的人员")

# ============================================================
# 上传区域
# ============================================================
col_upload, col_info = st.columns([2, 1])

with col_upload:
    uploaded_file = st.file_uploader(
        "📁 选择监控图片",
        type=["jpg", "jpeg", "png", "bmp"],
        help="支持 JPG / PNG / BMP 格式",
    )

with col_info:
    st.info("""
    ### 📋 使用说明
    1. 上传施工现场监控图片
    2. 在图片上点击绘制危险区域（至少3个点）
    3. 点击"开始检测"分析区域内安全帽佩戴情况
    4. 红色高亮区域内未佩戴安全帽的人员

    **提示**: 多边形顶点按点击顺序连接，最后点击"完成绘制"
    """)

# ============================================================
# 区域绘制 + 检测逻辑
# ============================================================
if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image is not None:
        h, w = image.shape[:2]

        # 初始化 session_state
        if "zone_points" not in st.session_state:
            st.session_state.zone_points = []
        if "zone_done" not in st.session_state:
            st.session_state.zone_done = False

        st.markdown("### 🎯 步骤一：绘制危险区域")
        st.caption(f"图片尺寸: {w} x {h} | 已点击 {len(st.session_state.zone_points)} 个点")

        # 显示图片并收集点击坐标（使用 Streamlit 的交互方式）
        # 由于 Streamlit 不支持直接在图片上点击，使用坐标输入方式
        col_img, col_ctrl = st.columns([2, 1])

        with col_img:
            # 显示原始图片
            img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            st.image(img_rgb, width='stretch')

        with col_ctrl:
            st.markdown("#### 📍 输入区域顶点")
            st.caption("在图片上找到危险区域的顶点，输入坐标 (x, y)")

            # 添加点
            col_x, col_y = st.columns(2)
            with col_x:
                new_x = st.number_input("X 坐标", min_value=0, max_value=w, value=w//2, step=10)
            with col_y:
                new_y = st.number_input("Y 坐标", min_value=0, max_value=h, value=h//2, step=10)

            if st.button("➕ 添加顶点", type="secondary"):
                st.session_state.zone_points.append((int(new_x), int(new_y)))
                st.rerun()

            # 显示已添加的点
            if st.session_state.zone_points:
                st.markdown("**已添加的顶点：**")
                for i, (px, py) in enumerate(st.session_state.zone_points):
                    cols = st.columns([3, 1])
                    with cols[0]:
                        st.text(f"  点 {i+1}: ({px}, {py})")
                    with cols[1]:
                        if st.button("🗑️", key=f"del_{i}"):
                            st.session_state.zone_points.pop(i)
                            st.rerun()

            if st.button("✅ 完成绘制", type="primary", disabled=len(st.session_state.zone_points) < 3):
                st.session_state.zone_done = True
                st.rerun()

            if st.button("🔄 重新绘制"):
                st.session_state.zone_points = []
                st.session_state.zone_done = False
                st.rerun()

        # 绘制预览
        if st.session_state.zone_points:
            preview = image.copy()
            pts = np.array(st.session_state.zone_points, np.int32).reshape((-1, 1, 2))
            cv2.polylines(preview, [pts], st.session_state.zone_done, (0, 165, 255), 2)
            # 画顶点
            for i, (px, py) in enumerate(st.session_state.zone_points):
                cv2.circle(preview, (px, py), 5, (0, 255, 255), -1)
                cv2.putText(preview, str(i+1), (px+8, py), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

            if st.session_state.zone_done:
                overlay = preview.copy()
                cv2.fillPoly(overlay, [pts], (0, 0, 255))
                preview = cv2.addWeighted(overlay, 0.2, preview, 0.8, 0)

            st.markdown("### 👁️ 区域预览")
            st.image(cv2.cvtColor(preview, cv2.COLOR_BGR2RGB), width='stretch')

        # ============================================================
        # 检测逻辑
        # ============================================================
        if st.session_state.zone_done and st.session_state.zone_points:
            st.markdown("---")
            st.markdown("### 🧠 步骤二：开始检测")

            if st.button("🚀 开始检测", type="primary"):
                with st.spinner("🧠 YOLOv8 正在检测危险区域..."):
                    checker = load_zone_checker()
                    checker.set_zone(st.session_state.zone_points)
                    results = checker.check(image)

                # 绘制结果
                result_img = checker.draw_results(image, results)

                # 违规截图自动保存
                if results.get('violation_count', 0) > 0:
                    save_violation_screenshot(result_img, results.get('detections', []), source="危险区域检测")

                col_res, col_stat = st.columns([2, 1])

                with col_res:
                    st.markdown("#### 🔍 检测结果")
                    st.image(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB), width='stretch')

                with col_stat:
                    st.markdown("#### 📊 区域统计")
                    st.metric("👥 区域内总人数", results['helmet_in_zone'] + results['head_in_zone'])
                    st.markdown('<div class="metric-safe">', unsafe_allow_html=True)
                    st.metric("✅ 区域内戴安全帽", results['helmet_in_zone'])
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.markdown('<div class="metric-violation">', unsafe_allow_html=True)
                    st.metric("🚨 区域内违章人数", results['violation_count'])
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.metric("📊 全图安全帽数", results['total_helmet'])
                    st.metric("📊 全图人头数", results['total_head'])

                    # 违规率
                    total_in_zone = results['helmet_in_zone'] + results['head_in_zone']
                    if total_in_zone > 0:
                        rate = results['violation_count'] / total_in_zone * 100
                        st.markdown(f"**区域违规率: {rate:.1f}%**")
                        st.progress(rate / 100.0)

                # 违规详情
                if results['zone_violations']:
                    with st.expander("🚨 违规详情", expanded=True):
                        for i, v in enumerate(results['zone_violations']):
                            st.error(f"违章 #{i+1}: 位置 {v['bbox']} | 置信度 {v['confidence']:.1%}")
                else:
                    st.success("✅ 危险区域内未发现违章人员！")

                # 保存到 session_state
                if "detection_history" not in st.session_state:
                    st.session_state.detection_history = []
                from utils.get_statistics import get_statistics
                stats = get_statistics(results['detections'])
                st.session_state.detection_history.append(stats)

    else:
        st.error("❌ 无法解析图片文件。")
else:
    st.markdown("### 👇 上传图片开始绘制危险区域")
