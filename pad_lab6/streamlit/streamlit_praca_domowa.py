import streamlit as st
import pandas as pd
import time
import plotly.express as px


if 'first_name' not in st.session_state:
    st.session_state['first_name'] = ''

if 'last_name' not in st.session_state:
    st.session_state['last_name'] = ''

page = st.sidebar.selectbox('Select page', ['Ankieta', 'Staty'])

if page == 'Ankieta':
    firstname = st.text_input("Enter your first name", st.session_state.first_name)
    st.session_state.first_name = firstname.title()
    if firstname != '':
        st.success(f'First name: {st.session_state.first_name}')

    lastname = st.text_input("Enter your last name", st.session_state.last_name)
    st.session_state.last_name = lastname.title()
    if lastname != '':
        st.success(f'Last name: {st.session_state.last_name}')
else:
    data = st.file_uploader("Upload your dataset", type=['csv'])

    if data is not None:
        with st.spinner("Loading data..."):
            time.sleep(2)

        df = pd.read_csv(data)
        st.dataframe(df)

        plots_menu = ['Sales quantity by category', 'Revenue by month (03.2013 - 04.2017)']
        st.set_option('deprecation.showPyplotGlobalUse', False)
        selected_plot = st.selectbox("Select plot", plots_menu)
        if selected_plot == 'Sales quantity by category':
            qty_df = df[['tshirt_category', 'tshirt_price']].groupby('tshirt_category').agg('sum')

            fig = px.bar(qty_df,
                         title="Sales quantity by category",
                         labels={'value': 'quantity'})
            fig.layout.update(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        else:
            price_df = df[['order_date', 'tshirt_price']].groupby('order_date').agg('sum').copy()
            price_df.index = pd.to_datetime(price_df.index)
            price_df.reset_index(inplace=True)
            price_df['month_year'] = pd.to_datetime(price_df['order_date']).dt.to_period('M')

            price_months_years_df = price_df[['month_year', 'tshirt_price']].groupby(['month_year']).agg('sum')
            price_months_years_df.index = price_months_years_df.index.astype(str)

            fig = px.line(price_months_years_df,
                          title="Revenue by month (03.2013 - 04.2017)",
                          labels={'value': 'revenue'})
            fig.layout.update(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
