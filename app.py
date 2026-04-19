import streamlit as st
import anthropic
import json
import re

st.set_page_config(
    page_title="TPRM Inherent Risk Simulator",
    page_icon="🛡️",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.main { background-color: #0a0c0f; }

[data-testid="stAppViewContainer"] {
    background-color: #0a0c0f;
    background-image:
        linear-gradient(rgba(79,255,176,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(79,255,176,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { display: none; }

.block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 800px; }

h1, h2, h3 { font-family: 'DM Sans', sans-serif !important; color: #e8eaf0 !important; }

.logo-chip {
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.12em;
    color: #4fffb0;
    background: rgba(79,255,176,0.08);
    border: 1px solid rgba(79,255,176,0.2);
    padding: 4px 10px;
    border-radius: 4px;
    margin-bottom: 8px;
}

.card {
    background: #111318;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

.field-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.08em;
    color: #555b6e;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.field-val { font-size: 14px; color: #e8eaf0; line-height: 1.55; margin-bottom: 1rem; }

.badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 500;
    padding: 2px 8px;
    border-radius: 4px;
    margin: 2px 3px 2px 0;
}
.b-red    { background: rgba(255,92,92,0.12);  color: #ff8080; border: 1px solid rgba(255,92,92,0.2); }
.b-amber  { background: rgba(255,179,71,0.10); color: #ffca7a; border: 1px solid rgba(255,179,71,0.2); }
.b-blue   { background: rgba(77,184,255,0.10); color: #7fcfff; border: 1px solid rgba(77,184,255,0.2); }
.b-gray   { background: rgba(255,255,255,0.05); color: #8b90a0; border: 1px solid rgba(255,255,255,0.08); }

.section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.1em;
    color: #555b6e;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.vendor-name {
    font-size: 22px;
    font-weight: 500;
    color: #e8eaf0;
    letter-spacing: -0.02em;
    margin-bottom: 2px;
}

.result-correct { background: rgba(79,255,176,0.12);  color: #4fffb0; border: 1px solid rgba(79,255,176,0.25); padding: 4px 14px; border-radius: 4px; font-family: 'IBM Plex Mono', monospace; font-size: 12px; }
.result-close   { background: rgba(255,179,71,0.12);  color: #ffca7a; border: 1px solid rgba(255,179,71,0.25);  padding: 4px 14px; border-radius: 4px; font-family: 'IBM Plex Mono', monospace; font-size: 12px; }
.result-wrong   { background: rgba(255,92,92,0.12);   color: #ff7070; border: 1px solid rgba(255,92,92,0.25);   padding: 4px 14px; border-radius: 4px; font-family: 'IBM Plex Mono', monospace; font-size: 12px; }

.feedback-header {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.08em;
    color: #555b6e;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.model-card {
    background: #111318;
    border: 1px solid rgba(79,255,176,0.18);
    border-left: 3px solid #4fffb0;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}

.score-display {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #555b6e;
    letter-spacing: 0.06em;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background-color: #181c23 !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 6px !important;
    color: #e8eaf0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(79,255,176,0.4) !important;
    box-shadow: none !important;
}

div[data-testid="stSelectbox"] > div {
    background-color: #181c23 !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    color: #e8eaf0 !important;
}

.stButton > button {
    background-color: #4fffb0 !important;
    color: #000 !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
    transition: opacity 0.2s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stButton.secondary > button {
    background-color: transparent !important;
    color: #8b90a0 !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
}

label, .stSelectbox label, .stTextArea label, .stTextInput label {
    color: #8b90a0 !important;
    font-size: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stMarkdownContainer"] p { color: #8b90a0; font-size: 14px; }

hr { border-color: rgba(255,255,255,0.08) !important; }

.pip-row { display: flex; gap: 4px; margin-bottom: 1.5rem; }
.pip { width: 28px; height: 6px; border-radius: 3px; display: inline-block; }
.pip-empty   { background: #181c23; border: 1px solid rgba(255,255,255,0.08); }
.pip-correct { background: #4fffb0; }
.pip-close   { background: #ffb347; }
.pip-wrong   { background: #ff5c5c; }

.final-score {
    text-align: center;
    background: #111318;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 3rem 2rem;
    margin-top: 2rem;
}
.final-num {
    font-size: 64px;
    font-weight: 500;
    color: #4fffb0;
    letter-spacing: -0.04em;
    font-family: 'DM Sans', sans-serif;
}
</style>
""", unsafe_allow_html=True)

TOTAL = 10
TIERS = ["Low", "Moderate", "High", "Very High"]
TIER_COLORS = {"Low": "result-correct", "Moderate": "result-close", "High": "result-close", "Very High": "result-wrong"}

# ── session state ──────────────────────────────────────────────────────────────
for k, v in {
    "api_key": "", "started": False, "scenario_num": 0,
    "scenario": None, "phase": "scenario",
    "results": [], "score": 0, "used_types": [],
    "tiers_used": [], "loading": False
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── helpers ───────────────────────────────────────────────────────────────────

def call_claude(prompt: str) -> str:
    client = anthropic.Anthropic(api_key=st.session_state.api_key)
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )
    return msg.content[0].text.strip()


def parse_json(raw: str) -> dict:
    cleaned = re.sub(r"```json|```", "", raw).strip()
    return json.loads(cleaned)


def force_tier() -> str:
    recent = st.session_state.tiers_used[-2:]
    available = [t for t in TIERS if t not in recent]
    import random
    chosen = random.choice(available)
    st.session_state.tiers_used.append(chosen)
    return chosen


def generate_scenario() -> dict:
    tier = force_tier()
    used = ", ".join(st.session_state.used_types) or "none yet"
    prompt = f"""You are a TPRM scenario generator. Generate a realistic vendor intake scenario.

REQUIRED inherent risk tier: {tier}
Previously used service types (DO NOT REPEAT): {used}
Choose from: SaaS application, Call center/BPO, Cloud provider, IT support vendor, Payment-related vendor, Marketing/analytics tool, HR platform, Legal tech, Logistics/supply chain

Respond ONLY with valid JSON (no markdown):
{{
  "vendorName": "fictional company name",
  "serviceType": "one of the categories above",
  "businessPurpose": "2-3 sentence description",
  "dataTypes": ["array","of","data","type","strings"],
  "dataBadgeColors": ["array matching dataTypes: red=critical PII/PHI/financial, amber=sensitive, blue=moderate, gray=low"],
  "accessLevel": "description of access level",
  "hostingEnvironment": "cloud/on-prem/hybrid with detail",
  "userBase": "who is affected and approximate scale",
  "integrations": "what systems they connect to, or None",
  "regulatoryConsiderations": "relevant regulations",
  "correctTier": "{tier}"
}}

Make it realistic and appropriately ambiguous."""
    return parse_json(call_claude(prompt))


def evaluate_response(scenario: dict, tier: str, justification: str, drivers: str) -> dict:
    correct = scenario["correctTier"]
    prompt = f"""You are a TPRM instructor evaluating a student's inherent risk assessment.

VENDOR SCENARIO:
- Vendor: {scenario['vendorName']}
- Service Type: {scenario['serviceType']}
- Purpose: {scenario['businessPurpose']}
- Data Types: {', '.join(scenario['dataTypes'])}
- Access Level: {scenario['accessLevel']}
- Hosting: {scenario['hostingEnvironment']}
- User Base: {scenario['userBase']}
- Integrations: {scenario['integrations']}
- Regulatory: {scenario['regulatoryConsiderations']}

CORRECT TIER: {correct}

STUDENT RESPONSE:
- Selected Tier: {tier}
- Justification: {justification}
- Risk Drivers: {drivers or 'Not provided'}

Respond ONLY with valid JSON (no markdown):
{{
  "whatRight": "2-3 sentences on what student correctly identified",
  "whatMissed": "2-4 sentences on what they missed, be direct and specific",
  "keyDrivers": "bullet list of 3-5 key risk drivers, each line starting with - ",
  "modelAnswer": "3-4 sentence professional model answer from an experienced GRC analyst"
}}

Tone: professional, direct, real-world. Push the student to think deeper."""
    return parse_json(call_claude(prompt))


def score_pips_html() -> str:
    results = st.session_state.results
    total = TOTAL
    pips = ""
    for i in range(total):
        if i < len(results):
            cls = f"pip pip-{results[i]}"
        else:
            cls = "pip pip-empty"
        pips += f'<div class="{cls}"></div>'
    return f'<div class="pip-row">{pips}</div>'


# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown('<div class="logo-chip">GRC TRAINING</div>', unsafe_allow_html=True)
st.markdown("# TPRM Inherent Risk Simulator")
st.markdown("Practice identifying inherent risk tiers across realistic vendor scenarios. Powered by Claude AI.")
st.markdown("---")

# ── API KEY GATE ──────────────────────────────────────────────────────────────
if not st.session_state.started:
    st.markdown("### Enter your Anthropic API Key to begin")
    st.markdown("Your key is used only within this app session. Get a free key at [console.anthropic.com](https://console.anthropic.com).")
    key_input = st.text_input("API Key", type="password", placeholder="sk-ant-...", label_visibility="collapsed")
    if st.button("Start Simulator"):
        if key_input.startswith("sk-"):
            st.session_state.api_key = key_input
            st.session_state.started = True
            st.rerun()
        else:
            st.error("Please enter a valid Anthropic API key (starts with sk-ant-).")
    st.stop()

# ── FINAL SCORE ───────────────────────────────────────────────────────────────
if st.session_state.scenario_num > TOTAL:
    score = st.session_state.score
    msg = "Excellent — strong GRC instincts." if score >= 8 else "Solid performance. Review the edge cases." if score >= 6 else "Keep practicing. TPRM takes pattern recognition."
    st.markdown(f"""
    <div class="final-score">
      <div style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#555b6e;letter-spacing:.1em;margin-bottom:8px;">FINAL SCORE</div>
      <div class="final-num">{score}<span style="font-size:28px;color:#555b6e">/{TOTAL}</span></div>
      <div style="font-size:14px;color:#8b90a0;margin-top:8px;">{msg}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Start New Session"):
        for k in ["scenario_num","scenario","phase","results","score","used_types","tiers_used","loading"]:
            st.session_state[k] = [] if k in ["results","used_types","tiers_used"] else (0 if k in ["scenario_num","score"] else None if k == "scenario" else "scenario" if k == "phase" else False)
        st.rerun()
    st.stop()

# ── LOAD SCENARIO ─────────────────────────────────────────────────────────────
if st.session_state.scenario is None:
    with st.spinner("Generating vendor scenario..."):
        try:
            st.session_state.scenario = generate_scenario()
            st.session_state.scenario_num += 1
            st.session_state.used_types.append(st.session_state.scenario["serviceType"])
            st.session_state.phase = "scenario"
        except Exception as e:
            st.error(f"Error generating scenario: {e}")
            if st.button("Retry"):
                st.rerun()
            st.stop()

s = st.session_state.scenario

# ── SCORE BAR ─────────────────────────────────────────────────────────────────
st.markdown(score_pips_html(), unsafe_allow_html=True)

# ── SCENARIO DISPLAY ──────────────────────────────────────────────────────────
st.markdown(f'<div class="vendor-name">{s["vendorName"]}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="score-display">SCENARIO {st.session_state.scenario_num} OF {TOTAL} &nbsp;·&nbsp; Score: {st.session_state.score}/{len(st.session_state.results)}</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Service overview card
badges = "".join(
    f'<span class="badge b-{(s.get("dataBadgeColors") or ["gray"]*10)[i]}">{d}</span>'
    for i, d in enumerate(s["dataTypes"])
)

st.markdown(f"""
<div class="card">
  <div class="section-label">Service Overview</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem 2rem;">
    <div>
      <div class="field-label">Service Type</div>
      <div class="field-val">{s['serviceType']}</div>
    </div>
    <div>
      <div class="field-label">Business Purpose</div>
      <div class="field-val">{s['businessPurpose']}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="card">
  <div class="section-label">Data &amp; Access Profile</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem 2rem;">
    <div>
      <div class="field-label">Data Types</div>
      <div class="field-val">{badges}</div>
    </div>
    <div>
      <div class="field-label">Access Level</div>
      <div class="field-val">{s['accessLevel']}</div>
    </div>
    <div>
      <div class="field-label">User Base</div>
      <div class="field-val">{s['userBase']}</div>
    </div>
    <div>
      <div class="field-label">Regulatory Considerations</div>
      <div class="field-val">{s['regulatoryConsiderations']}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="card">
  <div class="section-label">Technical Profile</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem 2rem;">
    <div>
      <div class="field-label">Hosting Environment</div>
      <div class="field-val">{s['hostingEnvironment']}</div>
    </div>
    <div>
      <div class="field-label">Integrations</div>
      <div class="field-val">{s['integrations']}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── ASSESSMENT FORM ───────────────────────────────────────────────────────────
if st.session_state.phase == "scenario":
    st.markdown("---")
    st.markdown("### Your Inherent Risk Assessment")

    tier_choice = st.selectbox(
        "1. Select inherent risk tier",
        ["— select —"] + TIERS
    )

    justification = st.text_area(
        "2. Justification — why did you assign this tier?",
        placeholder="Describe your reasoning...",
        height=100
    )

    drivers = st.text_area(
        "3. Key risk drivers you identified",
        placeholder="List the specific factors that influenced your rating...",
        height=80
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        skip = st.button("Skip", key="skip_btn")
    with col2:
        submit = st.button("Submit Assessment →", key="submit_btn")

    if skip:
        st.session_state.results.append("wrong")
        st.session_state.scenario = None
        if st.session_state.scenario_num >= TOTAL:
            st.session_state.scenario_num = TOTAL + 1
        st.rerun()

    if submit:
        if tier_choice == "— select —" or not justification.strip():
            st.error("Please select a tier and provide your justification.")
        else:
            with st.spinner("Evaluating your response..."):
                try:
                    feedback = evaluate_response(s, tier_choice, justification, drivers)
                    correct = s["correctTier"]
                    diff = abs(TIERS.index(tier_choice) - TIERS.index(correct))
                    outcome = "correct" if tier_choice == correct else ("close" if diff == 1 else "wrong")
                    if outcome == "correct":
                        st.session_state.score += 1
                    st.session_state.results.append(outcome)
                    st.session_state.feedback = feedback
                    st.session_state.student_tier = tier_choice
                    st.session_state.phase = "feedback"
                    st.rerun()
                except Exception as e:
                    st.error(f"Error evaluating response: {e}")

# ── FEEDBACK ──────────────────────────────────────────────────────────────────
elif st.session_state.phase == "feedback":
    fb = st.session_state.get("feedback", {})
    correct = s["correctTier"]
    student = st.session_state.get("student_tier", "")
    diff = abs(TIERS.index(student) - TIERS.index(correct))
    outcome = "correct" if student == correct else ("close" if diff == 1 else "wrong")

    verdict_map = {
        "correct": ("Correct — well assessed.", "#4fffb0"),
        "close":   ("Close — one tier off.",    "#ffb347"),
        "wrong":   ("Incorrect — review the analysis below.", "#ff5c5c")
    }
    verdict_text, verdict_color = verdict_map[outcome]

    st.markdown("---")
    st.markdown(f"""
    <div class="card" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
      <div style="font-size:15px;font-weight:500;color:{verdict_color};">{verdict_text}</div>
      <div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap;">
        <div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#555b6e;margin-bottom:3px;">YOU SELECTED</div>
          <span class="{TIER_COLORS.get(student,'result-close')}">{student}</span>
        </div>
        <div>
          <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#555b6e;margin-bottom:3px;">CORRECT TIER</div>
          <span class="result-correct">{correct}</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
      <div class="feedback-header">What you got right</div>
      <p style="color:#8b90a0;font-size:14px;line-height:1.65;">{fb.get('whatRight','')}</p>
    </div>
    <div class="card">
      <div class="feedback-header">What you missed</div>
      <p style="color:#8b90a0;font-size:14px;line-height:1.65;">{fb.get('whatMissed','')}</p>
    </div>
    <div class="card">
      <div class="feedback-header">Key risk drivers</div>
      <p style="color:#8b90a0;font-size:14px;line-height:1.65;white-space:pre-line;">{fb.get('keyDrivers','')}</p>
    </div>
    <div class="model-card">
      <div class="feedback-header" style="color:#4fffb0;">Model answer</div>
      <p style="color:#8b90a0;font-size:14px;line-height:1.65;">{fb.get('modelAnswer','')}</p>
    </div>
    """, unsafe_allow_html=True)

    score_label = f"Score: {st.session_state.score}/{len(st.session_state.results)}"
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f'<div class="score-display" style="padding-top:12px;">{score_label}</div>', unsafe_allow_html=True)
    with col2:
        if st.button("Next Scenario →", key="next_btn"):
            st.session_state.scenario = None
            st.session_state.phase = "scenario"
            if st.session_state.scenario_num >= TOTAL:
                st.session_state.scenario_num = TOTAL + 1
            st.rerun()
