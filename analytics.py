import pandas as pd
import plotly.express as px
import streamlit as st

# Official figures published by the Senate of Pakistan.
# Values are intentionally labelled to distinguish categories that are not identical.
ANNUAL_DATA = {
    "2025–2026": {
        "period": "12 March 2025 – 11 March 2026",
        "sessions": 12,
        "sittings": 64,
        "working_days": 112,
        "joint_sittings": 3,
        "private_members_days": 11,
        "government_bills_introduced": 17,
        "government_bills_passed": 14,
        "bills_received_from_na": 31,
        "government_or_received_bills_passed": 33,
        "private_member_bills_introduced": 40,
        "private_member_bills_passed": 44,
        "starred_questions_received": 1157,
        "starred_questions_answered_on_floor": 479,
        "resolutions_tabled": 85,
        "resolutions_adopted": 19,
        "resolutions_unanimous": 15,
        "motions_received": 119,
        "committees": 38,
        "committee_meetings": 346,
        "committee_hours": 780,
        "committee_reports": 106,
        "peak_attendance": 88,
        "average_attendance": 55,
    },
    "2024–2025": {
        "period": "12 March 2024 – 11 March 2025",
        "sessions": 12,
        "working_days": 111,
        "joint_sittings": 3,
        "government_bills_passed": 12,
        "private_member_bills_passed": 11,
    },
}

SOURCES = {
    "2025–2026": "https://senate.gov.pk/en/news_content.php?catid=6&cattitle=Press+Releases&id=NzE2OA%3D%3D&subcatid=59",
    "2024–2025": "https://senate.gov.pk/en/news_content.php?id=NTk0NQ%3D%3D",
    "reports": "https://senate.gov.pk/en/reports.php",
}


