import pandas as pd
import streamlit as st
import numpy as np
from streamlit_option_menu import option_menu 
import plotly.graph_objects as go
from datetime import datetime, timedelta
from streamlit_extras.metric_cards import style_metric_cards
import base64
import time
from streamlit_js_eval import streamlit_js_eval
from streamlit.components.v1 import components
import streamlit.components.v1 as components
from streamlit_javascript import st_javascript


# Load the Excel data
df = pd.read_excel("jun-jul.xlsx", sheet_name='Sheet1', header=0)

cols = ['ST Clicks', 'Boxes', 'Accessories', 'Hours', 'QPay', 'BPH', 'APH',
       'APB', 'QPay Conv', 'ST Conv', 'Retention']
for i in cols: 
    df[i] = pd.to_numeric(df[i], errors='coerce')

df.rename(columns={
    "QPay Conv": "QPay (%)",
    "ST Conv": "ST (%)",
    "Retention": "Retention (%)"
}, inplace=True)

df['Month'] = pd.to_datetime(df['Month'])

# Create an empty list to store counts
month_counts = []

# Group the data by the 'Month' column
groups = df.groupby(df['Month'].dt.to_period('M'))

# Loop through each group and assign counts manually
for name, group in groups:
    count = range(1, len(group) + 1)  # Create a sequence of numbers from 1 to the length of the group
    month_counts.extend(count)  # Extend the list with the sequence

# Assign the month counts back to the dataframe
df['Month_Count'] = month_counts


