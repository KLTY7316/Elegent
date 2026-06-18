"""
AI 报告页面 —— 集成 C 的 llm_report.py，调用真实 LLM 生成报告
"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="安全帽检测 - AI报告",
    page_icon="⛑️",
    layout="wide",
)

from utils.styles import inject_common_styles
inject_common_styles()

st.markdown('<h1 class="main-header">🤖 AI 安全分析报告</h1>', unsafe_allow_html=True)
st.markdown("---")
st.caption("基于 LLM 大语言模型（Ollama qwen:4b），自动生成安全帽佩戴情况分析报告")

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

    # 从 session_state 获取真实检测数据，如果没有则使用默认
    if "detection_history" in st.session_state and st.session_state.detection_history:
        latest_stats = st.session_state.detection_history[-1]
        st.success(f"✅ 已加载最新检测数据（{latest_stats.get('timestamp', '未知时间')}）")
    else:
        st.warning("⚠️ 暂无检测数据，将使用示例数据生成报告")
        latest_stats = {
            'total_persons': 12,
            'helmet_count': 10,
            'head_count': 2,
            'violation_rate': 0.167,
            'timestamp': '2026-06-10 10:00:00'
        }

    # llm_report 需要的字段映射
    stats_for_llm = {
        'total_workers': latest_stats.get('total_persons', 0),
        'helmet_count': latest_stats.get('helmet_count', 0),
        'head_count': latest_stats.get('no_helmet_count', latest_stats.get('head_count', 0)),
        'violation_rate': latest_stats.get('violation_rate', 0) / 100.0
        if latest_stats.get('violation_rate', 0) > 1
        else latest_stats.get('violation_rate', 0),
    }

    # 风险等级
    violation_rate_pct = stats_for_llm['violation_rate'] * 100
    if violation_rate_pct < 10:
        risk_text = "🟢 低风险"
        risk_color = "#00C853"
    elif violation_rate_pct < 20:
        risk_text = "🟡 中风险"
        risk_color = "#FF9100"
    else:
        risk_text = "🔴 高风险"
        risk_color = "#FF1744"

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("👥 检测人数", stats_for_llm['total_workers'])
        st.metric("✅ 佩戴人数", stats_for_llm['helmet_count'])
    with col_s2:
        st.metric("🚨 违规人数", stats_for_llm['head_count'])
        st.metric("⚠️ 违规率", f"{violation_rate_pct:.1f}%")
        st.markdown(f"<p style='color:{risk_color};font-size:18px;font-weight:bold;'>{risk_text}</p>", unsafe_allow_html=True)

    generate_btn = st.button("🤖 生成 AI 报告", type="primary", key="gen_report")

with col_preview:
    st.info("""
    ### 📋 报告说明
    AI 报告基于检测结果自动生成，包含：
    - 📊 检测数据统计与分析
    - 🔍 风险评估与预警
    - 💡 改进建议与措施
    - 📈 趋势分析与预测

    **技术栈**: Ollama + qwen:4b 本地大模型
    **服务地址**: http://localhost:11434
    """)

# ============================================================
# 生成报告
# ============================================================
if generate_btn:
    with st.spinner("🤖 AI 正在分析数据并生成报告..."):
        from utils.llm_report import generate_report

        report = generate_report(stats_for_llm)

    # 展示报告
    st.markdown("---")
    st.markdown("### 📄 报告预览")
    st.markdown(report)

    # 操作按钮
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 保存报告", key="save_report"):
            from utils.llm_report import save_report
            filepath = save_report(report, stats_for_llm)
            st.success(f"✅ 报告已保存到: {filepath}")
    with col2:
        if st.button("📋 复制报告", key="copy_report"):
            st.code(report, language="markdown")

else:
    # 默认显示提示
    st.markdown("---")
    st.markdown("### 📄 使用说明")
    st.markdown("""
    1. 先在「图片检测」或「视频检测」页面进行检测，数据会自动汇总
    2. 回到本页面，点击「🤖 生成 AI 报告」按钮
    3. AI 将基于最新检测数据生成安全分析报告
    4. 报告可保存为 Markdown 文件或复制到剪贴板

    **注意**: 需要本地安装并运行 Ollama（qwen:4b 模型）
    """)
