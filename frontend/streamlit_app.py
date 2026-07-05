"""
LoanWise - Smart Bank Loan Optimization System
================================================
Streamlit Frontend  ·  Calls the C++ backend via subprocess.

"""
# ─────────────────────────────────────────────────────────────────────────────
#  IMPORTS
# ─────────────────────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import subprocess
import json
import os
import tempfile
import platform
from typing import Optional, List, Dict, Tuple
import hashlib
import io

import matplotlib
matplotlib.use("Agg")          # non-interactive backend — required for Streamlit
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG  — must be the very first Streamlit call
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LoanWise — Loan Portfolio Optimizer",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
#  GLOBAL CSS
#  FIX 7: sidebar selectors are now tightly scoped so they never bleed into
#          the main content area.
# ─────────────────────────────────────────────────────────────────────────────
GLOBAL_CSS = """
<style>
/* ── Readability fixes for Streamlit metrics ─────── */
div[data-testid="stMetricValue"] { color: #0F172A !important; }
div[data-testid="stMetricLabel"] { color: #64748B !important; font-weight: 650 !important; }
div[data-testid="stMetricDelta"] { color: #64748B !important; }

/* ── Base ──────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
    color: #1E293B;
}
.stApp { background-color: #F1F5F9; }

/* Make markdown headings readable (fix “white headings”) */
div[data-testid="stMarkdownContainer"] h1,
div[data-testid="stMarkdownContainer"] h2,
div[data-testid="stMarkdownContainer"] h3,
div[data-testid="stMarkdownContainer"] h4,
div[data-testid="stMarkdownContainer"] p,
div[data-testid="stMarkdownContainer"] span {
    color: #0F172A !important;
}

/* ── Header bar ─────────────────────────────────── */
.bank-header {
    background: linear-gradient(135deg, #1A4B8C 0%, #2563EB 100%);
    color: white;
    padding: 20px 32px 16px 32px;
    border-radius: 12px;
    margin-bottom: 24px;
    box-shadow: 0 4px 16px rgba(26,75,140,0.18);
}
.bank-header h1 { margin:0; font-size:2rem; font-weight:800; letter-spacing:-0.5px; }
.bank-header p  { margin:4px 0 0 0; font-size:0.9rem; opacity:0.80; }

/* ── Section titles ─────────────────────────────── */
.section-title {
    font-size:0.72rem; font-weight:700;
    letter-spacing:0.1em; text-transform:uppercase;
    color:#334155; margin-bottom:10px;
    padding-bottom:6px; border-bottom:2px solid #E2E8F0;
}

/* ── KPI cards ──────────────────────────────────── */
.kpi-card {
    background:#FFFFFF; border-radius:10px;
    padding:20px 22px; box-shadow:0 1px 6px rgba(0,0,0,0.07);
    border-left:4px solid #2563EB; height:100%;
}
.kpi-card.green { border-left-color:#059669; }
.kpi-card.amber { border-left-color:#D97706; }
.kpi-card.red   { border-left-color:#DC2626; }
.kpi-card.blue  { border-left-color:#2563EB; }
.kpi-card.slate { border-left-color:#64748B; }
.kpi-label {
    font-size:0.70rem; font-weight:700; letter-spacing:0.08em;
    text-transform:uppercase; color:#64748B; margin-bottom:6px;
}
.kpi-value { font-size:1.75rem; font-weight:800; color:#0F172A; line-height:1.1; }
.kpi-sub   { font-size:0.76rem; color:#94A3B8; margin-top:4px; }

/* ── Alerts ─────────────────────────────────────── */
.stAlert { border-radius:8px !important; }

/* ── Main-area tabs ─────────────────────────────── */
.stTabs [data-baseweb="tab"] {
    font-weight: 650;
    font-size: 0.90rem;
    color: #0F172A !important;
}
.stTabs [aria-selected="true"] {
    color: #2563EB !important;
}

/* ── Main-area buttons — */
.stButton > button {
    background-color: #2563EB !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 8px 20px !important;
}
.stButton > button:hover {
    background-color: #1D4ED8 !important;
    color: white !important;
}

/* Download buttons can appear “invisible” without explicit styling */
.stDownloadButton > button {
    background-color: #0F172A !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 650 !important;
    padding: 8px 18px !important;
}
.stDownloadButton > button:hover {
    background-color: #111827 !important;
    color: white !important;
}

/* Main-area inputs: clearer focus state */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea {
    background: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 10px !important;
    caret-color: #0F172A !important;
}
/* Hide Streamlit's “Press Enter to apply” hint (placeholder) */
div[data-testid="stNumberInput"] input::placeholder,
div[data-testid="stTextInput"] input::placeholder,
div[data-testid="stTextArea"] textarea::placeholder {
    color: transparent !important;
}
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextInput"] input:focus,
div[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(37,99,235,0.7) !important;
    box-shadow: 0 0 0 4px rgba(37,99,235,0.12) !important;
}

/* Expanders: ensure label is readable */
div[data-testid="stExpander"] details > summary {
    color: #0F172A !important;
    font-weight: 650 !important;
}

/* Expander “button” look (fix black bar / invisible control) */
div[data-testid="stExpander"] details {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
div[data-testid="stExpander"] details > summary {
    background: #FFFFFF !important;
    padding: 10px 12px !important;
    border-bottom: 1px solid #EEF2F7 !important;
}
div[data-testid="stExpander"] details[open] > summary {
    background: #F8FAFC !important;
}
div[data-testid="stExpander"] details > summary:hover {
    background: #F1F5F9 !important;
}
/* Expander chevron/icon visibility */
div[data-testid="stExpander"] details > summary svg {
    fill: #2563EB !important;
    color: #2563EB !important;
}

/* ── Sidebar — tightly scoped ────────────── */
[data-testid="stSidebar"] > div:first-child {
    background-color: #1A4B8C;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: #E2E8F0 !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: #2563EB !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    width: 100% !important;
    padding: 12px 0 !important;
    font-size: 1rem !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #1D4ED8 !important;
}
[data-testid="stSidebar"] input {
    background: #1E3A5F !important;
    color: white !important;
    border: 1px solid #3B82F6 !important;
    border-radius: 6px !important;
    caret-color: #FFFFFF !important;
}
[data-testid="stSidebar"] input::placeholder {
    color: transparent !important;
}

/* ── Data frame ─────────────────────────────────── */
div[data-testid="stDataFrame"] { border-radius:8px; overflow:hidden; }
div[data-testid="stDataFrame"] * { color: #0F172A !important; }
div[data-testid="stDataFrame"] table { background: #FFFFFF !important; }
div[data-testid="stDataFrame"] thead tr th { background: #F8FAFC !important; }
div[data-testid="stDataFrame"] tbody tr td { background: #FFFFFF !important; }
hr { border:none; border-top:1px solid #E2E8F0; margin:20px 0; }

/* Custom stats table (avoid Streamlit dark table styles) */
.lw-stats {
    width: 100%;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 1px 6px rgba(0,0,0,0.07);
    background: #FFFFFF;
}
.lw-stats table { width:100%; border-collapse: collapse; }
.lw-stats thead th {
    text-align: left;
    background: #F8FAFC;
    color: #0F172A;
    font-size: 0.86rem;
    padding: 10px 12px;
    border-bottom: 1px solid #E2E8F0;
}
.lw-stats tbody td {
    padding: 10px 12px;
    border-bottom: 1px solid #EEF2F7;
    font-size: 0.88rem;
    color: #0F172A;
}
.lw-stats tbody tr:last-child td { border-bottom: none; }
.lw-stats td.value { text-align: right; font-weight: 700; }

/* Technical analysis aligned blocks (tabular feel, not a dataframe) */
.lw-tech {
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    background: #FFFFFF;
    box-shadow: 0 1px 6px rgba(0,0,0,0.07);
    padding: 14px 14px 10px 14px;
}
.lw-tech .title {
    font-weight: 800;
    color: #0F172A;
    font-size: 1.02rem;
    margin-bottom: 8px;
}
.lw-tech .sub {
    color: #64748B;
    font-size: 0.86rem;
    margin-bottom: 10px;
}
.lw-tech .grid {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 10px 14px;
    align-items: baseline;
}
.lw-tech .label {
    color: #64748B;
    font-size: 0.86rem;
}
.lw-tech .value {
    color: #0F172A;
    font-weight: 800;
    font-size: 0.92rem;
    text-align: right;
    white-space: nowrap;
}
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  BACKEND PATH RESOLUTION
# ─────────────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "backend"))
EXE_NAME    = "loan_optimizer.exe" if platform.system() == "Windows" else "loan_optimizer"
BACKEND_EXE = os.path.join(BACKEND_DIR, EXE_NAME)
DATA_DIR    = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "data"))


# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────

def _default_manual_rows() -> List[Dict]:
    """Default 10-row sample for the manual entry table."""
    return [
        {"id": 1,  "loan_amount": 50000.0, "interest_rate": 7.50,  "credit_score": 720},
        {"id": 2,  "loan_amount": 30000.0, "interest_rate": 9.00,  "credit_score": 680},
        {"id": 3,  "loan_amount": 80000.0, "interest_rate": 6.25,  "credit_score": 750},
        {"id": 4,  "loan_amount": 20000.0, "interest_rate": 11.50, "credit_score": 640},
        {"id": 5,  "loan_amount": 60000.0, "interest_rate": 8.75,  "credit_score": 710},
        {"id": 6,  "loan_amount": 15000.0, "interest_rate": 12.00, "credit_score": 620},
        {"id": 7,  "loan_amount": 45000.0, "interest_rate": 7.00,  "credit_score": 730},
        {"id": 8,  "loan_amount": 25000.0, "interest_rate": 10.50, "credit_score": 660},
        {"id": 9,  "loan_amount": 70000.0, "interest_rate": 6.75,  "credit_score": 740},
        {"id": 10, "loan_amount": 35000.0, "interest_rate": 9.50,  "credit_score": 690},
    ]


def _default_manual_df() -> pd.DataFrame:
    """Default manual-entry DataFrame (used by st.data_editor)."""
    return pd.DataFrame(_default_manual_rows(), columns=["id", "loan_amount", "interest_rate", "credit_score"])


def init_session_state():
    """Initialise all session-state keys exactly once per browser session."""
    defaults = {
        # CSV-only UI
        "active_mode":        "csv",
        "uploaded_csv_bytes": None,        # raw bytes from file_uploader
        "uploader_version":   0,           # bumps file_uploader key to clear it
        "all_applicants":     [],
        "result_data":        None,
        "result_budget":      0.0,
        "show_tech":          False,
        "show_alt_plan":      False,       # persist alternative plan visibility across reruns
        "last_input_hash":    None,        # used to mark results stale when inputs change
        "results_stale":      False,
        "last_run_applicants_display": None,  # list[dict] used for last successful run
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    # Manual entry removed: ignore legacy manual keys if present.


# ─────────────────────────────────────────────────────────────────────────────
#  UTILITY HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def fmt_inr(value: float) -> str:
    return "Rs. {:,.0f}".format(value)

def fmt_pct(value: float) -> str:
    return "{:.1f}%".format(value)

def risk_profile(avg_credit: float) -> Tuple[str, str]:
    """Return (label, kpi_card_colour_class)."""
    if avg_credit >= 720:
        return "Low Risk",    "green"
    elif avg_credit >= 660:
        return "Medium Risk", "amber"
    else:
        return "High Risk",   "red"

def kpi_card_html(label: str, value: str,
                  subtitle: str = "", colour: str = "blue") -> str:
    """Return HTML string for a single KPI metric tile."""
    sub = '<div class="kpi-sub">{}</div>'.format(subtitle) if subtitle else ""
    return (
        '<div class="kpi-card {c}">'
        '<div class="kpi-label">{l}</div>'
        '<div class="kpi-value">{v}</div>'
        '{s}</div>'
    ).format(c=colour, l=label, v=value, s=sub)

def section_title(text: str):
    st.markdown('<div class="section-title">{}</div>'.format(text),
                unsafe_allow_html=True)

def write_temp_csv(csv_bytes: bytes) -> str:
    """Write bytes to a temporary CSV file and return its path."""
    tmp = tempfile.NamedTemporaryFile(mode="wb", suffix=".csv", delete=False)
    tmp.write(csv_bytes)
    tmp.close()
    return tmp.name

def build_results_df(applicants: List[Dict]) -> pd.DataFrame:
    """Format backend applicant list into a display DataFrame."""
    return pd.DataFrame([
        {
            "ID":              int(a["id"]),
            "Loan Amount":     fmt_inr(a["loan_amount"]),
            "Interest Rate":   "{:.2f}%".format(a["interest_rate"]),
            "Credit Score":    int(a["credit_score"]),
            "Expected Return": fmt_inr(a["profit"]),
        }
        for a in applicants
    ])


# ─────────────────────────────────────────────────────────────────────────────
#  DATA VALIDATION
# ─────────────────────────────────────────────────────────────────────────────

def validate_csv_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate a DataFrame parsed from an uploaded CSV.
    Returns the cleaned DataFrame or raises ValueError.
    """
    required = {"id", "loan_amount", "interest_rate", "credit_score"}
    actual   = set(df.columns.str.strip().str.lower())
    missing  = required - actual
    if missing:
        raise ValueError(
            "Missing required columns: {}".format(", ".join(sorted(missing))))
    # Normalise column names
    df.columns = df.columns.str.strip().str.lower()
    df = df[["id", "loan_amount", "interest_rate", "credit_score"]].copy()
    df = df.dropna()
    if df.empty:
        raise ValueError("CSV file contains no valid data rows.")
    return df


