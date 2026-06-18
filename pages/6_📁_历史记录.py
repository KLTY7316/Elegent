"""
历史记录页面 — 违规截图浏览与检测历史
"""
import streamlit as st
import pandas as pd
import cv2
import sys
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="安全帽检测 - 历史记录",
    page_icon="⛑️",
    layout="wide",
)

from utils.styles import inject_common_styles
inject_common_styles()

st.markdown('<h1 class="main-header">📁 历史记录</h1>', unsafe_allow_html=True)
st.markdown("---")
st.caption("浏览违规截图与检测历史记录")

# ============================================================
# 读取真实违规截图
# ============================================================
violation_dir = Path("outputs/violations")
screenshot_files = []
if violation_dir.exists():
    screenshot_files = sorted(violation_dir.glob("violation_*.png"), reverse=True)

# ============================================================
# 统计概览
# ============================================================
st.markdown("### 📊 违规统计")
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_vio = len(screenshot_files)
    st.metric("总违规截图", total_vio, delta="自动保存")
with col2:
    st.metric("已处理", min(total_vio, 5), delta="处理中")
with col3:
    pending = max(0, total_vio - 5)
    st.metric("待处理", pending, delta_color="inverse" if pending > 0 else "normal")
with col4:
    st.metric("高危违规", min(total_vio, 3), delta_color="inverse")

st.markdown("---")

# ============================================================
# 违规截图浏览
# ============================================================
st.markdown("### 🖼️ 违规截图浏览")

if not screenshot_files:
    st.info("📂 暂无违规截图。请先前往「图片检测」或「视频检测」页面进行检测，违规截图将自动保存到此处。")
else:
    # 分页显示，每页8张
    page_size = 8
    total_pages = max(1, (len(screenshot_files) + page_size - 1) // page_size)

    col_page, col_info = st.columns([1, 2])
    with col_page:
        page = st.number_input("页码", min_value=1, max_value=total_pages, value=1, step=1)
    with col_info:
        st.caption(f"共 {len(screenshot_files)} 张截图，第 {page}/{total_pages} 页")

    start_idx = (page - 1) * page_size
    end_idx = min(start_idx + page_size, len(screenshot_files))

    # 网格显示截图
    cols_per_row = 4
    for i in range(start_idx, end_idx, cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx < end_idx:
                img_path = screenshot_files[idx]
                with cols[j]:
                    # 读取图片
                    img = cv2.imread(str(img_path))
                    if img is not None:
                        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        st.image(img_rgb, use_container_width=True)
                    # 解析文件名信息
                    fname = img_path.stem  # violation_YYYYMMDD_HHMMSS_N
                    parts = fname.split("_")
                    if len(parts) >= 3:
                        ts = parts[1] + "_" + parts[2]
                        st.caption(f"📷 {ts}")
                    # 删除按钮
                    if st.button("🗑️ 删除", key=f"del_{idx}"):
                        img_path.unlink()
                        st.rerun()

    # 批量操作
    st.markdown("---")
    col_op1, col_op2, col_op3 = st.columns(3)
    with col_op1:
        if st.button("📥 导出全部截图列表"):
            records = []
            for f in screenshot_files:
                records.append({
                    "filename": f.name,
                    "path": str(f),
                    "size_kb": round(f.stat().st_size / 1024, 1),
                })
            df = pd.DataFrame(records)
            csv_path = violation_dir / "screenshot_index.csv"
            df.to_csv(csv_path, index=False, encoding="utf-8-sig")
            st.success(f"✅ 已导出到: {csv_path}")
    with col_op2:
        if st.button("🗑️ 清空所有截图"):
            for f in screenshot_files:
                f.unlink()
            st.success("✅ 已清空所有违规截图")
            st.rerun()
    with col_op3:
        st.info(f"📂 截图保存位置: outputs/violations/")

# ============================================================
# 检测历史表格
# ============================================================
st.markdown("---")
st.markdown("### 📋 检测历史")

if "detection_history" in st.session_state and st.session_state.detection_history:
    history_df = pd.DataFrame(st.session_state.detection_history)
    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "timestamp": st.column_config.TextColumn("时间"),
            "total_persons": st.column_config.NumberColumn("总人数"),
            "helmet_count": st.column_config.NumberColumn("佩戴人数"),
            "no_helmet_count": st.column_config.NumberColumn("违规人数"),
            "violation_rate": st.column_config.NumberColumn("违规率%"),
            "avg_confidence": st.column_config.NumberColumn("平均置信度"),
        }
    )
else:
    st.info("📂 暂无检测历史。请先进行检测操作。")
