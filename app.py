import streamlit as st
import anthropic
import json
import re
import datetime
import random

st.set_page_config(page_title="TPRM IRQ Simulator | Linguen Enterprises", page_icon="🛡️", layout="centered")

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&family=Source+Serif+4:ital,wght@0,300;0,400;0,500;0,600;1,400&family=DM+Mono:wght@400;500&display=swap');

html,body,[class*="css"]{font-family:'Source Serif 4',Georgia,serif;}
[data-testid="stAppViewContainer"]{background-color:#f5f4f0;}
[data-testid="stHeader"]{background:transparent;}
[data-testid="stToolbar"]{display:none;}
[data-testid="stSidebar"]{display:none;}
.block-container{padding-top:0;padding-bottom:4rem;max-width:860px;}

.top-rule{height:4px;background:#1a2d4a;border-radius:1px;margin-bottom:2rem;}
h1,h2{font-family:'Playfair Display',Georgia,serif!important;color:#1a2d4a!important;}
h3{font-family:'Source Serif 4',serif!important;color:#1a1814!important;}

.company-label{font-family:'DM Mono',monospace;font-size:11px;letter-spacing:.12em;color:#9a948a;text-transform:uppercase;margin-bottom:4px;}
.company-name{font-family:'Playfair Display',serif;font-size:20px;font-weight:600;color:#1a2d4a;margin-bottom:1.25rem;}

.chip{display:inline-block;font-family:'DM Mono',monospace;font-size:10px;letter-spacing:.1em;padding:3px 10px;border-radius:2px;}
.chip-grc{color:#1a2d4a;background:#e8edf4;border:1px solid #c0cbdb;}
.chip-fold1{color:#1a6b45;background:#eaf4ee;border:1px solid #b8ddc8;}
.chip-fold2{color:#1a4a6b;background:#eaf0f4;border:1px solid #b8cedd;}
.chip-B{color:#1a6b45;background:#eaf4ee;border:1px solid #b8ddc8;}
.chip-I{color:#7a4f1a;background:#f4f0ea;border:1px solid #ddc8b8;}
.chip-A{color:#6b1a1a;background:#f4eaea;border:1px solid #ddb8b8;}

.tier{display:inline-block;font-family:'DM Mono',monospace;font-size:11px;font-weight:500;padding:3px 12px;border-radius:2px;}
.tier-Critical{color:#6b1a1a;background:#f4eaea;border:1px solid #ddb8b8;}
.tier-High{color:#7a4f1a;background:#f4f0ea;border:1px solid #ddc8b8;}
.tier-Moderate{color:#1a4a6b;background:#eaf0f4;border:1px solid #b8cedd;}
.tier-Low{color:#1a6b45;background:#eaf4ee;border:1px solid #b8ddc8;}

.vbadge{display:inline-block;font-family:'DM Mono',monospace;font-size:11px;padding:2px 9px;border-radius:2px;margin:2px 3px 2px 0;}
.vb-blue{color:#1a4a6b;background:#eaf0f4;border:1px solid #b8cedd;}
.vb-purple{color:#4a1a6b;background:#f0eaf4;border:1px solid #cdb8dd;}
.vb-amber{color:#7a4f1a;background:#f4f0ea;border:1px solid #ddc8b8;}
.vb-green{color:#1a6b45;background:#eaf4ee;border:1px solid #b8ddc8;}
.vb-gray{color:#5a5650;background:#f0eeea;border:1px solid #ddd9d0;}

.card{background:#fff;border:1px solid #ddd9d0;border-radius:4px;padding:1.5rem;margin-bottom:1rem;box-shadow:0 1px 3px rgba(0,0,0,.04);}
.card-green{background:#eaf4ee;border:1px solid #b8ddc8;border-left:3px solid #1a6b45;border-radius:4px;padding:1.25rem 1.5rem;margin-bottom:1rem;}
.card-blue{background:#eaf0f4;border:1px solid #b8cedd;border-left:3px solid #1a4a6b;border-radius:4px;padding:1.25rem 1.5rem;margin-bottom:1rem;}
.card-amber{background:#f4f0ea;border:1px solid #ddc8b8;border-left:3px solid #7a4f1a;border-radius:4px;padding:1.25rem 1.5rem;margin-bottom:1rem;}
.card-red{background:#f4eaea;border:1px solid #ddb8b8;border-left:3px solid #6b1a1a;border-radius:4px;padding:1.25rem 1.5rem;margin-bottom:1rem;}
.card-navy{background:#1a2d4a;border-radius:4px;padding:1.5rem;margin-bottom:1rem;}

.flabel{font-family:'DM Mono',monospace;font-size:10px;letter-spacing:.08em;color:#9a948a;text-transform:uppercase;margin-bottom:4px;}
.fval{font-size:14px;color:#1a1814;line-height:1.55;margin-bottom:1rem;}
.slabel{font-family:'DM Mono',monospace;font-size:10px;letter-spacing:.1em;color:#9a948a;text-transform:uppercase;margin-bottom:.75rem;}

.vendor-name{font-family:'Playfair Display',serif;font-size:24px;font-weight:600;color:#1a2d4a;letter-spacing:-.01em;margin-bottom:2px;}
.score-line{font-family:'DM Mono',monospace;font-size:11px;color:#9a948a;letter-spacing:.06em;}

.result-banner{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;}
.verdict{font-family:'Playfair Display',serif;font-size:16px;font-weight:500;}
.tier-compare{display:flex;gap:16px;flex-wrap:wrap;}
.tier-compare-item{text-align:right;}
.tier-compare-label{font-family:'DM Mono',monospace;font-size:10px;color:#9a948a;margin-bottom:3px;}

.fb-header{font-family:'DM Mono',monospace;font-size:10px;letter-spacing:.08em;color:#9a948a;text-transform:uppercase;margin-bottom:8px;}
.err-section{margin-bottom:10px;}
.err-tag{font-family:'DM Mono',monospace;font-size:10px;letter-spacing:.06em;margin-bottom:4px;}
.err-item{font-size:13px;color:#5a5650;padding:2px 0;}

.final-wrap{text-align:center;background:#1a2d4a;border-radius:4px;padding:3rem 2rem;margin-top:2rem;}
.final-num{font-family:'Playfair Display',serif;font-size:72px;font-weight:600;color:#fff;letter-spacing:-.02em;line-height:1;}
.final-sub{font-size:13px;color:rgba(255,255,255,.5);font-family:'DM Mono',monospace;margin-top:4px;}
.final-msg{font-size:15px;color:rgba(255,255,255,.75);margin-top:12px;font-style:italic;}

.pip-row{display:flex;gap:5px;margin-bottom:1.5rem;}
.pip{width:32px;height:5px;border-radius:1px;display:inline-block;}
.pip-empty{background:#e8e5df;border:1px solid #ddd9d0;}
.pip-correct{background:#1a6b45;}
.pip-close{background:#c8880a;}
.pip-wrong{background:#b83030;}

.student-row{display:flex;align-items:center;justify-content:space-between;padding:9px 0;border-bottom:1px solid #ddd9d0;font-size:13px;}
.student-row:last-child{border-bottom:none;}
.ref-item{padding:10px 0;border-bottom:1px solid #ddd9d0;}
.ref-item:last-child{border-bottom:none;}
.ref-title{font-size:13px;color:#1a1814;font-weight:500;margin-bottom:3px;}
.ref-desc{font-size:12px;color:#9a948a;line-height:1.5;}

.use-case-quote{font-size:15px;color:#5a5650;line-height:1.75;font-style:italic;border-left:3px solid #1a2d4a;padding:.75rem 1rem;margin-bottom:1rem;background:#f0eeea;border-radius:0 3px 3px 0;}

div[data-testid="stTextInput"] input,div[data-testid="stTextArea"] textarea{
  background-color:#fff!important;border:1px solid #c8c3b8!important;border-radius:3px!important;
  color:#1a1814!important;font-family:'Source Serif 4',serif!important;box-shadow:inset 0 1px 2px rgba(0,0,0,.04)!important;
}
div[data-testid="stTextInput"] input:focus,div[data-testid="stTextArea"] textarea:focus{border-color:#1a2d4a!important;box-shadow:0 0 0 3px rgba(26,45,74,.08)!important;}
div[data-testid="stSelectbox"]>div{background-color:#fff!important;border:1px solid #c8c3b8!important;border-radius:3px!important;color:#1a1814!important;}

.stButton>button{
  background-color:#1a2d4a!important;color:#fff!important;border:none!important;border-radius:3px!important;
  font-family:'Source Serif 4',serif!important;font-weight:500!important;padding:.5rem 1.5rem!important;
}
.stButton>button:hover{background-color:#243d62!important;}

label,.stSelectbox label,.stTextArea label,.stTextInput label{
  color:#5a5650!important;font-size:13px!important;font-family:'Source Serif 4',serif!important;font-weight:500!important;
}
[data-testid="stMarkdownContainer"] p{color:#5a5650;font-size:14px;}
hr{border-color:#ddd9d0!important;}

.dash-stat{background:#fff;border:1px solid #ddd9d0;border-radius:4px;padding:1.25rem;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.04);}
.dash-num{font-family:'Playfair Display',serif;font-size:32px;font-weight:600;color:#1a2d4a;}
.dash-label{font-family:'DM Mono',monospace;font-size:10px;color:#9a948a;letter-spacing:.08em;text-transform:uppercase;margin-top:4px;}

.mode-card-wrap{background:#fff;border:2px solid #ddd9d0;border-radius:4px;padding:1.25rem;margin-bottom:.5rem;box-shadow:0 1px 3px rgba(0,0,0,.04);}
.mode-card-wrap.sel{border-color:#1a2d4a;box-shadow:0 0 0 3px rgba(26,45,74,.08);}
.mode-tag-txt{font-family:'DM Mono',monospace;font-size:10px;letter-spacing:.08em;margin-bottom:6px;}
.mode-title-txt{font-family:'Playfair Display',serif;font-size:15px;font-weight:500;color:#1a2d4a;margin-bottom:5px;}
.mode-desc-txt{font-size:12px;color:#9a948a;line-height:1.55;}

.irq-field-block{background:#f0eeea;border:1px solid #ddd9d0;border-radius:3px;padding:.6rem .9rem;margin-bottom:.5rem;}
.irq-q{font-size:12px;color:#9a948a;font-family:'DM Mono',monospace;letter-spacing:.04em;margin-bottom:2px;}
.irq-a{font-size:14px;color:#1a1814;}
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ──────────────────────────────────────────────────────────────────
TOTAL = 3
TIERS = ["Low", "Moderate", "High", "Critical"]

VENDOR_TYPES = [
    "Cloud SaaS", "Cloud PaaS", "Cloud IaaS",
    "Generative AI", "Hardware", "On-Premises Software",
    "Professional Services", "Service Outsourcing"
]

DIFFICULTY_SETTINGS = {
    "Beginner":     "Risk signals are clear and direct. Good for first exposure to TPRM concepts.",
    "Intermediate": "Some conflicting signals require weighing multiple factors.",
    "Advanced":     "Edge cases, misleading details, regulatory nuance. No easy answers.",
}

TIER_DEFS = """
RISK TIER DEFINITIONS:
- LOW: Minimal/no sensitive data, no regulatory exposure, non-critical, no system access.
- MODERATE: Limited sensitive data (internal only), some regulatory awareness, limited integrations, moderate business impact.
- HIGH: Significant PII/PHI/financial data, meaningful regulatory scope (GDPR/HIPAA/PCI/SOX), production access, business-critical. External customer data involved.
- CRITICAL: Highly sensitive data (PHI, financial account data, credentials), privileged/production access, critical regulatory obligations, broad external impact, or single point of failure.
"""

VT_GUIDANCE = """
VENDOR TYPE RISK DRIVERS:
- Cloud SaaS: data hosted, user scope, integrations to core systems.
- Cloud PaaS: what's built on it, developer access, production pipeline exposure.
- Cloud IaaS: infrastructure criticality, network access, data residency, tenant isolation.
- Generative AI: data ingested/prompted, confidentiality, IP leakage, EU AI Act, model training on company data.
- Hardware: physical access, firmware supply chain, devices handling sensitive data (POS/medical/HSMs).
- On-Premises Software: installation footprint in company network, vendor remote access for support/updates, patch dependency, access to sensitive internal data stores.
- Professional Services: access during engagement, data reviewed, NDA scope, personnel vetting.
- Service Outsourcing: data volume, regulatory scope, geographic exposure, subprocessor chain.
"""

DATA_CLASS_OPTS = ["Internal", "Confidential", "Customer Confidential", "Confidential Sensitive"]
ACCESS_OPTS     = ["Yes", "No"]
YESNO_UNK       = ["Yes", "No", "Unknown"]
RECORD_OPTS     = ["0", "1–1,000", "1,001–10,000", "10,001–100,000", "100,001–500,000", "500,001–1,000,000", "1,000,000+"]
RISK_OPTS       = ["Low", "Medium", "High"]

REFERENCE_MATERIALS = [
    {"title": "NIST SP 800-161 — Supply Chain Risk Management", "desc": "Federal framework for managing cybersecurity risks in the supply chain.", "url": "https://csrc.nist.gov/publications/detail/sp/800-161/rev-1/final"},
    {"title": "ISO 27001 — Information Security Management", "desc": "International standard for infosec. Annex A covers third-party relationship controls.", "url": "https://www.iso.org/standard/27001"},
    {"title": "FFIEC Third-Party Risk Guidance", "desc": "Banking regulator guidance on managing third-party relationships.", "url": "https://www.ffiec.gov/press/PDF/FFIEC_Third_Party_Relationships_Guidance.pdf"},
    {"title": "OCC Third-Party Relationships (2023)", "desc": "Updated OCC bulletin covering risk-based approach to third-party oversight.", "url": "https://www.occ.gov/news-issuances/bulletins/2023/bulletin-2023-17.html"},
    {"title": "GDPR Article 28 — Processor Obligations", "desc": "Legal basis for vendor data processing agreements when EU personal data is involved.", "url": "https://gdpr-info.eu/art-28-gdpr/"},
    {"title": "EU AI Act — High-Risk AI Systems", "desc": "EU regulation on AI risk classification. Critical for Generative AI vendor assessments.", "url": "https://artificialintelligenceact.eu/"},
    {"title": "SOC 2 Trust Services Criteria", "desc": "AICPA framework for evaluating vendor security, availability, and confidentiality controls.", "url": "https://www.aicpa-cima.com/resources/landing/system-and-organization-controls-soc-suite-of-services"},
    {"title": "PCI DSS v4.0 — Requirement 12.8", "desc": "Payment card industry requirements for managing third-party service providers.", "url": "https://www.pcisecuritystandards.org/document_library/"},
    {"title": "HIPAA Business Associate Requirements", "desc": "HHS guidance on PHI handling by business associates.", "url": "https://www.hhs.gov/hipaa/for-professionals/covered-entities/index.html"},
]

# ── SESSION STATE ──────────────────────────────────────────────────────────────
defaults = {
    "page": "setup", "mode": None, "difficulty": None, "student_name": "",
    "scenario_num": 0, "scenario": None, "phase": "scenario",
    "results": [], "result_log": [], "score": 0,
    "used_types": [], "used_tiers": [],
    "hint": None, "hint_used": False,
    "session_history": [], "dash_auth": False,
    "feedback": None, "student_tier": "",
    "completed_scenarios": [],  # stores full scenario + feedback for end review
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── API KEY (from Streamlit secrets — no student input needed) ─────────────────
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except Exception:
    st.error("⚠️ ANTHROPIC_API_KEY not configured in Streamlit secrets.")
    st.stop()

try:
    INSTRUCTOR_PASS      = st.secrets.get("INSTRUCTOR_PASSWORD", "tprm2024")
    INSTRUCTOR_MODE_PASS = st.secrets.get("INSTRUCTOR_MODE_PASSWORD", "instructor")
except Exception:
    INSTRUCTOR_PASS      = "tprm2024"
    INSTRUCTOR_MODE_PASS = "instructor"

# ── HELPERS ────────────────────────────────────────────────────────────────────
def call_claude(prompt: str, max_tokens: int = 1400) -> str:
    client = anthropic.Anthropic(api_key=api_key)
    msg = client.messages.create(
        model="claude-sonnet-4-5", max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )
    return msg.content[0].text.strip()

def parse_json(raw: str) -> dict:
    return json.loads(re.sub(r"```json|```", "", raw).strip())

def next_params():
    avT = [t for t in VENDOR_TYPES if t not in st.session_state.used_types] or VENDOR_TYPES
    recent = st.session_state.used_tiers[-2:]
    avR = [t for t in TIERS if t not in recent] or TIERS
    return random.choice(avT), random.choice(avR)

def tier_chip(t: str) -> str:
    cls = {"Critical": "tier-Critical", "High": "tier-High", "Moderate": "tier-Moderate", "Low": "tier-Low"}.get(t, "tier-Low")
    return f'<span class="{cls}">{t.upper()}</span>'

def vt_badge(vt: str) -> str:
    cls = {"Cloud SaaS":"vb-blue","Cloud PaaS":"vb-blue","Cloud IaaS":"vb-blue",
           "Generative AI":"vb-purple","Hardware":"vb-amber","On-Premises Software":"vb-green",
           "Professional Services":"vb-gray","Service Outsourcing":"vb-gray"}.get(vt,"vb-gray")
    return f'<span class="vbadge {cls}">{vt}</span>'

def pip_row_html() -> str:
    pips = ""
    for i in range(TOTAL):
        if i < len(st.session_state.results):
            cls = {"correct":"pip-correct","close":"pip-close","wrong":"pip-wrong"}.get(st.session_state.results[i],"pip-empty")
        else:
            cls = "pip-empty"
        pips += f'<div class="pip {cls}"></div>'
    return f'<div class="pip-row">{pips}</div>'

def diff_chip(d: str) -> str:
    cls = {"Beginner":"chip-B","Intermediate":"chip-I","Advanced":"chip-A"}.get(d,"chip-B")
    return f'<span class="chip {cls}">{d.upper()}</span>'

def save_session():
    if not st.session_state.result_log:
        return
    st.session_state.session_history.append({
        "student":    st.session_state.student_name or "Anonymous",
        "mode":       st.session_state.mode,
        "difficulty": st.session_state.difficulty,
        "score":      st.session_state.score,
        "total":      TOTAL,
        "pct":        round(st.session_state.score / TOTAL * 100),
        "results":    list(st.session_state.results),
        "log":        list(st.session_state.result_log),
        "timestamp":  datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    })

def reset_sim():
    for k in ["scenario_num","scenario","phase","results","result_log","score",
              "used_types","used_tiers","hint","hint_used","feedback","student_tier",
              "completed_scenarios"]:
        st.session_state[k] = [] if isinstance(defaults.get(k), list) else defaults.get(k)

# ── SCENARIO GENERATORS ────────────────────────────────────────────────────────
def generate_fold1(vt: str, tier: str, diff: str) -> dict:
    ambig = {"Beginner":"Risk signals obvious from context.","Intermediate":"Some ambiguity — infer risk factors.","Advanced":"Deliberately vague. Regulatory implications not obvious."}
    prompt = f"""You are a TPRM scenario generator for GRC training.
{TIER_DEFS}{VT_GUIDANCE}
Generate a BUSINESS USE CASE a business owner would submit when requesting a new vendor.
Required inherent risk tier: {tier} | Vendor type: {vt} | Difficulty: {diff} — {ambig[diff]}
Respond ONLY in valid JSON (no markdown):
{{"vendorName":"fictional realistic name","vendorType":"{vt}","useCaseTitle":"short title",
"useCaseDescription":"3-5 sentence narrative as business owner — embed risk factors naturally",
"businessUnit":"e.g. Marketing/Finance/HR","expectedUserCount":"approximate count","goLiveTimeline":"e.g. Q3 2025",
"correctTier":"{tier}",
"correctIRQAnswers":{{"use_plan":"ideal answer","nonpublic_data":"Yes or No","data_scope":"if Yes what data",
"data_classification":"Internal|Confidential|Customer Confidential|Confidential Sensitive",
"service_type":"correct vendor type","pii":"Yes or No","record_count":"appropriate range",
"phi":"Yes or No","internal_access":"Yes or No","cloud_storage":"Yes|No|Unknown",
"ai_use":"Yes|No|Unknown","conf_risk":"Low|Medium|High","int_risk":"Low|Medium|High","avail_risk":"Low|Medium|High"}},
"hintText":"one focused hint without revealing answer",
"keyLearning":"2-3 sentence core TPRM lesson",
"evaluationNotes":"guidance for evaluating this IRQ"}}"""
    return parse_json(call_claude(prompt))

def generate_fold2(vt: str, tier: str, diff: str) -> dict:
    has_errors = random.random() < 0.55
    ambig = {"Beginner":"Errors if any are obvious.","Intermediate":"Errors require domain knowledge.","Advanced":"Subtle errors requiring deep expertise."}
    err_instr = "Include 1-3 realistic errors (wrong data classification, incorrect PII/PHI, wrong record count, understated risks). Set hasErrors true." if has_errors else "Fill accurately. Set hasErrors false, errorList []."
    prompt = f"""You are a TPRM scenario generator for GRC training.
{TIER_DEFS}{VT_GUIDANCE}
Generate a PRE-FILLED IRQ submitted by a business owner.
Required risk tier: {tier} | Vendor type: {vt} | Difficulty: {diff} — {ambig[diff]}
Error instruction: {err_instr}
Respond ONLY in valid JSON (no markdown):
{{"vendorName":"realistic fictional name","vendorType":"{vt}","businessUnit":"e.g. Finance",
"usePlan":"how the business owner plans to use this vendor",
"nonpublicData":"Yes or No","dataScope":"data in scope if Yes else N/A",
"dataClassification":"Internal|Confidential|Customer Confidential|Confidential Sensitive",
"pii":"Yes or No","recordCount":"0|1–1,000|1,001–10,000|10,001–100,000|100,001–500,000|500,001–1,000,000|1,000,000+",
"phi":"Yes or No","internalAccess":"Yes or No","cloudStorage":"Yes|No|Unknown","aiUse":"Yes|No|Unknown",
"confRisk":"Low|Medium|High","intRisk":"Low|Medium|High","availRisk":"Low|Medium|High",
"contactName":"fictional name","contactEmail":"fictional email","expectedUserCount":"scale",
"correctTier":"{tier}","hasErrors":{str(has_errors).lower()},"errorList":["errors if any"],
"hintText":"one hint toward correct tier","keyLearning":"2-3 sentence TPRM lesson"}}"""
    return parse_json(call_claude(prompt))

# ── EVALUATORS ─────────────────────────────────────────────────────────────────
def evaluate_fold1(scenario: dict, answers: dict, diff: str) -> dict:
    c = scenario.get("correctIRQAnswers", {})
    prompt = f"""You are a TPRM instructor evaluating a student's IRQ as business owner.
{TIER_DEFS}
USE CASE: {scenario['vendorName']} ({scenario['vendorType']}) — {scenario['useCaseTitle']}
{scenario['useCaseDescription']}
Business Unit: {scenario['businessUnit']} | Users: {scenario['expectedUserCount']}
CORRECT: use_plan={c.get('use_plan')} | nonpublic={c.get('nonpublic_data')} | scope={c.get('data_scope')}
class={c.get('data_classification')} | pii={c.get('pii')} | records={c.get('record_count')} | phi={c.get('phi')}
internal_access={c.get('internal_access')} | cloud={c.get('cloud_storage')} | ai={c.get('ai_use')}
conf={c.get('conf_risk')} | int={c.get('int_risk')} | avail={c.get('avail_risk')}
Correct Tier: {scenario['correctTier']} | Eval Notes: {scenario.get('evaluationNotes','')}
STUDENT: use_plan={answers.get('use_plan')} | nonpublic={answers.get('nonpublic_data')} | scope={answers.get('data_scope')}
class={answers.get('data_classification')} | type={answers.get('service_type')} | pii={answers.get('pii')}
records={answers.get('record_count')} | phi={answers.get('phi')} | internal={answers.get('internal_access')}
cloud={answers.get('cloud_storage')} | ai={answers.get('ai_use')}
conf={answers.get('conf_risk')} | int={answers.get('int_risk')} | avail={answers.get('avail_risk')}
contact={answers.get('contact_name')} / {answers.get('contact_email')} | Difficulty: {diff}
Respond ONLY in valid JSON (no markdown):
{{"impliedTier":"Low|Moderate|High|Critical","tierMatch":true,"irqQuality":"Excellent|Good|Needs Improvement|Incomplete",
"whatRight":"2-3 sentences","whatMissed":"2-4 sentences","criticalMisses":["list"],
"modelIRQ":{{"use_plan":"ideal","nonpublic_data":"ideal","data_scope":"ideal","data_classification":"ideal",
"pii":"ideal","record_count":"ideal","phi":"ideal","internal_access":"ideal","cloud_storage":"ideal",
"ai_use":"ideal","conf_risk":"ideal","int_risk":"ideal","avail_risk":"ideal"}},
"modelAnswer":"3-4 sentence professional answer","deeperDive":"1-2 sentences"}}"""
    return parse_json(call_claude(prompt, 1600))

def evaluate_fold2(scenario: dict, tier: str, issues: str, diff: str) -> dict:
    prompt = f"""You are a TPRM instructor evaluating a student's IRQ review.
{TIER_DEFS}
IRQ: {scenario['vendorName']} ({scenario['vendorType']}) | Unit: {scenario['businessUnit']}
usePlan={scenario.get('usePlan')} | nonpublic={scenario.get('nonpublicData')} | scope={scenario.get('dataScope')}
class={scenario.get('dataClassification')} | pii={scenario.get('pii')} | records={scenario.get('recordCount')}
phi={scenario.get('phi')} | internal={scenario.get('internalAccess')} | cloud={scenario.get('cloudStorage')}
ai={scenario.get('aiUse')} | conf={scenario.get('confRisk')} | int={scenario.get('intRisk')} | avail={scenario.get('availRisk')}
contact={scenario.get('contactName')} / {scenario.get('contactEmail')} | users={scenario.get('expectedUserCount')}
hasErrors={scenario['hasErrors']} | actualErrors={json.dumps(scenario.get('errorList',[]))}
Correct Tier: {scenario['correctTier']} | Difficulty: {diff}
STUDENT: Tier={tier} | Issues={issues or 'None'}
Respond ONLY in valid JSON (no markdown):
{{"tierCorrect":true,"tierFeedback":"2-3 sentences","errorsCorrectlyIdentified":["list"],
"errorsMissed":["list"],"falsePositives":["list"],"irqReviewQuality":"Thorough|Adequate|Superficial|Missed Critical Issues",
"whatRight":"2-3 sentences","whatMissed":"2-4 sentences","keyDrivers":"3-5 drivers, each line starting with -",
"modelAnswer":"3-4 sentence professional answer","deeperDive":"1-2 sentences"}}"""
    return parse_json(call_claude(prompt, 1600))

def compute_outcome_fold1(fb: dict) -> str:
    q = fb.get("irqQuality","Needs Improvement")
    tm = fb.get("tierMatch", False)
    if q == "Excellent" and tm: return "correct" if not st.session_state.hint_used else "close"
    if q == "Good" or tm:       return "close"
    return "wrong"

def compute_outcome_fold2(fb: dict) -> str:
    tc = fb.get("tierCorrect", False)
    rq = fb.get("irqReviewQuality","Superficial")
    if tc and rq in ("Thorough","Adequate"): return "correct" if not st.session_state.hint_used else "close"
    if tc or rq == "Adequate":               return "close"
    return "wrong"

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SETUP
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "setup":
    st.markdown('<div class="top-rule"></div>', unsafe_allow_html=True)
    st.markdown('<span class="chip chip-grc">GRC TRAINING</span>', unsafe_allow_html=True)
    st.markdown('<div class="company-label">Presented by</div><div class="company-name">Linguen Enterprises LLC</div>', unsafe_allow_html=True)
    st.markdown("# TPRM IRQ Simulator")
    st.markdown("*A dual-mode simulator for practicing Inherent Risk Questionnaire skills.*")
    st.markdown("---")

    name = st.text_input("Your Name", placeholder="e.g. Jordan Smith", value=st.session_state.student_name)
    st.session_state.student_name = name

    st.markdown("---")
    st.markdown("**Session Mode**")
    col1, col2 = st.columns(2)
    with col1:
        sel1 = st.session_state.mode == "fold1"
        st.markdown(f'<div class="mode-card-wrap {"sel" if sel1 else ""}"><div class="mode-tag-txt" style="color:#1a6b45;">FOLD 1 — IRQ AUTHOR</div><div class="mode-title-txt">Fill Out the IRQ</div><div class="mode-desc-txt">You\'re the business owner. Given a vendor use case, complete the IRQ fields to reflect the real risk picture.</div></div>', unsafe_allow_html=True)
        if st.button("Select Fold 1", key="sel_f1"):
            st.session_state.mode = "fold1"; st.rerun()
    with col2:
        sel2 = st.session_state.mode == "fold2"
        st.markdown(f'<div class="mode-card-wrap {"sel" if sel2 else ""}"><div class="mode-tag-txt" style="color:#1a4a6b;">FOLD 2 — IRQ REVIEWER</div><div class="mode-title-txt">Review & Rate</div><div class="mode-desc-txt">A business owner submitted an IRQ. Review it, assign the inherent risk tier, and flag any errors or omissions.</div></div>', unsafe_allow_html=True)
        if st.button("Select Fold 2", key="sel_f2"):
            st.session_state.mode = "fold2"; st.rerun()

    with st.expander("🔒 Instructor: Lock mode for all students"):
        ip = st.text_input("Instructor password", type="password", key="mode_pw")
        forced = st.selectbox("Force mode", ["— let student choose —","Fold 1 — IRQ Author","Fold 2 — IRQ Reviewer"])
        if st.button("Apply", key="apply_mode"):
            if ip == INSTRUCTOR_MODE_PASS:
                if "Fold 1" in forced: st.session_state.mode = "fold1"
                elif "Fold 2" in forced: st.session_state.mode = "fold2"
                st.success("Mode applied."); st.rerun()
            else:
                st.error("Incorrect password.")

    st.markdown("---")
    st.markdown("**Difficulty**")
    dcols = st.columns(3)
    for i, (diff, desc) in enumerate(DIFFICULTY_SETTINGS.items()):
        with dcols[i]:
            sel = st.session_state.difficulty == diff
            border = "#1a2d4a" if sel else "#ddd9d0"
            st.markdown(f'<div style="background:#fff;border:{"2px" if sel else "1px"} solid {border};border-radius:4px;padding:1rem;min-height:95px;box-shadow:{"0 0 0 3px rgba(26,45,74,.08)" if sel else "0 1px 2px rgba(0,0,0,.03)"};"><div style="font-family:\'Playfair Display\',serif;font-size:14px;font-weight:500;color:#1a2d4a;margin-bottom:4px;">{diff}</div><div style="font-size:11px;color:#9a948a;line-height:1.5;">{desc}</div></div>', unsafe_allow_html=True)
            if st.button(f"Select {diff}", key=f"d_{diff}"):
                st.session_state.difficulty = diff; st.rerun()

    st.markdown("---")
    c1, c2, c3 = st.columns([2,1,1])
    with c1:
        if st.button("Start Session →"):
            if not st.session_state.mode:       st.error("Please select a mode.")
            elif not st.session_state.difficulty: st.error("Please select a difficulty.")
            else:
                reset_sim(); st.session_state.page = "sim"; st.rerun()
    with c2:
        if st.button("Dashboard"):
            st.session_state.page = "dashboard"; st.rerun()
    with c3:
        if st.button("References"):
            st.session_state.page = "references"; st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SIMULATOR
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "sim":
    diff = st.session_state.difficulty
    mode = st.session_state.mode
    mode_lbl = "IRQ Author" if mode == "fold1" else "IRQ Reviewer"

    st.markdown('<div class="top-rule"></div>', unsafe_allow_html=True)
    ch1, ch2 = st.columns([3,1])
    with ch1:
        st.markdown(f'<span class="chip chip-grc">GRC TRAINING</span> <span class="chip {"chip-fold1" if mode=="fold1" else "chip-fold2"}">{mode_lbl.upper()}</span> {diff_chip(diff)}', unsafe_allow_html=True)
        st.markdown('<div style="font-family:\'Playfair Display\',serif;font-size:20px;font-weight:600;color:#1a2d4a;margin-top:4px;">TPRM IRQ Simulator</div>', unsafe_allow_html=True)
    with ch2:
        if st.button("← Exit"):
            save_session(); st.session_state.page = "setup"; st.rerun()

    # ── FINAL SCORE ────────────────────────────────────────────────────────────
    if st.session_state.scenario_num > TOTAL:
        save_session()
        score = st.session_state.score
        pct   = round(score / TOTAL * 100)
        msg   = "Excellent — strong GRC instincts." if score == TOTAL else "Solid performance. Review the breakdowns below." if score >= 2 else "Keep practicing. Review each scenario carefully below."

        # Score banner
        st.markdown(f'<div class="final-wrap"><div style="font-family:\'DM Mono\',monospace;font-size:11px;color:rgba(255,255,255,.5);letter-spacing:.1em;margin-bottom:8px;">SESSION COMPLETE · {mode_lbl.upper()} · {diff.upper()}</div><div class="final-num">{score}<span style="font-size:28px;opacity:.4">/{TOTAL}</span></div><div class="final-sub">{pct}% accuracy</div><div class="final-msg">{msg}</div></div>', unsafe_allow_html=True)

        # ── SCENARIO REVIEW ────────────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Session Review")
        st.markdown('<p style="color:#9a948a;font-size:13px;margin-bottom:1.5rem;font-style:italic;">Full breakdown of each scenario — your responses, what you missed, and the model answer.</p>', unsafe_allow_html=True)

        for i, entry in enumerate(st.session_state.completed_scenarios):
            sc  = entry["scenario"]
            fb  = entry["feedback"]
            oc  = entry["outcome"]
            oc_color = {"correct":"#1a6b45","close":"#c8880a","wrong":"#b83030"}.get(oc,"#9a948a")
            oc_label = {"correct":"✓ Correct","close":"~ Close","wrong":"✗ Incorrect"}.get(oc,"—")

            with st.expander(f"Scenario {i+1} — {sc.get('vendorName','')} · {sc.get('vendorType','')} · {tier_chip(sc.get('correctTier',''))}  |  {oc_label}", expanded=False):
                # Scenario summary
                if entry["mode"] == "fold1":
                    st.markdown(f'<div class="card"><div class="slabel">Use Case</div><div style="font-family:\'Playfair Display\',serif;font-size:15px;font-weight:500;color:#1a2d4a;margin-bottom:8px;">{sc.get("useCaseTitle","")}</div><div class="use-case-quote">"{sc.get("useCaseDescription","")}"</div><div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:.75rem;"><div><div class="flabel">Business Unit</div><div class="fval">{sc.get("businessUnit","")}</div></div><div><div class="flabel">Users</div><div class="fval">{sc.get("expectedUserCount","")}</div></div><div><div class="flabel">Correct Tier</div><div class="fval">{tier_chip(sc.get("correctTier",""))}</div></div></div></div>', unsafe_allow_html=True)

                    # Student's IRQ answers
                    answers = entry.get("answers",{})
                    ans_rows = "".join(f'<div class="irq-field-block"><div class="irq-q">{k.replace("_"," ").upper()}</div><div class="irq-a">{v or "—"}</div></div>' for k,v in answers.items() if v and v not in ("— select —","N/A",""))
                    st.markdown(f'<div class="card"><div class="slabel">Your IRQ Submission</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:.5rem;">{ans_rows}</div></div>', unsafe_allow_html=True)

                    # Result
                    st.markdown(f'<div class="card result-banner"><div><div class="verdict" style="color:{oc_color};">{oc_label}</div><div style="font-size:12px;color:#9a948a;margin-top:3px;">IRQ Quality: {fb.get("irqQuality","")}</div></div><div class="tier-compare"><div class="tier-compare-item"><div class="tier-compare-label">YOUR IRQ IMPLIED</div>{tier_chip(fb.get("impliedTier",""))}</div><div class="tier-compare-item"><div class="tier-compare-label">CORRECT TIER</div>{tier_chip(sc.get("correctTier",""))}</div></div></div>', unsafe_allow_html=True)

                else:  # fold2
                    yn = lambda v: f'<span style="color:{"#1a6b45" if v=="Yes" else "#5a5650"};">{v or "—"}</span>'
                    rc = lambda v: {"High":"#6b1a1a","Medium":"#7a4f1a","Low":"#1a6b45"}.get(v,"#5a5650")
                    st.markdown(f'<div class="card"><div class="slabel">Pre-Filled IRQ You Reviewed</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:.5rem 2rem;"><div><div class="flabel">Vendor Type</div><div class="fval">{sc.get("vendorType","")}</div></div><div><div class="flabel">Business Unit</div><div class="fval">{sc.get("businessUnit","")}</div></div><div style="grid-column:span 2;"><div class="flabel">Use Plan</div><div class="fval">{sc.get("usePlan","—")}</div></div><div><div class="flabel">PII</div><div class="fval">{yn(sc.get("pii"))}</div></div><div><div class="flabel">PHI</div><div class="fval">{yn(sc.get("phi"))}</div></div><div><div class="flabel">Records at risk</div><div class="fval">{sc.get("recordCount","—")}</div></div><div><div class="flabel">Data classification</div><div class="fval">{sc.get("dataClassification","—")}</div></div><div><div class="flabel">Conf risk</div><div class="fval" style="color:{rc(sc.get("confRisk"))};">{sc.get("confRisk","—")}</div></div><div><div class="flabel">Correct Tier</div><div class="fval">{tier_chip(sc.get("correctTier",""))}</div></div></div></div>', unsafe_allow_html=True)

                    st.markdown(f'<div class="card result-banner"><div><div class="verdict" style="color:{oc_color};">{oc_label}</div><div style="font-size:12px;color:#9a948a;margin-top:3px;">Review Quality: {fb.get("irqReviewQuality","")}</div></div><div class="tier-compare"><div class="tier-compare-item"><div class="tier-compare-label">YOU ASSIGNED</div>{tier_chip(entry.get("student_tier",""))}</div><div class="tier-compare-item"><div class="tier-compare-label">CORRECT TIER</div>{tier_chip(sc.get("correctTier",""))}</div></div></div>', unsafe_allow_html=True)

                    # Error analysis
                    caught = fb.get("errorsCorrectlyIdentified",[])
                    missed = fb.get("errorsMissed",[])
                    fp     = fb.get("falsePositives",[])
                    if not sc.get("hasErrors") and not missed:
                        err_html = '<div style="font-size:13px;color:#1a6b45;">✓ This IRQ was clean — no errors to find.</div>'
                    else:
                        err_html = ""
                        if caught: err_html += f'<div class="err-section"><div class="err-tag" style="color:#1a6b45;">✓ CAUGHT</div>{"".join(f"<div class=\'err-item\'>{e}</div>" for e in caught)}</div>'
                        if missed: err_html += f'<div class="err-section"><div class="err-tag" style="color:#b83030;">✗ MISSED</div>{"".join(f"<div class=\'err-item\'>{e}</div>" for e in missed)}</div>'
                        if fp:     err_html += f'<div class="err-section"><div class="err-tag" style="color:#c8880a;">⚡ FALSE FLAGS</div>{"".join(f"<div class=\'err-item\'>{e}</div>" for e in fp)}</div>'
                    st.markdown(f'<div class="card"><div class="slabel">IRQ Error Analysis</div>{err_html}</div>', unsafe_allow_html=True)

                # Shared feedback blocks
                st.markdown(f'<div class="card"><div class="fb-header">What you got right</div><p style="color:#5a5650;font-size:14px;line-height:1.65;">{fb.get("whatRight","")}</p></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card"><div class="fb-header">What you missed</div><p style="color:#5a5650;font-size:14px;line-height:1.65;">{fb.get("whatMissed","")}</p></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="card-green"><div class="fb-header" style="color:#1a6b45;">Model Answer</div><p style="color:#5a5650;font-size:14px;line-height:1.65;">{fb.get("modelAnswer","")}</p></div>', unsafe_allow_html=True)
                kl = sc.get("keyLearning",""); dd = fb.get("deeperDive","")
                if kl or dd:
                    st.markdown(f'<div class="card-blue"><div class="fb-header" style="color:#1a4a6b;">📚 Learning Takeaway</div>{f"<p style=\'color:#5a5650;font-size:14px;line-height:1.65;margin-bottom:8px;\'>{kl}</p>" if kl else ""}{f"<p style=\'color:#9a948a;font-size:13px;margin:0;\'><strong style=\'color:#5a5650;\'>Study next:</strong> {dd}</p>" if dd else ""}</div>', unsafe_allow_html=True)

        st.markdown("---")
        c1,c2 = st.columns(2)
        with c1:
            if st.button("New Session"):
                st.session_state.page = "setup"; st.rerun()
        with c2:
            if st.button("View References →"):
                st.session_state.page = "references"; st.rerun()
        st.stop()

    # ── LOAD SCENARIO ──────────────────────────────────────────────────────────
    if st.session_state.scenario is None:
        with st.spinner("Generating scenario..."):
            try:
                vt, tier = next_params()
                sc = generate_fold1(vt, tier, diff) if mode == "fold1" else generate_fold2(vt, tier, diff)
                st.session_state.scenario = sc
                st.session_state.scenario_num += 1
                st.session_state.used_types.append(vt)
                st.session_state.used_tiers.append(tier)
                st.session_state.phase = "scenario"
                st.session_state.hint = None
                st.session_state.hint_used = False
            except Exception as e:
                st.error(f"Error generating scenario: {e}")
                if st.button("Retry"): st.rerun()
                st.stop()

    s = st.session_state.scenario
    st.markdown(pip_row_html(), unsafe_allow_html=True)
    st.markdown(f'<div class="vendor-name">{s.get("vendorName","")}</div>', unsafe_allow_html=True)
    st.markdown(vt_badge(s.get("vendorType","")), unsafe_allow_html=True)
    st.markdown(f'<div class="score-line" style="margin-top:6px;">SCENARIO {st.session_state.scenario_num} OF {TOTAL} &nbsp;·&nbsp; Score: {st.session_state.score}/{len(st.session_state.results)}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # FOLD 1
    # ══════════════════════════════════════════════════════════════════════════
    if mode == "fold1":
        if st.session_state.phase == "scenario":
            st.markdown(f"""<div class="card"><div class="slabel">Vendor Request — Business Owner Submission</div>
            <div style="font-family:'Playfair Display',serif;font-size:16px;font-weight:500;color:#1a2d4a;margin-bottom:12px;">{s.get('useCaseTitle','')}</div>
            <div class="flabel">What the business owner said:</div>
            <div class="use-case-quote">"{s.get('useCaseDescription','')}"</div>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;">
              <div><div class="flabel">Business Unit</div><div class="fval">{s.get('businessUnit','')}</div></div>
              <div><div class="flabel">Expected Users</div><div class="fval">{s.get('expectedUserCount','')}</div></div>
              <div><div class="flabel">Timeline</div><div class="fval">{s.get('goLiveTimeline','')}</div></div>
            </div></div>""", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### Complete the IRQ")
            st.markdown('<p style="font-size:13px;color:#9a948a;margin-bottom:1rem;">You are the business owner. Fill out the Inherent Risk Questionnaire based on the use case above.</p>', unsafe_allow_html=True)

            answers = {}
            answers["use_plan"]           = st.text_area("1. How do you plan to use this vendor?", placeholder="Describe how your business unit will use this vendor...", height=90)
            answers["nonpublic_data"]     = st.selectbox("2. Will this vendor be exposed to any non-public data?", ["— select —","Yes","No"])
            if answers["nonpublic_data"] == "Yes":
                answers["data_scope"]     = st.text_area("   If yes — describe in detail the data in scope", placeholder="Describe the specific non-public data...", height=80)
            else:
                answers["data_scope"]     = "N/A"
            answers["data_classification"]= st.selectbox("3. What type of data will the third party be handling?", ["— select —"] + DATA_CLASS_OPTS)
            answers["service_type"]       = st.selectbox("4. Select the type of vendor", ["— select —"] + VENDOR_TYPES)
            answers["pii"]                = st.selectbox("5. Will the vendor host, process, store or transmit PII?", ["— select —"] + ACCESS_OPTS)
            answers["record_count"]       = st.selectbox("6. Estimated volume of records (PII, PHI, or PCI data) in scope for this engagement", ["— select —"] + RECORD_OPTS)
            answers["phi"]                = st.selectbox("7. Will the vendor host, process, store or transmit PHI?", ["— select —"] + ACCESS_OPTS)
            answers["internal_access"]    = st.selectbox("8. Will the vendor have access to company internal systems, applications or networks?", ["— select —"] + ACCESS_OPTS)
            answers["cloud_storage"]      = st.selectbox("9. Will the third party store data in the cloud?", ["— select —"] + YESNO_UNK)
            answers["ai_use"]             = st.selectbox("10. Will the vendor use AI to process or deliver these services?", ["— select —"] + YESNO_UNK)
            answers["conf_risk"]          = st.selectbox("11. Confidentiality Risk", ["— select —"] + RISK_OPTS)
            answers["int_risk"]           = st.selectbox("12. Integrity Risk", ["— select —"] + RISK_OPTS)
            answers["avail_risk"]         = st.selectbox("13. Availability Risk", ["— select —"] + RISK_OPTS)
            answers["contact_name"]       = st.text_input("14. Vendor Contact Name", placeholder="e.g. Jane Smith")
            answers["contact_email"]      = st.text_input("15. Vendor Contact Email", placeholder="e.g. jsmith@vendor.com")

            if st.session_state.hint:
                st.markdown(f'<div class="card-amber"><div class="fb-header" style="color:#7a4f1a;">💡 Hint</div><p style="color:#5a5650;font-size:14px;line-height:1.65;margin:0;">{st.session_state.hint}</p></div>', unsafe_allow_html=True)
                st.markdown('<div class="hint-note">Hint used — a correct answer will be scored as Close.</div>', unsafe_allow_html=True)

            c1,c2,c3 = st.columns([1,1,2])
            with c1:
                if st.button("Skip", key="skip_f1"):
                    st.session_state.results.append("wrong")
                    st.session_state.result_log.append({"vendor":s.get("vendorName",""),"vendor_type":s.get("vendorType",""),"correct_tier":s.get("correctTier",""),"outcome":"wrong"})
                    st.session_state.scenario = None
                    if st.session_state.scenario_num >= TOTAL: st.session_state.scenario_num = TOTAL + 1
                    st.rerun()
            with c2:
                if st.button("💡 Hint", key="hint_f1"):
                    st.session_state.hint = s.get("hintText","Consider which factor most significantly drives risk here.")
                    st.session_state.hint_used = True; st.rerun()
            with c3:
                if st.button("Submit IRQ →", key="sub_f1"):
                    required = ["use_plan","nonpublic_data","data_classification","service_type","pii","record_count","phi","internal_access","cloud_storage","ai_use","conf_risk","int_risk","avail_risk"]
                    if answers["nonpublic_data"] == "Yes": required.append("data_scope")
                    empty = [k for k in required if not answers.get(k) or answers.get(k) == "— select —"]
                    if empty:
                        st.error(f"Please complete all required fields.")
                    else:
                        with st.spinner("Evaluating your IRQ..."):
                            try:
                                fb = evaluate_fold1(s, answers, diff)
                                outcome = compute_outcome_fold1(fb)
                                if outcome == "correct": st.session_state.score += 1
                                st.session_state.results.append(outcome)
                                st.session_state.result_log.append({"vendor":s.get("vendorName",""),"vendor_type":s.get("vendorType",""),"correct_tier":s.get("correctTier",""),"outcome":outcome})
                                st.session_state.completed_scenarios.append({"mode":"fold1","scenario":dict(s),"feedback":fb,"outcome":outcome,"answers":dict(answers)})
                                st.session_state.feedback = fb
                                st.session_state.phase = "feedback"; st.rerun()
                            except Exception as e:
                                st.error(f"Evaluation error: {e}")

        elif st.session_state.phase == "feedback":
            fb      = st.session_state.feedback or {}
            outcome = st.session_state.results[-1] if st.session_state.results else "wrong"
            vc      = {"correct":"#1a6b45","close":"#c8880a","wrong":"#b83030"}[outcome]
            vt_txt  = {"correct":"IRQ Well Completed","close":"Good Attempt — Some Gaps","wrong":"Significant Gaps — Review Below"}[outcome]

            st.markdown("---")
            st.markdown(f'<div class="card result-banner"><div><div class="verdict" style="color:{vc};">{vt_txt}</div><div style="font-size:12px;color:#9a948a;margin-top:3px;">IRQ Quality: {fb.get("irqQuality","")}</div></div><div class="tier-compare"><div class="tier-compare-item"><div class="tier-compare-label">YOUR IRQ IMPLIED</div>{tier_chip(fb.get("impliedTier",""))}</div><div class="tier-compare-item"><div class="tier-compare-label">CORRECT TIER</div>{tier_chip(s.get("correctTier",""))}</div></div></div>', unsafe_allow_html=True)

            misses = fb.get("criticalMisses",[])
            if misses:
                st.markdown(f'<div class="card-red"><div class="fb-header" style="color:#6b1a1a;">Critical Omissions</div>{"".join(f"<div style=\'font-size:13px;color:#6b1a1a;padding:3px 0;\'>⚠ {m}</div>" for m in misses)}</div>', unsafe_allow_html=True)

            st.markdown(f'<div class="card"><div class="fb-header">What you got right</div><p style="color:#5a5650;font-size:14px;line-height:1.65;">{fb.get("whatRight","")}</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card"><div class="fb-header">What you missed</div><p style="color:#5a5650;font-size:14px;line-height:1.65;">{fb.get("whatMissed","")}</p></div>', unsafe_allow_html=True)

            mirq = fb.get("modelIRQ",{})
            if mirq:
                rows = "".join(f'<div style="padding:6px 0;border-bottom:1px solid #ddd9d0;"><div class="flabel">{k.replace("_"," ")}</div><div style="font-size:13px;color:#1a1814;">{v}</div></div>' for k,v in mirq.items())
                st.markdown(f'<div class="card-green"><div class="fb-header" style="color:#1a6b45;">Model IRQ Answers</div>{rows}</div>', unsafe_allow_html=True)

            st.markdown(f'<div class="card-green"><div class="fb-header" style="color:#1a6b45;">Model Answer</div><p style="color:#5a5650;font-size:14px;line-height:1.65;">{fb.get("modelAnswer","")}</p></div>', unsafe_allow_html=True)

            kl = s.get("keyLearning",""); dd = fb.get("deeperDive","")
            if kl or dd:
                st.markdown(f'<div class="card-blue"><div class="fb-header" style="color:#1a4a6b;">📚 Learning Takeaway</div>{f"<p style=\'color:#5a5650;font-size:14px;line-height:1.65;margin-bottom:8px;\'>{kl}</p>" if kl else ""}{f"<p style=\'color:#9a948a;font-size:13px;margin:0;\'><strong style=\'color:#5a5650;\'>Study next:</strong> {dd}</p>" if dd else ""}</div>', unsafe_allow_html=True)

            c1,c2,c3 = st.columns([1,1,1])
            with c1: st.markdown(f'<div class="score-line" style="padding-top:12px;">Score: {st.session_state.score}/{len(st.session_state.results)}</div>', unsafe_allow_html=True)
            with c2:
                if st.button("References →", key="ref_f1"): st.session_state.page = "references"; st.rerun()
            with c3:
                if st.button("Next Scenario →", key="next_f1"):
                    st.session_state.scenario = None; st.session_state.phase = "scenario"
                    if st.session_state.scenario_num >= TOTAL: st.session_state.scenario_num = TOTAL + 1
                    st.rerun()

    # ══════════════════════════════════════════════════════════════════════════
    # FOLD 2
    # ══════════════════════════════════════════════════════════════════════════
    elif mode == "fold2":
        if st.session_state.phase == "scenario":
            yn = lambda v: f'<span style="color:{"#1a6b45" if v=="Yes" else "#5a5650"};">{v or "—"}</span>'
            rc = lambda v: {"High":"#6b1a1a","Medium":"#7a4f1a","Low":"#1a6b45"}.get(v,"#5a5650")

            st.markdown(f"""<div class="card">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1rem;flex-wrap:wrap;gap:.5rem;">
              <div class="slabel" style="margin:0;">Pre-Filled IRQ — Submitted by Business Owner</div>
              <span style="font-family:'DM Mono',monospace;font-size:10px;color:#9a948a;">Review for accuracy &amp; assign risk tier</span>
            </div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem 2rem;">
              <div><div class="flabel">Vendor Type</div><div class="fval">{s.get('vendorType','')}</div></div>
              <div><div class="flabel">Business Unit</div><div class="fval">{s.get('businessUnit','')}</div></div>
              <div style="grid-column:span 2;"><div class="flabel">How they plan to use this vendor</div><div class="fval">{s.get('usePlan','—')}</div></div>
              <div><div class="flabel">Exposed to non-public data?</div><div class="fval">{yn(s.get('nonpublicData'))}</div></div>
              <div><div class="flabel">Data in scope</div><div class="fval">{s.get('dataScope','N/A')}</div></div>
              <div><div class="flabel">Data classification</div><div class="fval">{s.get('dataClassification','—')}</div></div>
              <div><div class="flabel">Expected users</div><div class="fval">{s.get('expectedUserCount','—')}</div></div>
              <div><div class="flabel">Will vendor handle PII?</div><div class="fval">{yn(s.get('pii'))}</div></div>
              <div><div class="flabel">Records at risk</div><div class="fval">{s.get('recordCount','—')}</div></div>
              <div><div class="flabel">Will vendor handle PHI?</div><div class="fval">{yn(s.get('phi'))}</div></div>
              <div><div class="flabel">Access to internal systems?</div><div class="fval">{yn(s.get('internalAccess'))}</div></div>
              <div><div class="flabel">Store data in cloud?</div><div class="fval">{s.get('cloudStorage','—')}</div></div>
              <div><div class="flabel">Uses AI to deliver services?</div><div class="fval">{s.get('aiUse','—')}</div></div>
              <div><div class="flabel">Confidentiality risk</div><div class="fval" style="color:{rc(s.get('confRisk'))};">{s.get('confRisk','—')}</div></div>
              <div><div class="flabel">Integrity risk</div><div class="fval" style="color:{rc(s.get('intRisk'))};">{s.get('intRisk','—')}</div></div>
              <div><div class="flabel">Availability risk</div><div class="fval" style="color:{rc(s.get('availRisk'))};">{s.get('availRisk','—')}</div></div>
              <div><div class="flabel">Vendor contact</div><div class="fval">{s.get('contactName','—')}</div></div>
              <div><div class="flabel">Vendor contact email</div><div class="fval">{s.get('contactEmail','—')}</div></div>
            </div>
            {"<div style='font-size:12px;color:#7a4f1a;font-family:DM Mono,monospace;margin-top:.75rem;'>⚠ This IRQ may contain errors or omissions. Identify them below.</div>" if s.get('hasErrors') else ""}
            </div>""", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### Your Review")
            tier_choice = st.selectbox("1. Assign inherent risk tier", ["— select —"] + TIERS)
            issues = st.text_area("2. Flag any errors, omissions, or concerns in this IRQ", placeholder="Describe any fields that appear incorrect, missing, or misleading. If the IRQ looks complete, write 'No issues identified'.", height=120)

            if st.session_state.hint:
                st.markdown(f'<div class="card-amber"><div class="fb-header" style="color:#7a4f1a;">💡 Hint</div><p style="color:#5a5650;font-size:14px;line-height:1.65;margin:0;">{st.session_state.hint}</p></div>', unsafe_allow_html=True)

            c1,c2,c3 = st.columns([1,1,2])
            with c1:
                if st.button("Skip", key="skip_f2"):
                    st.session_state.results.append("wrong")
                    st.session_state.result_log.append({"vendor":s.get("vendorName",""),"vendor_type":s.get("vendorType",""),"correct_tier":s.get("correctTier",""),"outcome":"wrong"})
                    st.session_state.scenario = None
                    if st.session_state.scenario_num >= TOTAL: st.session_state.scenario_num = TOTAL + 1
                    st.rerun()
            with c2:
                if st.button("💡 Hint", key="hint_f2"):
                    st.session_state.hint = s.get("hintText","Look closely at the data fields — do they align with what this vendor actually does?")
                    st.session_state.hint_used = True; st.rerun()
            with c3:
                if st.button("Submit Review →", key="sub_f2"):
                    if not tier_choice or tier_choice == "— select —":
                        st.error("Please select a risk tier.")
                    else:
                        with st.spinner("Evaluating your review..."):
                            try:
                                fb = evaluate_fold2(s, tier_choice, issues, diff)
                                outcome = compute_outcome_fold2(fb)
                                if outcome == "correct": st.session_state.score += 1
                                st.session_state.results.append(outcome)
                                st.session_state.result_log.append({"vendor":s.get("vendorName",""),"vendor_type":s.get("vendorType",""),"correct_tier":s.get("correctTier",""),"student_tier":tier_choice,"outcome":outcome})
                                st.session_state.completed_scenarios.append({"mode":"fold2","scenario":dict(s),"feedback":fb,"outcome":outcome,"student_tier":tier_choice})
                                st.session_state.feedback = fb
                                st.session_state.student_tier = tier_choice
                                st.session_state.phase = "feedback"; st.rerun()
                            except Exception as e:
                                st.error(f"Evaluation error: {e}")

        elif st.session_state.phase == "feedback":
            fb      = st.session_state.feedback or {}
            outcome = st.session_state.results[-1] if st.session_state.results else "wrong"
            vc      = {"correct":"#1a6b45","close":"#c8880a","wrong":"#b83030"}[outcome]
            vt_txt  = {"correct":"Correct Assessment","close":"Partially Correct","wrong":"Needs Improvement"}[outcome]
            student_tier = st.session_state.student_tier

            st.markdown("---")
            st.markdown(f'<div class="card result-banner"><div><div class="verdict" style="color:{vc};">{vt_txt}</div><div style="font-size:12px;color:#9a948a;margin-top:3px;">Review Quality: {fb.get("irqReviewQuality","")}</div></div><div class="tier-compare"><div class="tier-compare-item"><div class="tier-compare-label">YOU ASSIGNED</div>{tier_chip(student_tier)}</div><div class="tier-compare-item"><div class="tier-compare-label">CORRECT TIER</div>{tier_chip(s.get("correctTier",""))}</div></div></div>', unsafe_allow_html=True)

            caught  = fb.get("errorsCorrectlyIdentified",[])
            missed  = fb.get("errorsMissed",[])
            fp      = fb.get("falsePositives",[])
            no_err  = not s.get("hasErrors") and not missed
            if no_err:
                err_html = '<div style="font-size:13px;color:#1a6b45;padding:4px 0;">✓ This IRQ was clean — no errors to find.</div>'
            else:
                err_html = ""
                if caught: err_html += f'<div class="err-section"><div class="err-tag" style="color:#1a6b45;">✓ CAUGHT</div>{"".join(f"<div class=\'err-item\'>{e}</div>" for e in caught)}</div>'
                if missed: err_html += f'<div class="err-section"><div class="err-tag" style="color:#b83030;">✗ MISSED</div>{"".join(f"<div class=\'err-item\'>{e}</div>" for e in missed)}</div>'
                if fp:     err_html += f'<div class="err-section"><div class="err-tag" style="color:#c8880a;">⚡ FALSE FLAGS</div>{"".join(f"<div class=\'err-item\'>{e}</div>" for e in fp)}</div>'
            st.markdown(f'<div class="card"><div class="slabel">IRQ Error Analysis</div>{err_html}</div>', unsafe_allow_html=True)

            st.markdown(f'<div class="card"><div class="fb-header">What you got right</div><p style="color:#5a5650;font-size:14px;line-height:1.65;">{fb.get("whatRight","")}</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card"><div class="fb-header">What you missed</div><p style="color:#5a5650;font-size:14px;line-height:1.65;">{fb.get("whatMissed","")}</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card"><div class="fb-header">Key risk drivers</div><p style="color:#5a5650;font-size:14px;line-height:1.65;white-space:pre-line;">{fb.get("keyDrivers","")}</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="card-green"><div class="fb-header" style="color:#1a6b45;">Model Answer</div><p style="color:#5a5650;font-size:14px;line-height:1.65;">{fb.get("modelAnswer","")}</p></div>', unsafe_allow_html=True)

            kl = s.get("keyLearning",""); dd = fb.get("deeperDive","")
            if kl or dd:
                st.markdown(f'<div class="card-blue"><div class="fb-header" style="color:#1a4a6b;">📚 Learning Takeaway</div>{f"<p style=\'color:#5a5650;font-size:14px;line-height:1.65;margin-bottom:8px;\'>{kl}</p>" if kl else ""}{f"<p style=\'color:#9a948a;font-size:13px;margin:0;\'><strong style=\'color:#5a5650;\'>Study next:</strong> {dd}</p>" if dd else ""}</div>', unsafe_allow_html=True)

            c1,c2,c3 = st.columns([1,1,1])
            with c1: st.markdown(f'<div class="score-line" style="padding-top:12px;">Score: {st.session_state.score}/{len(st.session_state.results)}</div>', unsafe_allow_html=True)
            with c2:
                if st.button("References →", key="ref_f2"): st.session_state.page = "references"; st.rerun()
            with c3:
                if st.button("Next Scenario →", key="next_f2"):
                    st.session_state.scenario = None; st.session_state.phase = "scenario"
                    if st.session_state.scenario_num >= TOTAL: st.session_state.scenario_num = TOTAL + 1
                    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: INSTRUCTOR DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "dashboard":
    if not st.session_state.dash_auth:
        st.markdown('<div class="top-rule"></div>', unsafe_allow_html=True)
        st.markdown("# Instructor Dashboard")
        pw = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Instructor password")
        c1,c2 = st.columns([1,3])
        with c1:
            if st.button("Enter"):
                if pw == INSTRUCTOR_PASS: st.session_state.dash_auth = True; st.rerun()
                else: st.error("Incorrect password.")
        with c2:
            if st.button("← Back"): st.session_state.page = "setup"; st.rerun()
        st.stop()

    st.markdown('<div class="top-rule"></div>', unsafe_allow_html=True)
    st.markdown('<span class="chip chip-grc">INSTRUCTOR VIEW</span>', unsafe_allow_html=True)
    st.markdown("# Dashboard")
    if st.button("← Back to Setup"): st.session_state.page = "setup"; st.rerun()
    st.markdown("---")

    history = st.session_state.session_history
    if not history:
        st.markdown('<div style="text-align:center;padding:3rem;color:#9a948a;font-size:14px;font-style:italic;">No completed sessions yet.</div>', unsafe_allow_html=True)
    else:
        all_scores = [h["score"] for h in history]
        avg = round(sum(all_scores)/len(all_scores),1)
        correct_total = sum(h["results"].count("correct") for h in history)
        total_ans = sum(len(h["results"]) for h in history)
        oa = round(correct_total/total_ans*100) if total_ans else 0

        c1,c2,c3,c4 = st.columns(4)
        for col,num,lbl in [(c1,len(history),"Sessions"),(c2,f"{avg}/{TOTAL}","Avg Score"),(c3,f"{round(avg/TOTAL*100)}%","Avg Accuracy"),(c4,f"{oa}%","Overall Correct")]:
            with col: st.markdown(f'<div class="dash-stat"><div class="dash-num">{num}</div><div class="dash-label">{lbl}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        rows = ""
        for h in reversed(history):
            pc = "#1a6b45" if h["pct"]>=80 else "#c8880a" if h["pct"]>=60 else "#b83030"
            pips = "".join(f'<span style="display:inline-block;width:14px;height:4px;border-radius:1px;margin-right:2px;background:{"#1a6b45" if r=="correct" else "#c8880a" if r=="close" else "#b83030"};"></span>' for r in h["results"])
            ml = "Fold 1" if h.get("mode")=="fold1" else "Fold 2"
            rows += f'<div class="student-row"><div><div style="font-size:13px;color:#1a1814;">{h["student"]}</div><div style="font-size:11px;color:#9a948a;margin-top:2px;">{h["timestamp"]} · {ml} · {h.get("difficulty","—")}</div></div><div style="text-align:right;"><div style="font-size:14px;font-weight:500;color:{pc};">{h["score"]}/{h["total"]} <span style="font-size:11px;color:#9a948a;">({h["pct"]}%)</span></div><div style="margin-top:4px;">{pips}</div></div></div>'
        st.markdown(f'<div class="card"><div class="slabel">Student Sessions</div>{rows}</div>', unsafe_allow_html=True)

        if st.button("Clear All Session Data"):
            st.session_state.session_history = []; st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: REFERENCE MATERIALS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "references":
    st.markdown('<div class="top-rule"></div>', unsafe_allow_html=True)
    st.markdown('<span class="chip chip-grc">GRC TRAINING</span>', unsafe_allow_html=True)
    st.markdown("# Reference Materials")
    back = "sim" if 0 < st.session_state.scenario_num <= TOTAL else "setup"
    if st.button("← Back"): st.session_state.page = back; st.rerun()
    st.markdown("---")

    tiers_ref = [
        ("Critical","#6b1a1a","#f4eaea","Highly sensitive data (PHI/financial/credentials), privileged/production access, critical regulatory obligations, broad external user impact, or single point of failure.","Core banking, identity providers/SSO, managed security services, health claims systems"),
        ("High","#7a4f1a","#f4f0ea","Significant PII/PHI/financial data, meaningful regulatory scope (GDPR/HIPAA/PCI/SOX), production access, or business-critical. External customer data involved.","CRM with PII, cloud IaaS, HR platforms, payment gateways, GenAI with sensitive data"),
        ("Moderate","#1a4a6b","#eaf0f4","Limited sensitive data (internal only), some regulatory awareness, limited integrations, moderate business impact.","Marketing SaaS (anonymized), internal project tools, professional services with limited access"),
        ("Low","#1a6b45","#eaf4ee","Minimal or no sensitive data, no regulatory exposure, non-critical, no system access. Business impact negligible.","Office supplies, training tools, anonymous survey tools with no data sharing"),
    ]
    rows = ""
    for tier,color,bg,desc,examples in tiers_ref:
        rows += f'<div style="padding:12px 0;border-bottom:1px solid #ddd9d0;"><div style="margin-bottom:6px;"><span style="font-family:\'DM Mono\',monospace;font-size:11px;color:{color};background:{bg};border:1px solid {color}40;padding:2px 10px;border-radius:2px;">{tier.upper()}</span></div><div style="font-size:13px;color:#5a5650;line-height:1.55;margin-bottom:4px;">{desc}</div><div style="font-size:11px;color:#9a948a;font-style:italic;">e.g. {examples}</div></div>'
    st.markdown(f'<div class="card"><div class="slabel">Inherent Risk Tier Reference</div>{rows}</div>', unsafe_allow_html=True)

    vt_ref = [
        ("Cloud SaaS","Risk driven by: data hosted, user scope (internal vs. external customers), integrations to core systems, data residency."),
        ("Cloud PaaS","Risk driven by: what is built/deployed on it, developer/privileged access, production pipeline exposure."),
        ("Cloud IaaS","Risk driven by: infrastructure criticality, network/admin access, data residency and sovereignty, tenant isolation."),
        ("Generative AI","Risk driven by: data ingested or used as prompts, confidentiality of outputs, IP leakage, model training on company data, EU AI Act classification."),
        ("Hardware","Risk driven by: physical access, firmware supply chain integrity, devices handling sensitive data (POS, medical, HSMs)."),
        ("On-Premises Software","Risk driven by: installation footprint within company network, vendor remote access for support/updates, patch dependency, access to sensitive internal data stores."),
        ("Professional Services","Risk driven by: access granted during engagement, data reviewed or accessed, NDA enforceability, subcontractor use."),
        ("Service Outsourcing","Risk driven by: volume and sensitivity of data processed, regulatory scope of outsourced function, geographic exposure, subprocessor chain visibility."),
    ]
    rows2 = "".join(f'<div class="ref-item"><div class="ref-title">{vt}</div><div class="ref-desc">{desc}</div></div>' for vt,desc in vt_ref)
    st.markdown(f'<div class="card"><div class="slabel">Vendor Type Risk Drivers</div>{rows2}</div>', unsafe_allow_html=True)

    rows3 = "".join(f'<div class="ref-item"><div class="ref-title"><a href="{r["url"]}" target="_blank" style="color:#1a4a6b;text-decoration:none;">{r["title"]} ↗</a></div><div class="ref-desc">{r["desc"]}</div></div>' for r in REFERENCE_MATERIALS)
    st.markdown(f'<div class="card"><div class="slabel">Frameworks &amp; Standards</div>{rows3}</div>', unsafe_allow_html=True)
