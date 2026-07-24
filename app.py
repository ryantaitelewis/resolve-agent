import streamlit as st

from agent import run_prospect_agent


@st.cache_data(
    ttl=60 * 60 * 24,
    show_spinner=False,
)
def cached_run_prospect_agent(
    name: str,
    company: str,
    role: str,
    x_url: str,
    youtube_url: str,
):
    return run_prospect_agent(
        name=name,
        company=company,
        role=role,
        x_url=x_url,
        youtube_url=youtube_url,
    )


st.set_page_config(
    page_title="SideQuest",
    page_icon=":material/explore:",
    layout="centered",
)

st.markdown(
    """
    <style>
    /* Soft ambient depth behind the main canvas */
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(1200px 500px at 10% -10%, rgba(56, 189, 248, 0.14), transparent 55%),
            radial-gradient(900px 420px at 90% 0%, rgba(52, 211, 153, 0.08), transparent 50%),
            #0B1220;
    }

    /* Hero brand treatment */
    .sq-hero {
        margin: 0.35rem 0 1.75rem 0;
        padding: 1.6rem 1.55rem 1.45rem 1.55rem;
        border-radius: 18px;
        border: 1px solid rgba(56, 189, 248, 0.22);
        background:
            linear-gradient(135deg, rgba(21, 29, 46, 0.95) 0%, rgba(15, 23, 42, 0.88) 100%);
        box-shadow: 0 18px 40px rgba(0, 0, 0, 0.28);
    }
    .sq-kicker {
        display: inline-block;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #7DD3FC;
        margin-bottom: 0.55rem;
    }
    .sq-brand {
        font-size: 2.55rem;
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #F8FAFC;
        margin: 0 0 0.55rem 0;
    }
    .sq-subtitle {
        margin: 0;
        max-width: 38rem;
        color: #A7B4C8;
        font-size: 1.05rem;
        line-height: 1.55;
    }

    /* Highlighted recommendation card accent */
    .sq-reco-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #34D399;
        margin-bottom: 0.35rem;
    }

    /* Slightly quieter tertiary / secondary chrome */
    div[data-testid="stButton"] button[kind="secondary"],
    div[data-testid="stButton"] button[kind="tertiary"] {
        border-color: rgba(148, 163, 184, 0.28) !important;
        color: #94A3B8 !important;
    }

    /* Form card breathing room */
    div[data-testid="stForm"] {
        padding: 0.35rem 0.15rem 0.15rem 0.15rem;
    }

    /* Progress bars feel more “product” than chart */
    div[data-testid="stProgress"] > div > div {
        border-radius: 999px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="sq-hero">
      <div class="sq-kicker">Resolve · Sales intelligence</div>
      <h1 class="sq-brand">SideQuest</h1>
      <p class="sq-subtitle">
        Research public prospect signals and turn them into creative,
        relevant outreach — grounded in X, YouTube, and company context.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.markdown("##### :material/person_search: Prospect details")
    st.caption(
        "Add a name and company to start. Social links sharpen the research."
    )

    with st.form("prospect_form"):
        name = st.text_input(
            "Prospect name",
            placeholder="e.g. Jordan Lee",
        )
        company = st.text_input(
            "Company",
            placeholder="e.g. Acme Robotics",
        )
        role = st.text_input(
            "Role",
            placeholder="e.g. VP of Engineering",
        )

        url_col1, url_col2 = st.columns(2)
        with url_col1:
            x_url = st.text_input(
                "X profile URL",
                placeholder="https://x.com/…",
            )
        with url_col2:
            youtube_url = st.text_input(
                "YouTube interview URL",
                placeholder="https://youtube.com/…",
            )

        submitted = st.form_submit_button(
            "Research prospect",
            type="primary",
            icon=":material/travel_explore:",
            width="stretch",
        )

st.space("small")

with st.container(horizontal=True, horizontal_alignment="right"):
    if st.button(
        "Refresh saved results",
        type="tertiary",
        icon=":material/refresh:",
    ):
        st.cache_data.clear()
        st.success("Cache cleared.")

if submitted:
    if not name or not company:
        st.error(
            "Please enter a prospect name and company.",
            icon=":material/error:",
        )
    else:
        try:
            with st.spinner(
                "Researching X, YouTube, and company signals..."
            ):
                research, recommendation = cached_run_prospect_agent(
                    name=name.strip(),
                    company=company.strip(),
                    role=role.strip(),
                    x_url=x_url.strip(),
                    youtube_url=youtube_url.strip(),
                )

            st.success(
                f"Research and outreach recommendations complete "
                f"for {name} at {company}.",
                icon=":material/check_circle:",
            )

            st.space("small")

            st.subheader("Prospect summary")
            with st.container(border=True):
                st.write(research.prospect_summary)

            st.space("small")

            st.subheader("Recommended approach")
            with st.container(border=True):
                st.markdown(
                    '<div class="sq-reco-label">Best fit</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"### {recommendation.recommended_option_name}"
                )
                st.write(recommendation.recommendation_reason)
                st.badge(
                    "Recommended",
                    icon=":material/star:",
                    color="green",
                )

            st.space("small")

            st.subheader("Outreach options")
            st.caption(
                "Expand an option to review messaging, scores, and risks."
            )

            for option in recommendation.options:
                is_recommended = (
                    option.name
                    == recommendation.recommended_option_name
                )

                label = option.name
                if is_recommended:
                    label += " — Recommended"

                with st.expander(
                    label,
                    expanded=is_recommended,
                    icon=(
                        ":material/star:"
                        if is_recommended
                        else ":material/campaign:"
                    ),
                ):
                    with st.container(border=True):
                        st.markdown(
                            f"**Approach:** {option.approach}"
                        )

                        st.markdown(
                            f"**Opening hook:** "
                            f"{option.opening_hook}"
                        )

                        st.markdown(
                            f"**Resolve relevance:** "
                            f"{option.resolve_relevance}"
                        )

                        st.markdown("**LinkedIn message**")
                        st.code(
                            option.linkedin_message,
                            language=None,
                            wrap_lines=True,
                        )

                        if option.gift_or_activation:
                            st.markdown(
                                f"**Creative activation:** "
                                f"{option.gift_or_activation}"
                            )

                        st.markdown(
                            f"**Why it might work:** "
                            f"{option.why_it_might_work}"
                        )

                        score_col1, score_col2 = st.columns(2)

                        with score_col1:
                            st.metric(
                                "Relevance",
                                f"{option.relevance_score:.0%}",
                            )
                            st.progress(
                                option.relevance_score,
                                text="Relevance signal",
                            )
                            st.caption(
                                f"Relevance reason: "
                                f"{option.relevance_reason}"
                            )

                        with score_col2:
                            st.metric(
                                "Creepiness",
                                f"{option.creepiness_score:.0%}",
                            )
                            st.progress(
                                option.creepiness_score,
                                text="Creepiness signal",
                            )
                            st.caption(
                                f"Creepiness reason: "
                                f"{option.creepiness_reason}"
                            )

                        if option.risks:
                            st.markdown("**Risks**")
                            for risk in option.risks:
                                st.write(f"• {risk}")

            st.space("small")

            st.subheader("Source evidence")
            st.caption(
                "Signals gathered from public X, YouTube, and company sources."
            )

            with st.expander(
                "Research evidence",
                icon=":material/library_books:",
            ):
                sections = [
                    (
                        "Professional signals",
                        research.professional_signals,
                    ),
                    (
                        "Personal signals",
                        research.personal_signals,
                    ),
                    (
                        "Company signals",
                        research.company_signals,
                    ),
                ]

                for heading, signals in sections:
                    st.markdown(f"### {heading}")

                    if not signals:
                        st.caption("No strong signals found.")
                        continue

                    for signal in signals:
                        with st.container(border=True):
                            st.markdown(
                                f"**{signal.finding}**"
                            )

                            st.write(signal.evidence)

                            conf_col, creep_col = st.columns(2)
                            with conf_col:
                                st.progress(
                                    signal.confidence,
                                    text=(
                                        f"Confidence · "
                                        f"{signal.confidence:.0%}"
                                    ),
                                )
                            with creep_col:
                                st.progress(
                                    signal.creepiness_score,
                                    text=(
                                        f"Creepiness · "
                                        f"{signal.creepiness_score:.0%}"
                                    ),
                                )

                            st.markdown(
                                f"[Open source]"
                                f"({signal.source_url})"
                            )

            if research.caveats:
                with st.expander(
                    "Research caveats",
                    icon=":material/warning:",
                ):
                    for caveat in research.caveats:
                        st.warning(caveat)

        except Exception as error:
            st.error(
                f"Something went wrong: {error}",
                icon=":material/error:",
            )
