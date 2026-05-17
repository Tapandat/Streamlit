import streamlit as st
import yaml, os
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

st.set_page_config(page_title="🌍 Climate Lens", layout="wide", page_icon="🌍")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at top, #1a3a4a 0%, #0d1b2a 50%, #091520 100%);
    min-height: 100vh;
}
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04) !important;
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stHeader"] { background: transparent !important; }

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }

/* Input fix - black text */
input[type="text"],
input[type="password"],
input[type="email"] {
    background: rgba(255,255,255,0.92) !important;
    border: 1.5px solid rgba(0,201,255,0.3) !important;
    border-radius: 10px !important;
    color: #111111 !important;
    font-size: 0.95rem !important;
}
input:focus {
    border-color: #00c9ff !important;
    box-shadow: 0 0 0 3px rgba(0,201,255,0.15) !important;
}
input::placeholder { color: rgba(0,0,0,0.3) !important; }

/* Labels */
label, .stTextInput label {
    color: rgba(255,255,255,0.75) !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px;
}

/* Button */
.stButton > button {
    background: linear-gradient(90deg, #00c9ff, #00e676) !important;
    color: #0a1628 !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 2rem !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.5px;
    transition: all 0.25s ease !important;
    width: 100%;
    margin-top: 0.5rem;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(0,201,255,0.35) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04);
    border-radius: 14px;
    padding: 5px;
    gap: 5px;
    border: 1px solid rgba(255,255,255,0.08);
}
.stTabs [data-baseweb="tab"] {
    border
