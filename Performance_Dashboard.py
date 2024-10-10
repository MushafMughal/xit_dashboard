import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu 
import plotly.graph_objects as go
from datetime import datetime, timedelta
from streamlit_extras.metric_cards import style_metric_cards
import base64
import time
from streamlit_multi_menu import streamlit_multi_menu


#Decimals

def commas(number):
    return f"{number:,.2f}" 
def commas_nd(number):
    return f"{number:,.0f}"

# Load the Excel data

# Major Metrics PAGE

#ALL SECTION
df = pd.read_excel("KPI Record Dashboard.xlsx", sheet_name='ALL', header=0)  # Adjust header or skiprows as needed


cols = ['ST CLICKS', 'BOXES GOALS', 'BOXES', 'BOXES % TARGET', 'ACCESSORY GOAL',
       'ACCESSORIES', 'ACCESSORY % TARGET', 'HOURS', 'QPAY', 'BPH', 'APH',
       'APB', 'QPAY CONV', 'ST CONV', '1K Counts']

for i in cols: 
    df[i] = pd.to_numeric(df[i], errors='coerce')

df.rename(columns={
    "QPAY CONV": "QPAY (%)",
    "ST CONV": "ST (%)"
}, inplace=True)


df['MONTH'] = pd.to_datetime(df['MONTH'])
df["MONTH_G"] = df['MONTH']

month_counts = []
groups = df.groupby(df['MONTH_G'].dt.to_period('M'))
for name, group in groups:
    count = range(1, len(group) + 1) 
    month_counts.extend(count)

df['Month_Count'] = month_counts
df['MONTH'] = df['MONTH'].dt.strftime('%B')
df["BOXES % TARGET"] = df["BOXES % TARGET"].fillna(0)  # Fill NaN with 0 first
df["BOXES % TARGET"] = ((df["BOXES % TARGET"] * 100).round(2).astype(str) + "%")
df["ACCESSORY % TARGET"] = df["ACCESSORY % TARGET"].fillna(0)  # Fill NaN with 0 first
df["ACCESSORY % TARGET"] = ((df["ACCESSORY % TARGET"] * 100).round(2).astype(str) + "%")
df["BTS% BY BOXES"] = df["BTS% BY BOXES"].fillna(0)
df["BTS% BY BOXES"] = ((df['BTS% BY BOXES']*100).round(2).astype(str) + "%")
df["ST (%)"] = df["ST (%)"].fillna(0)
df["ST (%)"] = ((df['ST (%)']*100).round(2).astype(str) + "%")
df["QPAY (%)"] = df["QPAY (%)"].fillna(0)
df["QPAY (%)"] = ((df['QPAY (%)']*100).round(2).astype(str) + "%")
df["BPH"] = (df['BPH']).round(2)
df["APH"] = df["APH"].fillna(0)
df["APH"] = ("$"+(df['APH']).round(2).astype(str))
df["APB"] = df["APB"].fillna(0)
df["APB"] = ("$"+(df['APB']).round(2).astype(str))
df["BOXES GOALS"] = df["BOXES GOALS"].fillna(0)
df["BOXES GOALS"] = ((df['BOXES GOALS']).round(0).astype(int))
df["ACCESSORIES"] = ((df['ACCESSORIES']).round(2))
df["ACCESSORY GOAL"] = ((df['ACCESSORY GOAL']).round(2))

main_cols = ['MARKET', 'STORE', 'MD', 'DM',
       'ELB RANK', 'ST CLICKS', 'BOXES GOALS', 'BOXES', 'BOXES % TARGET',
       'ACCESSORY GOAL', 'ACCESSORIES', 'ACCESSORY % TARGET', 'HOURS', 'QPAY',
       'BPH', 'APH', 'APB', 'QPAY (%)', 'ST (%)', '1K Counts', 'HINT', 'BTS',
       'BTS% BY BOXES']

#MD SECTION
dfMD = pd.read_excel("KPI Record Dashboard.xlsx",sheet_name="MD", header=0) 
dfMD["MONTH"]= dfMD["MONTH"].dt.strftime('%B')
cols_md = ['ST CLICKS','BOXES GOALS', 'BOXES', 'BOXES % TARGET', 'ACCESSORY GOAL',
       'ACCESSORIES', 'ACCESSORY % TARGET', 'HOURS', 'QPAY', 'BPH', 'APH',
       'APB', 'QPAY CONV', 'ST CONV', '1K Counts', 'HINT', 'BTS',
       'BTS% BY BOXES']
for i in cols_md: 
    dfMD[i] = pd.to_numeric(dfMD[i], errors='coerce')
main_cols_md = ['TIME FRAME','MONTH',"MD",'ST CLICKS',
       'BOXES GOALS', 'BOXES', 'BOXES % TARGET', 'ACCESSORY GOAL',
       'ACCESSORIES', 'ACCESSORY % TARGET', 'HOURS', 'QPAY', 'BPH', 'APH',
       'APB', 'QPAY CONV', 'ST CONV', '1K Counts', 'HINT', 'BTS',
       'BTS% BY BOXES']

#DM SECTION
dfDM = pd.read_excel("KPI Record Dashboard.xlsx",sheet_name="DM", header=0) 
dfDM["MONTH"]= dfDM["MONTH"].dt.strftime('%B')
cols_dm = ['ST CLICKS','BOXES GOALS', 'BOXES', 'BOXES % TARGET', 'ACCESSORY GOAL',
       'ACCESSORIES', 'ACCESSORY % TARGET', 'HOURS', 'QPAY', 'BPH', 'APH',
       'APB', 'QPAY CONV', 'ST CONV', '1K Counts', 'HINT', 'BTS',
       'BTS% BY BOXES']
for i in cols_dm: 
    dfMD[i] = pd.to_numeric(dfDM[i], errors='coerce')
main_cols_dm = ['TIME FRAME','MONTH',"DM",'ST CLICKS',
       'BOXES GOALS', 'BOXES', 'BOXES % TARGET', 'ACCESSORY GOAL',
       'ACCESSORIES', 'ACCESSORY % TARGET', 'HOURS', 'QPAY', 'BPH', 'APH',
       'APB', 'QPAY CONV', 'ST CONV', '1K Counts', 'HINT', 'BTS',
       'BTS% BY BOXES']

#MONTH SECTION
dfMon = pd.read_excel("KPI Record Dashboard.xlsx",sheet_name="MONTH", header=0)
dfMon["MONTH"]= dfMon["MONTH"].dt.strftime('%B')
main_cols_mon = ['TIME FRAME', 'ST CLICKS', 'BOXES GOALS',
                'BOXES', 'BOXES % TARGET', 'ACCESSORY GOAL', 'ACCESSORIES',
                'ACCESSORY % TARGET', 'HOURS', 'QPAY', 'BPH', 'APH', 'APB', 'QPAY CONV',
                'ST CONV', '1K Counts', 'HINT', 'BTS', 'BTS% BY BOXES']

# Performance Bonus PAGE

df1 = pd.read_excel("PB YTD.xlsx", sheet_name='PB YTD', header=0)  # Adjust header or skiprows as needed
df1['MONTH'] = pd.to_datetime(df1['MONTH'])
df1['MONTH'] = df1['MONTH'].dt.strftime('%B')
df1["GROWTH % M"] = (df1["GROWTH %"]*100).round(2)
df1["95 ACT RET M"] = (df1["95 ACT RET"]*100).round(2)
df1["PB ATTAINMENT M"] = (df1["PB ATTAINMENT"]*100).round(2)

df1["GROWTH %"] = (df1["GROWTH %"] * 100).round(2).astype(str) + "%"
df1["95 ACT RET"] = (df1["95 ACT RET"] * 100).round(2).astype(str) + "%"
df1["PB ATTAINMENT"] = (df1["PB ATTAINMENT"] * 100).round(2).astype(str) + "%"


main_cols_pb = ['MONTH', 'MARKET', 'STORE', 'MD', 'DM',
                'GROWTH %', '95 ACT RET', 'PB BONUS', 'MISSED OPPORTUNITIES','PB ATTAINMENT']


# ELB PAGE
Jan = pd.read_excel("ELB  - Jan-24.xlsx", header=0)
Feb = pd.read_excel("ELB  - Feb-24.xlsx", header=0)
Mar = pd.read_excel("ELB  - Mar-24.xlsx", header=0)
Apr = pd.read_excel("ELB  - Apr-24.xlsx", header=0)
May = pd.read_excel("ELB  - May-24.xlsx", header=0)
Jun = pd.read_excel("ELB  - June-24.xlsx", header=0)
Jul = pd.read_excel("ELB  - July-24.xlsx", header=0)
Aug = pd.read_excel("ELB  - Aug-24.xlsx", header=0)

Jan["Act Conv"] = Jan["Act Conv"]*100
Jan["Phone% Tgt"] = Jan["Phone% Tgt"]*100
Jan["BTS & HSI % Tgt"] = Jan["BTS & HSI % Tgt"]*100
Jan["Upg Prot"] = Jan["Upg Prot"]*100
Jan["95 Act Ret"] = Jan["95 Act Ret"]*100
Jan["CTU"] = Jan["CTU"]*100

Feb["Act Conv"] = Feb["Act Conv"]*100
Feb["Phone% Tgt"] = Feb["Phone% Tgt"]*100
Feb["BTS & HSI % Tgt"] = Feb["BTS & HSI % Tgt"]*100
Feb["Upg Prot"] = Feb["Upg Prot"]*100
Feb["95 Act Ret"] = Feb["95 Act Ret"]*100

Mar["Act Conv"] = Mar["Act Conv"]*100
Mar["Phone% Tgt"] = Mar["Phone% Tgt"]*100
Mar["BTS & HSI % Tgt"] = Mar["BTS & HSI % Tgt"]*100
Mar["Upg Prot"] = Mar["Upg Prot"]*100
Mar["95 Act Ret"] = Mar["95 Act Ret"]*100

