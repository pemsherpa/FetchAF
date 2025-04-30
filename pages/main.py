import streamlit as st
from sqlalchemy import create_engine, text, inspect
from langchain_community.utilities.sql_database import SQLDatabase
import os
from dotenv import load_dotenv
import pandas as pd
import time
import cohere
import re

# Configure page to show sidebar (must be first Streamlit command)
st.set_page_config(layout="wide", page_title="FetchAF", page_icon=":bar_chart:")

# Load environment variables
load_dotenv()

# Apply minimalist dark theme styling with white text
st.markdown(
    """
    <style>
    /* Modern minimalist color palette */
    :root {
        --primary-green: #2ecc71;
        --dark-green: #27ae60;
        --light-green: rgba(46, 204, 113, 0.1);
        --accent-green: #46cb8c;
        --bg-dark: #1e1e2e;
        --bg-card: #2a2a3a;
        --bg-sidebar: #252538;
        --text-white: #f8f9fa;
        --text-light: #bdc3c7;
        --text-accent: #ecf0f1;
        --shadow: rgba(0, 0, 0, 0.2);
        --border-color: #3a3a4a;
    }
    
    /* Dark background */
    .main .block-container {
        background: var(--bg-dark);
        color: var(--text-white);
        max-width: 1400px;
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
    input[type="text"], .stTextInput>div>div>input {
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 0.8rem 1rem !important;
        background-color: #2a2a3a !important;
        color: var(--text-white) !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease !important;
    }
    
    input[type="text"]:focus, .stTextInput>div>div>input:focus {
        border-color: var(--primary-green) !important;
        box-shadow: 0 0 0 2px rgba(46, 204, 113, 0.15) !important;
    }
    
    /* Dark sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--bg-sidebar);
        border-right: 1px solid var(--border-color);
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] h1 {
        color: var(--primary-green);
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
    }
    
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: var(--primary-green);
        font-size: 1.2rem;
        margin-top: 1.5rem;
    }
    
    [data-testid="stSidebar"] p {
        color: var(--text-light);
    }
    
    /* Style buttons in sidebar */
    [data-testid="stSidebar"] .stButton>button {
        background-color: transparent !important;
        color: var(--primary-green) !important;
        border: 1px solid var(--primary-green) !important;
        width: 100%;
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stSidebar"] .stButton>button:hover {
        background-color: rgba(46, 204, 113, 0.1) !important;
    }
    
    /* Style expanders in sidebar */
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        border: 1px solid var(--border-color);
        border-radius: 8px;
        margin-bottom: 0.75rem;
        overflow: hidden;
    }
    
    [data-testid="stSidebar"] [data-testid="stExpander"] summary {
        padding: 0.5rem;
        border-radius: 8px;
        background-color: var(--bg-sidebar);
        transition: background-color 0.2s;
    }
    
    [data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {
        background-color: #2d2d42;
    }
    
    [data-testid="stSidebar"] [data-testid="stExpander"] summary p {
        color: var(--text-white) !important;
        font-weight: 500;
    }
    
    /* Sleek dataframe/table */
    .dataframe {
        background-color: var(--bg-card);
        border-radius: 10px;
        overflow: hidden;
        border: none !important;
        box-shadow: 0 2px 10px var(--shadow);
        color: var(--text-white);
    }
    
    .dataframe th {
        background-color: var(--primary-green);
        color: var(--bg-dark);
        font-weight: 500;
        text-align: left;
        padding: 12px 15px;
        border: none !important;
    }
    
    .dataframe td {
        padding: 10px 15px;
        border-bottom: 1px solid var(--border-color) !important;
        border-right: none !important;
        border-left: none !important;
        color: var(--text-white);
    }
    
    .dataframe tr:hover td {
        background-color: #32324a;
    }
    
    /* Style code display section */
    div[data-testid="stCode"] {
        border-radius: 10px !important;
        overflow: hidden;
        box-shadow: 0 2px 10px var(--shadow) !important;
    }
    
    pre code {
        font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
    }
    
    /* Style download button */
    [data-testid="baseButton-secondary"] {
        background-color: transparent !important;
        color: var(--primary-green) !important;
        border: 1px solid var(--primary-green) !important;
        font-weight: 500 !important;
        padding: 0.6rem 1.2rem !important;
        border-radius: 8px !important;
    }
    
    [data-testid="baseButton-secondary"]:hover {
        background-color: rgba(46, 204, 113, 0.1) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Modern cards */
    .card {
        background-color: var(--bg-card);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 15px var(--shadow);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px var(--shadow);
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background-color: var(--primary-green);
        height: 6px;
        border-radius: 3px;
    }
    
    .stProgress > div {
        height: 6px;
        border-radius: 3px;
        background-color: #3a3a4a;
    }
    
    /* Status messages */
    .stAlert {
        background-color: var(--bg-card) !important;
        border-radius: 10px !important;
        border: 1px solid var(--border-color) !important;
        box-shadow: 0 2px 10px var(--shadow) !important;
        padding: 0.75rem 1rem !important;
    }
    
    .stAlert > div {
        color: var(--bg-dark) !important;
    }
    
    /* Logo styling */
    .logo {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary-green);
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
    }
    
    .logo-accent {
        color: var(--text-white);
    }
    
    /* Divider styling */
    .divider {
        height: 1px;
        background-color: var(--border-color);
        margin: 1.5rem 0;
    }
    
    /* Connection status indicator */
    .connection-status {
        display: flex;
        align-items: center;
        background-color: var(--bg-card);
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border: 1px solid var(--border-color);
    }
    
    .connection-status .indicator {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: var(--primary-green);
        margin-right: 10px;
    }
    
    /* List styling */
    ul.feature-list {
        list-style-type: none;
        padding-left: 0;
    }
    
    ul.feature-list li {
        padding: 0.4rem 0;
        position: relative;
        padding-left: 1.5rem;
        color: var(--text-white);
    }
    
    ul.feature-list li:before {
        content: "→";
        position: absolute;
        left: 0;
        color: var(--primary-green);
    }
    
    /* Example list styling */
    ul.example-list {
        list-style-type: none;
        padding-left: 0;
    }
    
    ul.example-list li {
        padding: 0.6rem 0;
        border-bottom: 1px dashed var(--border-color);
        cursor: pointer;
        transition: all 0.2s;
        padding-left: 0;
        color: var(--text-white);
    }
    
    ul.example-list li:hover {
        color: var(--primary-green);
        padding-left: 5px;
    }
    
    ul.example-list li:last-child {
        border-bottom: none;
    }
    
    /* Footer */
    .app-footer {
        text-align: center;
        margin-top: 3rem;
        color: var(--text-light);
        font-size: 0.85rem;
        padding-top: 1.5rem;
        border-top: 1px solid var(--border-color);
    }
    
    /* Labels and text */
    label {
        color: var(--text-white) !important;
    }
    
    /* Fix other Streamlit elements */
    div[data-testid="stText"] p {
        color: var(--text-white);
    }
    
    /* Fix annotation text colors */
    .stAnnotated > div {
        color: var(--text-white) !important;
    }
    
    /* Make small text more readable */
    small {
        color: var(--text-light) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Add Back to Welcome button
if st.button("← Back", key="back_button"):
    try:
        st.switch_page("app.py")
    except Exception as e:
        st.error(f"Navigation error: {str(e)}")

db_status = st.empty()

db_user = os.getenv("DB_USER", "Pema")
db_password = os.getenv("DB_PASSWORD", "delusional")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5433")
db_name = os.getenv("DB_NAME", "AgileDB")

# Connect to PostgreSQL using SQLAlchemy
def get_db_engine():
    try:
        db_status.info("Connecting to database...")
        connection_string = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        engine = create_engine(connection_string, pool_pre_ping=True, pool_recycle=3600)
        db_status.success("Database connected!")
        time.sleep(0.5)
        db_status.empty()
        return engine
    except Exception as e:
        db_status.error(f"Database connection error: {str(e)}")
        return None

engine = get_db_engine()
if engine:
    db = SQLDatabase(engine)
else:
    st.error("Failed to establish database connection. Please check your connection settings.")

# Get schema information
@st.cache_data(ttl=3600)
def get_simplified_schema():
    if not engine:
        return {}
        
    try:
        tables_info = {}
        schema = "public"
        
        inspector = inspect(engine)
        tables = inspector.get_table_names(schema='public')
        
        for table in tables:
            columns = []
            for col in inspector.get_columns(table, schema='public'):
                columns.append((col['name'], str(col['type'])))
            tables_info[table] = columns
        
        return {"public": tables_info}
    except Exception as e:
        st.warning(f"Error getting schema: {str(e)}")
        return {"public": {}}

# Execute SQL query
def run_query(sql_query):
    if not engine:
        return []
        
    try:
        with engine.connect() as connection:
            result_proxy = connection.execute(text(sql_query)) 
            columns = list(result_proxy.keys())
            # Fetch all rows
            results = result_proxy.fetchall()
            
            if not results:
                return []
                
            return [dict(zip(columns, row)) for row in results]
    except Exception as e:
        st.error(f"Query failed: {str(e)}")
        return []

def generate_sql_query(question, tables_info, timeout=15):
    table_name = "f1drivers_dataset" # default
    
    schema_info = ""
    all_identifiers = set() 
    
    # Get sample data for the prompt to show correct values
    sample_values = ""
    
    for schema, tables in tables_info.items():
        if schema == "public" and tables:
            for table, columns in tables.items():
                all_identifiers.add(table)
                schema_info += f"Table: {table}\n"
                columns_list = []
                for name, type_info in columns:
                    all_identifiers.add(name)
                    columns_list.append(f'{name}')
                schema_info += f"Columns: {', '.join(columns_list)}\n\n"
    
    api_key = os.getenv("COHERE_API_KEY", "").strip()
    if not api_key:
        st.error("Cohere API key not found in .env file. Please add COHERE_API_KEY=your_key to your .env file.")
        return f'SELECT * FROM "{table_name}" LIMIT 10;'
    
    try:
        # Create a direct cohere client
        co = cohere.Client(api_key)
        
        # Create a simple, direct prompt with PostgreSQL specific instructions
        prompt = f"""Generate a PostgreSQL query to answer this question: "{question}"

Database Schema:
{schema_info}

CRITICAL FORMATTING RULES FOR POSTGRESQL:
1. Every column name and table name MUST always be enclosed in double quotes (")
2. Example: SELECT "Driver" FROM "f1drivers_dataset" WHERE "Driver" = 'Max Verstappen';
3. String values and literal values must be in single quotes (')
4. Return ONLY the raw SQL query without any explanations, markdown, or code blocks
5. The coulmn name are case-sensitive. Make sure not to change them.

IMPORTANT INFORMATION ABOUT THE DATA:
- All text values are case-sensitive and properly capitalized in the database
- Driver names are stored as "Max Verstappen" (not "max verstappen")
- Country names are stored with proper capitalization: "Italy", "Netherlands", "Germany" (not lowercase)
- {sample_values}

Your query:"""

        # Call the Cohere API directly
        response = co.chat(
            message=prompt,
            model="command",
            temperature=0.2
        )
        
        sql_query = response.text.strip()

        if "```sql" in sql_query:
            start = sql_query.find("```sql") + 6
            end = sql_query.find("```", start)
            if end != -1:
                sql_query = sql_query[start:end].strip()
        elif "```" in sql_query:
            start = sql_query.find("```") + 3
            end = sql_query.find("```", start)
            if end != -1:
                sql_query = sql_query[start:end].strip()
        
        if "SELECT" in sql_query:
            select_pos = sql_query.find("SELECT")
            sql_query = sql_query[select_pos:].strip()
            
            # Find last semicolon if there's text after it
            semicolon_pos = sql_query.rfind(";")
            if semicolon_pos != -1 and semicolon_pos < len(sql_query) - 1:
                sql_query = sql_query[:semicolon_pos+1]
        
        # Add semicolon if missing
        if not sql_query.endswith(";"):
            sql_query += ";"
            
        # Fix quote issues
        sql_query = sql_query.replace("`", "\"")
        
        for identifier in all_identifiers:
            pattern = r'\b{}\b(?!")'.format(re.escape(identifier))
            sql_query = re.sub(pattern, f'"{identifier}"', sql_query, flags=re.IGNORECASE)
        
        while '"""' in sql_query:
            sql_query = sql_query.replace('"""', '"')
        
        while '""' in sql_query:
            sql_query = sql_query.replace('""', '"')
            
        country_capitalization = {
            "'netherlands'": "'Netherlands'",
            "'italy'": "'Italy'",
            "'germany'": "'Germany'",
            "'france'": "'France'",
            "'spain'": "'Spain'",
            "'australia'": "'Australia'",
            "'belgium'": "'Belgium'",
            "'brazil'": "'Brazil'",
            "'finland'": "'Finland'",
            "'united kingdom'": "'United Kingdom'",
            "'uk'": "'UK'",
            "'england'": "'England'"
        }
        
        for lowercase, capitalized in country_capitalization.items():
            sql_query = sql_query.replace(lowercase, capitalized)
            
        return sql_query
        
    except Exception as e:
        st.error(f"Error from Cohere API: {str(e)}")
        return f'SELECT * FROM "{table_name}" LIMIT 10;'

# Set up the example questions for click handling
def set_question(q):
    st.session_state.question = q
    
# Get schema early
schema = get_simplified_schema()

# Main app UI with sidebar
with st.sidebar:
    st.markdown('<div class="logo">Fetch<span class="logo-accent">AF</span></div>', unsafe_allow_html=True)
    
    # Connection status
    st.markdown(
        f"""
        <div class="connection-status">
            <div class="indicator"></div>
            <div>Connected to <b>{db_host}/{db_name}</b></div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    if schema and "public" in schema and schema["public"]:
        st.subheader("Database Tables")
        
        for table_name, columns in schema["public"].items():
            with st.expander(f"📊 {table_name}"):
                # Display the column names
                for col in columns:
                    st.markdown(f"• **{col[0]}** <span style='color:#bdc3c7; font-size:0.85rem;'>({col[1]})</span>", unsafe_allow_html=True)
                
                # Add a button to preview the table
                if st.button(f"Preview Table", key=f"preview_{table_name}"):
                    try:
                        query = f'SELECT * FROM "{table_name}" LIMIT 5;'
                        with engine.connect() as conn:
                            result = conn.execute(text(query))
                            df = pd.DataFrame(result.fetchall(), columns=result.keys())
                            st.dataframe(df, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    else:
        st.warning("No tables found in database")
        
    # Add helpful tips in the sidebar
    st.markdown("### Tips")
    st.markdown("""
    <ul class="feature-list">
        <li>Ask specific questions about your data</li>
        <li>Include time periods or quantities when relevant</li>
        <li>Try different phrasings if you don't get the expected results</li>
    </ul>
    """, unsafe_allow_html=True)

# Initialize question in session state if not present
if 'question' not in st.session_state:
    st.session_state.question = ""

# Main content area - centered layout
main_col1, main_col2, main_col3 = st.columns([1, 4, 1])

with main_col2:
    # Logo and welcome message at the top
    st.markdown('<div class="logo">Fetch<span class="logo-accent">AF</span></div>', unsafe_allow_html=True)
    
    # Add a divider instead of the empty box
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Welcome message when no query is running
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## Welcome to FetchAF")
    st.markdown("""
    Transform how you interact with your database. Ask questions in plain English, and get answers in seconds.
    
    Enter your question below to get started.
    """)
    
    # Center the image
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:
        st.image("https://img.icons8.com/fluency/240/000000/database.png", width=100)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Question input and button only (without examples)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## Ask Your Question")
    
    # Question input section
    question_placeholder = "e.g., Show top drivers by race wins" if "f1drivers_dataset" in schema.get("public", {}) else "e.g., Show top customers by volume"
    
    # Use the session state to set the text input value
    question = st.text_input(
        "Enter your question about your data:", 
        value=st.session_state.question,
        placeholder=question_placeholder,
        key="question_input"
    )
    
    if st.button("Generate Report", type="primary", key="generate_report"):
        if not question:
            st.warning("Please enter a question first.")
        else:
            st.session_state.question = question
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

    # Only show results if there's a question in the session state
    if st.session_state.question:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"## Results for: '{st.session_state.question}'")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Update progress
        status_text.info("Generating SQL query...")
        progress_bar.progress(25)
        
        # Generate SQL
        sql_query = generate_sql_query(st.session_state.question, schema)
        progress_bar.progress(75)
        
        if sql_query:
            st.markdown("### Generated SQL")
            st.code(sql_query, language="sql")
            
            status_text.info("Executing query...")
            progress_bar.progress(85)
            
            results = run_query(sql_query)
            progress_bar.progress(100)
            status_text.success("Done!")
            time.sleep(0.5)
            status_text.empty()
            
            if results:
                st.markdown("### Query Results")
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True)
                
                # Add CSV download option
                csv = df.to_csv(index=False)
                st.download_button(
                    "Download as CSV",
                    csv,
                    f"query_results_{int(time.time())}.csv",
                    "text/csv",
                    key="download_csv"
                )
            else:
                st.info("Query returned no results. Try rephrasing your question.")
        else:
            # Clear progress if SQL generation failed
            progress_bar.empty()
            status_text.empty()
            
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Example questions at the end
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Try these examples:")
    
    if "f1drivers_dataset" in schema.get("public", {}):
        example_questions = [
            "Who are the top 5 drivers by race wins?",
            "How many drivers are from Germany?",
            "What is the average age of drivers from the UK?",
            "Compare points of Ferrari drivers in 2022"
        ]
    else:
        example_questions = [
            "Show me the top 10 customers by total purchases",
            "What products had the highest sales in 2022?",
            "Compare monthly sales between 2021 and 2022",
            "Which category has the best profit margin?"
        ]
    
    example_cols = st.columns(2)
    for i, q in enumerate(example_questions):
        col_idx = i % 2
        with example_cols[col_idx]:
            if st.button(q, key=f"ex_q_{i}"):
                st.session_state.question = q
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="app-footer">
    <p>Powered by Cohere AI, SQLAlchemy and Streamlit • Made with ♥</p>
</div>
""", unsafe_allow_html=True)