"""
ClaimSense: Streamlit Insurance Adjuster Dashboard
Interactive Claims Adjudication, RAG Policy Exploration & Fraud Analytics
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from src.data.schema import ClaimInput, ClaimType
from src.rag.chain import AdjudicationEngine
from src.rag.corpus import POLICY_CORPUS
from src.data.generate_synthetic_data import generate_synthetic_claims

st.set_page_config(
    page_title="ClaimSense — Claims Adjudication Assistant",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Engine
@st.cache_resource
def get_engine():
    return AdjudicationEngine()

@st.cache_data
def get_sample_claims():
    return generate_synthetic_claims(count=40)

engine = get_engine()
sample_claims = get_sample_claims()

# Sidebar
st.sidebar.title("🧾 ClaimSense AI")
st.sidebar.caption("RAG-Based Insurance Claims Adjudication")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation",
    ["🎯 Adjudicate Claim", "📋 Claims Queue", "📊 Fraud & Risk Analytics", "📖 Policy Knowledge Base"]
)
st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip**: Select a sample claim or customize values to test multi-factor fraud detection & RAG citation.")

# Header
st.title("🧾 ClaimSense: Intelligent Claims Adjudication")
st.markdown("Policy-aware claims decisioning powered by RAG retrieval and multi-factor fraud risk classification.")

# ─────────────────────────────────────────────────────────────
# PAGE 1: ADJUDICATE CLAIM
# ─────────────────────────────────────────────────────────────
if page == "🎯 Adjudicate Claim":
    st.subheader("1. Claim Intake & Details")
    
    col_sel, col_quick = st.columns([2, 1])
    with col_sel:
        claim_options = [f"{c['claim_id']} — {c['claim_type']} (₹{c['claim_amount']:,})" for c in sample_claims]
        selected_idx = st.selectbox("Select from Preloaded Claims or customize below:", range(len(claim_options)), format_func=lambda x: claim_options[x])
    
    chosen = sample_claims[selected_idx]

    with st.form("adjudication_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            claim_id = st.text_input("Claim ID", value=chosen["claim_id"])
            policy_number = st.text_input("Policy Number", value=chosen["policy_number"])
            policy_holder = st.text_input("Policyholder Name", value=chosen["policy_holder_name"])
        with c2:
            claim_type_val = st.selectbox("Claim Type", [t.value for t in ClaimType], index=[t.value for t in ClaimType].index(chosen["claim_type"]))
            claim_amount = st.number_input("Claim Amount (₹)", value=float(chosen["claim_amount"]), min_value=1000.0, step=10000.0)
            sum_insured = st.number_input("Sum Insured (₹)", value=float(chosen["sum_insured"]), min_value=10000.0, step=50000.0)
        with c3:
            policy_start = st.date_input("Policy Inception Date", value=datetime.strptime(chosen["policy_start_date"], "%Y-%m-%d").date())
            incident_dt = st.date_input("Incident Date", value=datetime.strptime(chosen["incident_date"], "%Y-%m-%d").date())
            prior_claims = st.number_input("Prior Claims Count", value=int(chosen["prior_claims_count"]), min_value=0, max_value=20)

        incident_desc = st.text_area("Incident Description & Circumstances", value=chosen["incident_description"], height=100)
        submit_btn = st.form_submit_button("⚡ Run Adjudication & RAG Retrieval", use_container_width=True)

    if submit_btn or st.session_state.get("auto_run", True):
        claim_obj = ClaimInput(
            claim_id=claim_id,
            policy_number=policy_number,
            policy_holder_name=policy_holder,
            claim_type=ClaimType(claim_type_val),
            claim_amount=claim_amount,
            sum_insured=sum_insured,
            policy_start_date=policy_start.strftime("%Y-%m-%d"),
            incident_date=incident_dt.strftime("%Y-%m-%d"),
            incident_time="14:30",
            incident_location="Mumbai",
            prior_claims_count=prior_claims,
            incident_description=incident_desc
        )

        with st.spinner("Analyzing claim, retrieving policy clauses, assessing fraud risk..."):
            res = engine.adjudicate(claim_obj)

        st.markdown("---")
        st.subheader("2. Adjudication Decision & Intelligence Summary")

        # Metric Cards
        m1, m2, m3, m4 = st.columns(4)
        
        # Color coding recommendation
        rec_color = "🟢" if res.recommendation.value == "Approve" else ("🟡" if "Investigation" in res.recommendation.value else "🔴")
        m1.metric("Recommendation", f"{rec_color} {res.recommendation.value}")
        
        risk_color = "🟢" if res.fraud_risk_level.value == "Low" else ("🟡" if res.fraud_risk_level.value == "Medium" else "🔴")
        m2.metric("Fraud Risk Score", f"{res.fraud_risk_score}/100 ({risk_color} {res.fraud_risk_level.value})")
        
        m3.metric("Sum Insured Utilization", f"{round(res.claim_to_sum_insured_ratio * 100, 1)}%")
        m4.metric("Days Since Policy Inception", f"{res.days_since_policy_start} Days")

        # Rationale Callout
        if res.recommendation.value == "Approve":
            st.success(f"**Adjudication Rationale**: {res.adjudication_rationale}")
        elif "Investigation" in res.recommendation.value:
            st.warning(f"**Adjudication Rationale**: {res.adjudication_rationale}")
        else:
            st.error(f"**Adjudication Rationale**: {res.adjudication_rationale}")

        # Two Column details: Risk Factors & Cited Clauses
        col_risk, col_clauses = st.columns([1, 1])

        with col_risk:
            st.markdown("### ⚠️ Risk & Anomaly Factors")
            if res.risk_factors:
                for rf in res.risk_factors:
                    st.markdown(f"- **{rf.factor_name}** (`+{rf.impact_score} pts`)  \n  *{rf.description}*")
            else:
                st.info("No significant risk or anomaly triggers detected for this claim.")

            if res.investigation_action_items:
                st.markdown("#### 📝 Recommended Next Action Items:")
                for act in res.investigation_action_items:
                    st.markdown(f"- {act}")

        with col_clauses:
            st.markdown("### 📜 RAG-Retrieved Policy Clauses")
            for clause in res.cited_clauses:
                badge = "🔴 Exclusion Clause" if clause.is_exclusion else "🟢 Insuring Agreement"
                with st.expander(f"{clause.clause_id} — {clause.title} ({badge})", expanded=True):
                    st.caption(f"**Policy Type:** {clause.policy_type} | **Section:** {clause.section} | **Match Score:** {clause.relevance_score}")
                    st.write(clause.content)

# ─────────────────────────────────────────────────────────────
# PAGE 2: CLAIMS QUEUE
# ─────────────────────────────────────────────────────────────
elif page == "📋 Claims Queue":
    st.subheader("Claims Triage & Processing Queue")
    
    df_claims = pd.DataFrame(sample_claims)
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_type = st.multiselect("Filter by Claim Type", options=df_claims["claim_type"].unique(), default=df_claims["claim_type"].unique())
    with col_f2:
        search_query = st.text_input("Search Policyholder or Claim ID", "")

    filtered_df = df_claims[df_claims["claim_type"].isin(filter_type)]
    if search_query:
        filtered_df = filtered_df[
            filtered_df["claim_id"].str.contains(search_query, case=False) |
            filtered_df["policy_holder_name"].str.contains(search_query, case=False)
        ]

    st.dataframe(
        filtered_df[["claim_id", "policy_number", "claim_type", "claim_amount", "sum_insured", "incident_date", "prior_claims_count"]],
        use_container_width=True
    )

# ─────────────────────────────────────────────────────────────
# PAGE 3: FRAUD & RISK ANALYTICS
# ─────────────────────────────────────────────────────────────
elif page == "📊 Fraud & Risk Analytics":
    st.subheader("Claims Intelligence & Adjudication Analytics")
    
    adjudicated_records = [engine.adjudicate(ClaimInput(**c)) for c in sample_claims]
    
    a1, a2 = st.columns(2)
    with a1:
        st.markdown("#### Adjudication Recommendation Distribution")
        rec_data = pd.Series([r.recommendation.value for r in adjudicated_records]).value_counts().reset_index()
        rec_data.columns = ["Recommendation", "Count"]
        st.bar_chart(rec_data.set_index("Recommendation"))

    with a2:
        st.markdown("#### Fraud Risk Level Breakdown")
        risk_data = pd.Series([r.fraud_risk_level.value for r in adjudicated_records]).value_counts().reset_index()
        risk_data.columns = ["Risk Level", "Count"]
        st.bar_chart(risk_data.set_index("Risk Level"))

    st.markdown("#### Top Cited Policy Clauses (Frequency)")
    clause_counts = {}
    for r in adjudicated_records:
        for cl in r.cited_clauses:
            clause_counts[f"{cl.clause_id}: {cl.title[:30]}..."] = clause_counts.get(f"{cl.clause_id}: {cl.title[:30]}...", 0) + 1
    
    df_clause = pd.DataFrame(list(clause_counts.items()), columns=["Clause", "Citations"]).sort_values("Citations", ascending=False).head(8)
    st.dataframe(df_clause, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# PAGE 4: POLICY KNOWLEDGE BASE
# ─────────────────────────────────────────────────────────────
elif page == "📖 Policy Knowledge Base":
    st.subheader("Policy Terms, Exclusion Clauses & IRDAI Directives")
    
    search_term = st.text_input("Search Knowledge Base (e.g., 'fire', 'waiting period', 'intoxicated', 'burglary')", "")
    
    for p in POLICY_CORPUS:
        if not search_term or (search_term.lower() in p["title"].lower() or search_term.lower() in p["content"].lower() or search_term.lower() in p["policy_type"].lower()):
            badge = "🔴 Exclusion Clause" if p.get("is_exclusion") else "🟢 Insuring Agreement"
            with st.expander(f"{p['clause_id']} — {p['title']} [{badge}]"):
                st.caption(f"**Policy Type**: {p['policy_type']} | **Section**: {p['section']}")
                st.write(p["content"])
