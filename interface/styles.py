"""
GRAVISIM: Interface Styling and Design System
==============================================

Applies color palette, typography, and component styling conforming to
GravitationalLensingFUnction.md:
- Primary Dark Blue: #2E3A8C
- Light Blue:        #4A5FD9
- Navy:              #1A2254
- White:             #FFFFFF
- Light Gray:        #F5F7FA
- Dark Gray:         #4A4A4A
- Black:             #1A1A1A
"""

import streamlit as st


def apply_custom_styles():
    """Inject custom CSS for scientific styling."""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1350px;
    }

    /* Top Application Header */
    .gravisim-header {
        background: linear-gradient(135deg, #1A2254 0%, #2E3A8C 100%);
        border-radius: 12px;
        padding: 24px 32px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(26, 34, 84, 0.4);
        border: 1px solid rgba(74, 95, 217, 0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .gravisim-title {
        color: #FFFFFF;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .gravisim-subtitle {
        color: #CAD5FD;
        font-size: 14px;
        margin-top: 4px;
        font-weight: 400;
    }

    /* Metric Cards */
    .metric-card {
        background-color: #1A2254;
        border: 1px solid rgba(74, 95, 217, 0.35);
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .metric-card:hover {
        border-color: #4A5FD9;
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(74, 95, 217, 0.35);
    }

    /* Animated pulsing glow for live badges */
    @keyframes live-pulse {
        0%, 100% { box-shadow: 0 0 4px rgba(0, 255, 170, 0.4); }
        50% { box-shadow: 0 0 12px rgba(0, 255, 170, 0.8); }
    }

    .badge-live {
        background-color: rgba(0, 255, 170, 0.18);
        color: #00FFAA;
        border: 1px solid rgba(0, 255, 170, 0.5);
        animation: live-pulse 2s ease-in-out infinite;
    }

    /* Quick-launch preset buttons */
    div.stButton > button {
        min-height: 72px;
        font-size: 13px;
        line-height: 1.35;
        white-space: pre-wrap;
    }

    /* Tab panels */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: rgba(26, 34, 84, 0.6);
        border-radius: 8px 8px 0 0;
        padding: 8px 16px;
        color: #CAD5FD;
        border: 1px solid rgba(74, 95, 217, 0.2);
    }

    .stTabs [aria-selected="true"] {
        background-color: #2E3A8C !important;
        color: #FFFFFF !important;
        border-color: #4A5FD9 !important;
    }

    /* Expander headers */
    .streamlit-expanderHeader {
        background-color: rgba(26, 34, 84, 0.5);
        border-radius: 8px;
        border: 1px solid rgba(74, 95, 217, 0.25);
    }

    /* Selectbox dropdown */
    div[data-baseweb="select"] > div {
        background-color: #1A2254;
        border-color: rgba(74, 95, 217, 0.35);
    }

    .metric-title {
        font-size: 13px;
        font-weight: 600;
        color: #CAD5FD;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 24px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 4px;
    }

    .metric-caption {
        font-size: 12px;
        color: #A0AEC0;
        line-height: 1.4;
    }

    /* Scientific Card Container */
    .scientific-card {
        background-color: rgba(26, 34, 84, 0.65);
        border: 1px solid rgba(74, 95, 217, 0.25);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 18px;
    }

    /* Primary and Secondary Button Accents */
    div.stButton > button:first-child {
        background-color: #2E3A8C;
        color: #FFFFFF;
        font-weight: 600;
        border-radius: 8px;
        border: 1px solid #4A5FD9;
        padding: 8px 18px;
        transition: all 0.2s ease;
    }

    div.stButton > button:first-child:hover {
        background-color: #4A5FD9;
        border-color: #CAD5FD;
        box-shadow: 0 4px 12px rgba(74, 95, 217, 0.4);
    }

    /* Badge Pills */
    .badge-pill {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        background-color: #2E3A8C;
        color: #FFFFFF;
        border: 1px solid #4A5FD9;
    }

    .badge-gold {
        background-color: rgba(255, 215, 0, 0.15);
        color: #FFD700;
        border: 1px solid rgba(255, 215, 0, 0.4);
    }

    .badge-green {
        background-color: rgba(0, 255, 170, 0.15);
        color: #00FFAA;
        border: 1px solid rgba(0, 255, 170, 0.4);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_metric_card(title: str, value: str, caption: str, badge: str = None):
    badge_html = f'<span class="badge-pill" style="float: right;">{badge}</span>' if badge else ""
    card_html = f"""
    <div class="metric-card">
        <div>{badge_html}<span class="metric-title">{title}</span></div>
        <div class="metric-value">{value}</div>
        <div class="metric-caption">{caption}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