# ─────────────────────────────────────────────────────────────────────────────
#  BACKEND INTEGRATION
# ─────────────────────────────────────────────────────────────────────────────

def get_active_csv_bytes() -> Optional[bytes]:
    """
    FIX 1 & 2: Single authoritative source of truth.

    Returns CSV bytes from whichever input source is currently active,
    or None if no valid data is available.

    CSV-only UI: returns uploaded_csv_bytes (set when user uploads)
    """
    return st.session_state.uploaded_csv_bytes  # may be None if upload cleared


def _display_applicants_from_df(df: pd.DataFrame) -> List[Dict]:
    """Convert a canonical applicants df into display-friendly dict rows."""
    disp = df.rename(columns={
        "id": "Applicant ID",
        "loan_amount": "Loan Amount (Rs.)",
        "interest_rate": "Interest Rate (%)",
        "credit_score": "Credit Score",
    }).copy()
    return disp.to_dict("records")


def get_active_applicants_display() -> Optional[List[Dict]]:
    """
    Return display-friendly applicants for the CURRENT active input source.
    Used to keep the “View All Applications” section consistent with the run.
    """
    if st.session_state.active_mode == "csv":
        b = st.session_state.uploaded_csv_bytes
        if not b:
            return None
        try:
            df = pd.read_csv(io.BytesIO(b))
            df = validate_csv_df(df)
            return _display_applicants_from_df(df)
        except Exception:
            return None

    # manual
    try:
        df = validate_manual_df(_get_manual_df())
        return _display_applicants_from_df(df)
    except Exception:
        return None


