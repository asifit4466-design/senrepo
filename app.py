import streamlit as st
from graphviz import Digraph
from workflows import WORKFLOWS, DOMAIN, SOURCES
from analytics import render_analytics

st.set_page_config(
    page_title="Senate of Pakistan — Parliamentary Business Workflows",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
.block-container{padding-top:1rem;max-width:1550px}
.hero{padding:1.45rem 1.7rem;border-radius:18px;background:linear-gradient(135deg,#073b2a,#126448);color:#fff;margin-bottom:1rem;box-shadow:0 5px 18px rgba(0,0,0,.08)}
.hero h1{margin:0 0 .3rem 0;font-size:2rem}.hero p{margin:.2rem 0;opacity:.95}
.card{padding:1rem;border:1px solid #cfd9d3;border-radius:14px;background:#fff;min-height:130px;color:#111827}
.card h4{color:#111827;margin-bottom:.4rem}.card p{color:#1f2937}
.step{padding:.9rem 1rem;border:1px solid #d7dfda;border-radius:12px;background:#fff;margin-bottom:.55rem;color:#111827}
.step b{color:#0b4e38}.muted{color:#334155}.note{padding:.9rem 1rem;border-left:4px solid #16805a;background:#eff8f3;border-radius:8px;color:#10231a}
.legend span{display:inline-block;padding:5px 9px;border-radius:12px;margin:3px;font-size:.82rem;border:1px solid #d5ddd8;color:#17211c;background:#fff}
.flow-banner{padding:.85rem 1rem;background:#f7f9f8;border:1px solid #d7dfda;border-radius:12px;color:#111827;margin:.6rem 0 1rem 0}
.flow-banner strong{color:#0b4e38}
.navrow{display:flex;justify-content:space-between;gap:.75rem;margin-top:.5rem}
.navhint{font-size:.9rem;color:#475569;text-align:center;padding-top:.6rem}
.metric-card{padding:1rem;border:1px solid #d7dfda;border-radius:14px;background:#fff;min-height:115px;color:#111827}
.metric-label{font-size:.86rem;font-weight:700;color:#334155}.metric-value{font-size:2rem;line-height:1.15;font-weight:800;color:#0b4e38}.metric-detail{font-size:.78rem;color:#64748b;margin-top:.25rem}
.section-kicker{font-size:.8rem;font-weight:800;letter-spacing:.04em;color:#64748b;text-transform:uppercase;margin-bottom:.25rem}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="hero">
<h1>🏛️ Senate of Pakistan — Parliamentary Business Workflow Explorer</h1>
<p><b>Follow the work visually:</b> start at the left, follow the arrows →, and see who acts, what happens next, and where the matter ends.</p>
<p>Use the step navigator to move through a workflow without guessing the sequence.</p>
</div>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("🔎 Choose Parliamentary Workflow")
    categories = []
    for k, v in WORKFLOWS.items():
        if v["category"] not in categories:
            categories.append(v["category"])
    cat = st.selectbox("Filter by business area", ["ALL"] + categories)
    available = [k for k, v in WORKFLOWS.items() if cat == "ALL" or v["category"] == cat]
    selected = st.selectbox("Select workflow", available)
    st.divider()
    st.markdown("### 📚 Recommended learning order")
    st.markdown(
        "1. Master Map\n"
        "2. Senator selection\n"
        "3. Chairman / Deputy Chairman\n"
        "4. Session & Orders of Day\n"
        "5. Ordinary Bill\n"
        "6. Money Bill\n"
        "7. Constitutional Amendment\n"
        "8. Committees\n"
        "9. Questions & Calling Attention\n"
        "10. Motions & Resolutions\n"
        "11. Joint Sitting\n"
        "12. Presidential Assent"
    )
    st.divider()
    st.markdown("### ⌨️ Navigation")
    st.caption("Use the on-screen ← Previous and Next → controls to move through each workflow step. The diagram always reads left → right.")
    st.divider()
    st.caption("Educational workflow model. Check the latest Constitution and Senate Rules for authoritative legal requirements.")

wf = WORKFLOWS[selected]
steps = wf["steps"]

COLORS = {
    "start": "#d8f3e5",
    "end": "#d8f3e5",
    "house": "#e3edff",
    "people": "#eee2ff",
    "schedule": "#fff1c9",
    "business": "#e4f7f2",
    "committee": "#e7f0f8",
    "decision": "#ffe1e1",
    "external": "#eee7ff",
    "record": "#edf0f2",
    "process": "#f7f8f7",
}


def graph_for(steps, focus=None):
    g = Digraph(format="svg")
    g.attr(rankdir="LR", bgcolor="transparent", pad=".40", nodesep=".46", ranksep=".72")
    g.attr(
        "node",
        shape="box",
        style="rounded,filled",
        fontname="Segoe UI",
        fontsize="11",
        margin=".18,.14",
        color="#aebdb5",
        fontcolor="#111827",
    )
    # Strong arrowheads make the legal/business sequence visually unambiguous.
    g.attr("edge", color="#305c4b", arrowsize="1.0", penwidth="2.2", arrowhead="normal", fontcolor="#111827")
    for i, (num, title, desc, kind) in enumerate(steps):
        label = f"{num}. {title}"
        if i == 0 or i == len(steps) - 1:
            label += f"\n{desc}"
        else:
            label += "\n" + desc
        attrs = {"fillcolor": COLORS.get(kind, "#f7f8f7")}
        if focus == i:
            attrs.update({"penwidth": "4", "color": "#0b6b4b", "fontcolor": "#071b12"})
        g.node(f"n{i}", label=label, **attrs)
        if i:
            edge_label = "NEXT"
            g.edge(f"n{i-1}", f"n{i}", label=edge_label, fontsize="8")
    return g


is_master = selected.startswith("00 — MASTER")

if is_master:
    t1, t2, t3, t4, t5 = st.tabs(
        ["🗺️ Workflow Map", "📊 Analytics", "🧩 Business Domain", "👥 Who Does What", "📚 Sources"]
    )
else:
    t1, t2, t3 = st.tabs(["🔄 Workflow", "🧠 Understand It", "📚 Sources"])

with t1:
    st.markdown(f'<div class="section-kicker">{wf["category"]}</div>', unsafe_allow_html=True)
    st.subheader(selected)
    st.write(wf["summary"])
   

    if "workflow_step" not in st.session_state or st.session_state.get("workflow_selected") != selected:
        st.session_state.workflow_selected = selected
        st.session_state.workflow_step = 0

    idx = int(st.session_state.workflow_step)
    idx = max(0, min(idx, len(steps) - 1))
    st.session_state.workflow_step = idx

    st.graphviz_chart(graph_for(steps, focus=idx), use_container_width=True)

    cols = st.columns([1, 3, 1])
    with cols[0]:
        if st.button("← Previous", disabled=idx == 0, use_container_width=True):
            st.session_state.workflow_step = max(0, idx - 1)
            st.rerun()
    with cols[1]:
        st.markdown(
            f'<div class="navhint"><b>Step {idx + 1} of {len(steps)}</b> &nbsp; • &nbsp; {steps[idx][1]} &nbsp; • &nbsp; <b>Use the arrows → to continue the business flow</b></div>',
            unsafe_allow_html=True,
        )
    with cols[2]:
        if st.button("Next →", disabled=idx == len(steps) - 1, use_container_width=True):
            st.session_state.workflow_step = min(len(steps) - 1, idx + 1)
            st.rerun()

    labels = [f"{i + 1}. {title}" for i, (_, title, _, _) in enumerate(steps)]
    picked = st.selectbox(
        "Jump to a workflow step",
        range(len(labels)),
        index=idx,
        format_func=lambda i: labels[i],
        key=f"jump_{selected}",
    )
    if picked != idx:
        st.session_state.workflow_step = int(picked)
        st.rerun()

    num, title, desc, kind = steps[idx]
    st.markdown(f"### Step {num}: {title}")
    st.write(desc)
    st.caption(f"Process type: {kind}  •  Next → {steps[idx + 1][1] if idx < len(steps) - 1 else 'Final outcome'}")

    # st.markdown('<div class="note"><b>Diagram rule:</b> every connector has a visible arrowhead and the word <b>NEXT</b>. This is intentional so a first-time reader can follow the sequence without knowing parliamentary jargon.</div>', unsafe_allow_html=True)

    with st.expander("Show all steps as a continuous arrow sequence"):
        arrow_parts = []
        for i, (_, title, _, _) in enumerate(steps):
            arrow_parts.append(f"<b>{i + 1}. {title}</b>")
        st.markdown(" <span style='color:#0b4e38;font-weight:700;'> → </span> ".join(arrow_parts), unsafe_allow_html=True)

with t2:
    if is_master:
        render_analytics()
    else:
        st.subheader("🧠 Understand the workflow like a process")
        st.write("Read the selected workflow as a chain of responsibility. The arrows show the intended sequence.")
        for i, (n, t, d, k) in enumerate(steps):
            arrow = "→" if i < len(steps) - 1 else "✓"
            st.markdown(
                f'<div class="step"><b>{i + 1}. {t}</b> <span style="color:#0b6b4b;font-weight:800;">{arrow}</span><br><span class="muted">{d}</span></div>',
                unsafe_allow_html=True,
            )

if is_master:
    with t3:
        st.subheader("🧩 All Senate Parliamentary Business Areas")
        st.write("Each card is a major business domain. Select a workflow from the sidebar to see its complete arrow-by-arrow process.")
        cols = st.columns(2)
        for i, (domain, items) in enumerate(DOMAIN.items()):
            with cols[i % 2]:
                st.markdown(
                    f'<div class="card"><h4>{domain}</h4><p>{" • ".join(items)}</p></div>',
                    unsafe_allow_html=True,
                )
                st.write("")
    with t4:
        roles = {
            "Senators": "Propose, debate, question, amend, vote and participate in committees.",
            "Chairman / Deputy Chairman": "Preside over proceedings and apply the constitutional/rules framework.",
            "Senate Secretariat": "Supports scheduling, notices, legislation, questions, records, committees and other House functions.",
            "Committees": "Conduct detailed scrutiny, oversight and reporting within their mandates.",
            "Government / Ministers": "Introduce Government business and answer parliamentary scrutiny where applicable.",
            "National Assembly": "Participates in two-House legislation and financial/constitutional processes as provided by law.",
            "President": "Performs constitutional functions in relation to Bills and other specified matters.",
        }
        for role, desc in roles.items():
            st.markdown(f'<div class="card"><h4>{role}</h4><p>{desc}</p></div>', unsafe_allow_html=True)
            st.write("")
    with t5:
        st.subheader("📚 Official reference material")
        for title, url in SOURCES:
            st.markdown(f"- [{title}]({url})")
        st.info("This application is an educational visualisation. The Constitution and the current Senate Rules remain the authoritative sources.")
else:
    with t3:
        st.subheader("📚 Official reference material")
        for title, url in SOURCES:
            st.markdown(f"- [{title}]({url})")
        st.info("The workflow is a plain-language learning model, not a replacement for the Constitution or Senate Rules.")
