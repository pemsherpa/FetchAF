# Standard library imports
import hashlib
import os
import time
import uuid

# Third-party imports
from dotenv import load_dotenv
import extra_streamlit_components as stx
from sqlalchemy import (
    create_engine,
    text,
    Table,
    Column,
    String,
    MetaData
)
import streamlit as st

# First Streamlit command must be set_page_config
st.set_page_config(page_title="FetchAF", layout="wide")

# Load environment variables
load_dotenv()

# Initialize cookie manager without caching
cookie_manager = stx.CookieManager()

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Hide Streamlit's default sidebar for login/signup and welcome pages
st.markdown(
    """
    <style>
    /* Hide default sidebar */
    [data-testid="stSidebar"] {display: none;}
    
    /* Modern minimalist color palette */
    :root {
        --primary-green: #2ecc71;
        --dark-green: #27ae60;
        --light-green: rgba(46, 204, 113, 0.1);
        --accent-green: #46cb8c;
        --bg-dark: #1e1e2e;
        --bg-card: #2a2a3a;
        --text-white: #f8f9fa;
        --text-light: #bdc3c7;
        --text-accent: #ecf0f1;
        --shadow: rgba(0, 0, 0, 0.2);
    }
    
    /* Dark background */
    .main .block-container {
        background: var(--bg-dark);
        color: var(--text-white);
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* Modern typography with white text */
    h1 {
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        color: var(--primary-green);
    }
    
    h2, h3 {
        font-weight: 600;
        color: var(--primary-green);
    }
    
    p, li {
        font-weight: 400;
        color: var(--text-white);
        line-height: 1.6;
    }
    
    /* Clean buttons */
    button, .stButton>button {
        background-color: var(--primary-green) !important;
        color: var(--bg-dark) !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 500 !important;
        padding: 0.6rem 1.2rem !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 5px var(--shadow) !important;
    }
    
    button:hover, .stButton>button:hover {
        background-color: var(--dark-green) !important;
        box-shadow: 0 4px 10px rgba(46, 204, 113, 0.2) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Minimal input fields */
    input[type="text"], input[type="password"], .stTextInput>div>div>input {
        border: 1px solid #4a4a5a !important;
        border-radius: 8px !important;
        padding: 0.8rem 1rem !important;
        background-color: #2a2a3a !important;
        color: var(--text-white) !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
    }
    
    input[type="text"]:focus, input[type="password"]:focus, .stTextInput>div>div>input:focus {
        border-color: var(--primary-green) !important;
        box-shadow: 0 0 0 2px rgba(46, 204, 113, 0.15) !important;
    }
    
    /* Modern tab interface */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #4a4a5a;
        padding-bottom: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        background-color: transparent !important;
        border-radius: 8px 8px 0 0 !important;
        color: var(--text-light) !important;
        font-weight: 500;
        border: none !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--primary-green) !important;
        border-bottom: 2px solid var(--primary-green) !important;
        background-color: transparent !important;
    }
    
    /* Status messages */
    .element-container div[data-testid="stImage"] {
        background-color: transparent;
        padding: 0;
        border-radius: 8px;
        color: var(--text-white);
    }
    
    /* Clean cards */
    .card {
        background-color: var(--bg-card);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid #3a3a4a;
        box-shadow: 0 4px 20px var(--shadow);
        transition: transform 0.2s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px var(--shadow);
    }
    
    /* Feature list styling */
    .feature-list {
        padding-left: 0;
    }
    
    .feature-list li {
        margin-bottom: 12px;
        list-style-type: none;
        position: relative;
        padding-left: 28px;
        color: var(--text-white);
    }
    
    .feature-list li:before {
        content: "✓";
        color: var(--primary-green);
        font-weight: bold;
        position: absolute;
        left: 0;
        font-size: 16px;
    }
    
    /* Links styling */
    a {
        color: var(--primary-green);
        text-decoration: none;
        font-weight: 500;
        transition: color 0.2s ease;
    }
    
    a:hover {
        color: var(--accent-green);
    }
    
    /* Modern footer */
    .app-footer {
        text-align: center;
        margin-top: 3rem;
        color: var(--text-light);
        font-size: 0.85rem;
        padding-top: 1.5rem;
        border-top: 1px solid #3a3a4a;
    }
    
    /* Logo styling */
    .logo {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--primary-green);
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }
    
    .logo-accent {
        color: var(--text-white);
    }
    
    /* Two-column layout */
    .flex-container {
        display: flex;
        gap: 2rem;
        align-items: center;
        margin: 2rem 0;
    }
    
    .flex-item {
        flex: 1;
    }
    
    @media (max-width: 768px) {
        .flex-container {
            flex-direction: column;
        }
    }
    
    /* Streamlit native elements */
    label {
        color: var(--text-white) !important;
    }
    
    .stAlert > div {
        color: var(--bg-dark) !important;
    }
    
    /* Code blocks */
    code {
        color: var(--primary-green) !important;
        background-color: #32324a !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Database configuration
DB_CONFIG = {
    'user': os.getenv("DB_USER", "Pema"),
    'password': os.getenv("DB_PASSWORD", "delusional"),
    'host': os.getenv("DB_HOST", "localhost"),
    'port': os.getenv("DB_PORT", "5433"),
    'name': os.getenv("DB_NAME", "AgileDB")
}

def get_db_engine():
    """Create and return a database engine."""
    try:
        conn_str = (
            f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
            f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['name']}"
        )
        return create_engine(conn_str)
    except Exception as e:
        st.error(f"Database connection error: {str(e)}")
        return None

def init_db():
    """Initialize database tables if they don't exist."""
    try:
        engine = get_db_engine()
        if not engine:
            return False

        metadata = MetaData()

        # Define users table
        Table(
            'users',
            metadata,
            Column('username', String, primary_key=True),
            Column('password_hash', String, nullable=False)
        )

        # Define sessions table
        Table(
            'sessions',
            metadata,
            Column('session_id', String, primary_key=True),
            Column('username', String, nullable=False)
        )

        # Create tables
        metadata.create_all(engine)
        return True
    except Exception as e:
        st.error(f"Database initialization error: {str(e)}")
        return False

def user_exists(username):
    """Check if a user exists in the database."""
    engine = get_db_engine()
    with engine.connect() as conn:
        query = "SELECT 1 FROM users WHERE username = :username"
        result = conn.execute(text(query), {"username": username})
        return result.fetchone() is not None

def set_auth_cookie(username):
    """Set authentication cookie for persistent login."""
    session_id = str(uuid.uuid4())
    expiry_time = int(time.time()) + (30 * 24 * 60 * 60)
    
    engine = get_db_engine()
    if not engine:
        return False

    try:
        with engine.connect() as conn:
            # Delete existing sessions
            delete_query = "DELETE FROM sessions WHERE username = :username"
            conn.execute(text(delete_query), {"username": username})
            
            # Create new session
            insert_query = (
                "INSERT INTO sessions (session_id, username, expires_at) "
                "VALUES (:session_id, :username, :expires_at)"
            )
            conn.execute(
                text(insert_query),
                {
                    "session_id": session_id,
                    "username": username,
                    "expires_at": str(expiry_time)
                }
            )
            conn.commit()
            
            cookie_manager.set("session_id", session_id, expires_at=expiry_time)
            return True
    except Exception as e:
        st.error(f"Session creation error: {str(e)}")
        return False

def verify_auth_cookie():
    """Verify the authentication cookie and update session state."""
    session_id = cookie_manager.get("session_id")
    if not session_id:
        return False

    engine = get_db_engine()
    with engine.connect() as conn:
        query = "SELECT username FROM sessions WHERE session_id = :session_id"
        result = conn.execute(text(query), {"session_id": session_id})
        user = result.fetchone()

    if user:
        st.session_state.current_user = user[0]
        st.session_state.logged_in = True
        return True
    
    st.session_state.current_user = None
    st.session_state.logged_in = False
    return False

def clear_auth_cookie():
    """Clear authentication cookie and session data."""
    session_id = cookie_manager.get("session_id")
    if session_id:
        engine = get_db_engine()
        if engine:
            try:
                with engine.connect() as conn:
                    query = "DELETE FROM sessions WHERE session_id = :session_id"
                    conn.execute(text(query), {"session_id": session_id})
                    conn.commit()
            except Exception as e:
                st.error(f"Session removal error: {str(e)}")
    
    cookie_manager.delete("session_id")

def navigate_to_main():
    """Navigate to the main page."""
    try:
        st.switch_page("pages/main.py")
    except Exception as e:
        st.error(f"Navigation error: {str(e)}")

def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_credentials(username, password):
    """Verify user credentials against stored hash."""
    engine = get_db_engine()
    if not engine:
        return False
    
    try:
        with engine.connect() as conn:
            query = "SELECT password_hash FROM users WHERE username = :username"
            result = conn.execute(text(query), {"username": username})
            user_data = result.fetchone()
            
            if user_data:
                stored_hash = user_data[0]
                return stored_hash == hash_password(password)
            return False
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        return False

def signup():
    """Handle user signup process."""
    st.subheader("Create a New Account")
    new_username = st.text_input("Username", key="new_username")
    new_password = st.text_input("Password", type="password", key="new_password")
    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="confirm_password"
    )

    if st.button("Sign Up", key="signup_button"):
        if not all([new_username, new_password, confirm_password]):
            st.error("Please fill in all fields!")
            return

        if user_exists(new_username):
            st.error("Username already exists!")
            return

        if new_password != confirm_password:
            st.error("Passwords do not match!")
            return

        engine = get_db_engine()
        if not engine:
            st.error("Database connection error. Please try again later.")
            return

        try:
            with engine.connect() as conn:
                query = (
                    "INSERT INTO users (username, password_hash) "
                    "VALUES (:username, :password_hash)"
                )
                conn.execute(
                    text(query),
                    {
                        "username": new_username,
                        "password_hash": hash_password(new_password)
                    }
                )
                conn.commit()
                st.success("Account created successfully! Please log in.")
        except Exception as e:
            st.error(f"Account creation failed: {str(e)}")