def compute_input_hash(csv_bytes: Optional[bytes], budget: float) -> Optional[str]:
    """Fingerprint current inputs to detect stale results."""
    if csv_bytes is None:
        return None
    h = hashlib.sha256()
    h.update(csv_bytes)
    h.update(("|budget:{:.2f}".format(float(budget))).encode("utf-8"))
    return h.hexdigest()


def call_backend(csv_path: str, budget: float) -> Dict:
    """
    Invoke the C++ loan_optimizer binary via subprocess.
    Returns the parsed JSON result dict, or raises RuntimeError.
    """
    if not os.path.isfile(BACKEND_EXE):
        raise RuntimeError(
            "C++ backend not found:\n{}\n\n"
            "Compile with:  cd backend && make\n"
            "Windows:  g++ -std=c++17 -O2 -static -static-libgcc "
            "-static-libstdc++ -o loan_optimizer.exe "
            "main.cpp greedy.cpp dp.cpp utils.cpp".format(BACKEND_EXE)
        )

    proc = subprocess.run(
        [BACKEND_EXE, csv_path, str(budget), "both"],
        capture_output=True,
        text=True,
        timeout=30,
    )

    raw = proc.stdout.strip()
    if not raw:
        raise RuntimeError(
            "Backend produced no output.\nStderr: {}".format(proc.stderr[:400]))

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Could not parse backend output as JSON.\n"
            "Raw: {}\nError: {}".format(raw[:400], exc)
        )

    if data.get("status") == "error":
        raise RuntimeError(data.get("message", "Unknown backend error."))

    return data


