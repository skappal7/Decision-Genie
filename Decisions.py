import streamlit as st
import requests

# 1) Set page config
st.set_page_config(
    page_title="Decision Genie",
    page_icon="🔮",
    layout="centered"
)

# 2) CSS for modern style and iconography
st.markdown("""
    <style>
    .title {
        font-size: 3rem;
        color: #6C63FF;
        text-align: center;
        font-weight: 900;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px #555;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #888;
        margin-bottom: 2rem;
    }
    .boxed {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1rem;
        background-color: #f9f9f9;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# 3) Title / header section
st.markdown('<h1 class="title">🔮 Decision Genie</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Let the magic of AI guide your decisions</p>', unsafe_allow_html=True)

with st.expander("How this works"):
    st.write("""
    1. Enter your decision or question.
    2. Select an analysis type and style.
    3. Click **Generate AI Analysis**.
    4. The Genie will fetch a rationale from the Rationale AI API and display the output below.
    """)

# 4) User input form
with st.form("decision_form"):
    decision_text = st.text_area(
        "What is your decision/question?",
        placeholder="e.g., Should we launch product A or product B this quarter?"
    )
    analysis_type = st.selectbox(
        "Pick an analysis type",
        ["proscons", "risks", "decisiontree", "perspectives"],
        index=0
    )
    analysis_style = st.selectbox(
        "Pick a style",
        ["concise", "detailed", "bulletpoints"],
        index=0
    )

    submitted = st.form_submit_button("Generate AI Analysis 🔮")

# 5) If user submits, call Rationale AI
if submitted:
    if not decision_text.strip():
        st.warning("Please enter some text to analyze.")
    else:
        # Build request payload
        payload = {
            "data": [{
                "decision": decision_text,
                "analysis": analysis_type,
                "style": analysis_style
            }]
        }
        
        # Rationale API endpoint & key
        url = "https://api.rationale.jina.ai/v1/decision"
        headers = {
            # For demonstration only—never hardcode keys in production
            "x-api-key": "token QKUYF6kacgeLVjH0dZXS:ef0936bae1d47573b7744df61bc709f46eb85820e230fd24609119c1a7d7e7df",
            "content-type": "application/json"
        }

        with st.spinner("The Genie is thinking..."):
            try:
                response = requests.post(url, json=payload, headers=headers, timeout=30)
                response.raise_for_status()  # raise an error for bad status
                data = response.json()

                # Display the raw or processed output.
                # The actual structure of `data` depends on Rationale's response format.
                st.markdown("## 🪄 AI Analysis Result")
                st.write("Below is the raw response from Rationale AI (for PoC):")
                st.json(data)

            except requests.exceptions.RequestException as e:
                st.error(f"Error calling Rationale API: {e}")

# 6) Footer or additional style
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #aaa;">
  <small>
    Built with ❤️ by Decision Genie.  
    <br>Remember: Always treat AI advice as one data point in your overall decision-making.
  </small>
</div>
""", unsafe_allow_html=True)