def login():
    """Handle user login process."""
    st.subheader("Login to Your Account")
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")
    remember_me = st.checkbox("Remember me", value=True)

    if st.button("Login", key="login_button"):
        if not all([username, password]):
            st.error("Please enter both username and password!")
            return

        if verify_credentials(username, password):
            st.session_state.logged_in = True
            st.session_state.current_user = username
            
            if remember_me:
                set_auth_cookie(username)
            
            st.success(f"Welcome back, {username}!")
            st.rerun()
        else:
            st.error("Invalid username or password!")

def welcome_page():
    """Display the welcome page."""
    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:
        if st.session_state.logged_in:
            st.markdown(f"# Welcome back, {st.session_state.current_user}! 👋")
        else:
            st.markdown("# Welcome to FetchAF! 👋")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### SQL from Plain English")
        st.markdown(
            "Query your PostgreSQL database using natural language - "
            "eliminate the need to write complex SQL queries."
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("Explore Now", key="explore_button"):
            navigate_to_main()

def login_signup_page():
    """Display the login/signup page."""
    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:
        st.markdown("# Login or Sign Up")
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        with tab1:
            login()
        with tab2:
            signup()

def main():
    """Main application entry point."""
    if not init_db():
        st.error("Database initialization failed. Authentication unavailable.")
        return

    if not st.session_state.logged_in and verify_auth_cookie():
        st.session_state.logged_in = True

    if st.session_state.logged_in:
        welcome_page()
    else:
        login_signup_page()

if __name__ == "__main__":
    main()