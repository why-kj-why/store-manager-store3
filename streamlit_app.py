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
        "What is the sum of number of transactions this year compared to last year for the store FIVE POINTS PLAZA?": {
            "sql": "SELECT SUM(f.TransactionCountTY) AS TotalTransactionsTY, SUM(f.TransactionCountLY) AS TotalTransactionsLY FROM fact_Basket f JOIN dim_Location_Latest l ON f.LocationLatestKey = l.LocationLatestKey WHERE l.LatestLocation = 'FIVE POINTS PLAZA';",
            "nlr": "The data table returned indicates that the total number of transactions for the latest location of the store, FIVE POINTS PLAZA, this year is 5,188, while the number of transactions from last year is 0. This suggests that the store has either just opened this year or has not recorded any transactions in the previous year.",
            
        },
        "What are the net margins in USD for the store FIVE POINTS PLAZA?": {
            "sql": "SELECT f.NetExVATUSDPlan FROM Fact_Store_Plan f JOIN dim_Location_Latest l ON f.LocationLatestKey = l.LocationLatestKey WHERE l.LatestLocation = 'FIVE POINTS PLAZA';",
            "nlr": "The data table returned consists of a series of net margin values in USD for the store located at FIVE POINTS PLAZA. Each value represents a recorded net margin, with some values appearing multiple times, indicating that these margins may have been recorded on different occasions or under different conditions.\n\nThe margins range from 0.0 to 11,009.72 USD, showcasing a variety of performance levels. Notably, several entries are zero, suggesting instances where the store may not have generated a profit. The highest recorded net margin is 11,009.72 USD, while the lowest is 0.0 USD, reflecting a significant variance in profitability.\n\nOverall, this data provides a snapshot of the financial performance of the store, highlighting both successful and challenging periods.",
        },
        "What is the net sales on July 31, 2023 compared to the same period last year for the store FIVE POINTS PLAZA?":
        {
            "sql": "SELECT f.NetSaleLocal, f.NetSaleLocalLY FROM fact_Sale f JOIN dim_Calendar c ON f.CalendarKey = c.CalendarKey JOIN dim_Location_Latest l ON f.LocationLatestKey = l.LocationLatestKey WHERE l.LatestLocation = 'FIVE POINTS PLAZA' AND c.CalendarDate = '2023-07-31';",
            "nlr": "On July 31, 2023, the net sales in USD for the latest location of the store FIVE POINTS PLAZA were as follows: 80.00, 196.96, and 484.48. In comparison, there were no net sales recorded for the same period last year."
        },
        "What is the Daily Sales Report (DSR) using our sales records for the store FIVE POINTS PLAZA on July 31, 2023?": {
            "sql": "SELECT f.NetSaleLocal, f.NetSaleUSD, f.NetQuantity, c.CalendarDate FROM fact_Sale f JOIN dim_Calendar c ON f.CalendarKey = c.CalendarKey JOIN dim_Location_Latest l ON f.LocationLatestKey = l.LocationLatestKey WHERE l.LatestLocation = 'FIVE POINTS PLAZA' AND c.CalendarDate = '2023-07-31';",
            "nlr": "The data table returned contains sales information for the store at FIVE POINTS PLAZA on July 31, 2023. Each row represents a different sales transaction or summary for that day.\n\nThe first column shows the total sales amount for each transaction, with values of 80.0, 196.96, and 484.48. These figures indicate the revenue generated from individual sales. The second column mirrors the first, confirming the sales amounts are consistent.\n\nThe third column indicates the number of transactions that contributed to each sales amount, all of which are 4 for the first two rows and 64 for the last row. This suggests that the first two sales amounts were generated from a smaller number of transactions compared to the last one, which had a significantly higher volume of sales.\n\nThe final column provides the date of the transactions, confirming that all entries are from July 31, 2023. Overall, this data reflects the sales performance of the store on that specific day, highlighting both the total sales and the number of transactions contributing to those totals.",
        },
        "Compare the average sales revenue for the store FIVE POINTS PLAZA with the average sales revenue for all stores in USA.": {
            "sql": "SELECT AVG(fs.NetSaleUSD) AS AverageSalesRevenue FROM fact_Sale fs JOIN dim_Location_Latest dl ON fs.LocationLatestKey = dl.LocationLatestKey WHERE dl.LatestLocation = 'FIVE POINTS PLAZA' \nGROUP BY dl.LatestCountry\nUNION\nSELECT AVG(fs.NetSaleUSD) AS AverageSalesRevenue FROM fact_Sale fs JOIN dim_Location_Latest dl ON fs.LocationLatestKey = dl.LocationLatestKey WHERE dl.LatestCountry = 'USA';",
            "nlr": "The data table returned two values representing average sales revenue. The first value, approximately 370.23, corresponds to the average sales revenue for the store located in FIVE POINTS PLAZA. The second value, approximately 471.99, represents the average sales revenue for all stores located in the USA. This comparison indicates that the average sales revenue for the store in FIVE POINTS PLAZA is lower than the average sales revenue for the stores across the entire country.",
        },
        "What were the sales during the 'Autumn/Winter' season for the store FIVE POINTS PLAZA?": {
            "sql": "SELECT dll.LatestLocation,SUM(f.NetSaleUSD) as TotalSales, d.Season, d.FiscalMonthName, d.FiscalYear \nFROM fact_Sale f JOIN dim_Calendar d ON f.CalendarKey = d.CalendarKey JOIN dim_Location_Latest dll ON f.LocationLatestKey =dll.LocationLatestKey WHERE d.Season = 'Autumn/Winter' AND f.LocationLatestKey = (SELECT LocationLatestKey FROM dim_Location_Latest dll WHERE dll.LatestLocation = 'FIVE POINTS PLAZA') GROUP BY d.FiscalMonthName, d.FiscalYear ORDER BY d.FiscalYear DESC, d.FiscalMonthName;",
            "nlr": "The data table returned indicates the sales figures for the 'Autumn/Winter' season at the store located in FIVE POINTS PLAZA. It shows two entries: the first entry reflects sales of $1,852.68 for the month of August in 2023, while the second entry reports sales of $8,446.11 for January in 2022. This information highlights the sales performance during the specified season across different months and years.",
        },
        "What is the average number of units sold per transaction at the store FIVE POINTS PLAZA?": {
            "sql": "SELECT AVG(f.TransactionCountTY) AS AverageUnitsSold FROM fact_Basket f\nJOIN dim_Location_Latest d ON f.LocationLatestKey = d.LocationLatestKey\nWHERE d.LatestLocation = 'FIVE POINTS PLAZA';",
            "nlr": "The data table returned indicates that the average number of units sold per transaction at the latest location of store FIVE POINTS PLAZA is approximately 27.02. This figure suggests that, on average, each transaction at this location involves the sale of just over 27 units.",
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

        # st.dataframe(getDataTable)

        nlr = store_questions[selected_query]["nlr"]
        st.write(nlr)

# Main Application
set_custom_css()

# Load the STORE MANAGER app directly without sidebar or toggle
store_manager_app()
