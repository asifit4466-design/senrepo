import html
import textwrap

import streamlit as st
import streamlit.components.v1 as components

from workflows import WORKFLOWS, DOMAIN, SOURCES
from analytics import render_analytics


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Senate of Pakistan — Parliamentary Business Workflows",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# GLOBAL STYLING
# ============================================================

st.markdown(
    """
<style>

.block-container {
    padding-top: 1rem;
    max-width: 1550px;
}

/* ----------------------------------------------------------
   HERO
---------------------------------------------------------- */

.hero {
    padding: 1.45rem 1.7rem;
    border-radius: 18px;
    background: linear-gradient(135deg, #073b2a, #126448);
    color: #ffffff;
    margin-bottom: 1rem;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.08);
}

.hero h1 {
    margin: 0 0 0.3rem 0;
    font-size: 2rem;
}

.hero p {
    margin: 0.2rem 0;
    opacity: 0.95;
}


/* ----------------------------------------------------------
   GENERAL CARDS
---------------------------------------------------------- */

.card {
    padding: 1rem;
    border: 1px solid #cfd9d3;
    border-radius: 14px;
    background: #ffffff;
    min-height: 130px;
    color: #111827;
}

.card h4 {
    color: #111827;
    margin-bottom: 0.4rem;
}

.card p {
    color: #1f2937;
}


/* ----------------------------------------------------------
   STEP CARDS
---------------------------------------------------------- */

.step {
    padding: 0.9rem 1rem;
    border: 1px solid #d7dfda;
    border-radius: 12px;
    background: #ffffff;
    margin-bottom: 0.55rem;
    color: #111827;
}

.step b {
    color: #0b4e38;
}

.muted {
    color: #334155;
}


/* ----------------------------------------------------------
   NOTES
---------------------------------------------------------- */

.note {
    padding: 0.9rem 1rem;
    border-left: 4px solid #16805a;
    background: #eff8f3;
    border-radius: 8px;
    color: #10231a;
}


/* ----------------------------------------------------------
   LEGEND
---------------------------------------------------------- */

.legend span {
    display: inline-block;
    padding: 5px 9px;
    border-radius: 12px;
    margin: 3px;
    font-size: 0.82rem;
    border: 1px solid #d5ddd8;
    color: #17211c;
    background: #ffffff;
}


/* ----------------------------------------------------------
   NAVIGATION
---------------------------------------------------------- */

.navrow {
    display: flex;
    justify-content: space-between;
    gap: 0.75rem;
    margin-top: 0.5rem;
}

.navhint {
    font-size: 0.9rem;
    color: #475569;
    text-align: center;
    padding-top: 0.6rem;
}


/* ----------------------------------------------------------
   METRICS
---------------------------------------------------------- */

.metric-card {
    padding: 1rem;
    border: 1px solid #d7dfda;
    border-radius: 14px;
    background: #ffffff;
    min-height: 115px;
    color: #111827;
}

.metric-label {
    font-size: 0.86rem;
    font-weight: 700;
    color: #334155;
}

.metric-value {
    font-size: 2rem;
    line-height: 1.15;
    font-weight: 800;
    color: #0b4e38;
}

.metric-detail {
    font-size: 0.78rem;
    color: #64748b;
    margin-top: 0.25rem;
}

.section-kicker {
    font-size: 0.8rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    color: #64748b;
    text-transform: uppercase;
    margin-bottom: 0.25rem;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero">

    <h1>
        🏛️ Senate of Pakistan — Parliamentary Business
        Workflow Explorer
    </h1>

    <p>
        <b>Follow the work visually:</b>
        start at the left, follow the arrows →
        and see who acts, what happens next, and where
        the matter ends.
    </p>

    <p>
        Use the step navigator to move through a workflow
        without guessing the sequence.
    </p>

</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🔎 Choose Parliamentary Workflow")

    categories = []

    for key, value in WORKFLOWS.items():

        if value["category"] not in categories:
            categories.append(value["category"])

    cat = st.selectbox(
        "Filter by business area",
        ["ALL"] + categories,
    )

    available = [
        key
        for key, value in WORKFLOWS.items()
        if cat == "ALL" or value["category"] == cat
    ]

    selected = st.selectbox(
        "Select workflow",
        available,
    )

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

    st.caption(
        "Use the on-screen ← Previous and Next → controls "
        "to move through each workflow step. "
        "The diagram always reads left → right."
    )

    st.divider()

    st.caption(
        "Educational workflow model. "
        "Check the latest Constitution and Senate Rules "
        "for authoritative legal requirements."
    )


# ============================================================
# SELECTED WORKFLOW
# ============================================================

wf = WORKFLOWS[selected]

steps = wf["steps"]


# ============================================================
# WORKFLOW COLORS
# ============================================================

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


# ============================================================
# TEXT WRAPPING
# ============================================================

def wrap_text(text, width=42):

    text = " ".join(
        str(text).split()
    )

    if not text:
        return [""]

    return textwrap.wrap(
        text,
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    ) or [text]


# ============================================================
# LARGE NATIVE WORKFLOW DIAGRAM
# NO GRAPHVIZ REQUIRED
# ============================================================
def render_large_workflow_graph(steps, focus=None):
    """
    Interactive horizontal workflow carousel.

    Features:
    - Large readable cards
    - Automatic horizontal movement
    - Clickable NEXT control
    - Clickable PREVIOUS control
    - Pause / Resume
    - Current step highlighted
    - No Graphviz required
    """

    cards = []

    for i, (
        num,
        title,
        desc,
        kind,
    ) in enumerate(steps):

        background = COLORS.get(
            kind,
            "#f7f8f7",
        )

        is_current = (
            focus == i
        )

        border = (
            "#0b6b4b"
            if is_current
            else "#aebdb5"
        )

        shadow = (
            "0 0 0 4px rgba(11,107,75,.16), "
            "0 6px 18px rgba(0,0,0,.08)"
            if is_current
            else "0 3px 10px rgba(0,0,0,.06)"
        )

        current_badge = ""

        if is_current:
            current_badge = """
            <div class="wf-current">
                ● CURRENT STEP
            </div>
            """

        title_html = html.escape(
            str(title)
        )

        description_html = "<br>".join(
            html.escape(line)
            for line in wrap_text(
                desc,
                42,
            )
        )

        cards.append(
            f"""
            <div
                class="wf-slide"
                data-index="{i}"
            >

                <div
                    class="wf-card"
                    style="
                        background:{background};
                        border-color:{border};
                        box-shadow:{shadow};
                    "
                >

                    <div class="wf-number">
                        {html.escape(str(num))}
                    </div>

                    <div class="wf-title">
                        {title_html}
                    </div>

                    {current_badge}

                    <div class="wf-description">
                        {description_html}
                    </div>

                </div>

            </div>
            """
        )


    html_doc = f"""
    <style>

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            background: transparent;
            font-family:
                "Segoe UI",
                Arial,
                sans-serif;
        }}

        /* ================================================
           MAIN VIEWPORT
        ================================================= */

        .wf-viewport {{
            width: 100%;
            overflow: hidden;
            padding: 20px 10px 10px 10px;
        }}


        /* ================================================
           HORIZONTAL TRACK
        ================================================= */

        .wf-track {{
            display: flex;
            gap: 28px;

            overflow-x: auto;
            scroll-behavior: smooth;

            padding:
                8px
                8px
                24px
                8px;

            scrollbar-width: thin;

            scroll-snap-type: x mandatory;
        }}


        .wf-track::-webkit-scrollbar {{
            height: 10px;
        }}

        .wf-track::-webkit-scrollbar-thumb {{
            background: #9caea5;
            border-radius: 10px;
        }}


        /* ================================================
           SLIDE
        ================================================= */

        .wf-slide {{
            flex:
                0 0 430px;

            width: 430px;

            scroll-snap-align: center;
        }}


        /* ================================================
           CARD
        ================================================= */

        .wf-card {{

            width: 430px;

            min-height: 310px;

            border: 3px solid;

            border-radius: 20px;

            padding:
                28px
                30px;

            color: #111827;

            transition:
                transform .35s ease,
                box-shadow .35s ease,
                border-color .35s ease;
        }}


        .wf-card:hover {{
            transform: translateY(-3px);
        }}


        .wf-number {{

            font-size: 15px;

            font-weight: 800;

            color: #475569;

            margin-bottom: 11px;
        }}


        .wf-title {{

            font-size: 27px;

            line-height: 1.18;

            font-weight: 800;

            color: #111827;

            margin-bottom: 16px;
        }}


        .wf-description {{

            font-size: 18px;

            line-height: 1.65;

            color: #1f2937;
        }}


        .wf-current {{

            display: inline-block;

            margin-bottom: 14px;

            padding:
                6px 12px;

            border-radius:
                999px;

            background:
                #e7f6ef;

            color:
                #0b6b4b;

            font-size:
                12px;

            font-weight:
                800;

            letter-spacing:
                .05em;
        }}


        /* ================================================
           CONTROLS
        ================================================= */

        .wf-controls {{

            display: flex;

            align-items: center;

            justify-content: center;

            gap: 12px;

            flex-wrap: wrap;

            padding:
                8px 10px 4px 10px;
        }}


        .wf-btn {{

            border: 2px solid #305c4b;

            background: #ffffff;

            color: #111827;

            border-radius: 10px;

            padding:
                10px 18px;

            font-size:
                15px;

            font-weight:
                800;

            cursor:
                pointer;

            min-width:
                125px;
        }}


        .wf-btn:hover {{

            background:
                #eaf5ef;
        }}


        .wf-next-btn {{

            background:
                #0b6b4b;

            color:
                #ffffff;
        }}


        .wf-next-btn:hover {{

            background:
                #084f39;
        }}


        .wf-counter {{

            color:
                #334155;

            font-size:
                14px;

            font-weight:
                700;

            padding:
                0 8px;
        }}


        /* ================================================
           AUTO PLAY INDICATOR
        ================================================= */

        .wf-status {{

            text-align:
                center;

            color:
                #64748b;

            font-size:
                13px;

            margin-top:
                7px;
        }}


        /* ================================================
           MOBILE
        ================================================= */

        @media (max-width: 600px) {{

            .wf-slide,
            .wf-card {{
                width: 340px;
                flex-basis: 340px;
            }}

            .wf-card {{
                min-height: 300px;
                padding: 22px;
            }}

            .wf-title {{
                font-size: 23px;
            }}

            .wf-description {{
                font-size: 16px;
            }}
        }}

    </style>


    <div class="wf-viewport">

        <div
            id="workflow-track"
            class="wf-track"
        >

            {''.join(cards)}

        </div>


        <div class="wf-controls">

            <button
                type="button"
                id="wf-prev"
                class="wf-btn"
            >
                ← Previous
            </button>


            <div
                id="wf-counter"
                class="wf-counter"
            >
                Step {focus + 1 if focus is not None else 1}
                of {len(steps)}
            </div>


            <button
                type="button"
                id="wf-next"
                class="wf-btn wf-next-btn"
            >
                NEXT →
            </button>


            <button
                type="button"
                id="wf-pause"
                class="wf-btn"
            >
                ⏸ Pause
            </button>

        </div>


        <div
            id="wf-status"
            class="wf-status"
        >
            Automatically moving through the workflow
        </div>

    </div>


    <script>

        (function() {{

            const track =
                document.getElementById(
                    "workflow-track"
                );

            const slides =
                Array.from(
                    track.querySelectorAll(
                        ".wf-slide"
                    )
                );

            const previous =
                document.getElementById(
                    "wf-prev"
                );

            const next =
                document.getElementById(
                    "wf-next"
                );

            const pause =
                document.getElementById(
                    "wf-pause"
                );

            const counter =
                document.getElementById(
                    "wf-counter"
                );

            const status =
                document.getElementById(
                    "wf-status"
                );


            let current =
                {focus if focus is not None else 0};


            let running = true;

            let timer = null;


            function updateCounter() {{

                counter.textContent =
                    "Step "
                    + (current + 1)
                    + " of "
                    + slides.length;
            }}


            function moveTo(index) {{

                if (!slides.length) {{
                    return;
                }}


                current =
                    Math.max(
                        0,
                        Math.min(
                            index,
                            slides.length - 1
                        )
                    );


                slides[current].scrollIntoView({{
                    behavior: "smooth",
                    inline: "center",
                    block: "nearest"
                }});


                updateCounter();
            }}


            function nextStep() {{

                if (current >= slides.length - 1) {{

                    current = 0;

                }} else {{

                    current += 1;
                }}


                moveTo(current);
            }}


            function previousStep() {{

                if (current <= 0) {{

                    current =
                        slides.length - 1;

                }} else {{

                    current -= 1;
                }}


                moveTo(current);
            }}


            function startAutoPlay() {{

                clearInterval(timer);

                timer =
                    setInterval(
                        function() {{

                            if (running) {{
                                nextStep();
                            }}

                        }},
                        4500
                    );

                running = true;

                pause.textContent =
                    "⏸ Pause";

                status.textContent =
                    "Automatically moving through the workflow";
            }}


            function stopAutoPlay() {{

                running = false;

                clearInterval(timer);

                pause.textContent =
                    "▶ Resume";

                status.textContent =
                    "Auto movement paused";
            }}


            next.addEventListener(
                "click",
                function() {{

                    nextStep();

                    startAutoPlay();

                }}
            );


            previous.addEventListener(
                "click",
                function() {{

                    previousStep();

                    startAutoPlay();

                }}
            );


            pause.addEventListener(
                "click",
                function() {{

                    if (running) {{

                        stopAutoPlay();

                    }} else {{

                        startAutoPlay();

                    }}

                }}
            );


            /*
             * Clicking directly on a workflow card
             * makes it the current visible stage.
             */

            slides.forEach(
                function(slide, index) {{

                    slide.addEventListener(
                        "click",
                        function() {{

                            moveTo(index);

                        }}
                    );

                }}
            );


            /*
             * Start from the selected Streamlit step.
             */

            setTimeout(
                function() {{

                    moveTo(current);

                    startAutoPlay();

                }},
                250
            );


            /*
             * Stop automatic movement when the
             * browser prefers reduced motion.
             */

            if (
                window.matchMedia(
                    "(prefers-reduced-motion: reduce)"
                ).matches
            ) {{

                stopAutoPlay();
            }}

        }})();

    </script>
    """


    components.html(
        html_doc,
        height=500,
        scrolling=False,
    )

# ============================================================
# MASTER WORKFLOW DETECTION
# ============================================================

is_master = selected.startswith(
    "00 — MASTER"
)


# ============================================================
# TABS
# ============================================================

if is_master:

    t1, t2, t3, t4, t5 = st.tabs(
        [
            "🗺️ Workflow Map",
            "📊 Analytics",
            "🧩 Business Domain",
            "👥 Who Does What",
            "📚 Sources",
        ]
    )

else:

    t1, t2, t3 = st.tabs(
        [
            "🔄 Workflow",
            "🧠 Understand It",
            "📚 Sources",
        ]
    )


# ============================================================
# MAIN WORKFLOW TAB
# ============================================================

with t1:

    st.markdown(
        f"""
        <div class="section-kicker">
            {html.escape(str(wf["category"]))}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader(
        selected
    )

    st.write(
        wf["summary"]
    )


    # --------------------------------------------------------
    # SESSION STATE
    # --------------------------------------------------------

    if (
        "workflow_step"
        not in st.session_state
        or st.session_state.get(
            "workflow_selected"
        )
        != selected
    ):

        st.session_state.workflow_selected = selected

        st.session_state.workflow_step = 0


    idx = int(
        st.session_state.workflow_step
    )

    idx = max(
        0,
        min(
            idx,
            len(steps) - 1,
        ),
    )

    st.session_state.workflow_step = idx


    # --------------------------------------------------------
    # LARGE WORKFLOW
    # --------------------------------------------------------

    render_large_workflow_graph(
        steps,
        focus=idx,
    )


    # --------------------------------------------------------
    # PREVIOUS / CURRENT / NEXT
    # --------------------------------------------------------

    cols = st.columns(
        [1, 3, 1]
    )


    with cols[0]:

        if st.button(
            "← Previous",
            disabled=(idx == 0),
            use_container_width=True,
        ):

            st.session_state.workflow_step = max(
                0,
                idx - 1,
            )

            st.rerun()

