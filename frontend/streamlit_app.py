import streamlit as st
import requests
import json


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="ResearchIQ",
    layout="wide"
)


# -----------------------------
# Session state
# -----------------------------

if "current_research" not in st.session_state:
    st.session_state.current_research = None


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("🔎 ResearchIQ")

st.sidebar.subheader("Research History")

history_response = requests.get(
    f"{API_URL}/research"
)

if history_response.status_code == 200:

    history = history_response.json()

    if history:

        for item in history:

            title = item["query"]

            if len(title) > 40:
                title = title[:40] + "..."

            if st.sidebar.button(
                title,
                key=f"research_{item['research_id']}"
            ):

                response = requests.get(
                    f"{API_URL}/research/{item['research_id']}"
                )

                if response.status_code == 200:
                    st.session_state.current_research = response.json()

    else:
        st.sidebar.info("No research yet.")

else:
    st.sidebar.error("Could not load research history.")


# -----------------------------
# Main page
# -----------------------------

st.title("ResearchIQ")

st.caption(
    "AI-powered research assistant"
)


st.divider()


st.subheader("New Research")

query = st.text_area(
    "What would you like to research?",
    placeholder=(
        "Example: Compare Tesla and BYD "
        "in the electric vehicle market"
    ),
    height=120
)


if st.button(
    "Start Research",
    type="primary"
):

    if not query.strip():

        st.warning(
            "Please enter a research question."
        )

    else:

        with st.spinner(
            "ResearchIQ is researching..."
        ):

            response = requests.post(
                f"{API_URL}/research",
                json={"query": query}
            )

        if response.status_code == 200:

            st.session_state.current_research = (
                response.json()
            )

            st.success(
                "Research completed!"
            )

        else:

            st.error(
                f"Research failed: {response.text}"
            )


# -----------------------------
# Display research
# -----------------------------

if st.session_state.current_research:

    research = (
        st.session_state.current_research
    )

    


    tab1, tab2, tab3 = st.tabs([
        " Report",
        " Verification",
        " Sources"
    ])


    with tab1:
        st.markdown(research["report"])


    with tab2:

        verification = research.get("verification", [])

        if isinstance(verification, str):
            try:
                verification = json.loads(verification)
            except json.JSONDecodeError:
                st.error("Invalid verification data.")
                verification = []

        if verification:

            for i, item in enumerate(verification, start=1):

                status = item["status"]

                if status == "supported":
                    icon = "Supported"
                elif status == "partially_supported":
                    icon = "Partially Supported"
                else:
                    icon = "Unsupported"

                with st.expander(f"{icon} - Claim {i}"):

                    st.markdown(f"**Claim:** {item['claim']}")

                    st.markdown(
                        f"**Explanation:** {item['explanation']}"
                    )

                    for source in item.get("supporting_sources", []):

                        st.link_button(
                            source["title"],
                            source["url"]
                        )

        else:
            st.info("No verification available.")

    with tab3:

        sources = research.get("sources", [])

        if sources:

            for i, source in enumerate(sources, start=1):

                with st.expander(
                    f"{i}. {source['title']}"
                ):

                    st.link_button(
                        "Open Source",
                        source["url"]
                    )

        else:
            st.info("No sources available.")