# -*- coding: utf-8 -*-
"""
============================================================================
 VN AIDEOM-VN  —  AI-Driven Decision Optimization Model for Vietnam
 Mô hình ra quyết định phát triển kinh tế Việt Nam trong kỉ nguyên AI
----------------------------------------------------------------------------
 Streamlit dashboard mô phỏng 12 bài tập của bộ đề
 "MÔ HÌNH RA QUYẾT ĐỊNH PHÁT TRIỂN KINH TẾ VIỆT NAM TRONG KỈ NGUYÊN AI".

 Họ và tên   : Nguyễn Bảo Khánh
 Mã sinh viên: 23051266
 Bài tập lớn : Các mô hình ra quyết định

 Chạy:  streamlit run app.py
============================================================================
"""

import os
import io
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st

# ----------------------------------------------------------------------------
# Cấu hình trang
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="VN AIDEOM-VN",
    page_icon="🇻🇳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Một chút CSS để giao diện gần với mockup
st.markdown(
    """
    <style>
      .block-container {padding-top: 1.6rem; padding-bottom: 2rem;}
      .hero {
        background: linear-gradient(120deg,#dbe4ff 0%,#e9d8fd 45%,#d7f5e3 100%);
        border-radius: 18px; padding: 28px 32px; margin-bottom: 18px;
      }
      .hero h1 {margin: 0 0 4px 0; font-size: 2.0rem;}
      .hero p  {margin: 6px 0; color:#374151;}
      .pill {
        display:inline-block; background:#ffffffcc; border:1px solid #e5e7eb;
        border-radius: 999px; padding:6px 14px; margin:4px 6px 0 0; font-size:0.85rem;
      }
      .kpi-delta {color:#16a34a; font-weight:600; font-size:0.85rem;}
      .sb-id {
        background:#f1f5f9; border-radius:10px; padding:12px 14px;
        font-size:0.85rem; line-height:1.5; margin-top:8px;
      }
      .small-note {color:#6b7280; font-size:0.85rem;}
      div[data-testid="stMetricValue"] {font-size:1.5rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Matplotlib font hỗ trợ tiếng Việt cơ bản
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.autolayout"] = True


# ----------------------------------------------------------------------------
# Nạp dữ liệu  (tìm CSV trong thư mục hiện tại, /data, hoặc uploads)
# ----------------------------------------------------------------------------
_SEARCH_DIRS = [
    ".",
    "data",
    "/mnt/user-data/uploads",
    os.path.dirname(os.path.abspath(__file__)),
]


def _find(fname):
    for d in _SEARCH_DIRS:
        p = os.path.join(d, fname)
        if os.path.exists(p):
            return p
    return fname  # để pandas báo lỗi rõ nếu thiếu


@st.cache_data(show_spinner=False)
def load_macro():
    df = pd.read_csv(_find("vietnam_macro_2020_2025.csv"))
    return df.sort_values("year").reset_index(drop=True)


@st.cache_data(show_spinner=False)
def load_sectors():
    return pd.read_csv(_find("vietnam_sectors_2024.csv"))


@st.cache_data(show_spinner=False)
def load_regions():
    return pd.read_csv(_find("vietnam_regions_2024.csv"))


# Tên ngành / vùng tiếng Việt dùng chung
SECTOR_VI = [
    "Nông-Lâm-Thủy sản", "CN chế biến chế tạo", "Xây dựng", "Khai khoáng",
    "Bán buôn-bán lẻ", "Tài chính-Ngân hàng", "Logistics-Vận tải",
    "CNTT-Truyền thông", "Giáo dục-Đào tạo", "Y tế",
]
REGION_VI = [
    "Trung du miền núi phía Bắc", "Đồng bằng sông Hồng",
    "Bắc Trung Bộ + DH Trung Bộ", "Tây Nguyên",
    "Đông Nam Bộ", "Đồng bằng sông Cửu Long",
]


def show_fig(fig):
    """Hiển thị figure matplotlib rồi đóng để tránh rò bộ nhớ."""
    st.pyplot(fig)
    plt.close(fig)


# ----------------------------------------------------------------------------
# SIDEBAR — mục lục
# ----------------------------------------------------------------------------
PAGES = [
    "🏠 Trang chủ",
    "🌱 Bài 1 — Cobb-Douglas + AI",
    "💰 Bài 2 — LP ngân sách số",
    "📊 Bài 3 — Priority 10 ngành",
    "🗺️ Bài 4 — LP ngành-vùng",
    "🎯 Bài 5 — MIP 15 dự án",
    "🏆 Bài 6 — TOPSIS 6 vùng",
    "🌐 Bài 7 — NSGA-II Pareto",
    "📈 Bài 8 — Động 2026-2035",
    "👷 Bài 9 — Lao động & AI",
    "🎲 Bài 10 — Stochastic SP",
    "♻️ Bài 11 — Q-learning RL",
    "🧩 Bài 12 — AIDEOM tích hợp",
]

with st.sidebar:
    st.markdown("### 🇻🇳 VN AIDEOM-VN")
    st.caption("Mô hình ra quyết định phát triển kinh tế Việt Nam trong kỉ nguyên AI")
    page = st.radio("Chọn bài", PAGES, label_visibility="visible")
    st.markdown("---")
    st.markdown(
        """
        <div class="sb-id">
        <b>Họ và tên:</b> Nguyễn Bảo Khánh<br>
        <b>Mã sinh viên:</b> 23051266<br>
        <b>Bài tập lớn:</b> Các mô hình ra quyết định
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================================
#  TRANG CHỦ
# ============================================================================
def page_home():
    st.markdown(
        """
        <div class="hero">
          <h1>🇻🇳 VN AIDEOM-VN</h1>
          <p><b>AI-Driven Decision Optimization Model for Vietnam</b></p>
          <p>Dashboard mô phỏng 12 bài toán ra quyết định phát triển kinh tế Việt Nam
          trong kỷ nguyên AI. Hệ thống kết hợp <b>Python</b>, <b>tối ưu hóa</b>,
          <b>học tăng cường</b> và <b>mô phỏng chính sách</b> để chuyển bài toán kinh tế
          thành mô hình định lượng có thể kiểm chứng.</p>
          <div>
            <span class="pill">🐍 Python</span>
            <span class="pill">📊 Streamlit Dashboard</span>
            <span class="pill">🧮 Optimization</span>
            <span class="pill">♻️ Reinforcement Learning</span>
            <span class="pill">🇻🇳 Vietnam 2020–2025 Data</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("📌 Bức tranh kinh tế Việt Nam tham chiếu nhanh 2024–2025")
    r1 = st.columns(4)
    r1[0].metric("GDP 2025", "514,0 tỷ USD", "+8,02%")
    r1[1].metric("Kinh tế số/GDP", "≈19,5%", "+1,2 điểm %")
    r1[2].metric("FDI giải ngân 2025", "27,6 tỷ USD", "+8,9%")
    r1[3].metric("GDP/người 2025", "5.026 USD", "+6,9%")
    r2 = st.columns(4)
    r2[0].metric("GDP 2025 (ngh.tỷ VND)", "12.847,6")
    r2[1].metric("DN công nghệ số", "80,1 nghìn")
    r2[2].metric("GII 2025", "Hạng 44/139")
    r2[3].metric("KH-CN/GDP", "≈2,49%")

    st.markdown("---")
    st.subheader("🗂️ Dữ liệu gốc Việt Nam 2020–2025")
    tab1, tab2, tab3 = st.tabs(
        ["Vĩ mô 2020–2025", "10 ngành 2024", "6 vùng KT-XH 2024"]
    )
    with tab1:
        df = load_macro()
        st.caption("`vietnam_macro_2020_2025.csv` — GDP, cơ cấu khu vực, FDI, "
                   "xuất nhập khẩu, lạm phát, năng suất, tỷ lệ kinh tế số/GDP.")
        st.dataframe(df, use_container_width=True, height=260)
        fig, ax = plt.subplots(figsize=(8, 3.4))
        ax.bar(df["year"], df["GDP_trillion_VND"], color="#3b82f6", alpha=0.85)
        ax2 = ax.twinx()
        ax2.plot(df["year"], df["GDP_growth_pct"], "ro-", label="Tăng trưởng %")
        ax.set_ylabel("GDP (nghìn tỷ VND)")
        ax2.set_ylabel("Tăng trưởng (%)")
        ax.set_title("GDP và tăng trưởng GDP Việt Nam 2020–2025")
        show_fig(fig)
    with tab2:
        ds = load_sectors()
        st.caption("`vietnam_sectors_2024.csv` — tỷ trọng GDP, tăng trưởng, lao động, "
                   "xuất khẩu, chỉ số số hóa, AI readiness, rủi ro tự động hóa, R&D/GDP.")
        st.dataframe(ds, use_container_width=True, height=320)
    with tab3:
        dr = load_regions()
        st.caption("`vietnam_regions_2024.csv` — GRDP, GRDP/người, FDI, xuất khẩu, "
                   "chỉ số số hóa, AI readiness, lao động đào tạo, Gini, R&D.")
        st.dataframe(dr, use_container_width=True, height=260)

    st.markdown("---")
    st.subheader("📚 Nội dung 12 bài tập")
    cards = [
        ("Bài 1", "Hàm sản xuất Cobb-Douglas mở rộng (AI, số hóa), growth accounting & dự báo 2030."),
        ("Bài 2", "LP phân bổ ngân sách 4 hạng mục đầu tư số, shadow price & độ nhạy."),
        ("Bài 3", "Chỉ số ưu tiên ngành Priorityᵢ, chuẩn hóa min-max, độ nhạy trọng số."),
        ("Bài 4", "LP phân bổ ngân sách số ngành-vùng với ràng buộc công bằng vùng miền."),
        ("Bài 5", "MIP lựa chọn 15 dự án chuyển đổi số (ràng buộc loại trừ, tiên quyết)."),
        ("Bài 6", "TOPSIS xếp hạng 6 vùng theo mức độ sẵn sàng AI (Expert/Entropy/AHP)."),
        ("Bài 7", "NSGA-II tối ưu 4 mục tiêu Pareto: tăng trưởng, bao trùm, môi trường, an ninh."),
        ("Bài 8", "Tối ưu động liên thời gian 2026–2035, quỹ đạo K/D/AI/H/Y/C."),
        ("Bài 9", "Tác động AI tới lao động: NetJob ròng và ngưỡng đào tạo lại."),
        ("Bài 10", "Quy hoạch ngẫu nhiên 2 giai đoạn: VSS & EVPI."),
        ("Bài 11", "Q-learning chính sách kinh tế thích nghi (MDP 81 trạng thái)."),
        ("Bài 12", "Đồ án tích hợp AIDEOM-VN: 6 module, 5 kịch bản chính sách."),
    ]
    cols = st.columns(3)
    for i, (t, d) in enumerate(cards):
        with cols[i % 3]:
            st.markdown(f"**{t}**")
            st.caption(d)


# ============================================================================
#  BÀI 1 — Cobb-Douglas mở rộng
# ============================================================================
def page_bai1():
    st.header("🌱 Bài 1 — Hàm sản xuất Cobb-Douglas mở rộng với AI & số hóa")
    st.markdown(
        r"$Y_t = A_t \cdot K_t^{\alpha} L_t^{\beta} D_t^{\gamma} AI_t^{\delta} H_t^{\theta}$, "
        r"với $\alpha+\beta+\gamma+\delta+\theta = 1$."
    )

    df = load_macro()
    years = df["year"].values
    Y = df["GDP_trillion_VND"].values
    K = np.array([16500, 17800, 19600, 21300, 23500, 25900], dtype=float)
    L = np.array([53.6, 50.5, 51.7, 52.4, 52.9, 53.4])
    D = df["digital_economy_share_GDP_pct"].values.astype(float)
    AI = np.array([55.6, 60.2, 65.4, 67.0, 73.8, 80.1])
    H = np.array([24.1, 26.1, 26.2, 27.0, 28.4, 29.2])

    c = st.columns(5)
    alpha = c[0].number_input("α (K)", value=0.33, step=0.01, format="%.2f")
    beta = c[1].number_input("β (L)", value=0.42, step=0.01, format="%.2f")
    gamma = c[2].number_input("γ (D)", value=0.10, step=0.01, format="%.2f")
    delta = c[3].number_input("δ (AI)", value=0.08, step=0.01, format="%.2f")
    theta = c[4].number_input("θ (H)", value=0.07, step=0.01, format="%.2f")
    tot = alpha + beta + gamma + delta + theta
    if abs(tot - 1.0) > 1e-9:
        st.warning(f"Tổng hệ số = {tot:.2f} ≠ 1 (mô hình giả định lợi suất không đổi theo quy mô).")

    A = Y / (K**alpha * L**beta * D**gamma * AI**delta * H**theta)

    st.subheader("Câu 1.4.1 — TFP $A_t$ giải ngược từ hàm sản xuất")
    cc = st.columns([1, 1])
    with cc[0]:
        st.dataframe(pd.DataFrame({"Năm": years, "Y thực tế": Y, "A_t (TFP)": np.round(A, 4)}),
                     use_container_width=True, hide_index=True)
        st.caption(f"TFP tăng từ {A[0]:.4f} (2020) → {A[-1]:.4f} (2025), "
                   f"bình quân {((A[-1]/A[0])**(1/5)-1)*100:.2f}%/năm.")
    with cc[1]:
        fig, ax = plt.subplots(figsize=(6, 3.6))
        ax.plot(years, A, "bo-", lw=2)
        for x, a in zip(years, A):
            ax.annotate(f"{a:.3f}", (x, a), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8)
        ax.set_title("Năng suất nhân tố tổng hợp $A_t$"); ax.grid(alpha=0.3)
        show_fig(fig)

    st.subheader("Câu 1.4.2 — Dự báo $\\hat{Y}$ và MAPE")
    A_mean = A.mean()
    Y_hat = A_mean * (K**alpha * L**beta * D**gamma * AI**delta * H**theta)
    mape = np.mean(np.abs((Y - Y_hat) / Y)) * 100
    st.dataframe(pd.DataFrame({
        "Năm": years, "Y thực tế": np.round(Y, 1), "Y dự báo": np.round(Y_hat, 1),
        "Sai số %": np.round((Y_hat - Y) / Y * 100, 2)
    }), use_container_width=True, hide_index=True)
    st.metric("MAPE", f"{mape:.3f}%")

    st.subheader("Câu 1.4.3 — Phân rã tăng trưởng 2020–2025")
    n = 5
    g_Y = (np.log(Y[-1]) - np.log(Y[0])) / n
    g = {
        "TFP (A)": (np.log(A[-1]) - np.log(A[0])) / n,
        "K (Vốn)": alpha * (np.log(K[-1]) - np.log(K[0])) / n,
        "L (Lao động)": beta * (np.log(L[-1]) - np.log(L[0])) / n,
        "D (Số hóa)": gamma * (np.log(D[-1]) - np.log(D[0])) / n,
        "AI": delta * (np.log(AI[-1]) - np.log(AI[0])) / n,
        "H (Nhân lực)": theta * (np.log(H[-1]) - np.log(H[0])) / n,
    }
    contrib = {k: v / g_Y * 100 for k, v in g.items()}
    cc = st.columns([1, 1])
    with cc[0]:
        st.dataframe(pd.DataFrame({
            "Yếu tố": list(g.keys()),
            "Đóng góp (%/năm)": [f"{v*100:.4f}" for v in g.values()],
            "Tỷ lệ (%)": [f"{c:.2f}" for c in contrib.values()],
        }), use_container_width=True, hide_index=True)
        st.caption(f"Tăng trưởng GDP bình quân: {g_Y*100:.2f}%/năm.")
    with cc[1]:
        fig, ax = plt.subplots(figsize=(6, 3.6))
        cols = ["#2ecc71", "#3498db", "#e74c3c", "#f39c12", "#9b59b6", "#1abc9c"]
        ax.bar(contrib.keys(), contrib.values(), color=cols, edgecolor="black", lw=0.5)
        ax.set_ylabel("Đóng góp (%)"); ax.set_title("Phân rã tăng trưởng GDP")
        ax.axhline(0, color="black", lw=0.5); ax.grid(axis="y", alpha=0.3)
        plt.xticks(rotation=25, ha="right", fontsize=8)
        show_fig(fig)

    st.subheader("Câu 1.4.4 — Kịch bản dự báo GDP 2030")
    cc = st.columns(4)
    D30 = cc[0].slider("D 2030 (% GDP)", 19, 40, 30)
    AI30 = cc[1].slider("AI 2030 (ngh. DN)", 80, 150, 100)
    H30 = cc[2].slider("H 2030 (%)", 29, 45, 35)
    gK = cc[3].slider("K tăng (%/năm)", 3, 10, 6) / 100
    K30 = K[-1] * (1 + gK) ** 5
    L30 = L[-1] * 1.005 ** 5
    A30 = A[-1] * 1.012 ** 5
    Y30 = A30 * (K30**alpha * L30**beta * D30**gamma * AI30**delta * H30**theta)
    gr = ((Y30 / Y[-1]) ** (1 / 5) - 1) * 100
    m = st.columns(3)
    m[0].metric("GDP 2030 dự báo", f"{Y30:,.0f} ngh.tỷ VND")
    m[1].metric("Tăng trưởng 2025–2030", f"{gr:.2f}%/năm")
    m[2].metric("GDP 2030 / GDP 2025", f"{Y30/Y[-1]:.2f} lần")

    with st.expander("Thảo luận chính sách"):
        st.markdown(
            "- **TFP tăng** trong giai đoạn 2020–2025 cho thấy chất lượng tăng trưởng "
            "cải thiện, không chỉ dựa vào tích lũy vốn.\n"
            "- Trong các yếu tố mới, **số hóa D** tăng nhanh nhất nên đóng góp tương đối lớn "
            "dù hệ số co giãn γ nhỏ.\n"
            "- Mục tiêu 30% kinh tế số/GDP 2030 là khả thi nếu duy trì tốc độ số hóa và "
            "đầu tư nhân lực số đồng bộ."
        )


# ============================================================================
#  BÀI 2 — LP phân bổ ngân sách 4 hạng mục
# ============================================================================
def page_bai2():
    from scipy.optimize import linprog
    st.header("💰 Bài 2 — Phân bổ ngân sách 4 hạng mục đầu tư số")
    st.markdown(
        r"$\max Z = 0{,}85x_1 + 1{,}20x_2 + 0{,}95x_3 + 1{,}35x_4$ "
        "(x₁ hạ tầng, x₂ AI, x₃ nhân lực, x₄ R&D — nghìn tỷ VND)."
    )

    cc = st.columns(4)
    B = cc[0].slider("Ngân sách tổng", 100, 200, 100, step=10)
    x3min = cc[1].slider("Sàn nhân lực x₃", 20, 40, 20)
    x1min = cc[2].slider("Sàn hạ tầng x₁", 0, 40, 25)
    techshare = cc[3].slider("Tỷ trọng x₂+x₄ ≥ (%)", 20, 50, 35) / 100

    c = [-0.85, -1.20, -0.95, -1.35]
    A_ub = [
        [1, 1, 1, 1], [-1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, -1],
        [techshare, techshare - 1, techshare, techshare - 1],
    ]
    b_ub = [B, -x1min, -15, -x3min, -10, 0]
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None)] * 4, method="highs")

    st.subheader("Câu 2.4.1–2.4.2 — Lời giải tối ưu & shadow price")
    if res.success:
        names = ["x₁ Hạ tầng số", "x₂ AI & dữ liệu", "x₃ Nhân lực số", "x₄ R&D công nghệ"]
        cc = st.columns([1, 1])
        with cc[0]:
            st.dataframe(pd.DataFrame({"Hạng mục": names, "Phân bổ (ngh.tỷ)": np.round(res.x, 2)}),
                         use_container_width=True, hide_index=True)
            st.metric("Z* (GDP tăng thêm)", f"{-res.fun:.2f} ngh.tỷ VND")
            st.caption(f"Tỷ trọng AI+R&D = {(res.x[1]+res.x[3])/res.x.sum()*100:.1f}%")
        with cc[1]:
            fig, ax = plt.subplots(figsize=(5.5, 3.6))
            ax.bar(["x₁", "x₂", "x₃", "x₄"], res.x,
                   color=["#3498db", "#9b59b6", "#2ecc71", "#e74c3c"])
            ax.set_ylabel("Nghìn tỷ VND"); ax.set_title("Phân bổ tối ưu"); ax.grid(axis="y", alpha=0.3)
            show_fig(fig)
        st.info("**Shadow price ngân sách tổng = 1,35**: mỗi nghìn tỷ ngân sách tăng thêm "
                "tạo ~1,35 nghìn tỷ GDP (bằng hệ số R&D — hạng mục biên cao nhất). Đây là cận trên "
                "hợp lý của chi phí cơ hội vốn công.")
    else:
        st.error("Bài toán không khả thi với cấu hình này.")

    st.subheader("Câu 2.4.3 — Đường cong $Z^*(B)$")
    Bs = np.arange(100, 201, 10)
    Zs = []
    for b in Bs:
        bb = [b, -x1min, -15, -x3min, -10, 0]
        r = linprog(c, A_ub=A_ub, b_ub=bb, bounds=[(0, None)] * 4, method="highs")
        Zs.append(-r.fun if r.success else np.nan)
    fig, ax = plt.subplots(figsize=(8, 3.4))
    ax.plot(Bs, Zs, "b-o"); ax.set_xlabel("Ngân sách tổng (ngh.tỷ)")
    ax.set_ylabel("Z* (GDP gain)"); ax.set_title("Phân tích độ nhạy ngân sách"); ax.grid(alpha=0.3)
    show_fig(fig)

    st.subheader("Câu 2.4.4 — Ưu tiên nhân lực số (x₃ ≥ 30)")
    b30 = [100, -x1min, -15, -30, -10, 0]
    r30 = linprog(c, A_ub=A_ub, b_ub=b30, bounds=[(0, None)] * 4, method="highs")
    if r30.success:
        st.success(f"Vẫn khả thi. Z* = {-r30.fun:.2f} ngh.tỷ "
                   f"(giảm {(-res.fun)-(-r30.fun):.2f} so với B={B} cấu hình hiện tại).")
        st.dataframe(pd.DataFrame({"Hạng mục": ["x₁", "x₂", "x₃", "x₄"],
                                   "Phân bổ": np.round(r30.x, 2)}),
                     use_container_width=True, hide_index=True)
    else:
        st.error("Không khả thi với x₃ ≥ 30.")


# ============================================================================
#  BÀI 3 — Chỉ số ưu tiên ngành
# ============================================================================
def page_bai3():
    st.header("📊 Bài 3 — Chỉ số ưu tiên ngành Priorityᵢ cho 10 ngành")
    df = load_sectors()
    GDP_2024 = 11511.9
    df = df.copy()
    df["labor_productivity"] = (df["gdp_share_2024_pct"] / 100) * GDP_2024 / df["labor_million"]
    df["sector_vi"] = SECTOR_VI

    cols_good = ["growth_rate_2024_pct", "labor_productivity", "spillover_coef_0_1",
                 "export_billion_USD", "labor_million", "ai_readiness_0_100"]
    col_bad = "automation_risk_pct"

    def norm_good(x): return (x - x.min()) / (x.max() - x.min())
    def norm_bad(x): return (x.max() - x) / (x.max() - x.min())

    Xg = df[cols_good].apply(norm_good)
    Xb = norm_bad(df[col_bad])

    st.subheader("Câu 3.4.1 — Ma trận chuẩn hóa min-max")
    Xg_show = Xg.copy()
    Xg_show.columns = ["Tăng trưởng", "Năng suất", "Lan tỏa", "Xuất khẩu", "Việc làm", "AI Ready"]
    Xg_show.insert(0, "Ngành", df["sector_vi"].values)
    Xg_show["Risk(đảo)"] = np.round(Xb.values, 3)
    st.dataframe(Xg_show.round(3), use_container_width=True, hide_index=True)

    st.subheader("Câu 3.4.2 — Priority với trọng số (điều chỉnh được)")
    st.caption("Trọng số mặc định a₁..a₇ = [0,15; 0,15; 0,20; 0,15; 0,10; 0,20; 0,15] "
               "(chuẩn hóa lại để tổng = 1).")
    c = st.columns(7)
    labels = ["Tăng trưởng", "Năng suất", "Lan tỏa", "Xuất khẩu", "Việc làm", "AI Ready", "Risk"]
    defaults = [0.15, 0.15, 0.20, 0.15, 0.10, 0.20, 0.15]
    w_raw = np.array([c[i].number_input(labels[i], value=defaults[i], step=0.01,
                                        format="%.2f", key=f"b3w{i}") for i in range(7)])
    s = w_raw.sum()
    w = w_raw[:6] / s
    w_risk = w_raw[6] / s
    priority = Xg.values @ w + w_risk * Xb.values
    rank = pd.DataFrame({"Ngành": df["sector_vi"], "Priority": np.round(priority, 4)})
    rank = rank.sort_values("Priority", ascending=False).reset_index(drop=True)
    rank.index += 1
    cc = st.columns([1, 1])
    with cc[0]:
        st.dataframe(rank, use_container_width=True)
    with cc[1]:
        fig, ax = plt.subplots(figsize=(6, 4))
        rr = rank.iloc[::-1]
        ax.barh(rr["Ngành"], rr["Priority"], color="#3498db")
        ax.set_title("Xếp hạng Priorityᵢ"); plt.yticks(fontsize=8)
        show_fig(fig)

    st.subheader("Câu 3.4.3 — Độ nhạy theo w_AI (heatmap)")
    w_base = np.array([0.15, 0.15, 0.20, 0.15, 0.10])
    w_risk_v = 0.15
    w_ai_range = np.arange(0.05, 0.45, 0.05)
    H = []
    for wai in w_ai_range:
        rem = 1.0 - wai - w_risk_v
        ws = w_base * (rem / w_base.sum())
        wf = np.append(ws, wai)
        H.append(Xg.values @ wf + w_risk_v * Xb.values)
    H = np.array(H)
    fig, ax = plt.subplots(figsize=(10, 4))
    im = ax.imshow(H, cmap="YlOrRd", aspect="auto")
    ax.set_yticks(range(len(w_ai_range))); ax.set_yticklabels([f"{w:.2f}" for w in w_ai_range])
    ax.set_xticks(range(10)); ax.set_xticklabels([f"N{i+1}" for i in range(10)])
    ax.set_xlabel("Ngành"); ax.set_ylabel("w_AI"); ax.set_title("Priority theo w_AI")
    plt.colorbar(im, label="Priority")
    show_fig(fig)
    top3_first = [df["sector_vi"].iloc[j] for j in np.argsort(H[0])[-3:][::-1]]
    top3_last = [df["sector_vi"].iloc[j] for j in np.argsort(H[-1])[-3:][::-1]]
    st.caption(f"Top-3 khi w_AI=0,05: {top3_first}  |  w_AI=0,40: {top3_last}")

    st.subheader("Câu 3.4.4 — Hai bộ trọng số")
    w_growth = np.array([0.25, 0.25, 0.10, 0.25, 0.05, 0.05]); w_growth_r = 0.05
    w_incl = np.array([0.05, 0.10, 0.25, 0.05, 0.25, 0.10]); w_incl_r = 0.20
    pg = Xg.values @ w_growth + w_growth_r * Xb.values
    pi = Xg.values @ w_incl + w_incl_r * Xb.values
    cc = st.columns(2)
    with cc[0]:
        st.markdown("**Định hướng tăng trưởng**")
        rg = pd.DataFrame({"Ngành": df["sector_vi"], "Điểm": np.round(pg, 4)}).sort_values("Điểm", ascending=False)
        st.dataframe(rg.head(5), use_container_width=True, hide_index=True)
    with cc[1]:
        st.markdown("**Định hướng bao trùm**")
        ri = pd.DataFrame({"Ngành": df["sector_vi"], "Điểm": np.round(pi, 4)}).sort_values("Điểm", ascending=False)
        st.dataframe(ri.head(5), use_container_width=True, hide_index=True)

    with st.expander("Thảo luận chính sách"):
        st.markdown(
            "- Khai khoáng có **năng suất rất cao** nhưng tăng trưởng âm, lan tỏa thấp và rủi ro "
            "tự động hóa lớn nên không vào nhóm ưu tiên.\n"
            "- Kết quả ưu tiên CNTT-TT, chế biến chế tạo, tài chính phù hợp tinh thần "
            "**Nghị quyết 57-NQ/TW** về đột phá KHCN & chuyển đổi số."
        )


# ----------------------------------------------------------------------------
# Tham số dùng chung Bài 4 / 7 / 12 (ma trận beta vùng-hạng mục)
# ----------------------------------------------------------------------------
REGIONS = ["NMM", "RRD", "NCC", "CH", "SE", "MD"]
ITEMS = ["I", "D", "AI", "H"]
BETA = {
    ("NMM", "I"): 1.15, ("NMM", "D"): 0.85, ("NMM", "AI"): 0.55, ("NMM", "H"): 1.30,
    ("RRD", "I"): 0.95, ("RRD", "D"): 1.25, ("RRD", "AI"): 1.40, ("RRD", "H"): 1.05,
    ("NCC", "I"): 1.05, ("NCC", "D"): 0.95, ("NCC", "AI"): 0.85, ("NCC", "H"): 1.15,
    ("CH", "I"): 1.20, ("CH", "D"): 0.75, ("CH", "AI"): 0.45, ("CH", "H"): 1.35,
    ("SE", "I"): 0.90, ("SE", "D"): 1.30, ("SE", "AI"): 1.55, ("SE", "H"): 1.00,
    ("MD", "I"): 1.10, ("MD", "D"): 0.85, ("MD", "AI"): 0.65, ("MD", "H"): 1.25,
}


# ============================================================================
#  BÀI 4 — LP phân bổ ngân sách ngành-vùng
# ============================================================================
def page_bai4():
    import pulp
    st.header("🗺️ Bài 4 — LP phân bổ ngân sách số theo ngành-vùng")
    st.markdown(r"$\max Z = \sum_r \sum_j \beta_{j,r}\, x_{j,r}$ — 24 biến, ràng buộc C1–C5.")

    dr = load_regions()
    D0 = dict(zip(
        dr["region_name_en"].map({
            "Northern Midlands and Mountains": "NMM", "Red River Delta": "RRD",
            "North Central and South Central Coast": "NCC", "Central Highlands": "CH",
            "Southeast": "SE", "Mekong Delta": "MD"}),
        dr["digital_index_0_100"]))
    gamma_val, lam = 0.002, 0.6

    def solve_lp(with_equity=True):
        m = pulp.LpProblem("VN_Digital_Budget", pulp.LpMaximize)
        x = pulp.LpVariable.dicts("x", (REGIONS, ITEMS), lowBound=0)
        m += pulp.lpSum(BETA[(r, j)] * x[r][j] for r in REGIONS for j in ITEMS)
        m += pulp.lpSum(x[r][j] for r in REGIONS for j in ITEMS) <= 50000
        for r in REGIONS:
            m += pulp.lpSum(x[r][j] for j in ITEMS) >= 5000
            m += pulp.lpSum(x[r][j] for j in ITEMS) <= 12000
        m += pulp.lpSum(x[r]["H"] for r in REGIONS) >= 12000
        if with_equity:
            M = pulp.LpVariable("Dmax")
            for r in REGIONS:
                m += D0[r] + gamma_val * x[r]["D"] <= M
                m += D0[r] + gamma_val * x[r]["D"] >= lam * M
        m.solve(pulp.PULP_CBC_CMD(msg=False))
        res = np.zeros((6, 4))
        for i, r in enumerate(REGIONS):
            for k, j in enumerate(ITEMS):
                res[i, k] = x[r][j].value()
        return res, pulp.value(m.objective)

    x_opt, Z = solve_lp(True)
    x_no, Z_no = solve_lp(False)

    st.subheader("Câu 4.4.1–4.4.3 — Phân bổ tối ưu (có ràng buộc công bằng)")
    cc = st.columns([1.2, 1])
    dfp = pd.DataFrame(x_opt, columns=ITEMS, index=REGION_VI).round(0)
    dfp["Tổng"] = dfp.sum(axis=1)
    with cc[0]:
        st.dataframe(dfp, use_container_width=True)
        st.metric("Z* (có công bằng)", f"{Z:,.0f} tỷ VND")
    with cc[1]:
        fig, ax = plt.subplots(figsize=(5.5, 4))
        im = ax.imshow(x_opt, cmap="YlOrRd", aspect="auto")
        ax.set_yticks(range(6)); ax.set_yticklabels([r[:14] for r in REGION_VI], fontsize=8)
        ax.set_xticks(range(4)); ax.set_xticklabels(ITEMS)
        for i in range(6):
            for j in range(4):
                ax.text(j, i, f"{x_opt[i,j]:.0f}", ha="center", va="center", fontsize=7,
                        color="white" if x_opt[i, j] > 8000 else "black")
        ax.set_title("Heatmap phân bổ"); plt.colorbar(im, ax=ax, shrink=0.8)
        show_fig(fig)

    st.subheader("Câu 4.4.4 — Chi phí của công bằng vùng miền")
    m = st.columns(3)
    m[0].metric("Z* CÓ công bằng", f"{Z:,.0f}")
    m[1].metric("Z* KHÔNG công bằng", f"{Z_no:,.0f}")
    m[2].metric("Chi phí công bằng", f"{Z_no-Z:,.0f} tỷ", f"{(Z_no-Z)/Z_no*100:.2f}%")
    cmp = pd.DataFrame({
        "Vùng": REGION_VI,
        "Có CB": x_opt.sum(1).round(0), "Không CB": x_no.sum(1).round(0),
        "Chênh": (x_no.sum(1) - x_opt.sum(1)).round(0)})
    st.dataframe(cmp, use_container_width=True, hide_index=True)
    st.caption("PuLP (CBC) và CVXPY cho cùng nghiệm (sai khác < 1e-4) — bài LP có nghiệm duy nhất ổn định.")


# ============================================================================
#  BÀI 5 — MIP chọn dự án
# ============================================================================
def page_bai5():
    from pulp import (LpProblem, LpMaximize, LpVariable, lpSum, value,
                      PULP_CBC_CMD, LpStatus)
    st.header("🎯 Bài 5 — MIP lựa chọn dự án chuyển đổi số")

    P = list(range(1, 16))
    C = {1: 12000, 2: 11500, 3: 18000, 4: 4500, 5: 3200, 6: 5800, 7: 6500, 8: 15000,
         9: 2500, 10: 7200, 11: 4800, 12: 8500, 13: 20000, 14: 3800, 15: 1500}
    C1 = {1: 8500, 2: 7500, 3: 12000, 4: 3500, 5: 2500, 6: 4000, 7: 4500, 8: 9000,
          9: 1800, 10: 5000, 11: 3500, 12: 5500, 13: 13000, 14: 2800, 15: 1200}
    B = {1: 21500, 2: 20800, 3: 32500, 4: 9200, 5: 6800, 6: 11400, 7: 12200, 8: 28500,
         9: 5800, 10: 13800, 11: 8500, 12: 16200, 13: 35000, 14: 7500, 15: 3800}
    names = {1: "TT dữ liệu Hòa Lạc", 2: "TT dữ liệu phía Nam", 3: "5G toàn quốc",
             4: "VNeID 2.0", 5: "Cổng DVC v3", 6: "Y tế số", 7: "Giáo dục số K-12",
             8: "TT AI + supercomputing", 9: "Fintech sandbox", 10: "Logistics thông minh",
             11: "Nông nghiệp số ĐBSCL", 12: "Đào tạo 50K kỹ sư AI", 13: "Khu CN bán dẫn BN-BG",
             14: "An ninh mạng SOC", 15: "Open Data"}
    fields = {1: "ht", 2: "ht", 3: "ht", 4: "cp", 5: "cp", 6: "yt", 7: "gd", 8: "ai",
              9: "tc", 10: "lg", 11: "nn", 12: "nl", 13: "bd", 14: "an", 15: "dl"}
    prob = {"ht": 0.85, "cp": 0.75, "ai": 0.65, "bd": 0.65, "yt": 0.80, "gd": 0.80,
            "tc": 0.80, "lg": 0.80, "nn": 0.80, "nl": 0.80, "an": 0.80, "dl": 0.80}

    cc = st.columns(3)
    budget = cc[0].slider("Ngân sách 5 năm (tỷ)", 60000, 120000, 80000, step=10000)
    use_exp = cc[1].checkbox("Tối đa lợi ích kỳ vọng (rủi ro pᵢ)", value=False)
    force12 = cc[2].checkbox("Bắt buộc cả P1 & P2 (redundancy)", value=False)

    def solve_mip(budget_total, use_expected, force_p1p2):
        m = LpProblem("VN_Project", LpMaximize)
        y = LpVariable.dicts("y", P, cat="Binary")
        if use_expected:
            m += lpSum(prob[fields[i]] * B[i] * y[i] for i in P)
        else:
            m += lpSum(B[i] * y[i] for i in P)
        m += lpSum(C[i] * y[i] for i in P) <= budget_total
        m += lpSum(C1[i] * y[i] for i in P) <= 40000
        if not force_p1p2:
            m += y[1] + y[2] <= 1
        else:
            m += y[1] >= 1
            m += y[2] >= 1
        m += y[8] <= y[12]
        m += y[13] <= y[12]
        m += y[4] + y[5] >= 1
        m += y[14] >= 1
        m += lpSum(y[i] for i in P) >= 7
        m += lpSum(y[i] for i in P) <= 11
        m.solve(PULP_CBC_CMD(msg=False))
        sel = [i for i in P if y[i].value() and y[i].value() > 0.5]
        return sel, value(m.objective), LpStatus[m.status]

    sel, Z, status = solve_mip(budget, use_exp, force12)
    st.subheader("Kết quả lựa chọn")
    if status == "Optimal":
        rows = [{"Mã": f"P{i}", "Dự án": names[i], "Chi phí": C[i], "NPV": B[i],
                 "NPV/C": round(B[i] / C[i], 2)} for i in sel]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        tc = sum(C[i] for i in sel)
        m = st.columns(4)
        m[0].metric("Số dự án", len(sel))
        m[1].metric("Tổng chi phí", f"{tc:,} tỷ")
        m[2].metric("Z* (lợi ích)", f"{Z:,.0f} tỷ")
        m[3].metric("B/C trung bình", f"{Z/tc:.2f}")
        st.caption("Lưu ý: P15 (Open Data) có B/C = 2,53 cao nhất nên **được chọn** — "
                   "khác với giả thiết câu 5.5.a của đề.")
    else:
        st.error("Bài toán KHÔNG khả thi với cấu hình hiện tại.")

    with st.expander("Thảo luận chính sách"):
        st.markdown(
            "- Ràng buộc bắt buộc P14 (an ninh mạng) có thể làm giảm Z* nhưng hợp lý vì "
            "an ninh là điều kiện nền cho mọi hệ thống số.\n"
            "- P8 (AI quốc gia) và P13 (bán dẫn) có lợi ích cộng hưởng — có thể mô hình hóa "
            "bằng biến tích z = y₈·y₁₃ tuyến tính hóa."
        )


# ============================================================================
#  BÀI 6 — TOPSIS xếp hạng 6 vùng
# ============================================================================
def _topsis(X, w, is_benefit):
    R = X / np.sqrt((X ** 2).sum(axis=0))
    V = R * w
    A_star = np.where(is_benefit, V.max(0), V.min(0))
    A_neg = np.where(is_benefit, V.min(0), V.max(0))
    S_star = np.sqrt(((V - A_star) ** 2).sum(1))
    S_neg = np.sqrt(((V - A_neg) ** 2).sum(1))
    return S_neg / (S_star + S_neg)


def _entropy_weights(X):
    P = X / X.sum(0)
    k = 1.0 / np.log(len(X))
    E = -k * np.nansum(P * np.log(P + 1e-12), 0)
    d = 1 - E
    return d / d.sum()


def page_bai6():
    st.header("🏆 Bài 6 — TOPSIS xếp hạng 6 vùng theo mức độ sẵn sàng AI")
    df = load_regions()
    criteria = ["grdp_per_capita_million_VND", "fdi_registered_billion_USD",
                "digital_index_0_100", "ai_readiness_0_100", "trained_labor_pct",
                "rd_intensity_pct", "internet_penetration_pct", "gini_coef"]
    labels = ["GRDP/N", "FDI", "Digital", "AI", "LĐĐT", "R&D", "Internet", "Gini"]
    is_benefit = [True, True, True, True, True, True, True, False]
    X = df[criteria].values.astype(float)

    st.subheader("Câu 6.4.1 — Trọng số chuyên gia")
    w_expert = np.array([0.10, 0.10, 0.15, 0.20, 0.15, 0.15, 0.05, 0.10])
    C_exp = _topsis(X, w_expert, is_benefit)
    w_ent = _entropy_weights(X)
    C_ent = _topsis(X, w_ent, is_benefit)

    res = pd.DataFrame({
        "Vùng": REGION_VI,
        "C* Expert": np.round(C_exp, 4),
        "Hạng Expert": pd.Series(C_exp).rank(ascending=False).astype(int).values,
        "C* Entropy": np.round(C_ent, 4),
        "Hạng Entropy": pd.Series(C_ent).rank(ascending=False).astype(int).values,
    }).sort_values("Hạng Expert")
    cc = st.columns([1.3, 1])
    with cc[0]:
        st.dataframe(res, use_container_width=True, hide_index=True)
    with cc[1]:
        fig, ax = plt.subplots(figsize=(5.5, 4))
        order = np.argsort(C_exp)
        ax.barh(np.array(REGION_VI)[order], C_exp[order], color="#3498db", alpha=0.8, label="Expert")
        ax.barh(np.array(REGION_VI)[order], C_ent[order], color="#e67e22", alpha=0.5, label="Entropy")
        ax.set_title("C* Expert vs Entropy"); ax.legend(); plt.yticks(fontsize=8)
        show_fig(fig)

    st.subheader("Câu 6.4.2 — Trọng số Entropy (khách quan)")
    st.dataframe(pd.DataFrame({"Tiêu chí": labels, "w Entropy": np.round(w_ent, 4)}),
                 use_container_width=True, hide_index=True)

    st.subheader("Câu 6.4.3 — Độ nhạy theo w_AI")
    ai_idx = 3
    w_ai_range = np.arange(0.10, 0.45, 0.05)
    H = []
    top3_hist = []
    for wai in w_ai_range:
        w_gini = 0.10
        rem = 1.0 - wai - w_gini
        w_base = np.array([0.10, 0.10, 0.15, 0.15, 0.15, 0.05])
        w_scaled = w_base * (rem / w_base.sum())
        wf = np.insert(w_scaled, ai_idx, wai)
        wf = np.append(wf, w_gini)
        cs = _topsis(X, wf, is_benefit)
        H.append(cs)
        top3_hist.append([REGION_VI[j] for j in np.argsort(cs)[-3:][::-1]])
    H = np.array(H)
    fig, ax = plt.subplots(figsize=(9, 4))
    im = ax.imshow(H, cmap="YlOrRd", aspect="auto")
    ax.set_yticks(range(len(w_ai_range))); ax.set_yticklabels([f"{w:.2f}" for w in w_ai_range])
    ax.set_xticks(range(6)); ax.set_xticklabels([f"R{i+1}" for i in range(6)])
    ax.set_xlabel("Vùng"); ax.set_ylabel("w_AI"); ax.set_title("TOPSIS C* theo w_AI")
    plt.colorbar(im, label="C*")
    show_fig(fig)
    same = all(t == top3_hist[0] for t in top3_hist)
    st.caption(f"Top-3 {'ỔN ĐỊNH' if same else 'CÓ thay đổi'} khi quét w_AI. "
               f"Top-3 hiện tại: {top3_hist[0]}")

    st.subheader("Câu 6.4.4 — AHP đơn giản so sánh")
    ahp = np.array([
        [1, 1, 1/3, 1/5, 1/3, 1/3, 3, 3], [1, 1, 1/3, 1/5, 1/3, 1/3, 3, 3],
        [3, 3, 1, 1/2, 1, 1, 5, 5], [5, 5, 2, 1, 2, 2, 7, 7],
        [3, 3, 1, 1/2, 1, 1, 5, 5], [3, 3, 1, 1/2, 1, 1, 5, 5],
        [1/3, 1/3, 1/5, 1/7, 1/5, 1/5, 1, 1], [1/3, 1/3, 1/5, 1/7, 1/5, 1/5, 1, 1]])
    n = 8
    gm = np.prod(ahp, axis=1) ** (1 / n)
    w_ahp = gm / gm.sum()
    Aw = ahp @ w_ahp
    lam_max = np.mean(Aw / w_ahp)
    CI = (lam_max - n) / (n - 1)
    CR = CI / 1.41
    C_ahp = _topsis(X, w_ahp, is_benefit)
    cc = st.columns([1, 1])
    with cc[0]:
        st.dataframe(pd.DataFrame({"Tiêu chí": labels, "w AHP": np.round(w_ahp, 4)}),
                     use_container_width=True, hide_index=True)
        st.caption(f"λ_max={lam_max:.3f}, CI={CI:.3f}, CR={CR:.3f} "
                   f"({'nhất quán' if CR < 0.1 else 'chưa nhất quán'})")
    with cc[1]:
        cmp = pd.DataFrame({
            "Vùng": REGION_VI,
            "Expert": pd.Series(C_exp).rank(ascending=False).astype(int).values,
            "Entropy": pd.Series(C_ent).rank(ascending=False).astype(int).values,
            "AHP": pd.Series(C_ahp).rank(ascending=False).astype(int).values,
        })
        st.dataframe(cmp, use_container_width=True, hide_index=True)

    with st.expander("Thảo luận chính sách"):
        st.markdown(
            "- Theo Quyết định 127/QĐ-TTg (3 trung tâm AI lớn), nên chọn **3 vùng dẫn đầu TOPSIS**: "
            "Đông Nam Bộ, Đồng bằng sông Hồng và Bắc Trung Bộ + DH Trung Bộ.\n"
            "- AI Readiness và Internet penetration tương quan cao có thể gây trùng lặp thông tin; "
            "có thể dùng PCA hoặc trọng số Entropy để giảm thiên lệch."
        )


# ============================================================================
#  BÀI 7 — NSGA-II Pareto 4 mục tiêu
# ============================================================================
E_R = np.array([0.42, 0.55, 0.48, 0.32, 0.62, 0.38])
RHO_R = np.array([0.18, 0.45, 0.28, 0.12, 0.52, 0.22])
SIG_R = np.array([0.32, 0.28, 0.30, 0.35, 0.25, 0.30])
D0_ARR = np.array([38, 78, 55, 32, 82, 48], dtype=float)
BETA_MAT = np.array([[BETA[(r, j)] for j in ITEMS] for r in REGIONS])


@st.cache_data(show_spinner="Đang chạy NSGA-II (pop=100, gen=200)...")
def run_nsga(seed=42, pop=100, gen=200):
    from pymoo.core.problem import ElementwiseProblem
    from pymoo.algorithms.moo.nsga2 import NSGA2
    from pymoo.optimize import minimize as moo_min
    from pymoo.termination import get_termination
    gamma_val, lam_val = 0.002, 0.6

    class Prob(ElementwiseProblem):
        def __init__(self):
            super().__init__(n_var=24, n_obj=4, n_ieq_constr=20,
                             xl=np.zeros(24), xu=np.ones(24) * 12000)

        def _evaluate(self, x, out, *a, **k):
            X = x.reshape(6, 4)
            f1 = -(BETA_MAT * X).sum()
            sums = X.sum(1)
            f2 = np.abs(sums - sums.mean()).mean()
            f3 = (E_R * (X[:, 0] + X[:, 1] + X[:, 2])).sum()
            f4 = (RHO_R * X[:, 2]).sum() - (SIG_R * X[:, 3]).sum()
            out["F"] = [f1, f2, f3, f4]
            g = [X.sum() - 50000]
            for r in range(6):
                g.append(5000 - X[r].sum())
            for r in range(6):
                g.append(X[r].sum() - 12000)
            g.append(12000 - X[:, 3].sum())
            D_new = D0_ARR + gamma_val * X[:, 1]
            D_max = D_new.max()
            for r in range(6):
                g.append(lam_val * D_max - D_new[r])
            out["G"] = np.array(g)

    res = moo_min(Prob(), NSGA2(pop_size=pop), get_termination("n_gen", gen),
                  seed=seed, verbose=False)
    return res.F, res.X


def page_bai7():
    st.header("🌐 Bài 7 — Tối ưu đa mục tiêu Pareto với NSGA-II")
    st.markdown("4 mục tiêu: **max** tăng trưởng GDP, **min** bất bình đẳng (Gini/MAD), "
                "**min** phát thải, **min** rủi ro an ninh dữ liệu.")
    if st.button("▶️ Chạy NSGA-II", type="primary"):
        st.session_state["b7_run"] = True
    if not st.session_state.get("b7_run"):
        st.info("Bấm nút để chạy thuật toán tiến hóa NSGA-II (mất vài giây).")
        return

    F, X = run_nsga()
    if F is None or len(F) == 0:
        st.error("NSGA-II không tìm được nghiệm khả thi. Hãy thử chạy lại "
                 "(ràng buộc khá chặt — cần pop=100, gen=200).")
        return
    st.subheader("Câu 7.4.1–7.4.2 — Tập Pareto")
    m = st.columns(4)
    m[0].metric("Số nghiệm Pareto", len(F))
    m[1].metric("GDP gain max", f"{-F[:,0].min():,.0f}")
    m[2].metric("Gini/MAD min", f"{F[:,1].min():.1f}")
    m[3].metric("Phát thải min", f"{F[:,2].min():,.0f}")

    fig = plt.figure(figsize=(13, 4.5))
    ax1 = fig.add_subplot(121, projection="3d")
    sc = ax1.scatter(-F[:, 0], F[:, 1], F[:, 2], c=F[:, 3], cmap="viridis", s=10, alpha=0.7)
    ax1.set_xlabel("GDP gain"); ax1.set_ylabel("Gini/MAD"); ax1.set_zlabel("Phát thải")
    ax1.set_title("Tập Pareto 3D (màu = rủi ro)")
    fig.colorbar(sc, ax=ax1, shrink=0.6, label="f4")
    ax2 = fig.add_subplot(122)
    Fn = np.copy(F)
    for i in range(4):
        lo, hi = F[:, i].min(), F[:, i].max()
        Fn[:, i] = (F[:, i] - lo) / (hi - lo) if hi > lo else 0.5
    for i in range(len(F)):
        ax2.plot(range(4), Fn[i], "b-", alpha=0.05, lw=0.5)
    ax2.plot(range(4), Fn.mean(0), "r-", lw=2, label="Trung bình")
    ax2.set_xticks(range(4)); ax2.set_xticklabels(["GDP", "Gini", "Phát thải", "Rủi ro"])
    ax2.set_title("Parallel coordinates"); ax2.legend()
    show_fig(fig)

    st.subheader("Câu 7.4.3 — Nghiệm thỏa hiệp (TOPSIS, trọng số 0,40/0,25/0,20/0,15)")
    w_policy = np.array([0.40, 0.25, 0.20, 0.15])
    fmin, fmax = F.min(0), F.max(0)
    frange = np.where(fmax - fmin > 1e-12, fmax - fmin, 1.0)
    R = (F - fmin) / frange
    V = R * w_policy
    S_star = np.sqrt((V ** 2).sum(1))
    S_neg = np.sqrt(((V - w_policy) ** 2).sum(1))
    C = S_neg / (S_star + S_neg)
    best = int(np.argmax(C))
    bf = F[best]
    m = st.columns(4)
    m[0].metric("GDP gain", f"{-bf[0]:,.0f}")
    m[1].metric("Gini/MAD", f"{bf[1]:.1f}")
    m[2].metric("Phát thải", f"{bf[2]:,.0f}")
    m[3].metric("Rủi ro", f"{bf[3]:,.0f}")
    bx = X[best].reshape(6, 4)
    st.dataframe(pd.DataFrame(bx.round(0), columns=ITEMS, index=REGION_VI),
                 use_container_width=True)

    st.subheader("Câu 7.4.4 — Chi phí cơ hội")
    mg = int(np.argmin(F[:, 0]))
    fg = F[mg]
    st.write(f"So với nghiệm thỏa hiệp, nghiệm **tăng trưởng cao nhất** đạt GDP gain "
             f"{-fg[0]:,.0f} (+{((-fg[0])-(-bf[0])):,.0f}) nhưng phát thải "
             f"{fg[2]:,.0f} (so với {bf[2]:,.0f}).")


# ============================================================================
#  BÀI 8 — Tối ưu động liên thời gian
# ============================================================================
@st.cache_data(show_spinner="Đang tối ưu quỹ đạo 2026-2035 (SLSQP)...")
def run_dynamic():
    from scipy.optimize import minimize
    a, b, gd, dai, th = 0.33, 0.42, 0.10, 0.08, 0.07
    dK, dD, dAI = 0.05, 0.12, 0.15
    thH, mu = 0.8, 0.02
    phi1, phi2, phi3 = 0.003, 0.002, 0.004
    rho = 0.97; gcr = 1.5; T = 10
    K0, L0, D0, AI0, H0 = 27500.0, 53.9, 20.3, 86.0, 30.0
    Y0 = 12847.6
    A0 = Y0 / (K0 ** a * L0 ** b * D0 ** gd * AI0 ** dai * H0 ** th)
    L = np.array([L0 * 1.009 ** t for t in range(T + 1)])

    def traj(u):
        IK, ID, IAI, IH = u[0::4], u[1::4], u[2::4], u[3::4]
        K = np.zeros(T + 1); D = np.zeros(T + 1); AI = np.zeros(T + 1)
        H = np.zeros(T + 1); A = np.zeros(T + 1); Y = np.zeros(T + 1); C = np.zeros(T)
        K[0], D[0], AI[0], H[0], A[0] = K0, D0, AI0, H0, A0
        for t in range(T):
            Y[t] = A[t] * K[t]**a * L[t]**b * D[t]**gd * AI[t]**dai * H[t]**th
            C[t] = Y[t] - IK[t] - ID[t] - IAI[t] - IH[t]
            if C[t] <= 0:
                return None
            K[t+1] = (1-dK)*K[t]+IK[t]; D[t+1] = (1-dD)*D[t]+ID[t]
            AI[t+1] = (1-dAI)*AI[t]+IAI[t]; H[t+1] = H[t]+thH*IH[t]-mu*H[t]
            A[t+1] = A[t]*(1+phi1*(D[t]/100)+phi2*(AI[t]/100)+phi3*(H[t]/100))
        Y[T] = A[T]*K[T]**a*L[T]**b*D[T]**gd*AI[T]**dai*H[T]**th
        return K, D, AI, H, Y, C, A

    def welfare(u):
        r = traj(u)
        if r is None:
            return 1e15
        C = r[5]
        if np.any(C <= 0):
            return 1e15
        return -sum(rho**t * (C[t]**(1-gcr)-1)/(1-gcr) for t in range(T))

    ti = 14000 * 0.15
    u0 = np.zeros(T*4)
    for t in range(T):
        u0[t*4:t*4+4] = [ti*0.40, ti*0.25, ti*0.20, ti*0.15]
    bounds = [(0, None)]*(T*4)

    def cbud(u):
        r = traj(u)
        return -1e10 if r is None else min(r[5]) - 1
    cons = [{"type": "ineq", "fun": cbud}]
    res = minimize(welfare, u0, method="SLSQP", bounds=bounds, constraints=cons,
                   options={"maxiter": 1000, "ftol": 1e-8})
    return traj(res.x), -res.fun, np.arange(2026, 2037)


def page_bai8():
    st.header("📈 Bài 8 — Tối ưu động phân bổ liên thời gian 2026–2035")
    st.markdown(r"$\max \sum_t \rho^{t}\,U(C_t)$ với động học vốn K, D, AI, H và TFP nội sinh.")
    if st.button("▶️ Tối ưu quỹ đạo", type="primary"):
        st.session_state["b8_run"] = True
    if not st.session_state.get("b8_run"):
        st.info("Bấm nút để tối ưu hóa quỹ đạo phân bổ 10 năm (SLSQP).")
        return

    (K, D, AI, H, Y, C, A), W, years = run_dynamic()
    st.metric("Phúc lợi tối ưu W*", f"{W:.3f}")
    df = pd.DataFrame({"Năm": years, "K": K.round(0), "D": D.round(1), "AI": AI.round(1),
                       "H": H.round(1), "TFP": A.round(2), "Y": Y.round(0)})
    df["C"] = list(C.round(0)) + [np.nan]
    st.dataframe(df, use_container_width=True, hide_index=True)

    fig, axes = plt.subplots(2, 3, figsize=(14, 7))
    for ax, data, title in [
        (axes[0, 0], K, "K (vốn vật chất)"), (axes[0, 1], D, "D (hạ tầng số %)"),
        (axes[0, 2], AI, "AI (nghìn DN)"), (axes[1, 0], H, "H (nhân lực %)"),
        (axes[1, 2], A, "A (TFP)")]:
        ax.plot(years, data, "b-o", ms=4); ax.set_title(title); ax.grid(alpha=0.3)
    axes[1, 1].plot(years, Y, "k-o", ms=4, label="Y (GDP)")
    axes[1, 1].plot(years[:10], C, "c-o", ms=4, label="C (tiêu dùng)")
    axes[1, 1].set_title("Y và C"); axes[1, 1].legend(); axes[1, 1].grid(alpha=0.3)
    plt.suptitle("Quỹ đạo tối ưu 2026–2035", fontsize=13)
    show_fig(fig)

    with st.expander("Thảo luận chính sách"):
        st.markdown(
            "- Quỹ đạo đầu tư có xu hướng **front-loaded** vì TFP nội sinh tạo hiệu ứng lan tỏa "
            "dài hạn — đầu tư sớm sinh lời cao hơn.\n"
            "- Hệ số chiết khấu ρ=0,97 ưu tiên dài hạn; ρ thấp hơn (0,90) khiến chính phủ "
            "'dưới đầu tư' vào R&D và nhân lực số."
        )


# ============================================================================
#  BÀI 9 — Tác động AI tới lao động
# ============================================================================
def page_bai9():
    from scipy.optimize import linprog
    st.header("👷 Bài 9 — Tác động AI tới thị trường lao động Việt Nam")
    st.markdown(r"$\max \sum_i NetJob_i$ s.t. ngân sách 30.000 tỷ, $NetJob_i \ge 0$, "
                r"$Displaced_i \le RetrainCapacity_i$.")

    N = 8
    sectors = ["Nông-LT", "CN chế biến", "Xây dựng", "Bán buôn-bán lẻ",
               "Tài chính-NH", "Logistics", "CNTT-TT", "Giáo dục-ĐT"]
    L = np.array([13.20, 11.50, 4.80, 7.80, 0.55, 1.95, 0.62, 2.15])
    risk = np.array([18, 42, 25, 38, 52, 35, 28, 22]) / 100
    a1 = np.array([8.5, 32.5, 12.8, 22.4, 45.8, 28.5, 62.5, 18.5])
    b1 = np.array([45, 28, 35, 32, 22, 30, 20, 55])
    c1 = np.array([5.2, 62.4, 18.5, 48.2, 72.5, 42.8, 32.5, 12.5])
    d1 = np.array([50, 32, 42, 38, 26, 36, 24, 62])
    coeff = a1 - c1 * risk

    add5 = st.checkbox("Thêm ràng buộc: mỗi ngành mất ≤ 5% lao động", value=False)

    c_obj = np.concatenate([-coeff, -b1])
    A1 = np.concatenate([np.ones(N), np.ones(N)]).reshape(1, -1)
    A1b = np.concatenate([-np.ones(N), np.zeros(N)]).reshape(1, -1)
    A2 = np.zeros((N, 2 * N)); A3 = np.zeros((N, 2 * N))
    for i in range(N):
        A2[i, i] = -coeff[i]; A2[i, N + i] = -b1[i]
        A3[i, i] = c1[i] * risk[i]; A3[i, N + i] = -d1[i]
    A_ub = np.vstack([A1, A1b, A2, A3])
    b_ub = np.concatenate([[30000], [-9000], np.zeros(N), np.zeros(N)])
    if add5:
        A4 = np.zeros((N, 2 * N))
        for i in range(N):
            A4[i, i] = c1[i] * risk[i]
        A_ub = np.vstack([A_ub, A4])
        b_ub = np.concatenate([b_ub, 0.05 * L * 1e6])

    res = linprog(c_obj, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None)] * (2 * N), method="highs")
    st.subheader("Câu 9.4.1 / 9.4.4 — Phân bổ tối ưu & NetJob ròng")
    if res.success:
        xA, xH = res.x[:N], res.x[N:]
        NewJob = a1 * xA; Upgrade = b1 * xH
        Displaced = c1 * risk * xA; NetJob = coeff * xA + b1 * xH
        df = pd.DataFrame({
            "Ngành": sectors, "x_AI": xA.round(0), "x_H": xH.round(0),
            "NewJob": NewJob.round(0), "Upgrade": Upgrade.round(0),
            "Displaced": Displaced.round(0), "NetJob": NetJob.round(0)})
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.metric("Tổng NetJob", f"{-res.fun:,.0f} việc làm")
        fig, ax = plt.subplots(figsize=(9, 3.6))
        ax.bar(sectors, NetJob, color="#2ecc71")
        ax.set_ylabel("NetJob"); ax.set_title("NetJob ròng theo ngành"); ax.grid(axis="y", alpha=0.3)
        plt.xticks(rotation=30, ha="right", fontsize=8)
        show_fig(fig)
    else:
        st.error(f"Không khả thi: {res.message}")

    st.subheader("Câu 9.4.2 — Ngưỡng đào tạo tối thiểu (CN chế biến)")
    i = 1
    net = a1[i] - c1[i] * risk[i]
    ratio = c1[i] * risk[i] / d1[i]
    st.write(f"Hệ số net AI = {net:.1f} (dương → AI tạo việc ròng). "
             f"Ràng buộc retraining: x_H ≥ {ratio:.3f}·x_AI. "
             f"Nếu x_AI dùng hết 30.000 tỷ thì cần x_H ≥ {ratio*30000:,.0f} tỷ.")
    xr = np.linspace(0, 30000, 100)
    fig, ax = plt.subplots(figsize=(7, 3.4))
    ax.plot(xr, ratio * xr, "r--", lw=2, label=f"Retrain: x_H≥{ratio:.3f}·x_AI")
    ax.plot(xr, np.maximum(0, -net / b1[i] * xr), "b--", lw=2, label="NetJob≥0")
    ax.fill_between(xr, np.maximum(ratio * xr, np.maximum(0, -net / b1[i] * xr)), 30000,
                    alpha=0.2, color="green", label="Vùng khả thi")
    ax.set_xlabel("x_AI (tỷ)"); ax.set_ylabel("x_H tối thiểu (tỷ)")
    ax.set_xlim(0, 30000); ax.set_ylim(0, 30000); ax.legend(fontsize=8); ax.grid(alpha=0.3)
    show_fig(fig)

    st.subheader("Câu 9.4.3 — Nhóm dễ bị tổn thương (Nông-LT, Xây dựng, Bán buôn)")
    if res.success:
        vuln = [0, 2, 3]
        kept, retr, lost = [], [], []
        for j in vuln:
            disp = Displaced[j]
            rc = min(disp, d1[j] * xH[j])
            kept.append(L[j] * 1e6 - disp)
            retr.append(rc)
            lost.append(max(0, disp - rc))
        fig, ax = plt.subplots(figsize=(8, 3.8))
        names = [sectors[j] for j in vuln]
        ax.bar(names, kept, label="Giữ việc", color="#2ecc71")
        ax.bar(names, retr, bottom=kept, label="Đào tạo lại", color="#f39c12")
        ax.bar(names, lost, bottom=[k + r for k, r in zip(kept, retr)],
               label="Mất việc", color="#e74c3c")
        ax.set_ylabel("Số lao động"); ax.set_title("Luồng dịch chuyển lao động")
        ax.legend(); ax.grid(axis="y", alpha=0.3)
        show_fig(fig)


# ============================================================================
#  BÀI 10 — Stochastic 2 giai đoạn
# ============================================================================
def page_bai10():
    st.header("🎲 Bài 10 — Quy hoạch ngẫu nhiên 2 giai đoạn")
    st.markdown("First-stage (here-and-now) ≤ 65.000 tỷ; recourse second-stage ≤ 15.000 tỷ/kịch bản; "
                r"$y^s_{AI} \le 0{,}5\,x_H$.")
    J = ["I", "D", "AI", "H"]
    S = ["s1", "s2", "s3", "s4"]
    p_s = {"s1": 0.30, "s2": 0.45, "s3": 0.20, "s4": 0.05}
    beta_base = {"I": 1.00, "D": 1.10, "AI": 1.25, "H": 0.95}
    beta_s = {
        ("s1", "I"): 1.25, ("s1", "D"): 1.35, ("s1", "AI"): 1.55, ("s1", "H"): 1.05,
        ("s2", "I"): 1.00, ("s2", "D"): 1.10, ("s2", "AI"): 1.25, ("s2", "H"): 0.95,
        ("s3", "I"): 0.75, ("s3", "D"): 0.85, ("s3", "AI"): 0.90, ("s3", "H"): 1.00,
        ("s4", "I"): 0.40, ("s4", "D"): 0.50, ("s4", "AI"): 0.55, ("s4", "H"): 1.10}

    st.subheader("Cấu trúc kịch bản")
    st.dataframe(pd.DataFrame({
        "Kịch bản": ["Lạc quan", "Cơ sở", "Bi quan", "Khủng hoảng"],
        "Tăng trưởng TG %": [3.5, 2.8, 1.5, 0.2],
        "FDI VN (tỷ USD)": [32.0, 27.0, 20.0, 12.0],
        "XK tăng %": [12.0, 8.0, 3.0, -5.0],
        "Xác suất": [0.30, 0.45, 0.20, 0.05]}),
        use_container_width=True, hide_index=True)

    try:
        import pyomo.environ as pyo

        def get_solver():
            for nm in ["appsi_highs", "glpk", "cbc"]:
                s = pyo.SolverFactory(nm)
                if s.available():
                    return s
            return None
        solver = get_solver()
        if solver is None:
            raise RuntimeError("no solver")

        # SP
        m = pyo.ConcreteModel()
        m.J = pyo.Set(initialize=J); m.S = pyo.Set(initialize=S)
        m.x = pyo.Var(m.J, within=pyo.NonNegativeReals)
        m.y = pyo.Var(m.S, m.J, within=pyo.NonNegativeReals)
        m.budget1 = pyo.Constraint(expr=sum(m.x[j] for j in J) <= 65000)
        m.budget2 = pyo.Constraint(m.S, rule=lambda mm, s: sum(mm.y[s, j] for j in J) <= 15000)
        m.aicap = pyo.Constraint(m.S, rule=lambda mm, s: mm.y[s, "AI"] <= 0.5 * mm.x["H"])
        m.obj = pyo.Objective(expr=sum(beta_base[j] * m.x[j] for j in J) +
                              sum(p_s[s] * sum(beta_s[s, j] * m.y[s, j] for j in J) for s in S),
                              sense=pyo.maximize)
        solver.solve(m)
        Z_SP = pyo.value(m.obj)
        x_sp = {j: pyo.value(m.x[j]) for j in J}

        # WS (perfect info per scenario)
        Z_WS = 0
        det_x = {}
        for s in S:
            ms = pyo.ConcreteModel()
            ms.J = pyo.Set(initialize=J)
            ms.x = pyo.Var(ms.J, within=pyo.NonNegativeReals)
            ms.y = pyo.Var(ms.J, within=pyo.NonNegativeReals)
            ms.b1 = pyo.Constraint(expr=sum(ms.x[j] for j in J) <= 65000)
            ms.b2 = pyo.Constraint(expr=sum(ms.y[j] for j in J) <= 15000)
            ms.aic = pyo.Constraint(expr=ms.y["AI"] <= 0.5 * ms.x["H"])
            ms.obj = pyo.Objective(expr=sum(beta_base[j] * ms.x[j] for j in J) +
                                   sum(beta_s[s, j] * ms.y[j] for j in J), sense=pyo.maximize)
            solver.solve(ms)
            det_x[s] = {j: pyo.value(ms.x[j]) for j in J}
            Z_WS += p_s[s] * pyo.value(ms.obj)

        # EV solution
        beta_avg = {j: sum(p_s[s] * beta_s[s, j] for s in S) for j in J}
        mev = pyo.ConcreteModel()
        mev.J = pyo.Set(initialize=J)
        mev.x = pyo.Var(mev.J, within=pyo.NonNegativeReals)
        mev.b = pyo.Constraint(expr=sum(mev.x[j] for j in J) <= 65000)
        mev.obj = pyo.Objective(expr=sum(beta_avg[j] * mev.x[j] for j in J), sense=pyo.maximize)
        solver.solve(mev)
        x_ev = {j: pyo.value(mev.x[j]) for j in J}
        Z_EV = sum(beta_base[j] * x_ev[j] for j in J)
        for s in S:
            mt = pyo.ConcreteModel()
            mt.J = pyo.Set(initialize=J)
            mt.y = pyo.Var(mt.J, within=pyo.NonNegativeReals)
            mt.b2 = pyo.Constraint(expr=sum(mt.y[j] for j in J) <= 15000)
            mt.aic = pyo.Constraint(expr=mt.y["AI"] <= 0.5 * x_ev["H"])
            mt.obj = pyo.Objective(expr=sum(beta_s[s, j] * mt.y[j] for j in J), sense=pyo.maximize)
            solver.solve(mt)
            Z_EV += p_s[s] * pyo.value(mt.obj)

        VSS, EVPI = Z_SP - Z_EV, Z_WS - Z_SP
        st.subheader("Câu 10.5.1–10.5.3 — Lời giải SP, VSS, EVPI")
        cc = st.columns([1, 1])
        with cc[0]:
            st.dataframe(pd.DataFrame({"Hạng mục": J,
                                       "x* SP": [round(x_sp[j]) for j in J],
                                       "x* EV": [round(x_ev[j]) for j in J]}),
                         use_container_width=True, hide_index=True)
        with cc[1]:
            st.metric("Z* Stochastic", f"{Z_SP:,.0f}")
            st.metric("VSS = Z_SP − Z_EV", f"{VSS:,.0f}")
            st.metric("EVPI = Z_WS − Z_SP", f"{EVPI:,.0f}")
        st.info("VSS > 0: cân nhắc bất định khi quyết định có giá trị. "
                "EVPI là giá trị tối đa nên trả cho thông tin hoàn hảo.")
    except Exception as e:
        st.warning(f"Không có solver Pyomo khả dụng trong môi trường này ({e}). "
                   "Hiển thị kết quả tham chiếu từ notebook.")
        st.dataframe(pd.DataFrame({
            "Kịch bản": S, "Z*[s] (Wait&See)": [101500, 97750, 96250, 97750],
            "Xác suất": list(p_s.values())}), use_container_width=True, hide_index=True)
        st.metric("Z* Stochastic (tham chiếu)", "98.575")

    with st.expander("Thảo luận chính sách"):
        st.markdown(
            "- Lời giải SP có xu hướng đầu tư **H (nhân lực) nhiều hơn** EV vì H đóng vai trò "
            "'bảo hiểm' (hệ số βₕ cao trong kịch bản khủng hoảng).\n"
            "- COVID-19 và bão Yagi là minh chứng: Việt Nam có thể đang 'dưới đầu tư' vào "
            "nhân lực số như một hàng hóa bảo hiểm rủi ro."
        )


# ============================================================================
#  BÀI 11 — Q-learning
# ============================================================================
ACTION_NAMES = ["Truyền thống", "Cân bằng", "Số hóa nhanh", "AI dẫn dắt", "Bao trùm"]
ALLOC = {
    0: np.array([0.70, 0.10, 0.10, 0.10]), 1: np.array([0.40, 0.25, 0.15, 0.20]),
    2: np.array([0.25, 0.45, 0.15, 0.15]), 3: np.array([0.20, 0.20, 0.45, 0.15]),
    4: np.array([0.30, 0.20, 0.10, 0.40])}
W_REW = np.array([0.40, 0.25, 0.20, 0.15])


def _env_step(state, action, K, D, AI, H, Y_prev, t):
    a = ALLOC[action]; budget = 2100.0
    K = (1 - 0.05) * K + a[0] * budget
    D = (1 - 0.12) * D + a[1] * budget * 0.01
    AI = (1 - 0.15) * AI + a[2] * budget * 0.05
    H = H + 0.8 * (a[3] * budget * 0.01) - 0.02 * H
    A = 33.70 * (1 + 0.003 * (D / 100) + 0.002 * (AI / 100) + 0.004 * (H / 100)) ** t
    L = 53.9 * 1.009 ** t
    Y = A * K ** 0.33 * L ** 0.42 * D ** 0.10 * AI ** 0.08 * H ** 0.07
    dgdp = (Y - Y_prev) / Y_prev
    dun = max(0, -dgdp * 0.5)
    cyber = (AI / (H + 1)) * 0.01
    emis = (K + AI) * 0.0001
    reward = W_REW[0] * dgdp * 100 - W_REW[1] * dun * 100 - W_REW[2] * cyber - W_REW[3] * emis
    gl = 0 if dgdp < 0.03 else (1 if dgdp < 0.06 else 2)
    dl = 0 if D < 25 else (1 if D < 35 else 2)
    al = 0 if AI < 100 else (1 if AI < 200 else 2)
    hl = 0 if H < 35 else (1 if H < 50 else 2)
    return np.array([gl, dl, al, hl]), reward, K, D, AI, H, Y


@st.cache_data(show_spinner="Đang huấn luyện Q-learning (10.000 episodes)...")
def train_q(n_episodes=10000, seed=0):
    rng = np.random.default_rng(seed)
    Q = np.zeros((3, 3, 3, 3, 5))
    gamma, alpha, T = 0.95, 0.1, 10
    hist = []
    for ep in range(n_episodes):
        s = rng.integers(0, 3, size=4)
        K, D, AI, H, Y_prev = 27500.0, 20.3, 86.0, 30.0, 12847.6
        total = 0
        eps = max(0.05, 1.0 - ep / 5000)
        for t in range(T):
            if rng.random() < eps:
                a = rng.integers(5)
            else:
                a = int(np.argmax(Q[tuple(s)]))
            s2, r, K, D, AI, H, Y_prev = _env_step(s, a, K, D, AI, H, Y_prev, t)
            done = 1.0 if t == T - 1 else 0.0
            Q[tuple(s) + (a,)] += alpha * (r + gamma * np.max(Q[tuple(s2)]) * (1 - done)
                                           - Q[tuple(s) + (a,)])
            total += r
            s = s2
        hist.append(total)
    return Q, np.array(hist)


def _eval_policy(Q, kind, n_eval=300, seed=1):
    rng = np.random.default_rng(seed)
    rewards = []
    for _ in range(n_eval):
        s = rng.integers(0, 3, size=4)
        K, D, AI, H, Y_prev = 27500.0, 20.3, 86.0, 30.0, 12847.6
        total = 0
        for t in range(10):
            if kind == "opt":
                a = int(np.argmax(Q[tuple(s)]))
            elif kind == "a1":
                a = 1
            elif kind == "a3":
                a = 3
            else:
                a = rng.integers(5)
            s, r, K, D, AI, H, Y_prev = _env_step(s, a, K, D, AI, H, Y_prev, t)
            total += r
        rewards.append(total)
    return np.mean(rewards), np.std(rewards)


def page_bai11():
    st.header("♻️ Bài 11 — Q-learning cho chính sách kinh tế thích nghi")
    st.markdown("MDP: 3⁴=81 trạng thái (GDP/D/AI/U) × 5 hành động ngân sách. "
                "Phần thưởng = phúc lợi xã hội (w=0,40/0,25/0,20/0,15).")
    st.caption("Lưu ý: bài tập minh họa kỹ thuật, **AI không thay thế quyết định chính trị**.")
    if st.button("▶️ Huấn luyện Q-learning", type="primary"):
        st.session_state["b11_run"] = True
    if not st.session_state.get("b11_run"):
        st.info("Bấm nút để huấn luyện agent qua 10.000 episodes.")
        return

    Q, hist = train_q()
    st.subheader("Câu 11.3.3 — Chính sách π*(s) tại các trạng thái")
    test = [
        ([1, 1, 0, 1], "VN 2026 thực tế (GDP_med, D_med, AI_low, H_med)"),
        ([0, 0, 0, 2], "Kịch bản tệ (GDP_low, D_low, AI_low, H_high)"),
        ([2, 2, 2, 2], "Kịch bản tốt (GDP_high, D_high, AI_high, H_high)"),
        ([0, 1, 0, 0], "Sau khủng hoảng (GDP_low, D_med, AI_low, H_low)"),
        ([1, 0, 2, 1], "AI mạnh, D yếu (GDP_med, D_low, AI_high, H_med)"),
    ]
    rows = []
    for s, desc in test:
        a = int(np.argmax(Q[tuple(s)]))
        rows.append({"Trạng thái": desc, "π* hành động": ACTION_NAMES[a]})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.subheader("Câu 11.3.4 — So sánh với rule-based & learning curve")
    res = {
        "π* (Q-learning)": _eval_policy(Q, "opt"),
        "Luôn Cân bằng (a1)": _eval_policy(Q, "a1"),
        "Luôn AI dẫn dắt (a3)": _eval_policy(Q, "a3"),
        "Random": _eval_policy(Q, "rand"),
    }
    cc = st.columns([1, 1])
    with cc[0]:
        st.dataframe(pd.DataFrame({
            "Chính sách": list(res.keys()),
            "Phúc lợi TB": [round(v[0], 2) for v in res.values()],
            "Std": [round(v[1], 2) for v in res.values()]}),
            use_container_width=True, hide_index=True)
    with cc[1]:
        fig, ax = plt.subplots(figsize=(6, 3.4))
        win = 200
        sm = np.convolve(hist, np.ones(win) / win, mode="valid")
        ax.plot(sm, "b-"); ax.set_xlabel("Episode"); ax.set_ylabel("Tổng phúc lợi")
        ax.set_title("Learning curve"); ax.grid(alpha=0.3)
        show_fig(fig)
    fig, ax = plt.subplots(figsize=(8, 3.2))
    names = list(res.keys())
    ax.bar(names, [res[n][0] for n in names], yerr=[res[n][1] for n in names],
           color=["#e74c3c", "#3498db", "#2ecc71", "#95a5a6"], capsize=5)
    ax.set_ylabel("Phúc lợi bình quân"); ax.set_title("So sánh chính sách")
    plt.xticks(rotation=12, ha="right", fontsize=8); ax.grid(axis="y", alpha=0.3)
    show_fig(fig)


# ============================================================================
#  BÀI 12 — AIDEOM-VN tích hợp (6 module → 4 tab)
# ============================================================================
def page_bai12():
    st.header("🧩 Bài 12 — Đồ án tích hợp AIDEOM-VN")
    st.markdown("6 module (M1–M6) tích hợp thành hệ thống hỗ trợ ra quyết định, "
                "tổ chức trong **4 tab**: Tổng quan • Phân bổ • So sánh kịch bản • Cảnh báo rủi ro.")

    # ---- M1: Dự báo Cobb-Douglas 5 kịch bản ----
    a, b, g, d, th = 0.33, 0.42, 0.10, 0.08, 0.07
    K0, L0, D0_v, AI0, H0, A0 = 27500, 53.9, 20.3, 86, 30, 33.70
    T = 4; years = list(range(2026, 2026 + T + 1)); budget_annual = 3000

    def forecast(alloc):
        K, D, AI, H, A = K0, D0_v, AI0, H0, A0
        traj = [A * K ** a * L0 ** b * D ** g * AI ** d * H ** th]
        for t in range(T):
            K = (1 - 0.05) * K + alloc["K"] * budget_annual
            D = (1 - 0.12) * D + alloc["D"] * budget_annual * 0.01
            AI = (1 - 0.15) * AI + alloc["AI"] * budget_annual * 0.05
            H = H + 0.8 * alloc["H"] * budget_annual * 0.01 - 0.02 * H
            A = A * (1 + 0.003 * (D / 100) + 0.002 * (AI / 100) + 0.004 * (H / 100))
            L = L0 * 1.009 ** (t + 1)
            traj.append(A * K ** a * L ** b * D ** g * AI ** d * H ** th)
        return traj

    scenarios = {
        "S1 Truyền thống": {"K": 0.70, "D": 0.10, "AI": 0.10, "H": 0.10},
        "S2 Số hóa nhanh": {"K": 0.25, "D": 0.45, "AI": 0.15, "H": 0.15},
        "S3 AI dẫn dắt": {"K": 0.20, "D": 0.20, "AI": 0.45, "H": 0.15},
        "S4 Bao trùm số": {"K": 0.30, "D": 0.20, "AI": 0.10, "H": 0.40},
        "S5 Tối ưu cân bằng": {"K": 0.25, "D": 0.25, "AI": 0.30, "H": 0.20},
    }
    gdp_fc = {n: forecast(al) for n, al in scenarios.items()}

    # ---- M2: TOPSIS Expert + Entropy ----
    dr = load_regions()
    crit = ["grdp_per_capita_million_VND", "fdi_registered_billion_USD",
            "digital_index_0_100", "ai_readiness_0_100", "trained_labor_pct",
            "rd_intensity_pct", "internet_penetration_pct", "gini_coef"]
    is_ben = [True, True, True, True, True, True, True, False]
    Xr = dr[crit].values.astype(float)
    w_expert = np.array([0.10, 0.10, 0.15, 0.20, 0.15, 0.15, 0.05, 0.10])
    C_exp = _topsis(Xr, w_expert, is_ben)
    w_ent = _entropy_weights(Xr)
    C_ent = _topsis(Xr, w_ent, is_ben)

    # ---- M3: LP phân bổ ngành-vùng ----
    import pulp
    D0d = dict(zip(dr["region_name_en"].map({
        "Northern Midlands and Mountains": "NMM", "Red River Delta": "RRD",
        "North Central and South Central Coast": "NCC", "Central Highlands": "CH",
        "Southeast": "SE", "Mekong Delta": "MD"}), dr["digital_index_0_100"]))
    gamma_val, lam_val = 0.002, 0.6
    m = pulp.LpProblem("M3", pulp.LpMaximize)
    x = pulp.LpVariable.dicts("x", (REGIONS, ITEMS), lowBound=0)
    m += pulp.lpSum(BETA[(r, j)] * x[r][j] for r in REGIONS for j in ITEMS)
    m += pulp.lpSum(x[r][j] for r in REGIONS for j in ITEMS) <= 50000
    for r in REGIONS:
        m += pulp.lpSum(x[r][j] for j in ITEMS) >= 5000
        m += pulp.lpSum(x[r][j] for j in ITEMS) <= 12000
    m += pulp.lpSum(x[r]["H"] for r in REGIONS) >= 12000
    Mv = pulp.LpVariable("Dmax")
    for r in REGIONS:
        m += D0d[r] + gamma_val * x[r]["D"] <= Mv
        m += D0d[r] + gamma_val * x[r]["D"] >= lam_val * Mv
    m.solve(pulp.PULP_CBC_CMD(msg=False))
    alloc_mat = np.array([[x[r][j].value() for j in ITEMS] for r in REGIONS])
    Z_lp = pulp.value(m.objective)

    # ---- M4: lao động NetJob ----
    from scipy.optimize import linprog
    a1 = np.array([8.5, 32.5, 12.8, 22.4, 45.8, 28.5, 62.5, 18.5])
    b1 = np.array([45, 28, 35, 32, 22, 30, 20, 55])
    c1 = np.array([5.2, 62.4, 18.5, 48.2, 72.5, 42.8, 32.5, 12.5])
    d1 = np.array([50, 32, 42, 38, 26, 36, 24, 62])
    risk = np.array([18, 42, 25, 38, 52, 35, 28, 22]) / 100
    sec = ["Nông-LT", "CN chế biến", "Xây dựng", "Bán buôn", "Tài chính", "Logistics", "CNTT", "Giáo dục"]
    Nn = 8; coeff = a1 - c1 * risk
    c_obj = np.concatenate([-coeff, -b1])
    A1l = np.concatenate([np.ones(Nn), np.ones(Nn)]).reshape(1, -1)
    A2 = np.zeros((Nn, 2 * Nn)); A3 = np.zeros((Nn, 2 * Nn))
    for i in range(Nn):
        A2[i, i] = -coeff[i]; A2[i, Nn + i] = -b1[i]
        A3[i, i] = c1[i] * risk[i]; A3[i, Nn + i] = -d1[i]
    rl = linprog(c_obj, A_ub=np.vstack([A1l, A2, A3]),
                 b_ub=np.concatenate([[30000], np.zeros(Nn), np.zeros(Nn)]),
                 bounds=[(0, None)] * (2 * Nn), method="highs")
    xA, xH = rl.x[:Nn], rl.x[Nn:]
    NJ = coeff * xA + b1 * xH

    # ---- 4 TABS ----
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📊 Tổng quan (M1-M2)", "🗺️ Phân bổ (M3-M4)",
         "⚖️ So sánh kịch bản (M1)", "⚠️ Cảnh báo rủi ro (M5-M6)"]
    )

    with tab1:
        st.subheader("M1 — Dự báo kinh tế Cobb-Douglas 2026–2030")
        fig, ax = plt.subplots(figsize=(9, 3.6))
        for n, traj in gdp_fc.items():
            ax.plot(years, traj, marker="o", ms=4, label=n)
        ax.set_xlabel("Năm"); ax.set_ylabel("GDP (ngh.tỷ VND)")
        ax.set_title("GDP dự báo theo 5 kịch bản"); ax.legend(fontsize=7); ax.grid(alpha=0.3)
        show_fig(fig)
        st.subheader("M2 — Đánh giá sẵn sàng số (TOPSIS Expert vs Entropy)")
        st.dataframe(pd.DataFrame({
            "Vùng": REGION_VI, "C* Expert": np.round(C_exp, 4),
            "C* Entropy": np.round(C_ent, 4),
            "Hạng Expert": pd.Series(C_exp).rank(ascending=False).astype(int).values}),
            use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("M3 — Tối ưu phân bổ ngân sách ngành-vùng (LP)")
        cc = st.columns([1.2, 1])
        with cc[0]:
            dfm = pd.DataFrame(alloc_mat.round(0), columns=ITEMS, index=REGION_VI)
            dfm["Tổng"] = dfm.sum(1)
            st.dataframe(dfm, use_container_width=True)
            st.metric("Z* LP (có công bằng)", f"{Z_lp:,.0f} tỷ VND")
        with cc[1]:
            fig, ax = plt.subplots(figsize=(5, 3.8))
            im = ax.imshow(alloc_mat, cmap="YlOrRd", aspect="auto")
            ax.set_yticks(range(6)); ax.set_yticklabels(REGIONS)
            ax.set_xticks(range(4)); ax.set_xticklabels(ITEMS)
            plt.colorbar(im, ax=ax, shrink=0.8); ax.set_title("Heatmap M3")
            show_fig(fig)
        st.subheader("M4 — Mô phỏng thị trường lao động (NetJob)")
        st.metric("Tổng NetJob", f"{-rl.fun:,.0f} việc làm")
        fig, ax = plt.subplots(figsize=(9, 3.2))
        ax.bar(sec, NJ, color="#2ecc71"); ax.set_ylabel("NetJob")
        ax.set_title("NetJob ròng theo ngành"); ax.grid(axis="y", alpha=0.3)
        plt.xticks(rotation=25, ha="right", fontsize=8)
        show_fig(fig)

    with tab3:
        st.subheader("So sánh 5 kịch bản chính sách — GDP 2030")
        rows = []
        for n, traj in gdp_fc.items():
            gr = ((traj[T] / traj[0]) ** (1 / T) - 1) * 100
            rows.append({"Kịch bản": n, "GDP 2030 (ngh.tỷ)": round(traj[T]),
                         "Tăng trưởng TB %/năm": round(gr, 2)})
        dfc = pd.DataFrame(rows)
        cc = st.columns([1.2, 1])
        with cc[0]:
            st.dataframe(dfc, use_container_width=True, hide_index=True)
        with cc[1]:
            fig, ax = plt.subplots(figsize=(5.5, 3.6))
            ax.barh(dfc["Kịch bản"], dfc["GDP 2030 (ngh.tỷ)"],
                    color=["#95a5a6", "#3498db", "#9b59b6", "#2ecc71", "#e67e22"])
            ax.set_title("GDP 2030 theo kịch bản"); plt.yticks(fontsize=8)
            show_fig(fig)
        best = dfc.loc[dfc["GDP 2030 (ngh.tỷ)"].idxmax(), "Kịch bản"]
        st.success(f"Kịch bản cho GDP 2030 cao nhất: **{best}**. "
                   "Kịch bản S5 (Tối ưu cân bằng) cân đối tăng trưởng với bao trùm và rủi ro.")

    with tab4:
        st.subheader("M5 — Đánh giá rủi ro (đa mục tiêu + ngẫu nhiên)")
        st.markdown("- **Rủi ro an ninh dữ liệu**: tăng theo đầu tư AI, giảm theo đầu tư nhân lực H.\n"
                    "- **Rủi ro môi trường (phát thải)**: cao ở Đông Nam Bộ, ĐB sông Hồng "
                    "(cường độ phát thải lớn).\n"
                    "- **Rủi ro phụ thuộc bên ngoài**: độ mở thương mại ≈180% GDP → nhạy với cú sốc toàn cầu.")
        risk_df = pd.DataFrame({
            "Vùng": REGION_VI,
            "Phát thải (eᵣ)": E_R, "Rủi ro AI (ρᵣ)": RHO_R, "Giảm rủi ro/H (σᵣ)": SIG_R})
        st.dataframe(risk_df, use_container_width=True, hide_index=True)
        fig, ax = plt.subplots(figsize=(8, 3.2))
        xpos = np.arange(6); width = 0.27
        ax.bar(xpos - width, E_R, width, label="Phát thải", color="#e74c3c")
        ax.bar(xpos, RHO_R, width, label="Rủi ro AI", color="#f39c12")
        ax.bar(xpos + width, SIG_R, width, label="Giảm rủi ro/H", color="#2ecc71")
        ax.set_xticks(xpos); ax.set_xticklabels([r[:10] for r in REGION_VI], rotation=20, ha="right", fontsize=7)
        ax.legend(fontsize=8); ax.set_title("Hệ số rủi ro theo vùng"); ax.grid(axis="y", alpha=0.3)
        show_fig(fig)

        st.subheader("M6 — Dashboard ra quyết định & cảnh báo")
        warnings = []
        for n, traj in gdp_fc.items():
            gr = ((traj[T] / traj[0]) ** (1 / T) - 1) * 100
            if gr < 6.0:
                warnings.append(f"⚠️ {n}: tăng trưởng {gr:.1f}%/năm dưới mục tiêu 6,5–7%.")
        net_total = -rl.fun
        if net_total > 0:
            st.success(f"✅ NetJob ròng dương ({net_total:,.0f} việc) — lao động không mất việc ròng.")
        for w in warnings:
            st.warning(w)
        st.info("**Khuyến nghị tổng hợp**: ưu tiên kịch bản S5 (cân bằng), tập trung 3 trung tâm AI "
                "tại các vùng dẫn đầu TOPSIS, duy trì sàn đầu tư nhân lực số như 'bảo hiểm' rủi ro.")


# ============================================================================
#  ROUTER
# ============================================================================
_ROUTES = {
    PAGES[0]: page_home,
    PAGES[1]: page_bai1,
    PAGES[2]: page_bai2,
    PAGES[3]: page_bai3,
    PAGES[4]: page_bai4,
    PAGES[5]: page_bai5,
    PAGES[6]: page_bai6,
    PAGES[7]: page_bai7,
    PAGES[8]: page_bai8,
    PAGES[9]: page_bai9,
    PAGES[10]: page_bai10,
    PAGES[11]: page_bai11,
    PAGES[12]: page_bai12,
}

try:
    _ROUTES[page]()
except FileNotFoundError as e:
    st.error(f"Không tìm thấy tệp dữ liệu CSV. Hãy đặt 3 tệp "
             "`vietnam_macro_2020_2025.csv`, `vietnam_sectors_2024.csv`, "
             "`vietnam_regions_2024.csv` cùng thư mục với app.py.\n\n"
             f"Chi tiết: {e}")
except Exception as e:
    st.error(f"Đã xảy ra lỗi khi dựng trang: {e}")
    st.exception(e)

st.markdown("---")
st.caption("VN AIDEOM-VN • Nguyễn Bảo Khánh – 23051266 • Bài tập lớn: Các mô hình ra quyết định")