# Main columns to display
main_cols = ["Time Frame", 'Market', 'Store', 'MD', 'DM','ST Clicks', 'Boxes', 'Accessories', 
             'Hours', 'QPay', 'BPH', 'APH','APB', 'QPay (%)', 'ST (%)', 
             'Retention (%)', 'Month_Count']


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
    </style>
    '''
    st.markdown(sidebar_style, unsafe_allow_html=True)

style_sidebar_multiselect()

with st.sidebar:
    selected2 = option_menu("Xclusive Trading Inc.", ["Home", 'Additional Pages'], 
        icons=['house', 'gear'], menu_icon="cast", default_index=0,
        styles={"nav-link": {"--hover-color": "#a42bad4b"},
                "nav-link-selected": {"background-color": "#832a80"}
                }) # #a52bad
    
if selected2 == "Home":
    st.title("Performance Dashboard")
    selected = option_menu(menu_title=None,options=["Data Record", "Data Visualization"],orientation='horizontal',
                        styles={
                            "nav-link": {"--hover-color": "#a42bad4b"},
                            "nav-link-selected": {"background-color": "#832a80"}
                            })

    if selected == "Data Record":
        
        st.sidebar.header('Please Filter here:')
        # Sidebar - Filter by MD (with multiselect)
        md_options = ['All'] + df['MD'].unique().tolist()  # Add 'All' to MD options
        selected_md = st.sidebar.multiselect('Select MD', md_options, default='All')
       
        # Filter MD only if 'All' is not selected
        if 'All' in selected_md or len(selected_md) == 0:
            filtered_df = df
        else:
            filtered_df = df[df['MD'].isin(selected_md)]

        # Ensure filtered_df is not empty before applying DM filter
        if not filtered_df.empty:
            dm_options = ['All'] + filtered_df['DM'].unique().tolist()  # Update DM options based on filtered MD data
            selected_dm = st.sidebar.multiselect('Select DM', dm_options, default='All')

            # Filter Market only if 'All' is not selected
            if 'All' not in selected_dm and len(selected_dm) > 0:
                filtered_df = filtered_df[filtered_df['DM'].isin(selected_dm)]

        # Ensure filtered_df is not empty before applying DM filter
        if not filtered_df.empty:
            market_options = ['All'] + filtered_df['Market'].unique().tolist()  # Update Market options based on filtered DM data
            selected_market = st.sidebar.multiselect('Select Market', market_options, default='All')

            # Filter Market only if 'All' is not selected
            if 'All' not in selected_market and len(selected_market) > 0:
                filtered_df = filtered_df[filtered_df['Market'].isin(selected_market)]

        css_body_container = f'''
        <style>
            [data-testid="stSidebar"] + section [data-testid="stVerticalBlock"] div:nth-of-type({1})
            [data-testid="stVerticalBlock"] {{background-color:#f1f1f1de}}
        </style>
        '''
        st.markdown(css_body_container,unsafe_allow_html=True)

        def commas(number):
            return f"{number:,.1f}"
        def commas_nd(number):
            return f"{number:,.0f}"

        with st.expander(label="Key Metrics",expanded=True):
            with st.container(border= True):

                if not filtered_df.empty:
                    
                    timeframe_options = ['All'] + filtered_df['Time Frame'].unique().tolist()
                    selected_timeframe = st.selectbox("Select Time Period:", timeframe_options, index=0)

                    # Filter only if 'All' is not selected
                    if selected_timeframe != 'All':
                        filtered_df = filtered_df[filtered_df['Time Frame'] == selected_timeframe]

                col1, col2= st.columns(2)
                if selected_md:
                    if len(selected_md) > 2:
                        display_md = f"{selected_md[0]}, {selected_md[1]} ..."
                    else:
                        display_md = ", ".join(selected_md)
                    if ["All"] in selected_md:
                        display_md = "All"
                    col1.metric(f"Managing Director:", display_md, delta = None)
                else:
                    col1.metric(f"Managing Director:", "-", delta = None)

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

                if len(selected_market) == 0 and len(selected_dm) == 0 and len(selected_md) == 0:
                    st.warning("No data to show. Please adjust the filters.")

                else: 
                    col5, col6, col7,  = st.columns(3)

                    col5.info(f'ST Clicks Sum: {commas_nd(filtered_df["ST Clicks"].sum())}')
                    col6.info(f'ST Clicks Avg: {commas_nd(filtered_df["ST Clicks"].mean())}')
                    col7.info(f'QPay Conv: {((filtered_df["Boxes"].sum() / filtered_df["QPay"].sum())*100).round(2)} %')
                    
                    col8,col9, col10, = st.columns(3)

                    col8.info(f"APH: $ {(filtered_df['Accessories'].sum()/filtered_df['Hours'].sum()).round(2)}")
                    col9.info(f"APB: $ {(filtered_df['Accessories'].sum()/filtered_df['Boxes'].sum()).round(2)}")
                    col10.info(f"BPH: {(filtered_df['Boxes'].sum()/filtered_df['Hours'].sum()).round(2)}")

        
        # Display filtered dataframe with selected MD, Market, DM, and Time Frame
        if len(selected_market) != 0 or len(selected_dm) != 0 or len(selected_md) != 0:
            with st.expander("Show Table", expanded=False):
                st.dataframe(filtered_df[main_cols], width=800)

    elif selected == 'Data Visualization':
        # Filter for 'HOUSTON' in the 'Market' column
        houston_data = df[df['Market'] == 'HOUSTON']

        # Filter to include only July (assuming Month column is a datetime type)
        houston_july = houston_data[houston_data['Month'].dt.month == 7]

        # Interpolate NaN values in 'ST Clicks' column for smooth plotting
        houston_july['ST Clicks Interpolated'] = houston_july['ST Clicks'].interpolate()

        # Identify NaN values in the original 'ST Clicks' column
        nan_indices = houston_july['ST Clicks'].isna()

        # Create the Plotly figure
        fig = go.Figure()

        # Plot the actual data (non-NaN points)
        fig.add_trace(go.Scatter(
            x=houston_july['Month_Count'],
            y=houston_july['ST Clicks'],
            mode='lines+markers',
            name='Actual Data',
            line=dict(color='blue'),
            marker=dict(symbol='circle')
        ))

        # Plot the interpolated sections as red dotted lines (without markers)
        added_null_label = False

        for i in range(1, len(houston_july)):
            if nan_indices.iloc[i] or nan_indices.iloc[i - 1]:
                label = 'Null Value' if not added_null_label else ""
                show_legend = not added_null_label  # Show the legend only for the first instance
                
                fig.add_trace(go.Scatter(
                    x=houston_july['Month_Count'].iloc[i-1:i+1],
                    y=houston_july['ST Clicks Interpolated'].iloc[i-1:i+1],
                    mode='lines',
                    line=dict(color='red', dash='dot'),
                    name=label,
                    showlegend=show_legend  # Only show legend for the first trace
                ))
                
                added_null_label = True  # Ensure 'Null Value' label is added once

        # Customize the layout of the plot
        fig.update_layout(
            title='ST Clicks in Houston for July',
            xaxis_title='Month: July',
            yaxis_title='ST Clicks',
            showlegend=True,
            xaxis_showgrid=False,  # Enable grid on the x-axis
            yaxis_showgrid=True   # Enable grid on the y-axis
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

if selected2 == "Additional Pages":
    settings_option = st.sidebar.radio(
        "Select page from the following:",
        ("Page 1", "Page 2", "Page 3")
    )

    # Page structure with titles and 'Under Development' message
    if settings_option == "Page 1":
        st.title("Page 1")
        st.write("This page is under development.")
    
    elif settings_option == "Page 2":
        st.title("Page 2")
        st.write("This page is under development.")
    
    elif settings_option == "Page 3":
        st.title("Page 3")
        st.write("This page is under development.")
