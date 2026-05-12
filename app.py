import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

SAVE_FILE = "piom_autosave.json"

FIELDS = [
    "kasus",
    "power_aktor",

    "institution_formal",
    "institution_informal",

    "incentive",
    "cost",

    "behavior",
    "outcome",
    "design",

    # tambahan baru
    "informasi",
    "nilai",

    # simulation variables
    "benefit_score",
    "cost_score",
    "info_score",
    "moral_score"
]
def autosave():
    data = {k: st.session_state.get(k, "") for k in FIELDS}
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.write("Error autosave:", e)
def autoload():
    try:
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            for k in FIELDS:
                if k in data:
                    st.session_state[k] = data[k]
    except Exception as e:
        st.write("Error autoload:", e)        
# =========================
# HELPER FUNCTIONS
# =========================
def score_level(text):
    if not text:
        return 0

    length = len(text.split())

    if length < 10:
        return 1
    elif length < 30:
        return 2
    else:
        return 3
# =========================
# PIOM SIMULATION ENGINE
# =========================

def calculate_behavior_score(B, C, N, M):

    # Formula PIOM
    S = B + N + M - C

    return S


def interpret_score(S):

    if S <= 0:
        return "Perilaku sulit berubah"

    elif S <= 5:
        return "Perubahan mungkin terjadi"

    elif S <= 10:
        return "Perubahan cukup kuat"

    else:
        return "Perubahan sangat mungkin terjadi"
    if not text:
        return 0
    length = len(text.split())
    if length < 10:
        return 1
    elif length < 25:
        return 2
    else:
        return 3


def analyze_piom():
    ins_score = score_level(st.session_state.incentive)
    cost_score = score_level(st.session_state.cost)

    if ins_score >= 2 and cost_score >= 2:
        root = "Masalah didorong oleh kombinasi insentif yang tidak tepat dan biaya transaksi yang tinggi."
    elif ins_score >= 2:
        root = "Masalah terutama disebabkan oleh insentif yang tidak selaras."
    elif cost_score >= 2:
        root = "Masalah terutama disebabkan oleh biaya transaksi yang tinggi."
    else:
        root = "Masalah belum cukup teridentifikasi secara struktural."

    causal = f"""
Institusi: {st.session_state.institution_formal}
→ menciptakan insentif: {st.session_state.incentive}
→ memengaruhi perilaku: {st.session_state.behavior}
→ menghasilkan outcome: {st.session_state.outcome}
"""

    return root, causal


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="PIOM Analyzer", layout="wide")

