import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from theme_utils import apply_theme

# Must be the first Streamlit command
st.set_page_config(
    page_title="InboxSentinel",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_theme()

# Toggle Theme Button at the very top right using columns
colA, colB = st.columns([8, 2])
with colA:
    st.title("InboxSentinel")
with colB:
    st.write("")
    if st.button("🌓 Toggle Theme"):
        if st.session_state.theme == 'light':
            st.session_state.theme = 'dark'
        else:
            st.session_state.theme = 'light'
        st.rerun()

# --- TOP NAVIGATION TABS ---
tab_home, tab_dashboard, tab_about = st.tabs(["🏠 Home", "📊 Dashboard", "ℹ️ About"])

# --- TAB 1: HOME ---
with tab_home:
    st.markdown("""
    <div class="card">
        <h3>Welcome, User 👋</h3>
        <p>This system uses a custom Agentic AI pipeline powered by <b>DistilBERT</b> to intelligently scan, classify, and act upon incoming emails in real-time.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <h4>System Status</h4>
            <p>✅ Connected to Mock Email Server</p>
            <p>🤖 Agent Engine: Online</p>
            <p>🧠 Model: mrm8488/bert-tiny-finetuned</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h4>Quick Actions</h4>
            <p>Trigger the agent to scan new incoming emails and classify them.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Scan Emails Now", use_container_width=True):
            with st.spinner("Agent is fetching and scanning emails..."):
                try:
                    response = requests.post("http://localhost:5000/api/scan")
                    if response.status_code == 200:
                        data = response.json()
                        st.success(data["message"])
                        st.balloons()
                    else:
                        st.error("Failed to connect to the backend agent.")
                except Exception as e:
                    st.error(f"Error: Make sure the Flask backend is running on port 5000. Details: {e}")

# --- TAB 2: DASHBOARD ---
with tab_dashboard:
    @st.cache_data(ttl=5)
    def fetch_stats():
        try:
            res = requests.get("http://localhost:5000/api/stats")
            if res.status_code == 200:
                return res.json()
        except:
            pass
        return {"total": 0, "spam": 0, "ham": 0, "spam_rate": 0.0}

    @st.cache_data(ttl=5)
    def fetch_emails():
        try:
            res = requests.get("http://localhost:5000/api/emails")
            if res.status_code == 200:
                return res.json()
        except:
            pass
        return []

    stats = fetch_stats()
    emails = fetch_emails()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><h2>{stats["total"]}</h2><p>Total Emails</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h2>{stats["spam"]}</h2><p>Spam Detected</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h2>{stats["ham"]}</h2><p>Ham Emails</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><h2>{stats["spam_rate"]}%</h2><p>Spam Rate</p></div>', unsafe_allow_html=True)

    if emails:
        st.markdown("### Agent Activity Visualizations")
        df = pd.DataFrame(emails)
        
        c1, c2 = st.columns(2)
        with c1:
            class_counts = df['classification'].value_counts().reset_index()
            class_counts.columns = ['classification', 'count']
            pie_colors = ['#EF4444', '#10B981'] if st.session_state.theme == 'dark' else ['#F87171', '#34D399']
            fig1 = px.pie(class_counts, values='count', names='classification', 
                         title="Spam vs Ham Distribution", hole=0.4,
                         color='classification',
                         color_discrete_map={'Spam': pie_colors[0], 'Ham': pie_colors[1]})
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                             font=dict(color='#E2E8F0' if st.session_state.theme == 'dark' else '#2E2E2E'))
            st.plotly_chart(fig1, use_container_width=True)
            
        with c2:
            fig2 = px.histogram(df, x="spam_probability", color="classification",
                                title="Agent Confidence Distribution", nbins=20, barmode="overlay",
                                color_discrete_map={'Spam': pie_colors[0], 'Ham': pie_colors[1]})
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                             font=dict(color='#E2E8F0' if st.session_state.theme == 'dark' else '#2E2E2E'))
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("### Processed Emails Log")
        display_df = df[['timestamp', 'subject', 'classification', 'spam_probability', 'action', 'explanation']]
        display_df['spam_probability'] = display_df['spam_probability'].apply(lambda x: f"{x:.1%}")
        st.dataframe(display_df, use_container_width=True, hide_index=True)
    else:
        st.info("No emails processed yet. Go to Home tab and click 'Scan Emails Now'.")

# --- TAB 3: ABOUT ---
with tab_about:
    st.markdown("""
    <div class="card">
        <h3>Project Overview</h3>
        <p>The <b>Spam-V-Ham Filtering System</b> is a full-stack AI application designed to autonomously scan, classify, and filter incoming emails.</p>
        <p>Unlike traditional spam filters, this system uses an Agentic architecture. The Agent not only predicts the probability of spam using advanced Transformer-based NLP, but also reasons about its prediction and executes intelligent actions.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h3>🧠 How the Agent Works</h3>
        <ol>
            <li><b>Ingestion:</b> Fetches new emails from the inbox.</li>
            <li><b>Classification:</b> Uses the pre-trained <code>mrm8488/bert-tiny-finetuned-sms-spam-detection</code> model from Hugging Face.</li>
            <li><b>Decision Engine:</b> Evaluates the probability against rule-based thresholds (e.g., >80% = Block, >50% = Flag).</li>
            <li><b>Explanation:</b> Analyzes the text to provide a human-readable reason for the classification.</li>
            <li><b>Execution:</b> Automatically applies the appropriate action to the email.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
