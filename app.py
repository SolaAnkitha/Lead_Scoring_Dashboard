"""
Lead Scoring Dashboard
Author: Ankeetha
Description: A streamlit app that calculates a lead score based on various factors 
"""
import streamlit as st
from datetime import datetime
import pandas as pd
def compute_lead_score(lead):
    score = 0
    reasons = []

    if lead["is_demo_requested"]:
        score += 45
        reasons.append("Requested Demo (+45)")

    if lead["registered"]:
        score += 28
        reasons.append("Completed Registration (+28)")

    if lead["referral"]:
        score += 21
        reasons.append("Referral Lead (+21)")

    if lead.get("company_size") == "Enterprise":
        score += 20
        reasons.append("Enterprise Client (+20)")


    if lead["enquiry_channel"] == "Call":
        score += 17
        reasons.append("Enquiry via Call (+17)")

    if lead["enquiry_channel"] == "WhatsApp":
        score += 15
        reasons.append("Enquiry via WhatsApp (+15)")

    if lead["event_lead"]:
        score += 15
        reasons.append("Lead from Event (+15)")

    if lead["checked_pricing"]:
        score += 15
        reasons.append("Compared Pricing (+15)")

    days_diff = (datetime.now().date() - lead["enquiry_date"]).days

    if days_diff <= 2:
        score += 10
        reasons.append("Recent Enquiry (+10)")
    elif days_diff <= 7:
        score += 5
        reasons.append("Enquiry within 7 days (+5)")

    return min(score, 100), reasons


def recommend_action(score):
    if score >= 80:
        return "Hot"
    elif score >= 50:
        return " Warm "
    elif score >= 30:
        return " Cold "
    else:
        return " Very Cold"


# UI
st.title(" AI Lead Scoring Dashboard")

st.sidebar.header("Enter Lead Details")

is_demo_requested = st.sidebar.checkbox("Demo Requested")
registered = st.sidebar.checkbox("Registration Completed")
referral = st.sidebar.checkbox("Referral Lead")
event_lead = st.sidebar.checkbox("Event Lead")
checked_pricing = st.sidebar.checkbox("Compared Pricing")

enquiry_channel = st.sidebar.selectbox(
    "Enquiry Channel",
    ["None", "Call", "WhatsApp"]
)
company_size = st.sidebar.selectbox(
    "Company Size",
    ["Small", "Medium", "Enterprise"]
)


enquiry_date = st.sidebar.date_input("Enquiry Date")

if st.sidebar.button("Calculate Score"):

    lead_data = {
        "is_demo_requested": is_demo_requested,
        "registered": registered,
        "referral": referral,
        "event_lead": event_lead,
        "checked_pricing": checked_pricing,
        "enquiry_channel": enquiry_channel,
        "enquiry_date": enquiry_date,
        "company_size": company_size
    }

    score, reasons = compute_lead_score(lead_data)
    action = recommend_action(score)

    st.subheader(" Lead Score")
    st.progress(score)
    st.metric("Score", f"{score}/100")

    st.subheader(" Explanation")
    for r in reasons:
        st.write("right", r)

    st.subheader("Recommended Action")
    st.success(action)

    st.subheader("Score Visualization")
    df = pd.DataFrame({
        "Category": ["Lead Score"],
        "Value": [score]
    })
    st.bar_chart(df.set_index("Category"))