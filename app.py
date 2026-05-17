import streamlit as st
import yaml, os
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

st.set_page_config(page_title="Climate Lens", layout="wide", page_icon="🌍")

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
#MainMenu, footer, header { visibility: hidden; }
input[type="text"], input[type="password"], input[type="email"] {
    background: rgba(255,255,255,0.92) !important;
    border: 1.5px solid rgba(0,201,255,0.3) !important;
    border-radius: 10px !important;
    color: #111111 !important;
    font-size: 0.95rem !important;
}
input::placeholder { color: rgba(0,0,0,0.3) !important; }
label, .stTextInput label {
    color: rgba(255,255,255,0.75) !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
}
.stButton > button {
    background: linear-gradient(90deg, #00c9ff, #00e676) !important;
    color: #0a1628 !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 2rem !important;
    font-size: 0.95rem !important;
    transition: all 0.25s ease !important;
    width: 100%;
    margin-top: 0.5rem;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(0,201,255,0.35) !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04);
    border-radius: 14px;
    padding: 5px;
    gap: 5px;
    border: 1px solid rgba(255,255,255,0.08);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    color: rgba(255,255,255,0.5) !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.5rem 1.8rem !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #00c9ff, #00e676) !important;
    color: #0a1628 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; padding: 2.5rem 1rem 1rem 1rem;'>
    <div style='display:inline-block; margin-bottom: 1.2rem;'>
        <svg width="110" height="110" viewBox="0 0 110 110" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <radialGradient id="earthGrad" cx="40%" cy="35%" r="60%">
                    <stop offset="0%" stop-color="#4fc3f7"/>
                    <stop offset="40%" stop-color="#1565c0"/>
                    <stop offset="100%" stop-color="#0a237a"/>
                </radialGradient>
                <clipPath id="circleClip">
                    <circle cx="55" cy="55" r="42"/>
                </clipPath>
            </defs>
            <circle cx="55" cy="55" r="50" fill="none" stroke="#00c9ff" stroke-width="1.5" opacity="0.4"/>
            <circle cx="55" cy="55" r="42" fill="url(#earthGrad)"/>
            <g clip-path="url(#circleClip)" fill="#2e7d32" opacity="0.85">
                <ellipse cx="32" cy="40" rx="12" ry="9" transform="rotate(-15 32 40)"/>
                <ellipse cx="28" cy="52" rx="7" ry="10" transform="rotate(-10 28 52)"/>
                <ellipse cx="58" cy="38" rx="7" ry="8" transform="rotate(10 58 38)"/>
                <ellipse cx="60" cy="56" rx="6" ry="13" transform="rotate(5 60 56)"/>
                <ellipse cx="76" cy="36" rx="14" ry="9" transform="rotate(-5 76 36)"/>
                <ellipse cx="80" cy="50" rx="9" ry="7" transform="rotate(10 80 50)"/>
                <ellipse cx="80" cy="70" rx="7" ry="5" transform="rotate(-10 80 70)"/>
                <ellipse cx="38" cy="68" rx="6" ry="10" transform="rotate(5 38 68)"/>
            </g>
            <g clip-path="url(#circleClip)">
                <ellipse cx="55" cy="18" rx="18" ry="7" fill="white" opacity="0.6"/>
                <ellipse cx="55" cy="92" rx="14" ry="5" fill="white" opacity="0.5"/>
            </g>
            <ellipse cx="42" cy="38" rx="14" ry="10" fill="white" opacity="0.08" transform="rotate(-20 42 38)"/>
        </svg>
    </div>
    <h1 style='font-size:3.2rem; font-weight:800; margin:0; background: linear-gradient(90deg, #00c9ff, #00e676); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Climate Lens</h1>
    <p style='color:rgba(255,255,255,0.55); font-size:0.95rem; margin: 0.5rem 0 0 0; letter-spacing: 1px; text-transform: uppercase; font-weight:600;'>Northern Hemisphere · Temperature Analysis · 1880 to Present</p>
</div>
<div style='height:1px; background:linear-gradient(90deg,transparent,rgba(0,201,255,0.4),transparent); margin: 1.5rem auto; max-width:500px;'></div>
""", unsafe_allow_html=True)

CONFIG_PATH = "config.yaml"

if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "w") as f:
        yaml.dump({
            "credentials": {"usernames": {}},
            "cookie": {"expiry_days": 30, "key": "climate_secret_key", "name": "climate_lens"},
            "preauthorized": {"emails": []}
        }, f)

with open(CONFIG_PATH) as f:
    config = yaml.load(f, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"]
)

col_l, col_m, col_r = st.columns([1, 2, 1])
with col_m:
    tab1, tab2 = st.tabs(["🔑  Sign In", "📝  Sign Up"])

    with tab1:
        authenticator.login(location="main")
        if st.session_state.get("authentication_status"):
            st.success(f"Welcome, **{st.session_state['name']}**! Use the sidebar to navigate.")
            authenticator.logout("Logout", location="sidebar")
        elif st.session_state.get("authentication_status") is False:
            st.error("❌ Wrong username or password.")
        else:
            st.info("ℹ️ Sign in to explore climate data.")

    with tab2:
        st.markdown("<p style='color:rgba(255,255,255,0.6); font-size:0.85rem;'>Create your free account</p>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        new_name     = c1.text_input("Full Name", placeholder="Tapan Datta")
        new_email    = c2.text_input("Email", placeholder="you@email.com")
        new_username = c1.text_input("Username", placeholder="tapan123")
        new_password = c2.text_input("Password", type="password", placeholder="••••••••")
        confirm_pass = st.text_input("Confirm Password", type="password", placeholder="••••••••")

        if st.button("🚀 Create Account", use_container_width=True):
            if not all([new_name, new_email, new_username, new_password, confirm_pass]):
                st.warning("⚠️ Please fill in all fields.")
            elif new_password != confirm_pass:
                st.error("❌ Passwords do not match.")
            elif new_username in config["credentials"]["usernames"]:
                st.error("❌ Username already taken.")
            else:
                try:
                    hashed = stauth.Hasher.hash(new_password)
                except TypeError:
                    hashed = stauth.Hasher([new_password]).generate()[0]
                config["credentials"]["usernames"][new_username] = {
                    "name": new_name, "email": new_email, "password": hashed
                }
                with open(CONFIG_PATH, "w") as f:
                    yaml.dump(config, f)
                st.success("✅ Account created! Switch to Sign In.")

st.markdown("""
<div style='text-align:center; margin-top:3rem; padding-bottom:2rem;'>
    <p style='color:rgba(255,255,255,0.2); font-size:0.8rem;'>Data: NASA GISS Surface Temperature Analysis (GISTEMP v4)</p>
</div>
""", unsafe_allow_html=True)
