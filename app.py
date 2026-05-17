

import streamlit as st
import yaml, os
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

st.set_page_config(page_title="🌍 Climate Lens", layout="wide", page_icon="🌍")

st.markdown("""
<style>
/* Global */
body { font-family: 'Segoe UI', sans-serif; }
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    min-height: 100vh;
}
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05) !important;
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(255,255,255,0.1);
}
[data-testid="stSidebar"] * { color: white !important; }

/* Hero */
.hero {
    text-align: center;
    padding: 3rem 1rem 1rem 1rem;
}
.hero h1 {
    font-size: 3.5rem;
    font-weight: 800;
    background: linear-gradient(90deg, #00c9ff, #92fe9d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.hero p {
    color: rgba(255,255,255,0.7);
    font-size: 1.1rem;
    margin-bottom: 2rem;
}
.divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #00c9ff, transparent);
    margin: 1rem 0 2rem 0;
    border: none;
}

/* Auth card */
.auth-card {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 20px;
    padding: 2rem;
    max-width: 700px;
    margin: 0 auto;
}

/* Inputs */
input[type="text"], input[type="password"], input[type="email"] {
    background: rgba(255,255,255,0.1) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: white !important;
    padding: 0.6rem 1rem !important;
}
input::placeholder { color: rgba(255,255,255,0.4) !important; }
label { color: rgba(255,255,255,0.85) !important; font-size: 0.9rem !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #00c9ff, #92fe9d) !important;
    color: #0f2027 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.6rem 2rem !important;
    font-size: 1rem !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0,201,255,0.4) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    color: rgba(255,255,255,0.6) !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #00c9ff, #92fe9d) !important;
    color: #0f2027 !important;
}

/* Alerts */
.stSuccess, .stInfo, .stError, .stWarning {
    border-radius: 12px !important;
    backdrop-filter: blur(10px) !important;
}
</style>
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

st.markdown("""
<div class='hero'>
    <h1>🌍 Climate Lens</h1>
    <p>Exploring Northern Hemisphere Temperature Trends since 1880</p>
</div>
<div class='divider'></div>
""", unsafe_allow_html=True)

st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🔑  Sign In", "📝  Sign Up"])

with tab1:
    authenticator.login(location="main")
    if st.session_state.get("authentication_status"):
        st.success(f"✅ Welcome back, **{st.session_state['name']}**! Use the sidebar to navigate.")
        authenticator.logout("Logout", location="sidebar")
    elif st.session_state.get("authentication_status") is False:
        st.error("❌ Incorrect username or password.")
    else:
        st.info("ℹ️ Enter your credentials to explore climate data.")

with tab2:
    st.markdown("##### Create your account")
    c1, c2 = st.columns(2)
    new_name     = c1.text_input("Full Name", placeholder="Tapan Datta")
    new_email    = c2.text_input("Email", placeholder="you@email.com")
    new_username = c1.text_input("Username", placeholder="tapan123")
    new_password = c2.text_input("Password", type="password", placeholder="••••••••")
    confirm_pass = c2.text_input("Confirm Password", type="password", placeholder="••••••••")

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
            st.success("✅ Account created! Switch to Sign In tab.")

st.markdown("</div>", unsafe_allow_html=True)
