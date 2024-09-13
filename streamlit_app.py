import streamlit as st
from pandas import DataFrame
from pymysql import connect

DB_HOST = "tellmoredb.cd24ogmcy170.us-east-1.rds.amazonaws.com"
DB_USER = "admin"
DB_PASS = "2yYKKH8lUzaBvc92JUxW"
DB_PORT = "3306"
DB_NAME = "claires"
CONVO_DB_NAME = "store_questions"

CLAIRE_DEEP_PURPLE = "#553D94"
CLAIRE_MAUVE = "#D2BBFF"

st.set_page_config(
    layout = 'wide', 
    initial_sidebar_state = 'collapsed',
    page_title = 'Store Manager App',
    page_icon = 'claires-logo.svg',
)

if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'display_df_and_nlr' not in st.session_state:
    st.session_state['display_df_and_nlr'] = False

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""

def connect_to_db(db_name):
    return connect(
        host = DB_HOST,
        port = int(DB_PORT),
        user = DB_USER,
        password = DB_PASS,
        db = db_name
    )

def set_custom_css():
    custom_css = """
    <style>
        .st-emotion-cache-9aoz2h.e1vs0wn30 {
            display: flex;
            justify-content: center; /* Center-align the DataFrame */
        }
        .st-emotion-cache-9aoz2h.e1vs0wn30 table {
            margin: 0 auto; /* Center-align the table itself */
        }

        .button-container {
            display: flex;
            justify-content: flex-end; /* Align button to the right */
            margin-top: 10px;
        }

        .circular-button {
            border-radius: 50%;
            background-color: #553D94; /* Button color */
            color: white;
            border: none;
            padding: 10px 15px; /* Adjust size as needed */
            cursor: pointer;
        }

        .circular-button:hover {
            background-color: #452a7f; /* Slightly darker shade on hover */
        }
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def store_manager_app():
    with open(r'claires-logo.svg', 'r') as image:
        image_data = image.read()
    st.logo(image=image_data)

    store_questions = {
        "Select a query": None,
        "What is the sum of number of transactions this year compared to last year for latest location of store FIVE POINTS PLAZA?": {
            "sql": "SELECT SUM(f.TransactionCountTY) AS TotalTransactionsTY, SUM(f.TransactionCountLY) AS TotalTransactionsLY FROM fact_Basket f JOIN dim_Location_Latest l ON f.LocationLatestKey = l.LocationLatestKey WHERE l.LatestLocation = 'FIVE POINTS PLAZA';",
            "nlr": "The data table returned indicates that the total number of transactions for the latest location of the store, FIVE POINTS PLAZA, this year is 5,188, while the number of transactions from last year is 0. This suggests that the store has either just opened this year or has not recorded any transactions in the previous year.",
            
        },
        "What are the net margins in USD for store with latest location FIVE POINTS PLAZA?": {
            "sql": "SELECT f.NetExVATUSDPlan FROM Fact_Store_Plan f JOIN dim_Location_Latest l ON f.LocationLatestKey = l.LocationLatestKey WHERE l.LatestLocation = 'FIVE POINTS PLAZA';",
            "nlr": "The data table returned consists of a series of net margin values in USD for the store located at FIVE POINTS PLAZA. Each value represents a recorded net margin, with some values appearing multiple times, indicating that these margins may have been recorded on different occasions or under different conditions.\n\nThe margins range from 0.0 to 11,009.72 USD, showcasing a variety of performance levels. Notably, several entries are zero, suggesting instances where the store may not have generated a profit. The highest recorded net margin is 11,009.72 USD, while the lowest is 0.0 USD, reflecting a significant variance in profitability.\n\nOverall, this data provides a snapshot of the financial performance of the store, highlighting both successful and challenging periods.",
        },
    }

    if 'queries' not in st.session_state:
        st.session_state['queries'] = {}

    st.markdown(f"""
    <h4 style="background-color: {CLAIRE_DEEP_PURPLE}; color: white; padding: 10px;">
        STORE MANAGER
    </h4>
    """, unsafe_allow_html=True)

    store_name_id_placeholder = st.markdown(f"""
    <h4 style="background-color: {CLAIRE_MAUVE}; color: black; padding: 10px;">
    </h4>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
        div.stButton {
            display: flex;
            justify-content: flex-end; /* Align button to the right */
            font-size: 30px; /* Increase font size */
            margin-top: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    store_name_id_placeholder.markdown(f"""
    <h4 style="background-color: {CLAIRE_MAUVE}; color: black; padding: 10px;">
        FIVE POINTS PLAZA
    </h4>
    """, unsafe_allow_html=True)

    query_options = list(store_questions.keys())
    selected_query = st.selectbox("Select a query", query_options if query_options else ["Select a query"])

    if selected_query and selected_query != "Select a query":
        sql_query = store_questions[selected_query]["sql"]
        conn = connect_to_db(DB_NAME)
        cur = conn.cursor()
        cur.execute(sql_query)
        getDataTable = cur.fetchall()
        columns = [column[0] for column in cur.description]
        getDataTable = DataFrame(getDataTable, columns=columns)

        st.dataframe(getDataTable)

        nlr = store_questions[selected_query]["nlr"]
        st.write(nlr)

# Main Application
set_custom_css()

# Load the STORE MANAGER app directly without sidebar or toggle
store_manager_app()
