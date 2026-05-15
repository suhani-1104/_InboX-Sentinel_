import streamlit as st

def apply_theme():
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

    if st.session_state.theme == 'light':
        bg_color = "#FAFAFA"
        primary_color = "#A7C7E7"
        secondary_bg = "#E6E6FA"
        accent_color = "#B8E0D2"
        text_color = "#2E2E2E"
    else:
        bg_color = "#0F172A"
        primary_color = "#6366F1"
        secondary_bg = "#1E293B"
        accent_color = "#8B5CF6"
        text_color = "#E2E8F0"

    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {bg_color};
            color: {text_color};
        }}
        .stButton>button {{
            background-color: {primary_color};
            color: {'#FFFFFF' if st.session_state.theme == 'dark' else '#000000'};
            border-radius: 8px;
            border: none;
        }}
        .stButton>button:hover {{
            background-color: {accent_color};
        }}
        div[data-testid="stSidebar"] {{
            background-color: {secondary_bg};
        }}
        .card {{
            background-color: {secondary_bg};
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .metric-card {{
            background-color: {primary_color};
            color: {'#FFFFFF' if st.session_state.theme == 'dark' else '#000000'};
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .metric-card h2 {{
            margin: 0;
            font-size: 2.5rem;
            color: {'#FFFFFF' if st.session_state.theme == 'dark' else '#000000'} !important;
        }}
        .metric-card p {{
            margin: 0;
            font-size: 1.2rem;
            color: {'#E2E8F0' if st.session_state.theme == 'dark' else '#2E2E2E'} !important;
        }}
        h1, h2, h3, h4, h5, p, span, div {{
            color: {text_color};
        }}
        </style>
    """, unsafe_allow_html=True)