Apr["Act Conv"] = Apr["Act Conv"]*100
Apr["Phone% Tgt"] = Apr["Phone% Tgt"]*100
Apr["BTS & HSI % Tgt"] = Apr["BTS & HSI % Tgt"]*100
Apr["Upg Prot"] = Apr["Upg Prot"]*100
Apr["95 Act Ret"] = Apr["95 Act Ret"]*100

May["Act Conv"] = May["Act Conv"]*100
May["Phone% Tgt"] = May["Phone% Tgt"]*100
May["BTS & HSI % Tgt"] = May["BTS & HSI % Tgt"]*100
May["Upg Prot"] = May["Upg Prot"]*100
May["95 Act Ret"] = May["95 Act Ret"]*100

Jun["Act Conv"] = Jun["Act Conv"]*100
Jun["Phone% Tgt"] = Jun["Phone% Tgt"]*100
Jun["BTS & HSI % Tgt"] = Jun["BTS & HSI % Tgt"]*100
Jun["Upg Prot"] = Jun["Upg Prot"]*100
Jun["95 Act Ret"] = Jun["95 Act Ret"]*100

Jul["Phone % to Target"] = Jul["Phone % to Target"]*100
Jul["BTS & HSI % Tgt"] = Jul["BTS & HSI % Tgt"]*100
Jul["BYOD % Act"] = Jul["BYOD % Act"]*100
Jul["Act % to Target"] = Jul["Act % to Target"]*100
Jul["Feat Attach"] = Jul["Feat Attach"]*100
Jul["Upg Prot"] = Jul["Upg Prot"]*100
Jul["155 Act Ret"] = Jul["155 Act Ret"]*100
Jul["95 Feature Ret"] = Jul["95 Feature Ret"]*100
Jul["Ready Training Complition"] = Jul["Ready Training Complition"]*100

Aug["Prepaid Act % Tgt"] = Aug["Prepaid Act % Tgt"]*100
Aug["Magenta in Metro"] = Aug["Magenta in Metro"]*100
Aug["BYOD % Act"] = Aug["BYOD % Act"]*100
Aug["Upg Prot"] = Aug["Upg Prot"]*100
Aug["155 Act Ret"] = Aug["155 Act Ret"]*100
Aug["95 Feature Ret"] = Aug["95 Feature Ret"]*100
Aug["Flagged Acts"] = Aug["Flagged Acts"]*100
Aug["Ready Training Complition"] = Aug["Ready Training Complition"]*100


data = {
    "January": Jan,
    "Feburary": Feb,
    "March": Mar,
    "April": Apr,
    "May": May,
    "June": Jun,
    "July": Jul,
    "August": Aug
}
lst = ["January","Feburary","March","April","May","June","July","August"]


# Audit Tracker Q3 PAGE
df2 = pd.read_excel("Audit Tracker - Q3.xlsx", header=0)  # Adjust header or skiprows as needed
df2["Score_C"] = df2["Score"]
df2["Score"] = (df2["Score"]*100).astype(str) + "%"
main_cols_audit = ['Score', 'Status', 'Market', 'Store', 'MD', 'DM', 'Audit Date',
       'Audit ID']

#PHONE PAGE

#Android section
dfAnd = pd.read_excel("iPhone and Android Avg Selling Price.xlsx",sheet_name="Android", header=0)  # Adjust header or skiprows as needed
dfAnd["MONTH"]=dfAnd["MONTH"].dt.strftime('%B')
cols_and = [ 'AVERAGE PRICE', 'QUANTITY']
for i in cols_and: 
    dfAnd[i] = pd.to_numeric(dfAnd[i], errors='coerce')
dfAnd['AVERAGE PRICE'] = dfAnd['AVERAGE PRICE'].round(2)
dfAnd['QUANTITY'] = dfAnd['QUANTITY'].round(2)
main_cols_and = ['TIME FRAME', 'MONTH', 'MARKET', 'STORE', 'MD', 'DM',
       'MODEL', 'AVERAGE PRICE', 'QUANTITY']

#Iphone section
dfIp = pd.read_excel("iPhone and Android Avg Selling Price.xlsx",sheet_name="IPhone", header=0)  # Adjust header or skiprows as needed
dfIp["MONTH"]=dfIp["MONTH"].dt.strftime('%B')
cols_ip = [ 'AVERAGE PRICE', 'QUANTITY']
for i in cols_ip: 
    dfIp[i] = pd.to_numeric(dfIp[i], errors='coerce')
dfIp['AVERAGE PRICE'] = dfIp['AVERAGE PRICE'].round(2)
dfIp['QUANTITY'] = dfIp['QUANTITY'].round(2)
main_cols_ip = ['TIME FRAME', 'MONTH', 'MARKET', 'STORE', 'MD', 'DM',
       'MODEL', 'AVERAGE PRICE', 'QUANTITY']

#Hiring Page
dfH = pd.read_excel("Avg Hiring YTD.xlsx", header=0)
dfH["MONTH"]=dfH["MONTH"].dt.strftime('%B')