# =========================
# SESSION STATE
# =========================
def init_state():
    defaults = {
        "step": "Masalah",
        "kasus": "",
        "kategori": "Publik",
        "power_aktor": "",
        "power_peran": "",
        "institution_formal": "",
        "institution_informal": "",
        "incentive": "",
        "cost": "",
        "informasi": "",
        "behavior": "",
        "outcome": "",
        "design": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
autoload()

# =========================
# SIDEBAR
# =========================
st.sidebar.title("PIOM Flow")

steps = [
    "Masalah","Power","Institution","Incentive",
    "Transaction Cost","Behavior","Outcome","Design","Simulation","Output"
]

st.session_state.step = st.sidebar.radio("Langkah Analisis", steps)

# =========================
# HEADER
# =========================
col1, col2 = st.columns([1,4])

with col1:
    st.image("yuhka.jpg", width=120)

with col2:
    st.title("PIOM Analyzer")
    st.caption("Laboratorium Desain Kelembagaan")
# ✅ DEBUG DI SINI
st.sidebar.write("DEBUG kasus:", st.session_state.get("kasus"))
st.markdown(
    "<p style='font-size:12px;color:gray;'>Dikembangkan oleh Yuhka Sundaya · Ekonomi Pembangunan · Universitas Islam Bandung</p>",
    unsafe_allow_html=True
)

# =========================
# MASALAH
# =========================
if st.session_state.step == "Masalah":
    st.header("Identifikasi Masalah")
    st.subheader("Problem Structuring")

    st.text_area(
        "Gejala Utama",
        key="problem_symptom",
        on_change=autosave
    )

    st.text_area(
        "Dampak Sistemik",
        key="systemic_impact",
        on_change=autosave
    )

    st.selectbox(
        "Arena Masalah",
        [
            "Publik",
            "Pasar",
            "Organisasi",
            "Politik",
            "Pendidikan",
            "Lingkungan"
        ],
        key="problem_arena"
    )

    st.text_area(
        "Aktor Terdampak",
        key="affected_actor",
        on_change=autosave
    )

    st.text_area(
        "Aktor Dominan",
        key="dominant_actor",
        on_change=autosave
    )

    st.text_area(
        "Konflik Kepentingan",
        key="conflict_interest",
        on_change=autosave
    )
    st.subheader("Principal-Agent Structure")

    st.text_input(
        "Principal",
        key="principal"
    )

    st.text_input(
        "Agent",
        key="agent"
    )

    st.text_area(
        "Mandat Formal",
        key="formal_mandate",
        on_change=autosave
    )

    st.text_area(
        "Potensi Penyimpangan",
        key="deviation_risk",
        on_change=autosave
    )

    info_score = st.slider(
        "Asimetri Informasi",
        0, 10, 5,
        key="info_asymmetry"
    )

    if info_score <= 2:
        st.caption("Informasi relatif terbuka")

    elif info_score <= 4:
        st.caption("Ada ketimpangan informasi ringan")

    elif info_score <= 6:
        st.caption("Monitoring mulai sulit")

    elif info_score <= 8:
        st.caption("Agent dominan dalam penguasaan informasi")

    else:
        st.caption("Informasi sangat tertutup")

    monitor_score = st.slider(
        "Kekuatan Monitoring",
        0, 10, 5,
        key="monitoring_strength"
    )

    if monitor_score <= 2:
        st.caption("Pengawasan hampir tidak ada")

    elif monitor_score <= 4:
        st.caption("Pengawasan lemah")

    elif monitor_score <= 6:
        st.caption("Monitoring moderat")

    elif monitor_score <= 8:
        st.caption("Monitoring kuat")

    else:
        st.caption("Monitoring sangat ketat")

# =========================
# POWER
# =========================
elif st.session_state.step == "Power":
    st.header("Power")

    st.text_area("Aktor", key="power_aktor", on_change=autosave)

    st.markdown("### Pertanyaan Kritis")
    st.write("Siapa yang diuntungkan?")
    st.write("Siapa punya kekuasaan?")
    st.write("Siapa dirugikan?")

# =========================
# INSTITUTION
# =========================
elif st.session_state.step == "Institution":
    st.header("Institution")

    st.text_area("Formal", key="institution_formal", on_change=autosave)
    st.text_area("Informal", key="institution_informal", on_change=autosave)

    st.markdown("### Pertanyaan Kritis")
    st.write("Aturan apa berlaku?")
    st.write("Norma apa dominan?")
    st.write("Apakah ditegakkan?")

# =========================
# INCENTIVE
# =========================
elif st.session_state.step == "Incentive":
    st.header("Incentive")

    st.text_area("Insentif", key="incentive", on_change=autosave)

    st.markdown("### Pertanyaan Kritis")
    st.write("Apa yang memotivasi?")
    st.write("Apakah effort dihargai?")
    st.write("Ada reward?")

# =========================
# COST
# =========================
elif st.session_state.step == "Transaction Cost":
    st.header("Transaction Cost")

    st.text_area("Biaya", key="cost", on_change=autosave)

    st.markdown("### Pertanyaan Kritis")
    st.write("Apa yang membuat sulit?")
    st.write("Ada biaya tersembunyi?")
    st.write("Info mudah diakses?")

# =========================
# BEHAVIOR
# =========================
elif st.session_state.step == "Behavior":
    st.header("Behavior")

    st.text_area("Perilaku", key="behavior", on_change=autosave)

    st.markdown("### Pertanyaan Kritis")
    st.write("Bagaimana respon aktor?")
    st.write("Apakah rasional?")

# =========================
# OUTCOME
# =========================
elif st.session_state.step == "Outcome":
    st.header("Outcome")

    st.text_area("Outcome", key="outcome", on_change=autosave)
    st.markdown("### Pertanyaan Kritis")
    st.write("Efisien?")
    st.write("Adil?")

# =========================
# DESIGN
# =========================
elif st.session_state.step == "Design":
    st.header("Design")

    st.text_area("Solusi", key="design", on_change=autosave)

    st.markdown("### Pertanyaan Kritis")
    st.write("Apa diubah?")
    st.write("Bagaimana insentif diperbaiki?")
    st.write("Bagaimana cost diturunkan?")
# =========================
# SIMULATION
# =========================

elif st.session_state.step == "Simulation":

    st.header("PIOM Institutional Design Simulator")

    st.markdown("""
    Simulasi perubahan perilaku sebelum dan sesudah institutional design.
    """)

    # =========================
    # EXISTING CONDITION
    # =========================

    st.subheader("Existing Condition")

    B1 = st.slider("Existing Benefit / Incentive", 0, 10, 2)
    C1 = st.slider("Existing Transaction Cost", 0, 10, 8)
    N1 = st.slider("Existing Information / Framing", 0, 10, 3)
    M1 = st.slider("Existing Moral Support", 0, 10, 3)

    S1 = calculate_behavior_score(B1, C1, N1, M1)

    probability1 = min(max((S1 + 10) * 5, 0), 100)

    st.metric("Existing Score", S1)
    st.metric("Existing Probability", f"{probability1}%")

    st.divider()

    # =========================
    # DESIGN SCENARIO
    # =========================

    st.subheader("After Institutional Design")

    B2 = st.slider("New Benefit / Incentive", 0, 10, 7)
    C2 = st.slider("New Transaction Cost", 0, 10, 3)
    N2 = st.slider("New Information / Framing", 0, 10, 7)
    M2 = st.slider("New Moral Support", 0, 10, 7)

    S2 = calculate_behavior_score(B2, C2, N2, M2)

    probability2 = min(max((S2 + 10) * 5, 0), 100)

    st.metric("New Score", S2)
    st.metric("New Probability", f"{probability2}%")

    st.divider()

    # =========================
    # DESIGN IMPACT
    # =========================

    delta_score = S2 - S1
    delta_probability = probability2 - probability1

    st.subheader("Design Impact")

    st.metric("Δ Score", delta_score)
    st.metric("Δ Probability", f"{delta_probability}%")

    # INTERPRETASI
    if delta_score <= 0:
        st.error("Design belum efektif mengubah perilaku.")

    elif delta_score <= 5:
        st.warning("Design mulai memberi pengaruh.")

    elif delta_score <= 10:
        st.success("Design cukup efektif.")

    else:
        st.success("Design sangat efektif mengubah perilaku.")

    # =========================
    # MATRIX
    # =========================
    st.subheader("PIOM Design Matrix")

    st.table({
        "Variable": ["Benefit", "Cost", "Information", "Moral"],
        "Existing": [B1, C1, N1, M1],
        "After Design": [B2, C2, N2, M2]
    })
    # =========================
    # RADAR CHART
    # =========================

    st.subheader("Institutional Design Radar")

    radar_df = pd.DataFrame({
        "Variable": ["Benefit", "Cost", "Information", "Moral"],
        "Existing": [B1, C1, N1, M1],
        "After Design": [B2, C2, N2, M2]
    })

    radar_long = radar_df.melt(
        id_vars="Variable",
        var_name="Condition",
        value_name="Score"
    )

    fig = px.line_polar(
        radar_long,
        r="Score",
        theta="Variable",
        color="Condition",
        line_close=True
    )

    st.plotly_chart(fig, use_container_width=True)
    # =========================
    # RESISTANCE ENGINE
    # =========================

    st.subheader("Institutional Resistance")

    power_resistance = st.slider(
        "Elite / Power Resistance",
        0, 10, 5
    )

    institutional_rigidity = st.slider(
        "Institutional Rigidity",
        0, 10, 5
    )

    status_quo_dependency = st.slider(
        "Status Quo Dependency",
        0, 10, 5
    )

    resistance_score = (
        power_resistance +
        institutional_rigidity +
        status_quo_dependency
    ) / 3

    st.metric(
        "Resistance Score",
        round(resistance_score, 2)
    )

    # INTERPRETATION
    if resistance_score <= 3:
        st.success("Reform feasibility tinggi")

    elif resistance_score <= 6:
        st.warning("Perlu strategi koalisi dan negosiasi")

    else:
        st.error("Potensi resistensi politik tinggi")    
# =========================
# OUTPUT
# =========================
elif st.session_state.step == "Output":
    st.header("Hasil Analisis")

    root, causal = analyze_piom()

    st.subheader("Analisis Inti")
    st.success(root)

    st.subheader("Rantai Kausal")
    st.write(causal)