def metric_card(label: str, value, detail: str = ""):
    st.markdown(
        f"""
        <div class='metric-card'>
          <div class='metric-label'>{label}</div>
          <div class='metric-value'>{value:,}</div>
          <div class='metric-detail'>{detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_analytics():
    st.subheader("📊 Senate Parliamentary Analytics")
    st.write(
        "This section turns the Senate's published annual performance figures into visual analytics. "
        "The latest complete annual reporting period is shown first."
    )

    period = st.selectbox("Analytics period", list(ANNUAL_DATA.keys()), index=0)
    data = ANNUAL_DATA[period]
    st.caption(f"Reporting period: {data['period']}")

    st.markdown("### Headline indicators")
    if period == "2025–2026":
        cols = st.columns(6)
        metrics = [
            ("Sessions", data["sessions"], "Senate sessions"),
            ("Sittings", data["sittings"], "House sittings"),
            ("Working days", data["working_days"], "Reported working days"),
            ("Bills passed", data["government_or_received_bills_passed"], "Government/received category"),
            ("PM bills passed", data["private_member_bills_passed"], "Private Members' Bills"),
            ("Committee meetings", data["committee_meetings"], "38 committees"),
        ]
        for col, item in zip(cols, metrics):
            with col:
                metric_card(*item)
    else:
        cols = st.columns(4)
        metrics = [
            ("Sessions", data["sessions"], "Senate sessions"),
            ("Working days", data["working_days"], "Reported working days"),
            ("Government bills passed", data["government_bills_passed"], "Published category"),
            ("PM bills passed", data["private_member_bills_passed"], "Published category"),
        ]
        for col, item in zip(cols, metrics):
            with col:
                metric_card(*item)

    st.markdown("### Legislation")
    if period == "2025–2026":
        legislative = pd.DataFrame([
            {"Metric": "Government Bills introduced", "Count": data["government_bills_introduced"]},
            {"Metric": "Government Bills passed", "Count": data["government_bills_passed"]},
            {"Metric": "Bills received from National Assembly", "Count": data["bills_received_from_na"]},
            {"Metric": "Government / received Bills passed", "Count": data["government_or_received_bills_passed"]},
            {"Metric": "Private Members' Bills introduced", "Count": data["private_member_bills_introduced"]},
            {"Metric": "Private Members' Bills passed", "Count": data["private_member_bills_passed"]},
        ])
        fig = px.bar(
            legislative,
            x="Count",
            y="Metric",
            orientation="h",
            text="Count",
            title="Legislative output — 2025–2026",
            labels={"Count": "Number of bills", "Metric": ""},
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(height=430, margin=dict(l=10, r=25, t=60, b=20), showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.caption(
            "Important: the Senate's annual report states that 31 bills received from the National Assembly were considered, "
            "with 33 government/received bills passed in total; private members' bills are reported separately."
        )
    else:
        legislative = pd.DataFrame([
            {"Metric": "Government Bills passed", "Count": data["government_bills_passed"]},
            {"Metric": "Private Members' Bills passed", "Count": data["private_member_bills_passed"]},
        ])
        fig = px.bar(
            legislative,
            x="Metric",
            y="Count",
            text="Count",
            title="Bills passed — 2024–2025 published categories",
            labels={"Count": "Number of bills", "Metric": ""},
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(height=360, margin=dict(l=10, r=20, t=60, b=25), showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("### Oversight and parliamentary scrutiny")
    if period == "2025–2026":
        oversight = pd.DataFrame([
            {"Metric": "Starred questions received", "Count": data["starred_questions_received"]},
            {"Metric": "Starred questions answered on floor", "Count": data["starred_questions_answered_on_floor"]},
            {"Metric": "Motions received", "Count": data["motions_received"]},
            {"Metric": "Resolutions tabled", "Count": data["resolutions_tabled"]},
            {"Metric": "Resolutions adopted", "Count": data["resolutions_adopted"]},
            {"Metric": "Committee reports", "Count": data["committee_reports"]},
        ])
        fig = px.bar(
            oversight,
            x="Count",
            y="Metric",
            orientation="h",
            text="Count",
            title="Questions, motions, resolutions and reports — 2025–2026",
            labels={"Count": "Number", "Metric": ""},
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(height=430, margin=dict(l=10, r=25, t=60, b=20), showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        c1, c2 = st.columns(2)
        with c1:
            q_df = pd.DataFrame([
                {"Status": "Answered on floor", "Count": data["starred_questions_answered_on_floor"]},
                {"Status": "Other / not answered on floor", "Count": data["starred_questions_received"] - data["starred_questions_answered_on_floor"]},
            ])
            fig = px.pie(q_df, names="Status", values="Count", hole=0.45, title="Starred questions: floor answers")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with c2:
            r_df = pd.DataFrame([
                {"Status": "Adopted", "Count": data["resolutions_adopted"]},
                {"Status": "Not adopted", "Count": data["resolutions_tabled"] - data["resolutions_adopted"]},
            ])
            fig = px.pie(r_df, names="Status", values="Count", hole=0.45, title="Resolutions: tabled vs adopted")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("### Committees and House activity")
    if period == "2025–2026":
        committee = pd.DataFrame([
            {"Metric": "Committees", "Count": data["committees"]},
            {"Metric": "Committee meetings", "Count": data["committee_meetings"]},
            {"Metric": "Committee reports", "Count": data["committee_reports"]},
            {"Metric": "Joint sittings", "Count": data["joint_sittings"]},
            {"Metric": "Private Members' Days", "Count": data["private_members_days"]},
        ])
        fig = px.bar(
            committee,
            x="Metric",
            y="Count",
            text="Count",
            title="Committees and House activity — 2025–2026",
            labels={"Count": "Count", "Metric": ""},
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(height=380, margin=dict(l=10, r=20, t=60, b=25), showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("### 2024–2025 → 2025–2026 comparison")
    comparable = pd.DataFrame([
        {"Metric": "Sessions", "2024–2025": ANNUAL_DATA["2024–2025"]["sessions"], "2025–2026": ANNUAL_DATA["2025–2026"]["sessions"]},
        {"Metric": "Working days", "2024–2025": ANNUAL_DATA["2024–2025"]["working_days"], "2025–2026": ANNUAL_DATA["2025–2026"]["working_days"]},
        {"Metric": "Joint sittings", "2024–2025": ANNUAL_DATA["2024–2025"]["joint_sittings"], "2025–2026": ANNUAL_DATA["2025–2026"]["joint_sittings"]},
    ])
    long = comparable.melt(id_vars="Metric", var_name="Year", value_name="Count")
    fig = px.bar(long, x="Metric", y="Count", color="Year", barmode="group", text="Count", title="Selected comparable activity")
    fig.update_layout(height=380, margin=dict(l=10, r=20, t=60, b=25))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("### Data sources")
    st.markdown(f"- [Senate Annual Report / release 2025–2026]({SOURCES['2025–2026']})")
    st.markdown(f"- [Senate Annual Report / release 2024–2025]({SOURCES['2024–2025']})")
    st.markdown(f"- [Senate Publications and Annual Reports]({SOURCES['reports']})")
    st.info(
        "These analytics are descriptive. A number such as 'bills passed' is an activity measure, not an assessment of legislative quality or effectiveness."
    )
