"""
AI 报告页面 — 模拟 LLM 生成安全分析报告
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.fake_data import fake_generate_report, fake_get_statistics, fake_detect
import numpy as np

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="AI 报告 - 安全帽检测系统",
    page_icon="🤖",
    layout="wide",
)

from utils.styles import inject_common_styles
inject_common_styles()

st.markdown('<h1 class="main-header">🤖 AI 安全分析报告</h1>', unsafe_allow_html=True)
st.markdown("---")
st.caption("基于 LLM 大语言模型，自动生成安全帽佩戴情况分析报告")

# ============================================================
# 控制面板
# ============================================================
col_ctrl, col_preview = st.columns([1, 2])

with col_ctrl:
    st.markdown("### ⚙️ 报告配置")

    report_type = st.selectbox(
        "报告类型",
        ["日报", "周报", "月报", "专项报告"],
        index=0,
    )

    time_range = st.selectbox(
        "时间范围",
        ["今日", "近3天", "近7天", "近30天"],
        index=0,
    )

    include_suggestions = st.toggle("包含改进建议", value=True)
    include_charts = st.toggle("包含图表描述", value=True)

    generate_btn = st.button("🤖 生成 AI 报告", type="primary", key="gen_report")

with col_preview:
    st.info("""
    ### 📋 报告说明
    AI 报告基于检测结果自动生成，包含：
    - 📊 检测数据统计与分析
    - 🔍 风险评估与预警
    - 💡 改进建议与措施
    - 📈 趋势分析与预测

    **注意**: 当前使用模拟数据，第二周将接入真实 LLM 接口。
    """)

# ============================================================
# 生成报告
# ============================================================
if generate_btn:
    with st.spinner("🤖 AI 正在分析数据并生成报告..."):
        import time
        time.sleep(2)  # 模拟生成延迟

        # 生成假统计数据
        fake_image = np.zeros((480, 640, 3), dtype=np.uint8)
        detections = fake_detect(fake_image)
        stats = fake_get_statistics(detections)

        # 生成报告
        # TODO: 第二周替换为 from utils.llm_report import generate_report
        report = fake_generate_report(stats)

    # 展示报告
    st.markdown("---")
    st.markdown("### 📄 报告预览")
    st.markdown(report)

    # 操作按钮
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 保存报告", key="save_report"):
            # 保存为 markdown
            report_path = Path("outputs/violations/ai_report.md")
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(report, encoding="utf-8")
            st.success(f"✅ 报告已保存到: {report_path}")
    with col2:
        if st.button("📋 复制报告", key="copy_report"):
            st.code(report, language="markdown")
    with col3:
        if st.button("📤 导出 PDF", key="export_pdf"):
            st.info("📄 PDF 导出功能将在第二周完善")

else:
    # 默认显示最近报告
    st.markdown("---")
    st.markdown("### 📄 最近报告")

    # 模拟最近报告列表
    reports = [
        {"date": "2026-06-06", "type": "日报", "status": "已完成"},
        {"date": "2026-06-05", "type": "日报", "status": "已完成"},
        {"date": "2026-06-02", "type": "周报", "status": "已完成"},
        {"date": "2026-05-30", "type": "日报", "status": "已完成"},
    ]

    for r in reports:
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            st.markdown(f"📄 **{r['date']}** — {r['type']}")
        with col2:
            st.markdown(f"类型: {r['type']}")
        with col3:
            st.markdown(f"状态: ✅ {r['status']}")
        with col4:
            st.button("查看", key=f"view_{r['date']}")
        st.divider()
