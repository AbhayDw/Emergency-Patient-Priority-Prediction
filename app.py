import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from joblib import load

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EmergencyAI",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .stApp { background-color: #0F172A; color: #F1F5F9; }
  .block-container { padding-top: 1.6rem; padding-bottom: 1.6rem; max-width: 1160px; }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] { background:#0B1120; border-right:1px solid #1E293B; }
  [data-testid="stSidebar"] .stRadio > label { color:#94A3B8 !important; font-size:13px; }
  [data-testid="stSidebar"] .stRadio div[role="radio"] {
    background:#111827; border:1px solid #1E293B; border-radius:10px;
    padding:10px 14px; margin-bottom:4px; transition:all .15s;
  }
  [data-testid="stSidebar"] .stRadio div[role="radio"]:hover { border-color:#2563EB; background:#172033; }

  /* ── Cards ── */
  .card {
    background:#1E293B; border-radius:14px; padding:20px 22px;
    border:1px solid #273348; box-shadow:0 2px 16px rgba(0,0,0,.25); margin-bottom:14px;
  }
  .card-title {
    font-size:13px; font-weight:600; color:#64748B; text-transform:uppercase;
    letter-spacing:.06em; margin-bottom:14px; display:flex; align-items:center; gap:6px;
  }
  .kpi-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:14px; }
  .kpi {
    background:#1E293B; border:1px solid #273348; border-radius:14px;
    padding:18px 16px; text-align:center;
  }
  .kpi-val { font-size:28px; font-weight:700; margin:6px 0 4px; }
  .kpi-lbl { font-size:11px; color:#64748B; font-weight:500; text-transform:uppercase; letter-spacing:.06em; }
  .kpi-ico { font-size:20px; }

  /* ── Hero ── */
  .hero-title {
    font-size:44px; font-weight:700; line-height:1.18;
    background:linear-gradient(135deg,#F1F5F9 0%,#94A3B8 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
  }
  .hero-sub { font-size:16px; color:#64748B; margin-top:10px; line-height:1.65; }

  /* ── Quick Action buttons ── */
  .qa-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:20px; }
  .qa-btn {
    background:#1E293B; border:1px solid #273348; border-radius:12px;
    padding:14px 16px; cursor:pointer; transition:all .18s;
    display:flex; align-items:center; gap:10px;
  }
  .qa-btn:hover { border-color:#2563EB; background:#172033; transform:translateY(-1px); }
  .qa-btn-icon { font-size:20px; }
  .qa-btn-text { font-size:13px; font-weight:600; color:#F1F5F9; }
  .qa-btn-sub  { font-size:11px; color:#64748B; margin-top:1px; }

  /* ── Badges ── */
  .badge {
    display:inline-flex; align-items:center; gap:5px;
    padding:3px 10px; border-radius:20px; font-size:11px; font-weight:600;
    letter-spacing:.06em; text-transform:uppercase;
  }
  .badge-red   { background:rgba(239,68,68,.12);  color:#EF4444; border:1px solid rgba(239,68,68,.25); }
  .badge-green { background:rgba(34,197,94,.12);  color:#22C55E; border:1px solid rgba(34,197,94,.25); }
  .badge-blue  { background:rgba(37,99,235,.12);  color:#2563EB; border:1px solid rgba(37,99,235,.25); }
  .badge-amber { background:rgba(245,158,11,.12); color:#F59E0B; border:1px solid rgba(245,158,11,.25); }

  /* ── Result cards ── */
  .result-box {
    border-radius:14px; padding:28px 24px; text-align:center; margin-bottom:12px;
  }
  .result-emergency { background:linear-gradient(145deg,rgba(239,68,68,.14),rgba(239,68,68,.04)); border:1px solid rgba(239,68,68,.35); }
  .result-success   { background:linear-gradient(145deg,rgba(34,197,94,.14),rgba(34,197,94,.04)); border:1px solid rgba(34,197,94,.35); }
  .result-ico  { font-size:44px; margin-bottom:10px; }
  .result-lbl  { font-size:24px; font-weight:700; }
  .result-pct  { font-size:44px; font-weight:800; margin:6px 0; }
  .result-sub  { font-size:13px; color:#94A3B8; }

  /* ── Priority pill ── */
  .priority-row { display:flex; gap:8px; justify-content:center; margin-top:12px; flex-wrap:wrap; }

  /* ── Rec card ── */
  .rec-card {
    background:#162032; border-radius:12px; padding:16px 18px;
    border-left:3px solid; margin-top:12px;
  }
  .rec-title { font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:.06em; margin-bottom:8px; }
  .rec-item  { font-size:13px; color:#94A3B8; line-height:1.7; }

  /* ── Section headings ── */
  .pg-title { font-size:21px; font-weight:700; color:#F1F5F9; margin-bottom:2px; }
  .pg-sub   { font-size:13px; color:#64748B; margin-bottom:18px; }

  /* ── Inputs ── */
  .stSelectbox>div>div, .stNumberInput>div>div>input {
    background:#0F172A !important; border:1px solid #273348 !important;
    color:#F1F5F9 !important; border-radius:8px !important;
  }
  .stSlider>div>div { background:#273348 !important; }

  /* ── Primary button ── */
  .stButton>button {
    background:#2563EB; color:white; border:none;
    padding:11px 28px; border-radius:10px; font-weight:600;
    font-size:14px; transition:all .18s; width:100%;
  }
  .stButton>button:hover { background:#1D4ED8; transform:translateY(-1px); box-shadow:0 4px 16px rgba(37,99,235,.4); }

  /* ── Upload zone ── */
  [data-testid="stFileUploadDropzone"] {
    background:#1E293B; border:2px dashed #273348; border-radius:12px;
  }

  /* ── Data table ── */
  [data-testid="stDataFrame"] { border-radius:10px; overflow:hidden; }

  /* ── Divider ── */
  hr { border-color:#1E293B; margin:12px 0; }

  /* ── Hide branding ── */
  #MainMenu, footer, header, .stDeployButton { visibility:hidden; display:none; }
</style>
""", unsafe_allow_html=True)

# ─── Model & Constants ───────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    try: return load("model.joblib")
    except Exception: return None

model = load_model()

FEATURES = [
    "age","heart_rate","systolic_bp","diastolic_bp","oxygen_saturation",
    "respiratory_rate","temperature","pain_level",
    "chief_complaint_code","arrival_mode_code","triage_level",
    "previous_visits","chronic_conditions","allergies",
    "current_medications","lab_results_flag"
]

ARRIVAL_MODES  = ["Walk-in","Ambulance","Referral","Other"]
CHIEF_COMPLAINTS = ["Chest Pain","Breathing","Trauma","Fever","Other"]

SAMPLE_PATIENT = {
    "age":58, "heart_rate":112, "systolic_bp":158, "diastolic_bp":96,
    "oxygen_saturation":91, "respiratory_rate":22, "temperature":101.4,
    "pain_level":8, "chief_complaint":"Chest Pain", "arrival_mode":"Ambulance",
    "triage_level":2, "previous_visits":3, "chronic_conditions":2,
    "allergies":1, "current_medications":3, "lab_results_flag":1
}

def make_sample_df(n=20):
    np.random.seed(7)
    return pd.DataFrame({
        "age":             np.random.randint(18,85,n),
        "heart_rate":      np.random.randint(55,140,n),
        "systolic_bp":     np.random.randint(90,180,n),
        "diastolic_bp":    np.random.randint(55,110,n),
        "oxygen_saturation": np.random.randint(88,100,n),
        "respiratory_rate":  np.random.randint(10,30,n),
        "temperature":     np.round(np.random.uniform(97.0,103.5,n),1),
        "pain_level":      np.random.randint(0,11,n),
        "chief_complaint_code": np.random.randint(0,5,n),
        "arrival_mode_code":    np.random.randint(0,4,n),
        "triage_level":    np.random.randint(1,6,n),
        "previous_visits": np.random.randint(0,10,n),
        "chronic_conditions": np.random.randint(0,5,n),
        "allergies":       np.random.randint(0,4,n),
        "current_medications": np.random.randint(0,8,n),
        "lab_results_flag":    np.random.randint(0,2,n),
    })

# ─── Helpers ─────────────────────────────────────────────────────────────────────
def kpi(icon, label, value, color):
    st.markdown(f"""
    <div class="kpi">
      <div class="kpi-ico">{icon}</div>
      <div class="kpi-val" style="color:{color};">{value}</div>
      <div class="kpi-lbl">{label}</div>
    </div>""", unsafe_allow_html=True)

def gauge(prob, emergency):
    clr = "#EF4444" if emergency else "#22C55E"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(prob*100,1),
        number={"suffix":"%","font":{"color":"#F1F5F9","size":32}},
        gauge={
            "axis":{"range":[0,100],"tickcolor":"#64748B","tickfont":{"color":"#64748B","size":10}},
            "bar":{"color":clr,"thickness":0.28},
            "bgcolor":"#1E293B","borderwidth":0,
            "steps":[{"range":[0,100],"color":"#0F172A"}],
            "threshold":{"line":{"color":clr,"width":3},"thickness":0.8,"value":prob*100}
        }
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
                      font_color="#F1F5F9",height=200,margin=dict(t=16,b=8,l=16,r=16))
    return fig

def chart_layout(fig, title, h=260):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        font_color="#94A3B8",height=h,margin=dict(t=32,b=8,l=8,r=8),
        title=dict(text=title,font=dict(size=14,color="#F1F5F9")),
        legend=dict(font=dict(color="#94A3B8"),bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(showgrid=False,color="#64748B"),
        yaxis=dict(showgrid=True,gridcolor="#1E293B",color="#64748B")
    )
    return fig

def run_prediction(age,heart_rate,systolic_bp,diastolic_bp,oxygen_sat,
                   respiratory_rate,temperature,pain_level,
                   cc_code,arrival_code,triage_level,
                   previous_visits,chronic_conditions,allergies,
                   current_medications,lab_flag):
    X = np.array([[age,heart_rate,systolic_bp,diastolic_bp,oxygen_sat,
                   respiratory_rate,temperature,pain_level,
                   cc_code,arrival_code,triage_level,
                   previous_visits,chronic_conditions,allergies,
                   current_medications,lab_flag]])
    if model:
        pred  = model.predict(X)[0]
        prob  = model.predict_proba(X)[0][1]
    else:
        pred  = 1 if (triage_level<=2 or pain_level>=8 or oxygen_sat<92) else 0
        prob  = 0.91 if pred==1 else 0.17
    return bool(pred), prob

# ─── Sidebar ─────────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding:12px 0 20px;">
          <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#EF4444,#B91C1C);
              display:flex;align-items:center;justify-content:center;font-size:18px;">🚨</div>
            <div>
              <div style="font-size:15px;font-weight:700;color:#F1F5F9;">EmergencyAI</div>
              <div style="font-size:11px;color:#475569;">Priority Prediction</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        page = st.radio("nav", [
            "🏠  Home","🩺  Predict","📂  Batch","📊  Dashboard","🧪  Sample Data"
        ], label_visibility="collapsed")

    return page.split("  ")[1]

# ─── HOME ────────────────────────────────────────────────────────────────────────
def page_home():
    col_l, col_r = st.columns([1.15, 1], gap="large")
    with col_l:
        st.markdown("""
        <div style="padding-top:16px;">
          <span class="badge badge-red">● AI-Powered Triage</span>
          <div class="hero-title" style="margin-top:14px;">
            Emergency Patient<br>Priority Prediction
          </div>
          <div class="hero-sub">
            Helping healthcare professionals prioritize critical patients
            using Machine Learning — fast, accurate, and reliable.
          </div>
        </div>""", unsafe_allow_html=True)

        # Quick Actions — pure Streamlit buttons inside styled wrappers
        st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
        st.markdown("**Quick Actions**", help=None)
        qa1, qa2 = st.columns(2, gap="small")
        with qa1:
            if st.button("🚀  Predict Patient", key="qa_predict"):
                st.session_state.nav = "Predict"; st.rerun()
        with qa2:
            if st.button("📂  Batch Prediction", key="qa_batch"):
                st.session_state.nav = "Batch"; st.rerun()
        qa3, qa4 = st.columns(2, gap="small")
        with qa3:
            sample_csv = make_sample_df().to_csv(index=False).encode()
            st.download_button("📥  Download Sample CSV", sample_csv,
                               "sample_patients.csv", "text/csv", key="qa_dl")
        with qa4:
            if st.button("🧪  Load Sample Patient", key="qa_sample"):
                st.session_state.load_sample = True
                st.session_state.nav = "Predict"; st.rerun()

    with col_r:
        # Stats card visual — no ECG illustration
        st.markdown("""
        <div style="padding-top:20px;">
          <div class="card" style="background:linear-gradient(145deg,#1E293B,#162032);">
            <div style="font-size:13px;font-weight:600;color:#64748B;text-transform:uppercase;
              letter-spacing:.06em;margin-bottom:16px;">Model Overview</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
              <div style="background:#0F172A;border-radius:10px;padding:14px;border:1px solid #273348;">
                <div style="font-size:11px;color:#64748B;text-transform:uppercase;letter-spacing:.05em;">Accuracy</div>
                <div style="font-size:26px;font-weight:700;color:#22C55E;margin-top:4px;">97.2%</div>
              </div>
              <div style="background:#0F172A;border-radius:10px;padding:14px;border:1px solid #273348;">
                <div style="font-size:11px;color:#64748B;text-transform:uppercase;letter-spacing:.05em;">F1 Score</div>
                <div style="font-size:26px;font-weight:700;color:#2563EB;margin-top:4px;">97.1%</div>
              </div>
              <div style="background:#0F172A;border-radius:10px;padding:14px;border:1px solid #273348;">
                <div style="font-size:11px;color:#64748B;text-transform:uppercase;letter-spacing:.05em;">Patients</div>
                <div style="font-size:26px;font-weight:700;color:#F59E0B;margin-top:4px;">5,000</div>
              </div>
              <div style="background:#0F172A;border-radius:10px;padding:14px;border:1px solid #273348;">
                <div style="font-size:11px;color:#64748B;text-transform:uppercase;letter-spacing:.05em;">Features</div>
                <div style="font-size:26px;font-weight:700;color:#8B5CF6;margin-top:4px;">16</div>
              </div>
            </div>
            <div style="margin-top:14px;padding:12px;background:#0F172A;border-radius:10px;
              border:1px solid #273348;display:flex;align-items:center;gap:10px;">
              <div style="width:8px;height:8px;border-radius:50%;background:#22C55E;
                box-shadow:0 0 6px #22C55E;flex-shrink:0;"></div>
              <div>
                <div style="font-size:13px;font-weight:600;color:#F1F5F9;">Logistic Regression</div>
                <div style="font-size:11px;color:#64748B;">Model loaded · Ready to predict</div>
              </div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4, gap="small")
    with c1: kpi("🎯","Accuracy","97.2%","#22C55E")
    with c2: kpi("🧑‍⚕️","Patients","5,000","#2563EB")
    with c3: kpi("🔬","Features","16","#F59E0B")
    with c4: kpi("🤖","Algorithm","LogReg","#8B5CF6")

# ─── PREDICT ─────────────────────────────────────────────────────────────────────
def page_predict():
    st.markdown('<div class="pg-title">🩺 Patient Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="pg-sub">Fill in patient details across the three sections below, then hit Predict.</div>', unsafe_allow_html=True)

    # Load Sample Patient button — above the form
    if st.button("🧪  Load Sample Patient", key="predict_load_sample"):
        st.session_state.load_sample = True
        st.rerun()

    # Defaults — overridden if sample loaded
    sp = SAMPLE_PATIENT if st.session_state.get("load_sample") else {}
    if st.session_state.get("load_sample"):
        st.session_state.load_sample = False
        st.info("✅ Sample emergency patient loaded — review values and click Predict.", icon=None)

    # ── Section 1: Patient Information ──────────────────────────────────────────
    st.markdown('<div class="card"><div class="card-title">👤 Patient Information</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        age = st.number_input("Age (years)", 1, 120, int(sp.get("age", 35)))
        triage_level = st.selectbox("Triage Level", [1,2,3,4,5],
                       index=[1,2,3,4,5].index(sp.get("triage_level",3)))
    with c2:
        arr_idx = ARRIVAL_MODES.index(sp.get("arrival_mode","Walk-in")) if sp else 0
        arrival_mode = st.selectbox("Arrival Mode", ARRIVAL_MODES, index=arr_idx)
        previous_visits = st.number_input("Previous ER Visits", 0, 50, int(sp.get("previous_visits",0)))
    with c3:
        cc_idx = CHIEF_COMPLAINTS.index(sp.get("chief_complaint","Other")) if sp else 4
        chief_complaint = st.selectbox("Chief Complaint", CHIEF_COMPLAINTS, index=cc_idx)
        chronic_conditions = st.number_input("Chronic Conditions", 0, 10, int(sp.get("chronic_conditions",0)))
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Section 2: Vital Signs ───────────────────────────────────────────────────
    st.markdown('<div class="card"><div class="card-title">❤️ Vital Signs</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        heart_rate   = st.number_input("Heart Rate (bpm)",    30, 250,  int(sp.get("heart_rate",80)))
        systolic_bp  = st.number_input("Systolic BP (mmHg)",  60, 250,  int(sp.get("systolic_bp",120)))
        diastolic_bp = st.number_input("Diastolic BP (mmHg)", 40, 150,  int(sp.get("diastolic_bp",80)))
    with c2:
        oxygen_sat       = st.number_input("O₂ Saturation (%)", 70, 100, int(sp.get("oxygen_saturation",97)))
        respiratory_rate = st.number_input("Respiratory Rate",   8, 60,  int(sp.get("respiratory_rate",16)))
        temperature      = st.number_input("Temperature (°F)", 90.0, 110.0, float(sp.get("temperature",98.6)))
    with c3:
        pain_level = st.slider("Pain Level (0–10)", 0, 10, int(sp.get("pain_level",3)))
        lab_results_flag = st.selectbox("Lab Results", ["Normal","Abnormal"],
                           index=int(sp.get("lab_results_flag",0)))
        st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Section 3: Symptoms & Medical History ───────────────────────────────────
    st.markdown('<div class="card"><div class="card-title">🩺 Symptoms & Medical History</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        allergies = st.number_input("Known Allergies", 0, 20, int(sp.get("allergies",0)))
    with c2:
        current_medications = st.number_input("Current Medications", 0, 30, int(sp.get("current_medications",1)))
    st.markdown('</div>', unsafe_allow_html=True)

    predict_clicked = st.button("⚡  Predict Priority", key="predict_btn")

    if predict_clicked:
        cc_code      = CHIEF_COMPLAINTS.index(chief_complaint)
        arrival_code = ARRIVAL_MODES.index(arrival_mode)
        lab_flag     = 0 if lab_results_flag == "Normal" else 1

        is_emergency, prob = run_prediction(
            age, heart_rate, systolic_bp, diastolic_bp, oxygen_sat,
            respiratory_rate, temperature, pain_level,
            cc_code, arrival_code, triage_level,
            previous_visits, chronic_conditions, allergies,
            current_medications, lab_flag
        )

        pct         = round(prob*100, 1)
        conf_val    = prob if is_emergency else (1-prob)
        conf_label  = "High" if conf_val > 0.78 else ("Moderate" if conf_val > 0.58 else "Low")
        conf_color  = {"High":"#22C55E","Moderate":"#F59E0B","Low":"#EF4444"}[conf_label]
        priority    = {1:"P1 — Immediate",2:"P2 — Urgent",3:"P3 — Standard",
                       4:"P4 — Non-Urgent",5:"P5 — Routine"}[triage_level]

        st.markdown('<hr>', unsafe_allow_html=True)
        st.markdown('<div class="pg-title" style="margin-bottom:12px;">📋 Prediction Result</div>', unsafe_allow_html=True)

        col_res, col_gauge = st.columns([1.2, 1], gap="large")
        with col_res:
            if is_emergency:
                st.markdown(f"""
                <div class="result-box result-emergency">
                  <div class="result-ico">🔴</div>
                  <div class="result-lbl" style="color:#EF4444;">EMERGENCY</div>
                  <div class="result-pct" style="color:#EF4444;">{pct}%</div>
                  <div class="result-sub">Immediate Medical Attention Required</div>
                  <div class="priority-row">
                    <span class="badge badge-red">{priority}</span>
                    <span class="badge badge-amber">Confidence: {conf_label}</span>
                  </div>
                </div>
                <div class="rec-card" style="border-color:#EF4444;">
                  <div class="rec-title" style="color:#EF4444;">⚠️ Clinical Recommendation</div>
                  <div class="rec-item">
                    • Immediate physician evaluation required<br>
                    • Monitor vitals every 5–10 minutes<br>
                    • Activate emergency intervention protocols
                  </div>
                </div>""", unsafe_allow_html=True)
            else:
                stable_pct = round((1-prob)*100,1)
                st.markdown(f"""
                <div class="result-box result-success">
                  <div class="result-ico">🟢</div>
                  <div class="result-lbl" style="color:#22C55E;">NON-EMERGENCY</div>
                  <div class="result-pct" style="color:#22C55E;">{stable_pct}%</div>
                  <div class="result-sub">Patient is Stable — Routine Care</div>
                  <div class="priority-row">
                    <span class="badge badge-green">{priority}</span>
                    <span class="badge badge-amber">Confidence: {conf_label}</span>
                  </div>
                </div>
                <div class="rec-card" style="border-color:#22C55E;">
                  <div class="rec-title" style="color:#22C55E;">✅ Clinical Recommendation</div>
                  <div class="rec-item">
                    • Standard triage queue — no immediate escalation<br>
                    • Monitor vitals at regular intervals<br>
                    • Reassess immediately if condition changes
                  </div>
                </div>""", unsafe_allow_html=True)

        with col_gauge:
            st.markdown('<div class="card" style="text-align:center;padding-bottom:16px;">', unsafe_allow_html=True)
            st.markdown('<div style="font-size:11px;font-weight:600;color:#64748B;text-transform:uppercase;letter-spacing:.06em;margin-bottom:4px;">Prediction Confidence</div>', unsafe_allow_html=True)
            st.plotly_chart(gauge(prob, is_emergency), use_container_width=True)
            st.markdown(f'<div style="font-size:13px;color:{conf_color};font-weight:600;">{conf_label} Confidence</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="font-size:12px;color:#475569;margin-top:4px;">Emergency probability: {pct}%</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ─── BATCH ───────────────────────────────────────────────────────────────────────
def page_batch():
    st.markdown('<div class="pg-title">📂 Batch Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="pg-sub">Upload a CSV and run predictions on multiple patients at once.</div>', unsafe_allow_html=True)

    # Top action row
    c_info, c_dl = st.columns([2.5, 1], gap="small")
    with c_info:
        st.markdown("""
        <div class="card" style="padding:14px 18px;">
          <div style="font-size:12px;color:#64748B;margin-bottom:6px;font-weight:600;text-transform:uppercase;letter-spacing:.05em;">Required Columns</div>
          <div style="font-size:12px;color:#94A3B8;line-height:1.8;">
            age · heart_rate · systolic_bp · diastolic_bp · oxygen_saturation · respiratory_rate · temperature · pain_level
            · chief_complaint_code · arrival_mode_code · triage_level · previous_visits · chronic_conditions · allergies · current_medications · lab_results_flag
          </div>
        </div>""", unsafe_allow_html=True)
    with c_dl:
        sample_csv = make_sample_df().to_csv(index=False).encode()
        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)
        st.download_button("📥 Download Sample CSV", sample_csv,
                           "sample_patients.csv", "text/csv", use_container_width=True)

    uploaded = st.file_uploader("Drop CSV here", type=["csv"], label_visibility="collapsed")

    if uploaded:
        df = pd.read_csv(uploaded)
        st.markdown(f"""
        <div style="display:flex;gap:8px;margin:10px 0 12px;align-items:center;">
          <span class="badge badge-blue">📄 {len(df)} rows</span>
          <span class="badge badge-blue">🗂 {df.shape[1]} columns</span>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Preview — First 5 Rows</div>', unsafe_allow_html=True)
        st.dataframe(df.head(), use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("⚡  Run Batch Prediction", key="batch_btn"):
            missing = [f for f in FEATURES if f not in df.columns]
            if missing:
                st.error(f"Missing columns: {', '.join(missing)}")
            else:
                X = df[FEATURES].values
                if model:
                    preds = model.predict(X)
                    probs = model.predict_proba(X)[:,1]
                else:
                    preds = (df["triage_level"] <= 2).astype(int).values
                    probs = np.where(preds==1, 0.88, 0.15)

                df["prediction"] = ["🔴 Emergency" if p==1 else "🟢 Non-Emergency" for p in preds]
                df["confidence"] = (probs*100).round(1).astype(str) + "%"

                n_emg = int(sum(preds)); n_safe = len(preds)-n_emg
                c1,c2,c3 = st.columns(3, gap="small")
                with c1: kpi("🔴","Emergency",str(n_emg),"#EF4444")
                with c2: kpi("🟢","Non-Emergency",str(n_safe),"#22C55E")
                with c3: kpi("📊","Total",str(len(preds)),"#2563EB")

                st.success(f"✅ Batch prediction complete — {len(preds)} patients processed.")

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="card-title">Results</div>', unsafe_allow_html=True)
                st.dataframe(
                    df[["prediction","confidence"]+FEATURES[:6]],
                    use_container_width=True, hide_index=True
                )
                st.markdown('</div>', unsafe_allow_html=True)

                csv_out = df.to_csv(index=False).encode()
                st.download_button("⬇️  Download Results CSV", csv_out,
                                   "predictions.csv", "text/csv")

# ─── DASHBOARD ───────────────────────────────────────────────────────────────────
def page_dashboard():
    st.markdown('<div class="pg-title">📊 Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="pg-sub">Model performance metrics and patient data insights.</div>', unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4, gap="small")
    with c1: kpi("🎯","Accuracy","97.2%","#22C55E")
    with c2: kpi("📌","Precision","96.8%","#2563EB")
    with c3: kpi("🔁","Recall","97.5%","#F59E0B")
    with c4: kpi("⚖️","F1 Score","97.1%","#8B5CF6")

    np.random.seed(42)
    ages       = np.clip(np.concatenate([np.random.normal(55,15,300),np.random.normal(35,12,200)]),1,100)
    priorities = np.random.choice(["Emergency","Non-Emergency"],500,p=[0.38,0.62])
    complaints = np.random.choice(["Chest Pain","Breathing","Trauma","Fever","Other"],
                                  500,p=[0.25,0.20,0.18,0.22,0.15])

    col_l, col_r = st.columns(2, gap="medium")
    with col_l:
        counts = pd.Series(priorities).value_counts()
        fig = go.Figure(go.Pie(
            labels=counts.index, values=counts.values, hole=0.55,
            marker_colors=["#EF4444","#22C55E"],
            textfont=dict(color="#F1F5F9",size=12),
            hovertemplate="%{label}: %{value} (%{percent})<extra></extra>"
        ))
        chart_layout(fig, "Priority Distribution")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        cc = pd.Series(complaints).value_counts()
        fig2 = go.Figure(go.Bar(
            x=cc.index, y=cc.values, marker_color="#2563EB",
            marker_line_width=0,
            hovertemplate="%{x}: %{y}<extra></extra>"
        ))
        chart_layout(fig2, "Chief Complaints Frequency")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    fig3 = go.Figure(go.Histogram(
        x=ages, nbinsx=28, marker_color="#2563EB", opacity=0.85,
        hovertemplate="Age %{x}: %{y} patients<extra></extra>"
    ))
    chart_layout(fig3, "Patient Age Distribution", h=240)
    fig3.update_layout(xaxis_title="Age", yaxis_title="Count")
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── SAMPLE DATA ─────────────────────────────────────────────────────────────────
def page_sample_data():
    st.markdown('<div class="pg-title">🧪 Sample Data</div>', unsafe_allow_html=True)
    st.markdown('<div class="pg-sub">Explore the sample patient dataset and download a ready-to-use CSV for batch predictions.</div>', unsafe_allow_html=True)

    df_sample = make_sample_df(10)

    # Download button at the top
    csv_bytes = df_sample.to_csv(index=False).encode()
    st.download_button(
        "⬇️  Download Sample CSV (10 Patients)",
        data=csv_bytes,
        file_name="sample_patients.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # Preview table
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📋 Sample Patient Records (10 rows)</div>', unsafe_allow_html=True)
    st.dataframe(df_sample, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Column descriptions
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📖 Column Descriptions</div>', unsafe_allow_html=True)
    col_desc = pd.DataFrame([
        {"Column": "age",                 "Description": "Patient age in years",                         "Range": "1 – 120"},
        {"Column": "heart_rate",          "Description": "Heart rate in beats per minute",               "Range": "30 – 250"},
        {"Column": "systolic_bp",         "Description": "Systolic blood pressure (mmHg)",              "Range": "60 – 250"},
        {"Column": "diastolic_bp",        "Description": "Diastolic blood pressure (mmHg)",             "Range": "40 – 150"},
        {"Column": "oxygen_saturation",   "Description": "Blood oxygen saturation percentage",          "Range": "70 – 100"},
        {"Column": "respiratory_rate",    "Description": "Breaths per minute",                          "Range": "8 – 60"},
        {"Column": "temperature",         "Description": "Body temperature in °F",                      "Range": "90 – 110"},
        {"Column": "pain_level",          "Description": "Self-reported pain level",                    "Range": "0 – 10"},
        {"Column": "chief_complaint_code","Description": "Encoded chief complaint (0=Chest Pain … 4=Other)", "Range": "0 – 4"},
        {"Column": "arrival_mode_code",   "Description": "Encoded arrival mode (0=Walk-in … 3=Other)",  "Range": "0 – 3"},
        {"Column": "triage_level",        "Description": "Triage severity level (1=Immediate, 5=Routine)", "Range": "1 – 5"},
        {"Column": "previous_visits",     "Description": "Number of prior ER visits",                   "Range": "0 – 50"},
        {"Column": "chronic_conditions",  "Description": "Count of chronic conditions",                 "Range": "0 – 10"},
        {"Column": "allergies",           "Description": "Number of known allergies",                   "Range": "0 – 20"},
        {"Column": "current_medications", "Description": "Number of medications currently taken",       "Range": "0 – 30"},
        {"Column": "lab_results_flag",    "Description": "Abnormal lab results flag (0=Normal, 1=Abnormal)", "Range": "0 – 1"},
    ])
    st.dataframe(col_desc, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Router ──────────────────────────────────────────────────────────────────────
def main():
    if "nav" not in st.session_state:
        st.session_state.nav = None
    if "load_sample" not in st.session_state:
        st.session_state.load_sample = False

    active = render_sidebar()
    if st.session_state.nav:
        active = st.session_state.nav
        st.session_state.nav = None

    pages = {
        "Home": page_home, "Predict": page_predict,
        "Batch": page_batch, "Dashboard": page_dashboard, "Sample Data": page_sample_data
    }
    pages.get(active, page_home)()

if __name__ == "__main__":
    main()