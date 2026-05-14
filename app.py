
import streamlit as st
import yaml, os
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

st.set_page_config(page_title="🌍 Climate Lens", layout="wide")

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
    <div style='text-align:center; padding: 2rem 0 1rem 0'>
        <h1 style='color:#1a7a6e; font-size:3rem;'>🌍 Climate Lens</h1>
        <p style='color:gray; font-size:1.1rem;'>
            Exploring Northern Hemisphere Temperature Trends since 1880
        </p>
    </div>
    <hr>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Sign Up"])

with tab1:
    authenticator.login(location="main")
    if st.session_state.get("authentication_status"):
        st.success(f"✅ Welcome, **{st.session_state['name']}**! Use the sidebar to navigate.")
        authenticator.logout("Logout", location="sidebar")
    elif st.session_state.get("authentication_status") is False:
        st.error("❌ Incorrect username or password.")
    else:
        st.info("ℹ️ Enter your credentials above to sign in.")

with tab2:
    st.subheader("Create a New Account")

    c1, c2 = st.columns(2)
    new_name     = c1.text_input("Full Name")
    new_email    = c2.text_input("Email")
    new_username = c1.text_input("Username")
    new_password = c2.text_input("Password", type="password")
    confirm_pass = c2.text_input("Confirm Password", type="password")

    if st.button("🚀 Create Account", use_container_width=True):
        if not all([new_name, new_email, new_username, new_password, confirm_pass]):
            st.warning("⚠️ Please fill in all fields.")
        elif new_password != confirm_pass:
            st.error("❌ Passwords do not match.")
        elif new_username in config["credentials"]["usernames"]:
            st.error("❌ Username already taken.")
        else:
            # ✅ Fixed: works with all versions of streamlit-authenticator
            try:
                hashed = stauth.Hasher.hash(new_password)        # newer versions
            except TypeError:
                hashed = stauth.Hasher([new_password]).generate()[0]  # older versions

            config["credentials"]["usernames"][new_username] = {
                "name": new_name, "email": new_email, "password": hashed
            }
            with open(CONFIG_PATH, "w") as f:
                yaml.dump(config, f)
            st.success("✅ Account created! Go to Sign In tab.")