# ─────────────────────────────────────────────────────────────────────────────
#  CHART HELPERS 
# ─────────────────────────────────────────────────────────────────────────────

def render_comparison_chart(rec_profit: float, alt_profit: float):
    """
    FIX 5: Render a clean, correctly labelled comparison bar chart
    using matplotlib instead of st.bar_chart, which is unreliable
    across Streamlit versions for custom colours and labels.
    """
    labels  = ["Recommended\nPlan", "Alternative\nPlan"]
    values  = [rec_profit, alt_profit]
    colours = ["#2563EB", "#10B981"]

    fig, ax = plt.subplots(figsize=(7, 3.8))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#F8FAFC")

    bars = ax.bar(labels, values, color=colours, width=0.4,
                  edgecolor="none", zorder=3)

    # Value labels above each bar
    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(values) * 0.02,
            fmt_inr(val),
            ha="center", va="bottom",
            fontsize=10, fontweight="bold", color="#1E293B",
        )

    # Axes formatting
    ax.set_ylabel("Expected Return (Rs.)", fontsize=9, color="#64748B")
    ax.set_ylim(0, max(values) * 1.28)
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, _: "Rs.{:.0f}k".format(x / 1000))
    )
    ax.tick_params(axis="both", colors="#64748B", labelsize=9)

    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color("#E2E8F0")

    ax.yaxis.grid(True, color="#E2E8F0", linestyle="--", linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def render_approval_chart(selected: int, total: int):
    """Simple bar chart for approved vs not-selected counts."""
    labels  = ["Approved", "Not\nSelected"]
    values  = [selected, max(total - selected, 0)]
    colours = ["#2563EB", "#CBD5E1"]

    fig, ax = plt.subplots(figsize=(3.5, 3))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("#F8FAFC")

    bars = ax.bar(labels, values, color=colours, width=0.4, edgecolor="none", zorder=3)
    for bar, val in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.15,
            str(val), ha="center", va="bottom",
            fontsize=10, fontweight="bold", color="#1E293B",
        )

    ax.set_ylim(0, max(values) * 1.35)
    ax.tick_params(axis="both", colors="#64748B", labelsize=9)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color("#E2E8F0")
    ax.yaxis.grid(True, color="#E2E8F0", linestyle="--", linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────

def render_sidebar() -> Tuple[float, bool]:
    """
    Render the sidebar.
    Returns (budget, run_clicked).
    """
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align:center;padding:18px 0 12px 0;">
              <div style="font-size:2.2rem;">🏦</div>
              <div style="font-size:1.15rem;font-weight:800;
                          color:white;margin-top:4px;">LoanWise</div>
              <div style="font-size:0.75rem;color:#93C5FD;
                          margin-top:2px;">Portfolio Optimizer</div>
            </div>
            <hr style="border-color:#3B82F6;margin:0 0 18px 0;">
            """,
            unsafe_allow_html=True,
        )

        st.markdown("**Loan Configuration**")
        st.caption("Set the total disbursement budget")

        budget = st.number_input(
            label="Total Bank Budget (Rs.)",
            min_value=1_000.0,
            max_value=100_000_000.0,
            value=200_000.0,
            step=10_000.0,
            format="%.0f",
            help="Maximum total amount the bank can disburse.",
        )

        # Show active input mode so user knows what data will be used
        mode_label = (
            "📂 CSV File" if st.session_state.active_mode == "csv"
            else "📂 CSV File"
        )
        st.caption("Active data source: **{}**".format(mode_label))

        st.markdown("<br>", unsafe_allow_html=True)
        run_clicked = st.button("▶  Run Optimization", use_container_width=True)

        st.markdown(
            '<hr style="border-color:#3B82F6;margin:16px 0 12px 0;">',
            unsafe_allow_html=True,
        )

        backend_ok  = os.path.isfile(BACKEND_EXE)
        icon        = "🟢" if backend_ok else "🔴"
        status_text = "Engine Ready" if backend_ok else "Engine Not Found"
        st.markdown(
            '<div style="font-size:0.78rem;color:#93C5FD;">'
            '{} Optimization {}</div>'.format(icon, status_text),
            unsafe_allow_html=True,
        )
        if not backend_ok:
            st.caption("Compile: `cd backend && make`")

        st.markdown(
            '<div style="font-size:0.72rem;color:#93C5FD;margin-top:14px;">'
            'LoanWise v2.1</div>',
            unsafe_allow_html=True,
        )

    return budget, run_clicked


def render_input_section():
    section_title("Applicant Data Input")

    st.markdown("<br>", unsafe_allow_html=True)

    col_up, col_hint = st.columns([2, 1])

    with col_up:
        uploader_key = "csv_uploader_v{}".format(st.session_state.uploader_version)
        uploaded = st.file_uploader(
            "Upload applicant data (CSV)",
            type=["csv"],
            help="Columns required: id, loan_amount, interest_rate, credit_score",
            label_visibility="collapsed",
            key=uploader_key,
        )

        # Show filename explicitly (built-in uploader text can be low-contrast)
        if uploaded is not None:
            st.markdown(
                '<div style="margin-top:6px; color:#0F172A; font-weight:650;">'
                'Uploaded file: <span style="font-weight:800;">{}</span>'
                '</div>'.format(uploaded.name),
                unsafe_allow_html=True,
            )

        if st.session_state.uploaded_csv_bytes is not None:
            if st.button("🧹  Clear uploaded CSV", use_container_width=True, key="btn_clear_csv"):
                st.session_state.uploaded_csv_bytes = None
                # If results exist, they now refer to a previous file/run
                if st.session_state.result_data is not None:
                    st.session_state.results_stale = True
                    st.session_state.last_run_applicants_display = None
                st.session_state.uploader_version += 1
                st.rerun()

    with col_hint:
        st.info(
            "**Required columns**\n"
            "- `id`\n- `loan_amount`\n"
            "- `interest_rate`\n- `credit_score`"
        )

    if uploaded is not None:
        # ── File present: read, validate, store ──
        try:
            uploaded.seek(0)
            df_raw = pd.read_csv(uploaded)
            df_clean = validate_csv_df(df_raw)

            # Store bytes for backend (re-serialise cleaned df)
            csv_bytes = df_clean.to_csv(index=False).encode("utf-8")
            st.session_state.uploaded_csv_bytes = csv_bytes

            # Cache for "View All Applications" display
            st.session_state.all_applicants = _display_applicants_from_df(df_clean)

            st.markdown("<br>", unsafe_allow_html=True)
            section_title("File Preview · {} records loaded".format(len(df_clean)))
            st.dataframe(
                df_clean, use_container_width=True, hide_index=True,
                height=min(300, 38 * len(df_clean) + 40),
            )
            st.success(
                "✅  {} applicants loaded from CSV. "
                "Click **Run Optimization** to proceed.".format(len(df_clean))
            )

        except (ValueError, Exception) as exc:
            st.error("Could not load file: {}".format(exc))
            st.session_state.uploaded_csv_bytes = None

    else:
        st.session_state.uploaded_csv_bytes = None


def _render_manual_entry_tab():
    """
    Render the manual entry data_editor.
    """
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Action buttons ────────────────────────────────────────────────────────
    col_add, col_clear, col_sample, _ = st.columns([1, 1, 1.6, 3])

    with col_add:
        if st.button("＋  Add Row", use_container_width=True, key="btn_add"):
            df = _get_manual_df()
            existing_ids = [int(x) for x in df["id"].dropna().tolist()] if "id" in df.columns else []
            next_id = (max(existing_ids) + 1) if existing_ids else 1
            df.loc[len(df)] = {
                "id": next_id,
                "loan_amount": 10000.0,
                "interest_rate": 8.0,
                "credit_score": 700,
            }
            st.session_state.manual_df = df
            st.rerun()

    with col_clear:
        if st.button("🗑  Clear", use_container_width=True, key="btn_clear"):
            st.session_state.manual_df = pd.DataFrame(
                [{"id": 1, "loan_amount": 0.0, "interest_rate": 0.0, "credit_score": 700}],
                columns=["id", "loan_amount", "interest_rate", "credit_score"],
            )
            st.rerun()

    with col_sample:
        if st.button("📋  Load Sample Data", use_container_width=True,
                     key="btn_sample"):
            st.session_state.manual_df = _default_manual_df()
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── data_editor — single source of truth: session_state.manual_df ────────
    edited_df = st.data_editor(
        _get_manual_df(),
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key="manual_editor",
        column_config={
            "id": st.column_config.NumberColumn(
                "Applicant ID",
                help="Unique integer ID",
                min_value=1, step=1, format="%d", required=True,
            ),
            "loan_amount": st.column_config.NumberColumn(
                "Loan Amount (Rs.)",
                help="Requested loan amount in Rupees",
                min_value=1_000.0, step=1_000.0,
                format="Rs. %.0f", required=True,
            ),
            "interest_rate": st.column_config.NumberColumn(
                "Interest Rate (%)",
                help="Annual interest rate, e.g. 8.5 for 8.5%",
                min_value=0.01, max_value=50.0,
                step=0.25, format="%.2f %%", required=True,
            ),
            "credit_score": st.column_config.NumberColumn(
                "Credit Score",
                help="CIBIL score between 300 and 850",
                min_value=300, max_value=850,
                step=1, format="%d", required=True,
            ),
        },
    )

    # Persist edits
    st.session_state.manual_df = edited_df.copy()

    # Switch active mode to manual only if no CSV is loaded
    if st.session_state.active_mode != "csv":
        st.session_state.active_mode = "manual"

    st.caption(
        "Edits apply when you press Enter or click outside a cell. "
        "Then click **Run Optimization**."
    )

    # Optional: validate on demand (prevents false warnings while typing)
    vcol1, vcol2 = st.columns([1, 3])
    with vcol1:
        validate_clicked = st.button("✅ Validate", use_container_width=True, key="btn_validate_manual")
    with vcol2:
        st.caption("Validate checks numeric types, ranges, and duplicate IDs.")

    if validate_clicked:
        try:
            cleaned_df = validate_manual_df(_get_manual_df())
            st.session_state.all_applicants = cleaned_df.to_dict("records")
            st.success("Manual data looks good: {} applicants.".format(len(cleaned_df)))
        except ValueError as exc:
            st.error("Manual data issue: {}".format(exc))


# ─────────────────────────────────────────────────────────────────────────────
#  RESULTS DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────

def render_results(data: Dict, budget: float):
    """
    Render the full results dashboard from the parsed backend JSON.

    data keys: 'status', 'budget', 'total_applicants', 'DP', 'Greedy'
    Recommended Plan  = DP  (globally optimal)
    Alternative Plan  = Greedy  (fast heuristic)
    """
    dp     = data.get("DP")
    greedy = data.get("Greedy")

    # Primary = DP if available, else Greedy
    rec = dp     or greedy
    alt = greedy if dp else None

    if not rec:
        st.error("No optimization results found in backend output.")
        return

    rec_apps = rec.get("selected_applicants", [])
    avg_credit = (
        sum(a["credit_score"] for a in rec_apps) / len(rec_apps)
        if rec_apps else 0.0
    )

    profit         = rec["total_profit"]
    loan_used      = rec["total_loan_used"]
    selected_count = rec["selected_count"]
    utilization    = (loan_used / budget * 100) if budget else 0.0
    total_received = data.get(
        "total_applicants",
        len(st.session_state.all_applicants)
    )

    risk_lbl, risk_colour = risk_profile(avg_credit)

    # ═══ 1. PORTFOLIO SUMMARY KPIs ═══════════════════════════════════════════
    section_title("Portfolio Summary")

    c1, c2, c3, c4, c5 = st.columns(5)
    tiles = [
        (c1, "Total Budget",        fmt_inr(budget),        "disbursement limit",                  "blue"),
        (c2, "Loan Distributed",    fmt_inr(loan_used),     fmt_pct(utilization) + " of budget",   "green"),
        (c3, "Expected Return",     fmt_inr(profit),        "annual interest income",               "green"),
        (c4, "Budget Utilization",  fmt_pct(utilization),   "{} utilised".format(fmt_inr(loan_used)), "amber"),
        (c5, "Portfolio Risk",      risk_lbl,               "avg credit {:.0f}".format(avg_credit), risk_colour),
    ]
    for col, label, value, subtitle, colour in tiles:
        with col:
            st.markdown(
                kpi_card_html(label, value, subtitle, colour),
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ═══ 2. APPLICANT OVERVIEW ════════════════════════════════════════════════
    section_title("Applicant Overview")

    ov1, ov2, _ = st.columns([1, 1, 2])
    with ov1:
        st.markdown(
            kpi_card_html(
                "Total Applications", str(total_received),
                "received for review", "slate"
            ),
            unsafe_allow_html=True,
        )
    with ov2:
        approval_rate = (
            selected_count / total_received * 100 if total_received else 0
        )
        st.markdown(
            kpi_card_html(
                "Applicants Selected",
                "{} / {}".format(selected_count, total_received),
                "approval rate {:.0f}%".format(approval_rate), "green"
            ),
            unsafe_allow_html=True,
        )

    all_apps_display = (
        st.session_state.last_run_applicants_display
        or st.session_state.all_applicants
        or []
    )
    apps_count = len(all_apps_display) if all_apps_display else int(total_received)

    with st.expander(
        "📋  View All Applications ({})".format(apps_count), expanded=False
    ):
        all_apps = all_apps_display
        if all_apps:
            df_all = pd.DataFrame(all_apps)
            # Normalise column names for display (supports both display keys and raw keys)
            df_all = df_all.rename(columns={
                "Applicant ID": "ID",
                "Loan Amount (Rs.)": "Loan Amount",
                "Interest Rate (%)": "Interest Rate",
                "Credit Score": "Credit Score",
                "id": "ID",
                "loan_amount": "Loan Amount",
                "interest_rate": "Interest Rate",
                "credit_score": "Credit Score",
            })
            st.dataframe(df_all, use_container_width=True, hide_index=True)
        else:
            st.caption("Applicant list not available.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ═══ 3. SELECTED APPLICANTS TABLE ════════════════════════════════════════
    section_title("Recommended Plan · Selected Applicants")

    df_rec = build_results_df(rec_apps)
    st.dataframe(df_rec, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ═══ 4. LOAN DISTRIBUTION INSIGHT ════════════════════════════════════════
    section_title("Loan Distribution Insight")

    ins1, ins2, ins3 = st.columns([1, 1.4, 1])

    with ins1:
        st.markdown("**Approved vs Not Selected**")
        render_approval_chart(selected_count, total_received)

    with ins2:
        st.markdown("**Portfolio Allocation**")
        for a in rec_apps:
            pct = (a["loan_amount"] / loan_used * 100) if loan_used else 0
            st.markdown(
                "**#{id}** &nbsp; {amt} "
                "<span style='color:#94A3B8;font-size:0.82rem;'>"
                "({pct:.1f}%)</span>".format(
                    id=a["id"], amt=fmt_inr(a["loan_amount"]), pct=pct
                ),
                unsafe_allow_html=True,
            )
            st.progress(round(pct) / 100)

    with ins3:
        st.markdown("**Portfolio Stat**")
        if rec_apps:
            avg_loan = loan_used / selected_count
            avg_rate = sum(a["interest_rate"] for a in rec_apps) / selected_count
            max_loan = max(a["loan_amount"] for a in rec_apps)
            min_loan = min(a["loan_amount"] for a in rec_apps)
        else:
            avg_loan = avg_rate = max_loan = min_loan = 0.0

        def _clamp01(x: float) -> float:
            return max(0.0, min(1.0, x))

        remaining = max(budget - loan_used, 0.0)
        approval_rate = (selected_count / total_received * 100) if total_received else 0.0
        alloc_pct = (loan_used / budget * 100) if budget else 0.0
        avg_loan_pct = (avg_loan / budget * 100) if budget else 0.0
        max_loan_pct = (max_loan / budget * 100) if budget else 0.0
        min_loan_pct = (min_loan / budget * 100) if budget else 0.0
        rem_pct = (remaining / budget * 100) if budget else 0.0

        # Interest rate doesn't have a natural "budget" denominator. Use a fixed
        # scale for a consistent UI (0–20% typical retail band; clamp beyond).
        rate_scale = 20.0
        rate_pct = (avg_rate / rate_scale * 100) if rate_scale else 0.0

        stat_lines = [
            ("Selected / Total", "{} / {}".format(selected_count, total_received), approval_rate),
            ("Total Allocated", fmt_inr(loan_used), alloc_pct),
            ("Avg. Loan Size", fmt_inr(avg_loan), avg_loan_pct),
            ("Avg. Interest Rate", "{:.2f}%".format(avg_rate), rate_pct),
            ("Largest Loan", fmt_inr(max_loan), max_loan_pct),
            ("Smallest Loan", fmt_inr(min_loan), min_loan_pct),
            ("Remaining Budget", fmt_inr(remaining), rem_pct),
        ]

        for label, value, pct in stat_lines:
            left, right = st.columns([1.15, 0.85])
            left.markdown(
                '<span style="color:#334155;font-weight:650;">{}</span>'.format(label),
                unsafe_allow_html=True,
            )
            right.markdown(
                '<div style="text-align:right;font-weight:800;color:#0F172A;">'
                '{} <span style="color:#64748B;font-weight:700;">({:.1f}%)</span>'
                '</div>'.format(value, pct),
                unsafe_allow_html=True,
            )
            st.progress(_clamp01(pct / 100.0))

    st.markdown("<br>", unsafe_allow_html=True)

    # ═══ 6. ALTERNATIVE PLAN (collapsible) ═══════════════════════════════════
    if alt:
        _alt_rendered_this_run = False
        with st.expander("🔁  View Alternative Plan", expanded=st.session_state.show_alt_plan):
            _alt_rendered_this_run = True
            st.session_state.show_alt_plan = True
            alt_apps = alt.get("selected_applicants", [])
            st.dataframe(
                build_results_df(alt_apps),
                use_container_width=True, hide_index=True,
            )
            a1, a2 = st.columns(2)
            a1.metric("Expected Return",  fmt_inr(alt["total_profit"]))
            a2.metric("Loan Distributed", fmt_inr(alt["total_loan_used"]))

    # ═══ 7. TECHNICAL DETAILS (hidden by default) ════════════════════════════
    st.markdown("---")
    tech_clicked_this_run = False
    if st.button("🔬  Show / Hide Technical Details", key="btn_tech"):
        st.session_state.show_tech = not st.session_state.show_tech
        tech_clicked_this_run = True

    # If user closed Alternative Plan (and this rerun was not caused by tech toggle),
    # allow it to stay closed on subsequent reruns.
    if alt and st.session_state.show_alt_plan and not _alt_rendered_this_run and not tech_clicked_this_run:
        st.session_state.show_alt_plan = False

    if st.session_state.show_tech:
        _render_technical_details(data, budget, greedy, dp)


def _render_technical_details(
    data: Dict,
    budget: float,
    greedy: Optional[Dict],  # FIX 3: was dict | None (Python 3.10+)
    dp: Optional[Dict],      # FIX 3: was dict | None (Python 3.10+)
):
    st.markdown(
        """
        <div style="background:#F8FAFC;border:1px solid #E2E8F0;
                    border-radius:10px;padding:20px 24px;margin-top:8px;">
          <div style="font-size:0.72rem;font-weight:700;letter-spacing:0.1em;
                      text-transform:uppercase;color:#64748B;margin-bottom:12px;">
            Technical Analysis — Algorithm Comparison
          </div>
        """,
        unsafe_allow_html=True,
    )

    if greedy and dp:
        tc1, tc2 = st.columns(2)

        with tc1:
            st.markdown(
                """
                <div class="lw-tech">
                  <div class="title">Greedy Algorithm</div>
                  <div class="sub">Time: O(n log n) &nbsp;|&nbsp; Space: O(n)</div>
                  <div class="grid">
                    <div class="label">Total Profit</div>
                    <div class="value">{profit}</div>
                    <div class="label">Loan Distributed</div>
                    <div class="value">{loan}</div>
                    <div class="label">Applicants Selected</div>
                    <div class="value">{count}</div>
                  </div>
                </div>
                """.format(
                    profit=fmt_inr(greedy["total_profit"]),
                    loan=fmt_inr(greedy["total_loan_used"]),
                    count=str(greedy["selected_count"]),
                ),
                unsafe_allow_html=True,
            )

        with tc2:
            st.markdown(
                """
                <div class="lw-tech">
                  <div class="title">Dynamic Programming</div>
                  <div class="sub">Time: O(n × W) &nbsp;|&nbsp; Space: O(n × W)</div>
                  <div class="grid">
                    <div class="label">Total Profit</div>
                    <div class="value">{profit}</div>
                    <div class="label">Loan Distributed</div>
                    <div class="value">{loan}</div>
                    <div class="label">Applicants Selected</div>
                    <div class="value">{count}</div>
                  </div>
                </div>
                """.format(
                    profit=fmt_inr(dp["total_profit"]),
                    loan=fmt_inr(dp["total_loan_used"]),
                    count=str(dp["selected_count"]),
                ),
                unsafe_allow_html=True,
            )

        diff = dp["total_profit"] - greedy["total_profit"]
        if diff > 0.01:
            st.success(
                "DP found **{}** more in expected return than Greedy.".format(
                    fmt_inr(diff))
            )
        else:
            st.info(
                "Both algorithms found the same optimal solution for this dataset."
            )

        # FIX 6: proper chart in technical section
        st.markdown("<br>**Expected Return Comparison**", unsafe_allow_html=True)
        render_comparison_chart(dp["total_profit"], greedy["total_profit"])

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────────────────────────────────────

def render_header():
    st.markdown(
        """
        <div class="bank-header">
          <h1>🏦 LoanWise</h1>
          <p>Smart Loan Portfolio Optimization System &nbsp;·&nbsp;
             Internal Banking Dashboard</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    init_session_state()
    render_header()

    budget, run_clicked = render_sidebar()

    # Input section updates session_state; does NOT return data directly
    render_input_section()

    # Detect input changes and mark existing results stale
    current_bytes = get_active_csv_bytes()
    current_hash = compute_input_hash(current_bytes, budget)
    # Mark stale when switching between different valid inputs
    if current_hash is not None and current_hash != st.session_state.last_input_hash:
        st.session_state.last_input_hash = current_hash
        if st.session_state.result_data is not None:
            st.session_state.results_stale = True
    # Also mark stale when we had a previous input but now have no file
    if current_hash is None and st.session_state.last_input_hash is not None:
        st.session_state.last_input_hash = None
        if st.session_state.result_data is not None:
            st.session_state.results_stale = True

    # ── Execute optimization ──────────────────────────────────────────────────
    if run_clicked:
        csv_bytes = get_active_csv_bytes()

        if csv_bytes is None:
            active = st.session_state.active_mode
            if active == "csv":
                st.error(
                    "⚠️  No CSV file uploaded. "
                    "Please upload a file in the **Upload CSV File** tab."
                )
            else:
                st.error(
                    "⚠️  Manual entry has validation errors. "
                    "Please fix the highlighted issues before running."
                )
        else:
            tmp_path = None
            try:
                tmp_path = write_temp_csv(csv_bytes)
                with st.spinner("Running optimization engine..."):
                    result = call_backend(tmp_path, budget)

                st.session_state.result_data   = result
                st.session_state.result_budget = budget
                st.session_state.results_stale = False
                # Freeze the “All Applications” list to the exact input used for this run
                st.session_state.last_run_applicants_display = get_active_applicants_display()
                st.success("Optimization complete.")

            except RuntimeError as exc:
                st.error("**Optimization failed:**\n\n{}".format(exc))
            except subprocess.TimeoutExpired:
                st.error("The optimization engine timed out.")
            finally:
                if tmp_path and os.path.exists(tmp_path):
                    os.unlink(tmp_path)

    # ── Render results ────────────────────────────────────────────────────────
    if st.session_state.result_data is not None:
        st.markdown("---")
        section_title("Optimization Results")
        if st.session_state.results_stale:
            st.warning("Results are from a previous run. Your inputs changed — click **Run Optimization** again.")
        render_results(st.session_state.result_data, st.session_state.result_budget)
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="text-align:center;padding:48px 0;color:#94A3B8;">
              <div style="font-size:3rem;">📊</div>
              <div style="font-size:1.1rem;font-weight:600;margin-top:10px;
                          color:#64748B;">
                Results will appear here after optimization
              </div>
              <div style="font-size:0.9rem;margin-top:6px;">
                Enter applicant data · set a budget · click Run Optimization
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
    