# Code
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    section.stAppViewMain.main  {
        background-image: url("data:image/png;base64,%s");
        background-size: contain;   /* Adjusts the image to cover the entire section */
        background-position: center;  /* Center the background image */
        background-repeat: no-repeat; /* Prevent the image from repeating */
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('111.png')

# function for styling the sidebar
def style_sidebar_multiselect():
    sidebar_style = '''
    <style>

    span[data-baseweb="tag"] {
        background-color: #832a80 !important;
        border: 2px solid #CCCCCC !important;
        padding: 5% 5% 5% 10% !important;
        border-radius: 25px !important;
        box-shadow: 0px 4px 6px #f3f3f3eb !important;
    }
    
    div.st-an.st-ao.st-ap.st-aq.st-ak.st-ar.st-am.st-as.st-at.st-au.st-av.st-aw.st-ax.st-ay.st-az.st-b0.st-b1.st-b2.st-b3.st-b4.st-b5.st-b6.st-b7.st-b8.st-b9.st-ba.st-bb.st-bc {
        border-radius: 25px !important;
    }

    div.st-emotion-cache-1n76uvr {
        top: -60px; !important;
    }

    div.st-an.st-ao.st-ap.st-aq.st-ak.st-ar.st-am.st-as.st-at.st-au.st-av.st-aw.st-ax.st-ay.st-az.st-b0.st-b1.st-b2.st-b3.st-b4.st-b5.st-b6.st-dm.st-dn.st-do.st-dp.st-dq.st-dr {
    border-radius: 7px; 
    background-color: #1c83e11a;
    color: #004280;
    }

    .st-emotion-cache-p38tq {
        font-size: 1.2rem;
        color: rgb(49, 51, 63);
        padding-bottom: 0.25rem;
        border-radius: 5px;
        padding-left: 0.65rem;
        padding-top: 0.25rem;
    }

    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main > div.stAppViewBlockContainer > div > div > div > div:nth-child(6) > details > div > div > div > div > div > div > div div[data-testid="stMarkdownContainer"] p {
        font-size: 0.88rem;  /* Set your desired font size for all instances */
    }

    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main > div.stAppViewBlockContainer > div > div > div > div:nth-child(8) > details > div > div > div > div > div > div > div div[data-testid="stMarkdownContainer"] p {
        font-size: 0.88rem;  /* Set your desired font size for all instances */
    }
    
    #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stSidebar > div > div > div > div > div > div > div:nth-child(1) {
        padding-top: 15px !important;
        border-bottom: 1.8px solid #bdbfc3 !important;}

    </style> 
    '''
    st.markdown(sidebar_style, unsafe_allow_html=True)

style_sidebar_multiselect()

sub_menus = {"Xclusive Trading Inc.":["Major Metrics","Performance Bonus","Express Leaderboard","Audit Tracker Q3","Phone's Sales","Hiring YTD"],}
sub_menu_icons = {"Xclusive Trading Inc.": ["home","grade","trending_up", "check_box","phone_iphone","person"]}
list_of_xti_imgs = ["https://www.shutterstock.com/shutterstock/photos/585123094/display_1500/stock-vector-abstract-polygonal-background-geometrical-backdrop-with-connecting-dots-lines-triangles-for-585123094.jpg",
                        "https://www.shutterstock.com/shutterstock/photos/1157434318/display_1500/stock-photo-wave-white-background-abstract-white-futuristic-background-wave-with-connecting-dots-and-lines-on-1157434318.jpg",
                        "https://www.shutterstock.com/shutterstock/photos/766689100/display_1500/stock-vector-abstract-financial-chart-with-up-trend-line-graph-and-arrow-in-stock-market-on-white-color-766689100.jpg",
                        "https://www.shutterstock.com/shutterstock/photos/1231011346/display_1500/stock-photo-wave-of-particles-on-white-background-abstract-interlacing-lines-and-points-digital-connection-of-1231011346.jpg",
                        "https://www.shutterstock.com/shutterstock/photos/1901428924/display_1500/stock-vector-abstract-background-of-hexagons-pattern-and-chemical-engineering-genetic-research-molecular-1901428924.jpg",
                        "https://www.shutterstock.com/shutterstock/photos/1727964232/display_1500/stock-vector-abstract-financial-chart-with-uptrend-line-graph-and-candlestick-on-black-and-white-color-1727964232.jpg"]
sub_menu_imgs = {"Xclusive Trading Inc.":list_of_xti_imgs}

with st.sidebar:
    selected2 = streamlit_multi_menu(menu_titles=list(sub_menus.keys()),
                                sub_menus=sub_menus,
                                sub_menu_icons = sub_menu_icons,
                                use_container_width=True,
                                sub_menu_imgs=sub_menu_imgs,sub_menu_text_align="center",
                                menu_titles_font_size = 28,
                                sub_menu_font_color = "#832a80",
                                sub_menu_font_size = 16.5,
                                sub_menu_border_radius = 10)
    
if not selected2:
    css_body_container = f'''
    <style>
        [data-testid="stSidebar"] + section [data-testid="stVerticalBlock"] div:nth-of-type({1})
        [data-testid="stVerticalBlock"] {{background-color:#f1f1f1de}}
    </style>
    '''
    st.markdown(css_body_container,unsafe_allow_html=True)

    with st.expander(label="Note",expanded=True):
        with st.container(border= True):
            st.title("Performance Dashboard")
            st.write("""
            Welcome to the Performance Dashboard! Navigate through the pages using the sidebar.
            """)

if selected2 == "Major Metrics":
    st.title("Major Metrics Dashboard")
    selected = option_menu(menu_title=None,options=["Data Record", "Data Visualization"],orientation='horizontal',
                        styles={
                            "nav-link": {"--hover-color": "#a42bad4b"},
                            "nav-link-selected": {"background-color": "#832a80"}
                            },key="0")

    if selected == "Data Record":

        radio_style = '''
        <style>
        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stSidebar > div > div > div > div > div > div > div:nth-child(2) > div > label > div > p {

            font-family: "Source Sans Pro", sans-serif;
            font-weight: 600 !important;
            font-size: 1.25rem !important;
            color: #31333f !important;}

        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stSidebar > div > div > div > div > div > div > div:nth-child(2) > div > div {
            border: 1.75px solid lightgrey; /* Light grey border */
            border-radius: 15px; /* Rounded corners */
            padding: 12px; /* Add some padding */
            background-color: #f9f9f9; /* Optional: light background for contrast */
            box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1) !important; /* Subtle shadow for a softer look */}

        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stSidebar > div > div > div > div > div > div > div:nth-child(2) > div > div > label > div:first-child {
            background-color: #832a80 !important;}    
        </style>
        '''
        st.markdown(radio_style, unsafe_allow_html=True)

        select_box_opts = ['All', "MD Wise", "DM Wise","Month Wise"]
        selected_radio = st.sidebar.radio(
            "Please Filter here:",
            options=select_box_opts,
            format_func=lambda x: x,
            horizontal=True,key="123"
        )
        
        if selected_radio == "All":

            css_body_container = """
            <style>

                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main > div.stAppViewBlockContainer > div > div > div > div:nth-child(8) > details > div > div > div > div > div > div > div div[data-testid="stMarkdownContainer"] p {
                    font-size: 0.88rem;
                }

                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main > div.stAppViewBlockContainer > div > div > div > div:nth-child(8) > details {
                    margin-top: -1.8em; /* or any other unit */

                }
            </style>
            """
            st.markdown(css_body_container, unsafe_allow_html=True)

            # Sidebar - Filter by MD (with multiselect)
            md_options = ['All'] + df['MD'].unique().tolist()  # Add 'All' to MD options
            selected_md = st.sidebar.multiselect('Select MD', md_options, default='All',key="1")
        
            # Filter MD only if 'All' is not selected
            if 'All' in selected_md or len(selected_md) == 0:
                filtered_df = df
            else:
                filtered_df = df[df['MD'].isin(selected_md)]

            # Ensure filtered_df is not empty before applying DM filter
            if not filtered_df.empty:
                dm_options = ['All'] + filtered_df['DM'].unique().tolist()  # Update DM options based on filtered MD data
                selected_dm = st.sidebar.multiselect('Select DM', dm_options, default='All',key="2")
                # Filter MARKET only if 'All' is not selected
                if 'All' not in selected_dm and len(selected_dm) > 0:
                    filtered_df = filtered_df[filtered_df['DM'].isin(selected_dm)]

            # Ensure filtered_df is not empty before applying DM filter
            if not filtered_df.empty:
                MARKET_options = ['All'] + filtered_df['MARKET'].unique().tolist()  # Update MARKET options based on filtered DM data
                selected_MARKET = st.sidebar.multiselect('Select MARKET', MARKET_options, default='All',key="3")

                # Filter MARKET only if 'All' is not selected
                if 'All' not in selected_MARKET and len(selected_MARKET) > 0:
                    filtered_df = filtered_df[filtered_df['MARKET'].isin(selected_MARKET)]

            # Ensure filtered_df is not empty before applying DM filter
            if not filtered_df.empty:
                Store_options = ['All'] + filtered_df['STORE'].unique().tolist()  # Update MARKET options based on filtered DM data
                selected_STORE = st.sidebar.multiselect('Select STORE', Store_options, default='All',key="4")

                # Filter MARKET only if 'All' is not selected
                if 'All' not in selected_STORE and len(selected_STORE) > 0:
                    filtered_df = filtered_df[filtered_df['STORE'].isin(selected_STORE)]

            if not filtered_df.empty:
                months_options = ['All'] + filtered_df['MONTH'].unique().tolist()
                selected_months = st.sidebar.multiselect('Select MONTH', months_options, default='All',key="5")

                # Filter only if 'All' is not selected
                if 'All' not in selected_months and len(selected_months) > 0:
                    filtered_df = filtered_df[filtered_df['MONTH'].isin(selected_months)]

            css_body_container = f'''
            <style>
                [data-testid="stSidebar"] + section [data-testid="stVerticalBlock"] div:nth-of-type({1})
                [data-testid="stVerticalBlock"] {{background-color:#f1f1f1de}}
            </style>
            '''
            st.markdown(css_body_container,unsafe_allow_html=True)

            with st.expander(label="Key Metrics",expanded=True):
                with st.container(border= True):

                    if not filtered_df.empty:
                        timeframe_options = ['All'] + filtered_df['TIME FRAME'].unique().tolist() 
                        selected_timeframe = st.selectbox("Select Time Period:", timeframe_options, index=0,key="6")

                        # Filter only if 'All' is not selected
                        if selected_timeframe != 'All':
                            filtered_df = filtered_df[(filtered_df['TIME FRAME'] == selected_timeframe)]

                    col1, col2= st.columns(2)
                    if selected_md:
                        if len(selected_md) > 2:
                            display_md = f"{selected_md[0]}, {selected_md[1]} ..."
                        else:
                            display_md = ", ".join(selected_md)
                        if ["All"] in selected_md:
                            display_md = "All"
                        col1.metric(f"Market Director:", display_md, delta = None)
                    else:
                        col1.metric(f"Market Director:", "-", delta = None)

                    if selected_dm:
                        if len(selected_dm) > 2:
                            display_dm = f"{selected_dm[0]}, {selected_dm[1]} ..."
                        else:
                            display_dm = ", ".join(selected_dm)
                        if ["All"] in selected_dm:
                            display_md = "All"
                        col2.metric(f"District Manager:", display_dm, delta = None)
                    else:
                        col2.metric(f"District Manager:", "-", delta = None)

                    if len(selected_MARKET) == 0 and len(selected_dm) == 0 and len(selected_md) == 0 and len(selected_months) == 0:
                        st.warning("No data to show. Please adjust the filters.")

                    else: 
                        col50,col5, col6, col8, col9 = st.columns(5)
                        col50.info(f'ELB Rank: {commas_nd(filtered_df["ELB RANK"].mean())}')
                        col5.info(f'Total ST: {commas_nd(filtered_df["ST CLICKS"].sum())}')
                        col6.info(f'ST Clicks Avg: {commas_nd(filtered_df["ST CLICKS"].mean())}')
                        col8.info(f'Boxes Sum: {commas_nd(filtered_df["BOXES"].sum())}')
                        col9.info(f'Boxes Avg: {commas_nd(filtered_df["BOXES"].mean())}')


                        col7,col13,col10,col11, col12, = st.columns(5)
                        col7.info(f'QPay Conv: {((filtered_df["BOXES"].sum() / filtered_df["QPAY"].sum())*100).round(2)}%')
                        
                        mean_value_col10 = (filtered_df['ACCESSORIES'].sum()/filtered_df['HOURS'].sum()).round(2)
                        col10.info(f"APH: ${mean_value_col10}")

                        mean_value_col11 = (filtered_df['ACCESSORIES'].sum()/filtered_df['BOXES'].sum()).round(2)
                        col11.info(f"APB: ${mean_value_col11}")
                        
                        mean_value_col12 = (filtered_df['BOXES'].sum()/filtered_df['HOURS'].sum()).round(2)
                        col12.info(f"BPH: {mean_value_col12}")

                        mean_value_col13 = ((filtered_df["BOXES"].sum() / filtered_df["ST CLICKS"].sum())*100).round(2)
                        col13.info(f'ST Conv: {mean_value_col13}%')


                        col14,col15,col18,col16,col17 = st.columns(5)

                        mean_value_col14 = ((filtered_df['ACCESSORIES'].sum()/filtered_df['ACCESSORY GOAL'].sum())*100).round(2)
                        col14.info(f"ACC % TGT: {mean_value_col14}%")

                        mean_value_col15 = ((filtered_df['BOXES'].sum()/filtered_df['BOXES GOALS'].sum())*100).round(2)
                        col15.info(f"PPD % TGT: {mean_value_col15}%")
                        
                        col18.info(f"BTS% / Boxes: {commas((filtered_df['BTS'].sum()/filtered_df['BOXES'].sum())*100)}%")
                        col16.info(f"Total 1K Days: {(filtered_df['1K Counts'].sum()).astype(int)}")
                        col17.info(f"1K Days Avg: {((filtered_df['1K Counts'].mean()).round(0)).astype(int)}")


            # Display filtered dataframe with selected MD, MARKET, DM, and TIME FRAME
            if len(selected_MARKET) != 0 or len(selected_dm) != 0 or len(selected_md) != 0 or len(selected_months) != 0:
                with st.expander("Show Table", expanded=False):
                    st.dataframe(filtered_df[main_cols], width=800)
        
        if selected_radio == "MD Wise":

            css_body_container = """
            <style>

                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main > div.stAppViewBlockContainer > div > div > div > div:nth-child(8) > details > div > div > div > div > div > div > div div[data-testid="stMarkdownContainer"] p {
                    font-size: 0.88rem;
                }

                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main > div.stAppViewBlockContainer > div > div > div > div:nth-child(8) > details {
                    margin-top: -1.8em; /* or any other unit */

                }
            </style>
            """
            st.markdown(css_body_container, unsafe_allow_html=True)
        
            # Sidebar - Filter by MD (with multiselect)
            md_options = ['All'] + dfMD['MD'].unique().tolist()  # Add 'All' to MD options
            selected_md = st.sidebar.multiselect('Select MD', md_options, default='All',key="7")
        
            # Filter MD only if 'All' is not selected
            if 'All' in selected_md or len(selected_md) == 0:
                filtered_df = dfMD
            else:
                filtered_df = dfMD[dfMD['MD'].isin(selected_md)]

            if not filtered_df.empty:
                months_options = ['All'] + filtered_df['MONTH'].unique().tolist()
                selected_months = st.sidebar.multiselect('Select MONTH', months_options, default='All',key="8")

                # Filter only if 'All' is not selected
                if 'All' not in selected_months and len(selected_months) > 0:
                    filtered_df = filtered_df[filtered_df['MONTH'].isin(selected_months)]

            css_body_container = f'''
            <style>
                [data-testid="stSidebar"] + section [data-testid="stVerticalBlock"] div:nth-of-type({1})
                [data-testid="stVerticalBlock"] {{background-color:#f1f1f1de}}
            </style>
            '''
            st.markdown(css_body_container,unsafe_allow_html=True)

            with st.expander(label="Key Metrics",expanded=True):
                with st.container(border= True):

                    if not filtered_df.empty:
                        timeframe_options = ['All'] + filtered_df['TIME FRAME'].unique().tolist() 
                        selected_timeframe = st.selectbox("Select Time Period:", timeframe_options, index=0,key="9")

                        # Filter only if 'All' is not selected
                        if selected_timeframe != 'All':
                            filtered_df = filtered_df[(filtered_df['TIME FRAME'] == selected_timeframe)]

                    col1,= st.columns(1)
                    if selected_md:
                        if len(selected_md) > 3:
                            display_md = f"{selected_md[0]}, {selected_md[1]},{selected_md[2]} ..."
                        else:
                            display_md = ", ".join(selected_md)
                        if ["All"] in selected_md:
                            display_md = "All"
                        col1.metric(f"Market Director:", display_md, delta = None)
                    else:
                        col1.metric(f"Market Director:", "-", delta = None)


                    if len(selected_md) == 0 and len(selected_months) == 0:
                        st.warning("No data to show. Please adjust the filters.")

                    else: 
                        col5, col6, col8, col9 = st.columns(4)
                        col5.info(f'Total ST: {commas_nd(filtered_df["ST CLICKS"].sum())}')
                        col6.info(f'ST Clicks Avg: {commas_nd(filtered_df["ST CLICKS"].mean())}')
                        col8.info(f'Boxes Sum: {commas_nd(filtered_df["BOXES"].sum())}')
                        col9.info(f'Boxes Avg: {commas_nd(filtered_df["BOXES"].mean())}')


                        col7,col13,col10,col11, col12, = st.columns(5)
                        col7.info(f'QPay Conv: {((filtered_df["BOXES"].sum() / filtered_df["QPAY"].sum())*100).round(2)}%')
                        
                        mean_value_col10 = (filtered_df['ACCESSORIES'].sum()/filtered_df['HOURS'].sum()).round(2)
                        col10.info(f"APH: ${mean_value_col10}")

                        mean_value_col11 = (filtered_df['ACCESSORIES'].sum()/filtered_df['BOXES'].sum()).round(2)
                        col11.info(f"APB: ${mean_value_col11}")
                        
                        mean_value_col12 = (filtered_df['BOXES'].sum()/filtered_df['HOURS'].sum()).round(2)
                        col12.info(f"BPH: {mean_value_col12}")

                        mean_value_col13 = ((filtered_df["BOXES"].sum() / filtered_df["ST CLICKS"].sum())*100).round(2)
                        col13.info(f'ST Conv: {mean_value_col13}%')


                        col14,col15,col18,col16,col17 = st.columns(5)

                        mean_value_col14 = ((filtered_df['ACCESSORIES'].sum()/filtered_df['ACCESSORY GOAL'].sum())*100).round(2)
                        col14.info(f"ACC % TGT: {mean_value_col14}%")

                        mean_value_col15 = ((filtered_df['BOXES'].sum()/filtered_df['BOXES GOALS'].sum())*100).round(2)
                        col15.info(f"PPD % TGT: {mean_value_col15}%")
                        
                        col18.info(f"BTS% / Boxes: {commas((filtered_df['BTS'].sum()/filtered_df['BOXES'].sum())*100)}%")
                        col16.info(f"Total 1K Days: {(filtered_df['1K Counts'].sum()).astype(int)}")
                        col17.info(f"1K Days Avg: {((filtered_df['1K Counts'].mean()).round(0)).astype(int)}")


            # Display filtered dataframe with selected MD, MARKET, DM, and TIME FRAME
            if len(selected_md) != 0 or len(selected_months) != 0:
                with st.expander("Show Table", expanded=False):
                    st.dataframe(filtered_df[main_cols_md], width=800)
            
        if selected_radio == "DM Wise":

            css_body_container = """
            <style>

                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main > div.stAppViewBlockContainer > div > div > div > div:nth-child(8) > details > div > div > div > div > div > div > div div[data-testid="stMarkdownContainer"] p {
                    font-size: 0.88rem;
                }

                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main > div.stAppViewBlockContainer > div > div > div > div:nth-child(8) > details {
                    margin-top: -1.8em; /* or any other unit */

                }
            </style>
            """
            st.markdown(css_body_container, unsafe_allow_html=True)
        
            # Sidebar - Filter by MD (with multiselect)
            dm_options = ['All'] + dfDM['DM'].unique().tolist()  # Add 'All' to MD options
            selected_dm = st.sidebar.multiselect('Select DM', dm_options, default='All',key="10")
        
            # Filter MD only if 'All' is not selected
            if 'All' in selected_dm or len(selected_dm) == 0:
                filtered_df = dfDM
            else:
                filtered_df = dfDM[dfDM['DM'].isin(selected_dm)]

            if not filtered_df.empty:
                months_options = ['All'] + filtered_df['MONTH'].unique().tolist()
                selected_months = st.sidebar.multiselect('Select MONTH', months_options, default='All',key="11")

                # Filter only if 'All' is not selected
                if 'All' not in selected_months and len(selected_months) > 0:
                    filtered_df = filtered_df[filtered_df['MONTH'].isin(selected_months)]

            css_body_container = f'''
            <style>
                [data-testid="stSidebar"] + section [data-testid="stVerticalBlock"] div:nth-of-type({1})
                [data-testid="stVerticalBlock"] {{background-color:#f1f1f1de}}
            </style>
            '''
            st.markdown(css_body_container,unsafe_allow_html=True)

            with st.expander(label="Key Metrics",expanded=True):
                with st.container(border= True):

                    if not filtered_df.empty:
                        timeframe_options = ['All'] + filtered_df['TIME FRAME'].unique().tolist() 
                        selected_timeframe = st.selectbox("Select Time Period:", timeframe_options, index=0,key="12")

                        # Filter only if 'All' is not selected
                        if selected_timeframe != 'All':
                            filtered_df = filtered_df[(filtered_df['TIME FRAME'] == selected_timeframe)]

                    col1,= st.columns(1)
                    if selected_dm:
                        if len(selected_dm) > 3:
                            display_dm = f"{selected_dm[0]}, {selected_dm[1]},{selected_dm[2]} ..."
                        else:
                            display_dm = ", ".join(selected_dm)
                        if ["All"] in selected_dm:
                            display_md = "All"
                        col1.metric(f"District Manager:", display_dm, delta = None)
                    else:
                        col1.metric(f"District Manager:", "-", delta = None)


                    if len(selected_dm) == 0 and len(selected_months) == 0:
                        st.warning("No data to show. Please adjust the filters.")

                    else: 
                        col5, col6, col8, col9 = st.columns(4)
                        col5.info(f'Total ST: {commas_nd(filtered_df["ST CLICKS"].sum())}')
                        col6.info(f'ST Clicks Avg: {commas_nd(filtered_df["ST CLICKS"].mean())}')
                        col8.info(f'Boxes Sum: {commas_nd(filtered_df["BOXES"].sum())}')
                        col9.info(f'Boxes Avg: {commas_nd(filtered_df["BOXES"].mean())}')


                        col7,col13,col10,col11, col12, = st.columns(5)
                        col7.info(f'QPay Conv: {((filtered_df["BOXES"].sum() / filtered_df["QPAY"].sum())*100).round(2)}%')
                        
                        mean_value_col10 = (filtered_df['ACCESSORIES'].sum()/filtered_df['HOURS'].sum()).round(2)
                        col10.info(f"APH: ${mean_value_col10}")

                        mean_value_col11 = (filtered_df['ACCESSORIES'].sum()/filtered_df['BOXES'].sum()).round(2)
                        col11.info(f"APB: ${mean_value_col11}")
                        
                        mean_value_col12 = (filtered_df['BOXES'].sum()/filtered_df['HOURS'].sum()).round(2)
                        col12.info(f"BPH: {mean_value_col12}")

                        mean_value_col13 = ((filtered_df["BOXES"].sum() / filtered_df["ST CLICKS"].sum())*100).round(2)
                        col13.info(f'ST Conv: {mean_value_col13}%')


                        col14,col15,col18,col16,col17 = st.columns(5)

                        mean_value_col14 = ((filtered_df['ACCESSORIES'].sum()/filtered_df['ACCESSORY GOAL'].sum())*100).round(2)
                        col14.info(f"ACC % TGT: {mean_value_col14}%")

                        mean_value_col15 = ((filtered_df['BOXES'].sum()/filtered_df['BOXES GOALS'].sum())*100).round(2)
                        col15.info(f"PPD % TGT: {mean_value_col15}%")
                        
                        col18.info(f"BTS% / Boxes: {commas((filtered_df['BTS'].sum()/filtered_df['BOXES'].sum())*100)}%")
                        col16.info(f"Total 1K Days: {(filtered_df['1K Counts'].sum()).astype(int)}")
                        col17.info(f"1K Days Avg: {((filtered_df['1K Counts'].mean()).round(0)).astype(int)}")


            # Display filtered dataframe with selected MD, MARKET, DM, and TIME FRAME
            if len(selected_dm) != 0 or len(selected_months) != 0:
                with st.expander("Show Table", expanded=False):
                    st.dataframe(filtered_df[main_cols_dm], width=800)
        
        if selected_radio == "Month Wise":
            # Sidebar - Filter by Months
            month_option = ['All'] + dfMon['MONTH'].unique().tolist()  # Add 'All' to MD options
            selected_month = st.sidebar.multiselect('Select Month', month_option, default='All',key="13")
        
            # Filter MD only if 'All' is not selected
            if 'All' in selected_month or len(selected_month) == 0:
                filtered_df = dfMon
            else:
                filtered_df = dfMon[dfMon['MONTH'].isin(selected_month)]

            css_body_container = """
            <style>
                [data-testid="stSidebar"] + section [data-testid="stVerticalBlock"] div:nth-of-type(1)
                [data-testid="stVerticalBlock"] {background-color: #f1f1f1de;}

                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main > div.stAppViewBlockContainer > div > div > div > div:nth-child(7) > details > div > div > div > div > div > div > div div[data-testid="stMarkdownContainer"] p {
                    font-size: 0.88rem;
                }

                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main > div.stAppViewBlockContainer > div > div > div > div:nth-child(7) > details {
                    margin-top: -0.8em; /* or any other unit */

                }
            </style>
            """
            st.markdown(css_body_container, unsafe_allow_html=True)

            with st.expander(label="Key Metrics",expanded=True):
                with st.container(border= True):

                    if not filtered_df.empty:
                        timeframe_options = ['All'] + filtered_df['TIME FRAME'].unique().tolist() 
                        selected_timeframe = st.selectbox("Select Time Period:", timeframe_options, index=0,key="14")

                        # Filter only if 'All' is not selected
                        if selected_timeframe != 'All':
                            filtered_df = filtered_df[(filtered_df['TIME FRAME'] == selected_timeframe)]

                    if len(selected_month) == 0 :
                        st.warning("No data to show. Please adjust the filters.")

                    else: 
                        col5, col6, col8, col9 = st.columns(4)
                        col5.info(f'Total ST: {commas_nd(filtered_df["ST CLICKS"].sum())}')
                        col6.info(f'ST Clicks Avg: {commas_nd(filtered_df["ST CLICKS"].mean())}')
                        col8.info(f'Boxes Sum: {commas_nd(filtered_df["BOXES"].sum())}')
                        col9.info(f'Boxes Avg: {commas_nd(filtered_df["BOXES"].mean())}')


                        col7,col13,col10,col11, col12, = st.columns(5)
                        col7.info(f'QPay Conv: {((filtered_df["BOXES"].sum() / filtered_df["QPAY"].sum())*100).round(2)}%')
                        
                        mean_value_col10 = (filtered_df['ACCESSORIES'].sum()/filtered_df['HOURS'].sum()).round(2)
                        col10.info(f"APH: ${mean_value_col10}")

                        mean_value_col11 = (filtered_df['ACCESSORIES'].sum()/filtered_df['BOXES'].sum()).round(2)
                        col11.info(f"APB: ${mean_value_col11}")
                        
                        mean_value_col12 = (filtered_df['BOXES'].sum()/filtered_df['HOURS'].sum()).round(2)
                        col12.info(f"BPH: {mean_value_col12}")

                        mean_value_col13 = ((filtered_df["BOXES"].sum() / filtered_df["ST CLICKS"].sum())*100).round(2)
                        col13.info(f'ST Conv: {mean_value_col13}%')


                        col14,col15,col18,col16,col17 = st.columns(5)

                        mean_value_col14 = ((filtered_df['ACCESSORIES'].sum()/filtered_df['ACCESSORY GOAL'].sum())*100).round(2)
                        col14.info(f"ACC % TGT: {mean_value_col14}%")

                        mean_value_col15 = ((filtered_df['BOXES'].sum()/filtered_df['BOXES GOALS'].sum())*100).round(2)
                        col15.info(f"PPD % TGT: {mean_value_col15}%")
                        
                        col18.info(f"BTS% / Boxes: {commas((filtered_df['BTS'].sum()/filtered_df['BOXES'].sum())*100)}%")
                        col16.info(f"Total 1K Days: {(filtered_df['1K Counts'].sum()).astype(int)}")
                        col17.info(f"1K Days Avg: {((filtered_df['1K Counts'].mean()).round(0)).astype(int)}")


            # Display filtered dataframe with selected MD, MARKET, DM, and TIME FRAME
            if len(selected_month) != 0 :
                with st.expander("Show Table", expanded=False):
                    st.dataframe(filtered_df[main_cols_mon], width=800)   
             
    elif selected == 'Data Visualization':
        st.write("Under-Development")
    
              
if selected2 == "Performance Bonus":
    st.title("Performance Bonus Dashboard")
    selected = option_menu(menu_title=None,options=["Data Record", "Data Visualization"],orientation='horizontal',
                        styles={
                            "nav-link": {"--hover-color": "#a42bad4b"},
                            "nav-link-selected": {"background-color": "#832a80"}
                            },key="7")

    if selected == "Data Record":
        
        st.sidebar.header('Please Filter here:')
        # Sidebar - Filter by MD (with multiselect)
        md_options = ['All'] + df1['MD'].unique().tolist()  # Add 'All' to MD options
        selected_md = st.sidebar.multiselect('Select MD', md_options, default='All',key="15")
    
        # Filter MD only if 'All' is not selected
        if 'All' in selected_md or len(selected_md) == 0:
            filtered_df = df1
        else:
            filtered_df = df1[df1['MD'].isin(selected_md)]

        # Ensure filtered_df is not empty before applying DM filter
        if not filtered_df.empty:
            dm_options = ['All'] + filtered_df['DM'].unique().tolist()  # Update DM options based on filtered MD data
            selected_dm = st.sidebar.multiselect('Select DM', dm_options, default='All',key="16")

            # Filter MARKET only if 'All' is not selected
            if 'All' not in selected_dm and len(selected_dm) > 0:
                filtered_df = filtered_df[filtered_df['DM'].isin(selected_dm)]

        # Ensure filtered_df is not empty before applying DM filter
        if not filtered_df.empty:
            MARKET_options = ['All'] + filtered_df['MARKET'].unique().tolist()  # Update MARKET options based on filtered DM data
            selected_MARKET = st.sidebar.multiselect('Select MARKET', MARKET_options, default='All',key="17")

            # Filter MARKET only if 'All' is not selected
            if 'All' not in selected_MARKET and len(selected_MARKET) > 0:
                filtered_df = filtered_df[filtered_df['MARKET'].isin(selected_MARKET)]

        # Ensure filtered_df is not empty before applying DM filter
        if not filtered_df.empty:
            Store_options = ['All'] + filtered_df['STORE'].unique().tolist()  # Update MARKET options based on filtered DM data
            selected_STORE = st.sidebar.multiselect('Select STORE', Store_options, default='All',key="18")

            # Filter MARKET only if 'All' is not selected
            if 'All' not in selected_STORE and len(selected_STORE) > 0:
                filtered_df = filtered_df[filtered_df['STORE'].isin(selected_STORE)]

        if not filtered_df.empty:
            months_options = ['All'] + filtered_df['MONTH'].unique().tolist()
            selected_months = st.sidebar.multiselect('Select MONTH', months_options, default='All',key="19")

            # Filter only if 'All' is not selected
            if 'All' not in selected_months and len(selected_months) > 0:
                filtered_df = filtered_df[filtered_df['MONTH'].isin(selected_months)]

        css_body_container = f'''
        <style>
            [data-testid="stSidebar"] + section [data-testid="stVerticalBlock"] div:nth-of-type({1})
            [data-testid="stVerticalBlock"] {{background-color:#f1f1f1de}}
        </style>
        '''
        st.markdown(css_body_container,unsafe_allow_html=True)

        with st.expander(label="Key Metrics",expanded=True):
            with st.container(border= True):

                if not filtered_df.empty:
                    timeframe_options = ['All'] + filtered_df['TIME FRAME'].unique().tolist() 
                    selected_timeframe = st.selectbox("Select Time Period:", timeframe_options, index=0,key="20")

                    # Filter only if 'All' is not selected
                    if selected_timeframe != 'All':
                        filtered_df = filtered_df[(filtered_df['TIME FRAME'] == selected_timeframe)]

                col1, col2= st.columns(2)
                if selected_md:
                    if len(selected_md) > 2:
                        display_md = f"{selected_md[0]}, {selected_md[1]} ..."
                    else:
                        display_md = ", ".join(selected_md)
                    if ["All"] in selected_md:
                        display_md = "All"
                    col1.metric(f"Market Director:", display_md, delta = None)
                else:
                    col1.metric(f"Market Director:", "-", delta = None)

                if selected_dm:
                    if len(selected_dm) > 2:
                        display_dm = f"{selected_dm[0]}, {selected_dm[1]} ..."
                    else:
                        display_dm = ", ".join(selected_dm)
                    if ["All"] in selected_dm:
                        display_md = "All"
                    col2.metric(f"District Manager:", display_dm, delta = None)
                else:
                    col2.metric(f"District Manager:", "-", delta = None)

                if len(selected_MARKET) == 0 and len(selected_dm) == 0 and len(selected_md) == 0 and len(selected_months) == 0:
                    st.warning("No data to show. Please adjust the filters.")

                else: 
                    col5, col6, col7, = st.columns(3)

                    mean_value_col5 = filtered_df["GROWTH % M"].mean().round(2)
                    col5.info(f'Growth AVG: {mean_value_col5}%')
                    
                    mean_value_col6 = filtered_df["95 ACT RET M"].mean().round(2)                        
                    col6.info(f'95 Act Ret AVG: {mean_value_col6}%')

                    mean_value_col7 = ((filtered_df["PB BONUS"].sum()/filtered_df["MIN EXPECTED"].sum())*100).round(2)
                    col7.info(f"PB Attainment:  {mean_value_col7}%")
                    
                    
                    col8,col9,col10 = st.columns(3)
                    
                    col8.info(f'PB Achieved: ${commas(filtered_df["PB BONUS"].sum())}')
                    col9.info(f'PB Available: ${commas(filtered_df["MAX AMOUNT"].sum())}')
                    col10.info(f'Missed Oppt: ${commas(filtered_df["MISSED OPPORTUNITIES"].sum())}')


        # Display filtered dataframe with selected MD, MARKET, DM, and TIME FRAME
        if len(selected_MARKET) != 0 or len(selected_dm) != 0 or len(selected_md) != 0 or len(selected_months) != 0:
            with st.expander("Show Table", expanded=False):
                st.dataframe(filtered_df[main_cols_pb], width=800)

    elif selected == 'Data Visualization':
        st.write("Under-Development")


if selected2 == "Express Leaderboard":
    st.title("Express Leaderboard Dashboard")
    selected = option_menu(menu_title=None,options=["Data Record", "Data Visualization"],orientation='horizontal',
                        styles={
                            "nav-link": {"--hover-color": "#a42bad4b"},
                            "nav-link-selected": {"background-color": "#832a80"}
                            },key="21")

    if selected == "Data Record":

        css_body_container = f'''
        <style>
            [data-testid="stSidebar"] + section [data-testid="stVerticalBlock"] div:nth-of-type({1})
            [data-testid="stVerticalBlock"] {{background-color:#f1f1f1de}}
        </style>
        '''
        st.markdown(css_body_container,unsafe_allow_html=True)

        #with st.container(border= True):
        months_options = lst
        last_month = lst[-1]
        ind = lst.index(last_month)
        selected_months = st.selectbox("Select Month:", months_options, index=ind)
        
        st.sidebar.header('Please Filter here:')
        # Sidebar - Filter by MD (with multiselect)
        md_options = ['All'] + data[selected_months]["MD"].unique().tolist()  # Add 'All' to MD options
        selected_md = st.sidebar.multiselect('Select MD', md_options, default='All')
    
        # Filter MD only if 'All' is not selected
        if 'All' in selected_md or len(selected_md) == 0:
            filtered_df = data[selected_months]
        else:
            filtered_df = data[selected_months][data[selected_months]['MD'].isin(selected_md)]
        
        # Ensure filtered_df is not empty before applying DM filter
        if not filtered_df.empty:
            dm_options = ['All'] + filtered_df['DM'].unique().tolist()  # Update DM options based on filtered MD data
            selected_dm = st.sidebar.multiselect('Select DM', dm_options, default='All')

            # Filter MARKET only if 'All' is not selected
            if 'All' not in selected_dm and len(selected_dm) > 0:
                filtered_df = filtered_df[filtered_df['DM'].isin(selected_dm)]

        # Ensure filtered_df is not empty before applying Market filter
        if not filtered_df.empty:
            MARKET_options = ['All'] + filtered_df['Market'].unique().tolist()  # Update MARKET options based on filtered DM data
            selected_MARKET = st.sidebar.multiselect('Select Market', MARKET_options, default='All')

            # Filter MARKET only if 'All' is not selected
            if 'All' not in selected_MARKET and len(selected_MARKET) > 0:
                filtered_df = filtered_df[filtered_df['Market'].isin(selected_MARKET)]


        css_body_container = f'''
        <style>
            [data-testid="stSidebar"] + section [data-testid="stVerticalBlock"] div:nth-of-type({1})
            [data-testid="stVerticalBlock"] {{background-color:#f1f1f1de}}
        </style>
        '''
        st.markdown(css_body_container,unsafe_allow_html=True)

        with st.expander(label="Key Metrics",expanded=True):
            with st.container(border= True):

                col1, col2= st.columns(2)
                if selected_md:
                    if len(selected_md) > 2:
                        display_md = f"{selected_md[0]}, {selected_md[1]} ..."
                    else:
                        display_md = ", ".join(selected_md)
                    if ["All"] in selected_md:
                        display_md = "All"
                    col1.metric(f"Market Director:", display_md, delta = None)
                else:
                    col1.metric(f"Market Director:", "-", delta = None)

                if selected_dm:
                    if len(selected_dm) > 2:
                        display_dm = f"{selected_dm[0]}, {selected_dm[1]} ..."
                    else:
                        display_dm = ", ".join(selected_dm)
                    if ["All"] in selected_dm:
                        display_md = "All"
                    col2.metric(f"District Manager:", display_dm, delta = None)
                else:
                    col2.metric(f"District Manager:", "-", delta = None)
                
                def display_avg_cards(filtered_df):
                    cols_per_row = 5
                    column_names = filtered_df.columns.tolist()
                    num_cols = len(column_names)
                    
                    for i in range(0, num_cols, cols_per_row):

                        col_names = [f'col{j+1}' for j in range(min(cols_per_row, num_cols - i))]
                        col_vars = st.columns(len(col_names))
                        
                        for j, col_name in enumerate(column_names[i:i + cols_per_row]):
                            avg_value = filtered_df[col_name].mean()
                            col_vars[j].info(f'{col_name} Avg: {commas(avg_value)}')

                display_avg_cards(filtered_df.iloc[:, 6:])

        if len(selected_MARKET) == 0 and len(selected_dm) == 0 and len(selected_md) == 0:
            st.warning("No data to show. Please adjust the filters.")

        else: 
            with st.expander("Show Table", expanded=False):
                st.dataframe(filtered_df, width=800)

    elif selected == 'Data Visualization':      
        st.write("Under-Development")

if selected2 == "Audit Tracker Q3":
    st.title("Audit Tracker Q3 Dashboard")
    selected = option_menu(menu_title=None,options=["Data Record", "Data Visualization"],orientation='horizontal',
                        styles={
                            "nav-link": {"--hover-color": "#a42bad4b"},
                            "nav-link-selected": {"background-color": "#832a80"}
                            },key="22")

    if selected == "Data Record":
        
        st.sidebar.header('Please Filter here:')
        # Sidebar - Filter by MD (with multiselect)
        md_options = ['All'] + df2['MD'].unique().tolist()  # Add 'All' to MD options
        selected_md = st.sidebar.multiselect('Select MD', md_options, default='All',key="23")
    
        # Filter MD only if 'All' is not selected
        if 'All' in selected_md or len(selected_md) == 0:
            filtered_df = df2
        else:
            filtered_df = df2[df2['MD'].isin(selected_md)]

        # Ensure filtered_df is not empty before applying DM filter
        if not filtered_df.empty:
            dm_options = ['All'] + filtered_df['DM'].unique().tolist()  # Update DM options based on filtered MD data
            selected_dm = st.sidebar.multiselect('Select DM', dm_options, default='All',key="24")

            # Filter MARKET only if 'All' is not selected
            if 'All' not in selected_dm and len(selected_dm) > 0:
                filtered_df = filtered_df[filtered_df['DM'].isin(selected_dm)]

        # Ensure filtered_df is not empty before applying DM filter
        if not filtered_df.empty:
            MARKET_options = ['All'] + filtered_df['Market'].unique().tolist()  # Update MARKET options based on filtered DM data
            selected_MARKET = st.sidebar.multiselect('Select Market', MARKET_options, default='All',key="25")

            # Filter MARKET only if 'All' is not selected
            if 'All' not in selected_MARKET and len(selected_MARKET) > 0:
                filtered_df = filtered_df[filtered_df['Market'].isin(selected_MARKET)]

        # Ensure filtered_df is not empty before applying DM filter
        if not filtered_df.empty:
            Store_options = ['All'] + filtered_df['Store'].unique().tolist()  # Update MARKET options based on filtered DM data
            selected_STORE = st.sidebar.multiselect('Select Store', Store_options, default='All',key="26")

            # Filter MARKET only if 'All' is not selected
            if 'All' not in selected_STORE and len(selected_STORE) > 0:
                filtered_df = filtered_df[filtered_df['Store'].isin(selected_STORE)]

        css_body_container = f'''
        <style>
            [data-testid="stSidebar"] + section [data-testid="stVerticalBlock"] div:nth-of-type({1})
            [data-testid="stVerticalBlock"] {{background-color:#f1f1f1de}}
        </style>
        '''
        st.markdown(css_body_container,unsafe_allow_html=True)

        with st.expander(label="Key Metrics",expanded=True):
            with st.container(border= True):

                if not filtered_df.empty:
                    Status_options = ['All'] + filtered_df['Status'].unique().tolist() 
                    selected_Status = st.selectbox("Select Status:", Status_options, index=0,key="27")

                    # Filter only if 'All' is not selected
                    if selected_Status != 'All':
                        filtered_df = filtered_df[(filtered_df['Status'] == selected_Status)]

                col1, col2= st.columns(2)
                if selected_md:
                    if len(selected_md) > 2:
                        display_md = f"{selected_md[0]}, {selected_md[1]} ..."
                    else:
                        display_md = ", ".join(selected_md)
                    if ["All"] in selected_md:
                        display_md = "All"
                    col1.metric(f"Market Director:", display_md, delta = None)
                else:
                    col1.metric(f"Market Director:", "-", delta = None)

                if selected_dm:
                    if len(selected_dm) > 2:
                        display_dm = f"{selected_dm[0]}, {selected_dm[1]} ..."
                    else:
                        display_dm = ", ".join(selected_dm)
                    if ["All"] in selected_dm:
                        display_md = "All"
                    col2.metric(f"District Manager:", display_dm, delta = None)
                else:
                    col2.metric(f"District Manager:", "-", delta = None)

                if len(selected_STORE) == 0 or 'All' in selected_STORE:
                    st.warning("No Score to show. Please select a Store.")

                else: 
                    col8, = st.columns(1)
                    col8.info(f'"{selected_STORE[0]}" Score: {((filtered_df["Score_C"].sum())*100).round(2)}%')

        # Display filtered dataframe with selected MD, MARKET, DM, and TIME FRAME
        if len(selected_MARKET) != 0 or len(selected_dm) != 0 or len(selected_md) != 0 or len(selected_STORE) != 0:
            with st.expander("Show Table", expanded=False):
                st.dataframe(filtered_df[main_cols_audit], width=800)

    elif selected == 'Data Visualization':
        st.write("Under-Development")

if selected2 == "Phone's Sales":
    st.title("Performance Dashboard")
    selected = option_menu(menu_title=None,options=["Data Record", "Data Visualization"],orientation='horizontal',
                        styles={
                            "nav-link": {"--hover-color": "#a42bad4b"},
                            "nav-link-selected": {"background-color": "#832a80"}
                            },key="28")

    if selected == "Data Record":

        radio_style = '''
        <style>
        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stSidebar > div > div > div > div > div > div > div:nth-child(2) > div > label > div > p {

            font-family: "Source Sans Pro", sans-serif;
            font-weight: 600 !important;
            font-size: 1.25rem !important;
            color: #31333f !important;}

        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stSidebar > div > div > div > div > div > div > div:nth-child(2) > div > div {
            border: 1.75px solid lightgrey; /* Light grey border */
            border-radius: 15px; /* Rounded corners */
            padding: 12px; /* Add some padding */
            background-color: #f9f9f9; /* Optional: light background for contrast */
            box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1) !important; /* Subtle shadow for a softer look */}

        #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stSidebar > div > div > div > div > div > div > div:nth-child(2) > div > div > label > div:first-child {
            background-color: #832a80 !important;}    
        </style>
        '''
        st.markdown(radio_style, unsafe_allow_html=True)

        select_box_opts = ["Android","iPhones"]
        selected_radio = st.sidebar.radio(
            "Please Filter here:",
            options=select_box_opts,
            format_func=lambda x: x,
            horizontal=True,key="321"
        )
        
        if selected_radio == "Android":

            css_body_container = """
            <style>

                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main > div.stAppViewBlockContainer > div > div > div > div:nth-child(8) > details > div > div > div > div > div > div > div div[data-testid="stMarkdownContainer"] p {
                    font-size: 0.88rem;
                }

                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main > div.stAppViewBlockContainer > div > div > div > div:nth-child(8) > details {
                    margin-top: -1.8em; /* or any other unit */

                }
            </style>
            """
            st.markdown(css_body_container, unsafe_allow_html=True)

            # Sidebar - Filter by MD (with multiselect)
            md_options = ['All'] + dfAnd['MD'].unique().tolist()  # Add 'All' to MD options
            selected_md = st.sidebar.multiselect('Select MD', md_options, default='All',key="29")
        
            # Filter MD only if 'All' is not selected
            if 'All' in selected_md or len(selected_md) == 0:
                filtered_df = dfAnd
            else:
                filtered_df = dfAnd[dfAnd['MD'].isin(selected_md)]

            # Ensure filtered_df is not empty before applying DM filter
            if not filtered_df.empty:
                dm_options = ['All'] + filtered_df['DM'].unique().tolist()  # Update DM options based on filtered MD data
                selected_dm = st.sidebar.multiselect('Select DM', dm_options, default='All',key="30")
                # Filter MARKET only if 'All' is not selected
                if 'All' not in selected_dm and len(selected_dm) > 0:
                    filtered_df = filtered_df[filtered_df['DM'].isin(selected_dm)]

            if not filtered_df.empty:
                months_options = ['All'] + filtered_df['MONTH'].unique().tolist()
                selected_months = st.sidebar.multiselect('Select MONTH', months_options, default='All',key="31")

                # Filter only if 'All' is not selected
                if 'All' not in selected_months and len(selected_months) > 0:
                    filtered_df = filtered_df[filtered_df['MONTH'].isin(selected_months)]

            # Ensure filtered_df is not empty before applying DM filter
            if not filtered_df.empty:
                MARKET_options = ['All'] + filtered_df['MARKET'].unique().tolist()  # Update MARKET options based on filtered DM data
                selected_MARKET = st.sidebar.multiselect('Select MARKET', MARKET_options, default='All',key="32")

                # Filter MARKET only if 'All' is not selected
                if 'All' not in selected_MARKET and len(selected_MARKET) > 0:
                    filtered_df = filtered_df[filtered_df['MARKET'].isin(selected_MARKET)]

            # Ensure filtered_df is not empty before applying DM filter
            if not filtered_df.empty:
                Store_options = ['All'] + filtered_df['STORE'].unique().tolist()  # Update MARKET options based on filtered DM data
                selected_STORE = st.sidebar.multiselect('Select STORE', Store_options, default='All',key="33")

                # Filter MARKET only if 'All' is not selected
                if 'All' not in selected_STORE and len(selected_STORE) > 0:
                    filtered_df = filtered_df[filtered_df['STORE'].isin(selected_STORE)]

            # Ensure filtered_df is not empty before applying DM filter
            if not filtered_df.empty:
                model_options = ['All'] + filtered_df['MODEL'].unique().tolist()  # Update MARKET options based on filtered DM data
                selected_model = st.sidebar.multiselect('Select MODEL', model_options, default='All',key="34")

                # Filter MARKET only if 'All' is not selected
                if 'All' not in selected_model and len(selected_model) > 0:
                    filtered_df = filtered_df[filtered_df['MODEL'].isin(selected_model)]


            css_body_container = f'''
            <style>
                [data-testid="stSidebar"] + section [data-testid="stVerticalBlock"] div:nth-of-type({1})
                [data-testid="stVerticalBlock"] {{background-color:#f1f1f1de}}
            </style>
            '''
            st.markdown(css_body_container,unsafe_allow_html=True)

            with st.expander(label="Key Metrics",expanded=True):
                with st.container(border= True):

                    if not filtered_df.empty:
                        timeframe_options = ['All'] + filtered_df['TIME FRAME'].unique().tolist() 
                        selected_timeframe = st.selectbox("Select Time Period:", timeframe_options, index=0,key="35")

                        # Filter only if 'All' is not selected
                        if selected_timeframe != 'All':
                            filtered_df = filtered_df[(filtered_df['TIME FRAME'] == selected_timeframe)]

                    col1, col2= st.columns(2)
                    if selected_md:
                        if len(selected_md) > 2:
                            display_md = f"{selected_md[0]}, {selected_md[1]} ..."
                        else:
                            display_md = ", ".join(selected_md)
                        if ["All"] in selected_md:
                            display_md = "All"
                        col1.metric(f"Market Director:", display_md, delta = None)
                    else:
                        col1.metric(f"Market Director:", "-", delta = None)

                    if selected_dm:
                        if len(selected_dm) > 2:
                            display_dm = f"{selected_dm[0]}, {selected_dm[1]} ..."
                        else:
                            display_dm = ", ".join(selected_dm)
                        if ["All"] in selected_dm:
                            display_md = "All"
                        col2.metric(f"District Manager:", display_dm, delta = None)
                    else:
                        col2.metric(f"District Manager:", "-", delta = None)

                    if len(selected_MARKET) == 0 and len(selected_model) == 0 and len(selected_dm) == 0 and len(selected_md) == 0 and len(selected_months) == 0:
                        st.warning("No data to show. Please adjust the filters.")

                    else: 
                        col50,col5 = st.columns(2)
                        col50.info(f'Average Price: {commas(filtered_df["AVERAGE PRICE"].mean())}')
                        col5.info(f'Quantity: {commas_nd(filtered_df["QUANTITY"].sum())}')

            # Display filtered dataframe with selected MD, MARKET, DM, and TIME FRAME
            if len(selected_MARKET) != 0 or len(selected_model) != 0 or len(selected_dm) != 0 or len(selected_md) != 0 or len(selected_months) != 0:
                with st.expander("Show Table", expanded=False):
                    st.dataframe(filtered_df[main_cols_and], width=800)
            
        if selected_radio == "iPhones":

            css_body_container = """
            <style>

                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main > div.stAppViewBlockContainer > div > div > div > div:nth-child(8) > details > div > div > div > div > div > div > div div[data-testid="stMarkdownContainer"] p {
                    font-size: 0.88rem;
                }

                #root > div:nth-child(1) > div.withScreencast > div > div > div > section.stAppViewMain.main > div.stAppViewBlockContainer > div > div > div > div:nth-child(8) > details {
                    margin-top: -1.8em; /* or any other unit */

                }
            </style>
            """
            st.markdown(css_body_container, unsafe_allow_html=True)

            # Sidebar - Filter by MD (with multiselect)
            md_options = ['All'] + dfAnd['MD'].unique().tolist()  # Add 'All' to MD options
            selected_md = st.sidebar.multiselect('Select MD', md_options, default='All',key="36")
        
            # Filter MD only if 'All' is not selected
            if 'All' in selected_md or len(selected_md) == 0:
                filtered_df = dfIp
            else:
                filtered_df = dfIp[dfIp['MD'].isin(selected_md)]

            # Ensure filtered_df is not empty before applying DM filter
            if not filtered_df.empty:
                dm_options = ['All'] + filtered_df['DM'].unique().tolist()  # Update DM options based on filtered MD data
                selected_dm = st.sidebar.multiselect('Select DM', dm_options, default='All',key="37")
                # Filter MARKET only if 'All' is not selected
                if 'All' not in selected_dm and len(selected_dm) > 0:
                    filtered_df = filtered_df[filtered_df['DM'].isin(selected_dm)]

            if not filtered_df.empty:
                months_options = ['All'] + filtered_df['MONTH'].unique().tolist()
                selected_months = st.sidebar.multiselect('Select MONTH', months_options, default='All',key="38")

                # Filter only if 'All' is not selected
                if 'All' not in selected_months and len(selected_months) > 0:
                    filtered_df = filtered_df[filtered_df['MONTH'].isin(selected_months)]

            # Ensure filtered_df is not empty before applying DM filter
            if not filtered_df.empty:
                MARKET_options = ['All'] + filtered_df['MARKET'].unique().tolist()  # Update MARKET options based on filtered DM data
                selected_MARKET = st.sidebar.multiselect('Select MARKET', MARKET_options, default='All',key="39")

                # Filter MARKET only if 'All' is not selected
                if 'All' not in selected_MARKET and len(selected_MARKET) > 0:
                    filtered_df = filtered_df[filtered_df['MARKET'].isin(selected_MARKET)]

            # Ensure filtered_df is not empty before applying DM filter
            if not filtered_df.empty:
                Store_options = ['All'] + filtered_df['STORE'].unique().tolist()  # Update MARKET options based on filtered DM data
                selected_STORE = st.sidebar.multiselect('Select STORE', Store_options, default='All',key="40")

                # Filter MARKET only if 'All' is not selected
                if 'All' not in selected_STORE and len(selected_STORE) > 0:
                    filtered_df = filtered_df[filtered_df['STORE'].isin(selected_STORE)]

            # Ensure filtered_df is not empty before applying DM filter
            if not filtered_df.empty:
                model_options = ['All'] + filtered_df['MODEL'].unique().tolist()  # Update MARKET options based on filtered DM data
                selected_model = st.sidebar.multiselect('Select MODEL', model_options, default='All',key="41")

                # Filter MARKET only if 'All' is not selected
                if 'All' not in selected_model and len(selected_model) > 0:
                    filtered_df = filtered_df[filtered_df['MODEL'].isin(selected_model)]


            css_body_container = f'''
            <style>
                [data-testid="stSidebar"] + section [data-testid="stVerticalBlock"] div:nth-of-type({1})
                [data-testid="stVerticalBlock"] {{background-color:#f1f1f1de}}
            </style>
            '''
            st.markdown(css_body_container,unsafe_allow_html=True)

            with st.expander(label="Key Metrics",expanded=True):
                with st.container(border= True):

                    if not filtered_df.empty:
                        timeframe_options = ['All'] + filtered_df['TIME FRAME'].unique().tolist() 
                        selected_timeframe = st.selectbox("Select Time Period:", timeframe_options, index=0,key="42")

                        # Filter only if 'All' is not selected
                        if selected_timeframe != 'All':
                            filtered_df = filtered_df[(filtered_df['TIME FRAME'] == selected_timeframe)]

                    col1, col2= st.columns(2)
                    if selected_md:
                        if len(selected_md) > 2:
                            display_md = f"{selected_md[0]}, {selected_md[1]} ..."
                        else:
                            display_md = ", ".join(selected_md)
                        if ["All"] in selected_md:
                            display_md = "All"
                        col1.metric(f"Market Director:", display_md, delta = None)
                    else:
                        col1.metric(f"Market Director:", "-", delta = None)

                    if selected_dm:
                        if len(selected_dm) > 2:
                            display_dm = f"{selected_dm[0]}, {selected_dm[1]} ..."
                        else:
                            display_dm = ", ".join(selected_dm)
                        if ["All"] in selected_dm:
                            display_md = "All"
                        col2.metric(f"District Manager:", display_dm, delta = None)
                    else:
                        col2.metric(f"District Manager:", "-", delta = None)

                    if len(selected_MARKET) == 0 and len(selected_model) == 0 and len(selected_dm) == 0 and len(selected_md) == 0 and len(selected_months) == 0:
                        st.warning("No data to show. Please adjust the filters.")

                    else: 
                        col50,col5 = st.columns(2)
                        col50.info(f'Average Price: {commas(filtered_df["AVERAGE PRICE"].mean())}')
                        col5.info(f'Quantity: {commas_nd(filtered_df["QUANTITY"].sum())}')

            # Display filtered dataframe with selected MD, MARKET, DM, and TIME FRAME
            if len(selected_MARKET) != 0 or len(selected_model) != 0 or len(selected_dm) != 0 or len(selected_md) != 0 or len(selected_months) != 0:
                with st.expander("Show Table", expanded=False):
                    st.dataframe(filtered_df[main_cols_ip], width=800)


if selected2 == "Hiring YTD":
        st.title("HIRING YTD Dashboard")
        selected = option_menu(menu_title=None,options=["Data Record", "Data Visualization"],orientation='horizontal',
                            styles={
                                "nav-link": {"--hover-color": "#a42bad4b"},
                                "nav-link-selected": {"background-color": "#832a80"}
                                },key="58")

        if selected == "Data Record":
            st.sidebar.header('Please Filter here:')
            # Sidebar - Filter by DM (with multiselect)
            dm_options = ['All'] + dfH['HIRING MANAGER'].unique().tolist()  # Add 'All' to MD options
            selected_dm = st.sidebar.multiselect('Select DM', dm_options, default='All',key="59")
        
            # Filter MD only if 'All' is not selected
            if 'All' in selected_dm or len(selected_dm) == 0:
                filtered_df = dfH
            else:
                filtered_df = dfH[dfH['HIRING MANAGER'].isin(selected_dm)]

            # Ensure filtered_df is not empty before applying DM filter
            if not filtered_df.empty:
                MARKET_options = ['All'] + filtered_df['MARKET'].unique().tolist()  # Update MARKET options based on filtered DM data
                selected_MARKET = st.sidebar.multiselect('Select Market', MARKET_options, default='All',key="60")

                # Filter MARKET only if 'All' is not selected
                if 'All' not in selected_MARKET and len(selected_MARKET) > 0:
                    filtered_df = filtered_df[filtered_df['MARKET'].isin(selected_MARKET)]

            # Ensure filtered_df is not empty before applying DM filter
            if not filtered_df.empty:
                month_options = ['All'] + filtered_df['MONTH'].unique().tolist()  # Update MARKET options based on filtered DM data
                selected_month = st.sidebar.multiselect('Select MONTH', month_options, default='All',key="61")

                # Filter MARKET only if 'All' is not selected
                if 'All' not in selected_month and len(selected_month) > 0:
                    filtered_df = filtered_df[filtered_df['MONTH'].isin(selected_month)]

            css_body_container = f'''
            <style>
                [data-testid="stSidebar"] + section [data-testid="stVerticalBlock"] div:nth-of-type({1})
                [data-testid="stVerticalBlock"] {{background-color:#f1f1f1de}}
            </style>
            '''
            st.markdown(css_body_container,unsafe_allow_html=True)

            with st.expander(label="Key Metrics",expanded=True):
                with st.container(border= True):

                    #if not filtered_df.empty:
                     #   Status_options = ['All'] + filtered_df['Status'].unique().tolist() 
                      #  selected_Status = st.selectbox("Select Status:", Status_options, index=0,key="62")

                        # Filter only if 'All' is not selected
                       # if selected_Status != 'All':
                        #    filtered_df = filtered_df[(filtered_df['Status'] == selected_Status)]

                    col1, col2= st.columns(2)
                    if selected_dm:
                        if len(selected_dm) > 2:
                            display_dm = f"{selected_dm[0]}, {selected_dm[1]} ..."
                        else:
                            display_dm = ", ".join(selected_dm)
                        if ["All"] in selected_dm:
                            display_dm = "All"
                        col1.metric(f"District Manager:", display_dm, delta = None)
                    else:
                        col1.metric(f"District Manager:", "-", delta = None)

                    if selected_MARKET:
                        if len(selected_MARKET) > 2:
                            display_market = f"{selected_MARKET[0]}, {selected_MARKET[1]} ..."
                        else:
                            display_market = ", ".join(selected_MARKET)
                        if ["All"] in selected_MARKET:
                            display_md = "All"
                        col2.metric(f"Market:", display_market, delta = None)
                    else:
                        col2.metric(f"Market:", "-", delta = None)

                    if len(selected_dm) == 0 | len(selected_MARKET) == 0 :
                        st.warning("No Data to show. Please adjust filters.")

                    else: 
                        col8, = st.columns(1)
                        col8.info(f'Total Avg of Hiring: {((filtered_df["AVERAGE OF HIRING"].mean())).round(2)}')

            # Display filtered dataframe with selected MD, MARKET, DM, and TIME FRAME
            if len(selected_MARKET) != 0 or len(selected_dm) != 0 or len(selected_month) != 0:
                with st.expander("Show Table", expanded=False):
                    st.dataframe(filtered_df, width=800)
