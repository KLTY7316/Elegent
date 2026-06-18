"""
历史记录 —— 违规截图浏览与检测历史
从 outputs/violations/ 读取真实的违规截图和记录
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(
    page_title="安全帽检测",
    page_icon="⛑️",
    layout="wide",
)

from utils.styles import inject_common_styles
from utils.history_manager import (
    load_all_records, get_history_stats, filter_records,
    update_record_status, delete_record, clear_all_records
)
inject_common_styles()

st.markdown('<h1 class="main-header">📁 历史记录</h1>', unsafe_allow_html=True)
st.markdown("---")
st.caption("浏览违规截图与检测历史记录，所有截图自动保存在 outputs/violations/ 目录")

# ============================================================
# 加载数据
# ============================================================
all_records = load_all_records()

# ============================================================
# 筛选器
# ============================================================
col_f1, col_f2, col_f3, col_f4 = st.columns(4)
with col_f1:
    time_range = st.selectbox("⏰ 时间范围", ["全部", "今日", "近7天", "近30天"], index=0)
with col_f2:
    source_list = ["全部"] + sorted(set(r.get("source", "未知") for r in all_records)) if all_records else ["全部"]
    source_filter = st.selectbox("📹 检测来源", source_list, index=0)
with col_f3:
    status_filter = st.selectbox("🚦 处理状态", ["全部", "待处理", "已处理"], index=0)
with col_f4:
    keyword = st.text_input("🔍 搜索记录ID/时间", placeholder="输入关键字...")

# 筛选
filtered = filter_records(all_records, time_range, source_filter, status_filter, keyword)

# ============================================================
# 统计概览
# ============================================================
stats = get_history_stats(all_records)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("总违规记录", stats["total_records"])
with col2:
    st.markdown('<div class="metric-safe">', unsafe_allow_html=True)
    st.metric("已处理", stats["handled"], delta=f"处理率 {stats['handle_rate']}%")
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-violation">', unsafe_allow_html=True)
    st.metric("待处理", stats["pending"])
    st.markdown('</div>', unsafe_allow_html=True)
with col4:
    st.metric("违规总数", stats["total_violations"])

st.markdown("---")

if not filtered:
    st.info("📭 暂无违规记录。检测到未佩戴安全帽时会自动保存截图。")
else:
    st.markdown(f"### 📋 违规记录列表（共 {len(filtered)} 条）")

    # 分页
    page_size = 6
    total_pages = max(1, (len(filtered) + page_size - 1) // page_size)
    if "history_page" not in st.session_state:
        st.session_state.history_page = 0
    page = st.session_state.history_page
    start_idx = page * page_size
    end_idx = min(start_idx + page_size, len(filtered))
    page_records = filtered[start_idx:end_idx]

    # 分页导航
    col_p1, col_p2, col_p3, col_p4 = st.columns([1, 1, 3, 1])
    with col_p1:
        if st.button("◀ 上一页", disabled=page == 0):
            st.session_state.history_page -= 1
            st.rerun()
    with col_p2:
        if st.button("下一页 ▶", disabled=page >= total_pages - 1):
            st.session_state.history_page += 1
            st.rerun()
    with col_p3:
        st.markdown(f'<p style="color:#8b9dc3; text-align:center; padding-top:8px;">第 {page+1}/{total_pages} 页（{start_idx+1}-{end_idx} / {len(filtered)}）</p>', unsafe_allow_html=True)
    with col_p4:
        if st.button("🔄 刷新", type="secondary"):
            st.rerun()

    # 截图网格展示
    for idx, record in enumerate(page_records):
        img_path = record.get("thumbnail_path") or record.get("image_path", "")
        has_image = img_path and Path(img_path).exists()

        col_card1, col_card2, col_card3 = st.columns([1, 2, 1])
        with col_card1:
            if has_image:
                st.image(str(img_path), width='stretch')
            else:
                st.markdown("""
                <div style="background:rgba(20,45,80,0.3); border-radius:12px; height:120px; display:flex; align-items:center; justify-content:center;">
                    <span style="font-size:2rem; color:#8b9dc3;">📷</span>
                </div>
                """, unsafe_allow_html=True)

        with col_card2:
            st.markdown(f"""
            <div style="padding-left:10px;">
                <p style="color:#e6edf7; font-size:0.9rem; margin:0; font-weight:600;">🆔 {record['id']}</p>
                <p style="color:#8b9dc3; font-size:0.8rem; margin:4px 0;">📅 {record['timestamp']}</p>
                <p style="color:#8b9dc3; font-size:0.8rem; margin:4px 0;">📹 来源: {record.get('source', '未知')}</p>
                <p style="color:#8b9dc3; font-size:0.8rem; margin:4px 0;">
                    违规: <span class="text-violation">{record.get('violation_count', 0)}</span> 处 |
                    违规率: <span class="{'text-violation' if record.get('violation_rate', 0) > 20 else 'text-warning' if record.get('violation_rate', 0) > 10 else 'text-safe'}">{record.get('violation_rate', 0)}%</span>
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col_card3:
            status = record.get("status", "待处理")
            if status == "已处理":
                badge_cls = "compliant-badge"
            else:
                badge_cls = "violation-badge"
            st.markdown(f'<span class="{badge_cls}">{status}</span>', unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                if status == "待处理":
                    if st.button("✅ 标记处理", key=f"handle_{record['id']}"):
                        update_record_status(record["id"], "已处理")
                        st.rerun()
            with col_b:
                if st.button("🗑️ 删除", key=f"del_{record['id']}"):
                    delete_record(record["id"])
                    st.rerun()

        # 如果是完整截图路径，展示查看原图链接
        full_path = record.get("image_path", "")
        if full_path and Path(full_path).exists():
            st.markdown(f'<p style="text-align:right; color:#60b8ff; font-size:0.75rem;">📸 查看原图: {Path(full_path).name}</p>', unsafe_allow_html=True)

        st.markdown("<hr style='margin:8px 0; opacity:0.3;'>", unsafe_allow_html=True)

# ============================================================
# 操作按钮
# ============================================================
st.markdown("---")
col_b1, col_b2 = st.columns(2)
with col_b1:
    if all_records and st.button("📥 导出全部记录 (CSV)", key="export_all"):
        import json, csv
        csv_path = Path("outputs/violations/violation_records.csv")
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["id","timestamp","source","violation_count","total_detected","violation_rate","status"])
            writer.writeheader()
            for r in all_records:
                writer.writerow({k: r.get(k, "") for k in writer.fieldnames})
        st.success(f"✅ 已导出 {len(all_records)} 条记录到 {csv_path}")
with col_b2:
    if all_records and st.button("🗑️ 清除所有记录", type="secondary"):
        if clear_all_records():
            st.warning("✅ 所有记录和截图已清除")
            st.rerun()
        else:
            st.error("❌ 清除失败")