with cols[1]:

    st.markdown(
        f"""
**Step {idx + 1} of {len(steps)}**  
{steps[idx][1]}  
**Follow →**
"""
    )


    with cols[2]:

        if st.button(
            "Next →",
            disabled=(
                idx
                == len(steps) - 1
            ),
            use_container_width=True,
        ):

            st.session_state.workflow_step = min(
                len(steps) - 1,
                idx + 1,
            )

            st.rerun()


    # --------------------------------------------------------
    # JUMP TO STEP
    # --------------------------------------------------------

    labels = [
        f"{i + 1}. {title}"
        for i, (
            _,
            title,
            _,
            _,
        ) in enumerate(steps)
    ]


    picked = st.selectbox(
        "Jump to a workflow step",

        range(len(labels)),

        index=idx,

        format_func=lambda i: labels[i],

        key=f"jump_{selected}",
    )


    if picked != idx:

        st.session_state.workflow_step = int(
            picked
        )

        st.rerun()


    # --------------------------------------------------------
    # CURRENT STEP DETAIL
    # --------------------------------------------------------

    num, title, desc, kind = steps[idx]


    st.markdown(
        f"### Step {num}: {title}"
    )

    st.write(
        desc
    )


    next_title = (
        steps[idx + 1][1]
        if idx < len(steps) - 1
        else "Final outcome"
    )


    st.caption(
        f"Process type: {kind}  •  "
        f"Next → {next_title}"
    )


    # --------------------------------------------------------
    # CONTINUOUS TEXT SEQUENCE
    # --------------------------------------------------------

    with st.expander(
        "Show all steps as a continuous arrow sequence"
    ):

        arrow_parts = []

        for i, (
            _,
            step_title,
            _,
            _,
        ) in enumerate(steps):

            arrow_parts.append(
                f"<b>{i + 1}. "
                f"{html.escape(str(step_title))}</b>"
            )


        st.markdown(
            """
            <span
                style="
                    color:#0b4e38;
                    font-weight:700;
                "
            >
                →
            </span>
            """.join(
                arrow_parts
            ),
            unsafe_allow_html=True,
        )


