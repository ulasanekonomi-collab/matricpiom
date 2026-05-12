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
domain = st.selectbox(
    "Institutional Ecology",
    [
        "Public Governance",
        "Business Organization",
        "Social Institution"
    ]
)
if domain == "Public Governance":
    principal_term = "Rakyat"
    agent_term = "Birokrasi"

elif domain == "Business Organization":
    principal_term = "Owner"
    agent_term = "Manager"

else:
    principal_term = "Community/Donor"
    agent_term = "Organizer"

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
        "principal_term",
        key="principal"
    )

    st.text_input(
        "agent_term",
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
    st.subheader("Institutional Gap Analysis")

    st.text_area(
        "Formal Rules / Official Procedures",
        key="formal_rules",
        on_change=autosave
    )

    st.text_area(
        "Actual Practices",
        key="actual_practices",
        on_change=autosave
    )

    st.text_area(
        "Enforcement Gap",
        key="enforcement_gap",
        on_change=autosave
    )
    st.subheader("Coalition & Resistance Mapping")

    st.text_area(
        "Reform Supporters",
        key="reform_supporters",
        on_change=autosave
    )

    st.text_area(
        "Reform Resistors",
        key="reform_resistors",
        on_change=autosave
    )

    st.text_area(
        "Veto Actors",
        key="veto_actors",
        on_change=autosave
    )

    st.text_area(
        "Potential Coalitions",
        key="potential_coalitions",
        on_change=autosave
    )   

    st.subheader("Stakeholder Power Matrix")

    supporter_power = st.slider(
        "Power of Reform Supporters",
        0, 10, 5,
        key="supporter_power"
    )

    resistor_power = st.slider(
        "Power of Reform Resistors",
        0, 10, 5,
        key="resistor_power"
    )

    veto_power = st.slider(
        "Power of Veto Actors",
        0, 10, 5,
        key="veto_power"
    )
    
    st.subheader("Reform Feasibility")

    coalition_score = score_level(
        st.session_state.potential_coalitions
    )

    resistance_score = score_level(
        st.session_state.reform_resistors
    )

    veto_score = score_level(
        st.session_state.veto_actors
    )

    reform_feasibility = (
        monitor_score +
        supporter_power -
        resistor_power -
        veto_power
    )

    reform_feasibility = max(
        0,
        min(10, reform_feasibility)
    )

    st.metric(
        "Reform Feasibility Score",
        reform_feasibility
    )

    if reform_feasibility <= 2:

        st.error("""
        Reformasi sangat sulit dilakukan.
        
        Resistance dan veto structure
        sangat dominan.
        """)

    elif reform_feasibility <= 5:

        st.warning("""
        Reformasi menghadapi hambatan signifikan.
        
        Diperlukan penguatan coalition support.
        """)

    elif reform_feasibility <= 8:

        st.info("""
        Reformasi cukup feasible.
        
        Terdapat peluang coalition building.
        """)

    else:

        st.success("""
        Reformasi memiliki feasibility tinggi.
        
        Struktur coalition relatif mendukung perubahan.
        """)
    st.subheader("Power–Position Matrix")

    power_df = pd.DataFrame({
        "Actor": [
            "Reform Supporters",
            "Reform Resistors",
            "Veto Actors"
        ],

        "Position": [
            1,
            -1,
            0
        ],

        "Power": [
            supporter_power,
            resistor_power,
            veto_power
        ]
    })

    fig = px.scatter(
        power_df,
        x="Position",
        y="Power",
        text="Actor",
        size="Power"
    )

    fig.update_traces(
        textposition="top center"
    )

    fig.update_layout(
        xaxis=dict(
            tickvals=[-1, 0, 1],
            ticktext=[
                "Resist",
                "Neutral/Veto",
                "Support"
            ]
        ),

        yaxis_title="Power",
        xaxis_title="Political Position"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )    

    
    st.subheader("Problem Severity Index")

    monitoring_weakness = 10 - monitor_score

    deviation_score = score_level(
        st.session_state.deviation_risk
    )
    psi = (
        monitoring_weakness +
        deviation_score
    ) / 2
    
    conflict_score = score_level(
        st.session_state.conflict_interest
    )

    PSI = (
        info_score +
        monitoring_weakness +
        deviation_score +
        conflict_score
    ) / 4

    st.metric(
        "PSI Score",
        round(PSI, 2)
    )
    st.subheader("Strategic Interpretation")

    interpretation = ""

    # Reform Coalition

    if supporter_power > resistor_power:

        interpretation += """
        Reform coalition relatif lebih kuat
        dibanding kelompok resistensi.

        """

    else:

        interpretation += """
        Kelompok resistensi masih memiliki
        kekuatan yang signifikan.

        """

    # Veto Dynamics

    if veto_power >= 7:

        interpretation += """
        Veto actors memiliki kapasitas tinggi
        untuk menghambat reformasi.

        """

    elif veto_power >= 4:

        interpretation += """
        Veto actors memiliki pengaruh moderat
        terhadap arah reformasi.

        """

    else:

        interpretation += """
        Kapasitas veto actors relatif terbatas.

        """

    # Monitoring

    if monitor_score <= 4:

        interpretation += """
        Kelemahan monitoring menjadi sumber
        utama institutional vulnerability.

        """

    # Information Asymmetry

    if info_score >= 7:

        interpretation += """
        Asimetri informasi tinggi
        meningkatkan risiko opportunistic behavior.

        """

    # PSI Severity

    if PSI >= 7:

        interpretation += """
        Tingkat keparahan masalah kelembagaan
        tergolong tinggi.

        """

    elif PSI >= 4:

        interpretation += """
        Terdapat tekanan kelembagaan moderat
        yang memerlukan reformasi bertahap.

        """

    else:

        interpretation += """
        Struktur kelembagaan relatif stabil,
        namun tetap membutuhkan penguatan adaptif.

        """

    st.info(interpretation)
    if PSI <= 2:
        st.success("Low Governance Problem")

    elif PSI <= 5:
        st.warning("Moderate Governance Problem")

    elif PSI <= 8:
        st.error("High Structural Governance Problem")

    else:
        st.error("Severe Institutional Failure")
    st.subheader("Reform Recommendations")

    recommendations = []

    # Monitoring Reform

    if monitor_score <= 4:

        recommendations.append(
            "- Perkuat monitoring dan evaluasi institusi."
        )

    # Information Transparency

    if info_score >= 7:

        recommendations.append(
            "- Tingkatkan transparansi dan akses informasi."
        )

    # Coalition Strategy

    if supporter_power < resistor_power:

        recommendations.append(
            "- Bangun coalition support sebelum reformasi besar dilakukan."
        )

    # Veto Management

    if veto_power >= 7:

        recommendations.append(
            "- Lakukan negotiated alignment dengan veto actors."
        )

    # Institutional Gap

    if len(st.session_state.enforcement_gap) > 20:

        recommendations.append(
            "- Kurangi implementation gap antara aturan formal dan praktik aktual."
        )

    # PSI Severity

    if PSI >= 7:

        recommendations.append(
            "- Prioritaskan reformasi struktural kelembagaan."
        )

    elif PSI >= 4:

        recommendations.append(
            "- Lakukan reformasi bertahap dan adaptif."
        )

    else:

        recommendations.append(
            "- Fokus pada penguatan kelembagaan preventif."
        )

    for rec in recommendations:

        st.write(rec)
    st.subheader("Reform Simulation")

    st.write(
        "Simulasikan dampak reformasi terhadap kondisi kelembagaan."
    )

    sim_monitor = st.slider(
        "Simulated Monitoring Strength",
        0, 10, monitor_score
    )

    sim_info = st.slider(
        "Simulated Information Transparency",
        0, 10, 10 - info_score
    )

    sim_support = st.slider(
        "Simulated Reform Coalition",
        0, 10, supporter_power
    )

    # Recalculate PSI

    sim_monitoring_weakness = 10 - sim_monitor

    sim_info_problem = 10 - sim_info

    simulated_PSI = (
        sim_monitoring_weakness +
        sim_info_problem +
        conflict_score +
        deviation_score
    ) / 4

    st.metric(
        "Simulated PSI",
        round(simulated_PSI, 2)
    )

    # Reform Capacity Index (RCI)

    simulated_RCI = (
        sim_support +
        sim_monitor -
        veto_power -
        resistor_power
    ) / 2

    st.metric(
        "Reform Capacity Index",
        round(simulated_RCI, 2)
    )
    if simulated_RCI >= 6:

        st.success(
            "Kapasitas reformasi tergolong kuat."
        )

    elif simulated_RCI >= 3:

        st.info(
            "Reformasi masih feasible "
            "dengan coalition management."
        )

    else:

        st.warning(
            "Kapasitas reformasi rendah."
        )
    st.subheader("Institutional Signal")

    # SIGNAL MATRIX

    if PSI >= 6 and simulated_RCI >= 6:

        st.success(
            "Tekanan kelembagaan tinggi, "
            "namun kapasitas reformasi juga kuat. "
            "Momentum reformasi terbuka."
        )

    elif PSI >= 6 and simulated_RCI < 6:

        st.error(
            "Masalah kelembagaan berat "
            "tetapi kapasitas reformasi rendah. "
            "Risiko institutional trap meningkat."
        )

    elif PSI < 6 and simulated_RCI >= 6:

        st.info(
            "Kondisi kelembagaan relatif stabil "
            "dengan kapasitas adaptasi yang baik."
        )

    else:

        st.warning(
            "Kelembagaan tampak stabil "
            "namun kapasitas reformasi masih lemah."
        )    
    # Interpretation

    if simulated_PSI < PSI:

        st.success(
            "Simulasi reformasi menunjukkan "
            "penurunan risiko kelembagaan."
        )

    elif simulated_PSI > PSI:

        st.error(
            "Simulasi menunjukkan kondisi "
            "kelembagaan memburuk."
        )

    else:

        st.info(
            "Tidak ada perubahan signifikan "
            "dalam struktur kelembagaan."
        )
    st.subheader("Institutional Failure Profile")

    failure_df = pd.DataFrame({
        "Dimension": [
            "Information Failure",
            "Monitoring Failure",
            "Conflict Intensity",
            "Governance Risk"
        ],
        "Score": [
            info_score,
            monitoring_weakness,
            conflict_score,
            deviation_score
        ]
    })

    st.table(failure_df)

    st.subheader("Institutional Failure Radar")

    fig = px.line_polar(
        failure_df,
        r="Score",
        theta="Dimension",
        line_close=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("PIOM Interpretation")

    dominant_failure = failure_df.loc[
        failure_df["Score"].idxmax(),
        "Dimension"
    ]

    if dominant_failure == "Information Failure":
        interpretation = """
        Masalah didominasi oleh information failure.
        
        Struktur governance menunjukkan
        tingginya asimetri informasi
        antara principal dan agent.
        
        Transparansi dan akses informasi
        perlu diperkuat.
        """

    elif dominant_failure == "Monitoring Failure":

        if domain == "Public Governance":

            interpretation = """
            Mekanisme pengawasan birokrasi
            masih belum cukup kuat.

            Kontrol terhadap pelaksana kebijakan
            masih lemah sehingga
            potensi penyimpangan meningkat.

            Reformasi perlu fokus pada:
            - penguatan pengawasan,
            - transparansi,
            - dan evaluasi kinerja institusi.
            """

        elif domain == "Business Organization":

            interpretation = """
            Sistem monitoring organisasi bisnis
            masih belum optimal.

            Owner belum memiliki visibilitas
            yang cukup terhadap
            perilaku dan performa manager.

            Organisasi perlu memperkuat:
            - KPI,
            - evaluasi kinerja,
            - dan sistem pelaporan internal.
            """

        else:

            interpretation = """
            Pengawasan komunitas
            dan keselarasan misi organisasi
            masih belum cukup kuat.

            Potensi ketidaksesuaian
            antara tujuan organisasi
            dan pelaksana lapangan meningkat.

            Diperlukan:
            - monitoring partisipatif,
            - transparansi aktivitas,
            - dan penguatan akuntabilitas sosial.
            """

    elif dominant_failure == "Conflict Intensity":
        interpretation = """
        Konflik kepentingan menjadi faktor dominan.
        
        Aktor memiliki kepentingan berbeda
        yang berpotensi menghambat reformasi.
        
        Diperlukan strategi koalisi
        dan negosiasi kelembagaan.
        """

    else:
        interpretation = """
        Risiko governance failure cukup tinggi.
        
        Potensi penyimpangan perilaku agent
        perlu diantisipasi melalui:
        - monitoring,
        - transparansi,
        - dan redesign insentif.
        """

    st.info(interpretation)
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