# ============================================================
# SECOND TAB
# ============================================================

with t2:

    if is_master:

        render_analytics()

    else:

        st.subheader(
            "🧠 Understand the workflow like a process"
        )

        st.write(
            "Read the selected workflow as a chain "
            "of responsibility. The arrows show "
            "the intended sequence."
        )


        for i, (
            n,
            t,
            d,
            k,
        ) in enumerate(steps):

            arrow = (
                "→"
                if i < len(steps) - 1
                else "✓"
            )


            st.markdown(
                f"""
                <div class="step">

                    <b>
                        {i + 1}. {html.escape(str(t))}
                    </b>

                    <span
                        style="
                            color:#0b4e38;
                            font-weight:800;
                        "
                    >
                        {arrow}
                    </span>

                    <br>

                    <span class="muted">
                        {html.escape(str(d))}
                    </span>

                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# MASTER ONLY — BUSINESS DOMAIN
# ============================================================

if is_master:

    with t3:

        st.subheader(
            "🧩 All Senate Parliamentary Business Areas"
        )

        st.write(
            "Each card is a major business domain. "
            "Select a workflow from the sidebar to "
            "see its complete arrow-by-arrow process."
        )


        cols = st.columns(2)


        for i, (
            domain,
            items,
        ) in enumerate(
            DOMAIN.items()
        ):

            with cols[i % 2]:

                st.markdown(
                    f"""
                    <div class="card">

                        <h4>
                            {html.escape(str(domain))}
                        </h4>

                        <p>
                            {
                                html.escape(
                                    " • ".join(items)
                                )
                            }
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.write("")


    # ========================================================
    # MASTER ONLY — WHO DOES WHAT
    # ========================================================

    with t4:

        roles = {

            "Senators":
                "Propose, debate, question, amend, "
                "vote and participate in committees.",

            "Chairman / Deputy Chairman":
                "Preside over proceedings and apply "
                "the constitutional/rules framework.",

            "Senate Secretariat":
                "Supports scheduling, notices, legislation, "
                "questions, records, committees and other "
                "House functions.",

            "Committees":
                "Conduct detailed scrutiny, oversight and "
                "reporting within their mandates.",

            "Government / Ministers":
                "Introduce Government business and answer "
                "parliamentary scrutiny where applicable.",

            "National Assembly":
                "Participates in two-House legislation and "
                "financial/constitutional processes as "
                "provided by law.",

            "President":
                "Performs constitutional functions in relation "
                "to Bills and other specified matters.",
        }


        for role, desc in roles.items():

            st.markdown(
                f"""
                <div class="card">

                    <h4>
                        {html.escape(str(role))}
                    </h4>

                    <p>
                        {html.escape(str(desc))}
                    </p>

                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write("")


    # ========================================================
    # MASTER ONLY — SOURCES
    # ========================================================

    with t5:

        st.subheader(
            "📚 Official reference material"
        )


        for title, url in SOURCES:

            st.markdown(
                f"- [{html.escape(str(title))}]({url})"
            )


        st.info(
            "This application is an educational "
            "visualisation. The Constitution and "
            "the current Senate Rules remain the "
            "authoritative sources."
        )


# ============================================================
# NON-MASTER — SOURCES
# ============================================================

else:

    with t3:

        st.subheader(
            "📚 Official reference material"
        )


        for title, url in SOURCES:

            st.markdown(
                f"- [{html.escape(str(title))}]({url})"
            )


        st.info(
            "The workflow is a plain-language "
            "learning model, not a replacement for "
            "the Constitution or Senate Rules."
        )