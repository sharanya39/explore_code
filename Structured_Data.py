import os
import streamlit as st
import pandas as pd
from openai import OpenAI
import numpy as np
import plotly.express as px  # interactive charts
from langchain.agents import AgentType, AgentExecutor
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_community.chat_models import ChatOpenAI
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
def app():
    file_formats = {
        "csv": pd.read_csv,
        "xls": pd.read_excel,
        "xlsx": pd.read_excel,
        "xlsm": pd.read_excel,
        "xlsb": pd.read_excel,
    }


    def clear_submit():
        """Clear the Submit Button State"""
        st.session_state["submit"] = False


    @st.cache_data(ttl="2h")
    def load_data(uploaded_file):
        try:
            ext = os.path.splitext(uploaded_file.name)[1][1:].lower()
        except:
            ext = uploaded_file.split(".")[-1]
        if ext in file_formats:
            return file_formats[ext](uploaded_file)
        else:
            st.error(f"Unsupported file format: {ext}")
            return None
    def chart_display():
    # Binning the data using pandas for the Age column
        patient_record_df = df
        bins = [1, 20, 30, 40, 50, 60, 80]
        labels = ["Age between 1-20 ", "Age between 21-30 ", "Age between 31-40 ", "Age between 41-50 ", "Age between 51-60 ", "Age between 61-80 "]
        patient_record_df['Age_count'] = pd.cut(patient_record_df['Age'], bins=bins, labels=labels)
        age_counts = patient_record_df['Age_count'].value_counts().sort_index().reset_index()
        age_counts.columns = ['Age_count', 'Count']
        # created new dataframe to remove records with 0 counts #
        age_countx=age_counts.query("Count != 0").sort_values("Age_count")
        # Group by data for sex
        sex_counts = df['Sex'].value_counts().reset_index()
        sex_counts.columns = ['Sex', 'Count']
        # Group by Ethnicity and count the occurrences
        ethnicity_counts = df['Ethnicity'].value_counts().reset_index()
        ethnicity_counts.columns = ['Ethnicity', 'Number_of_patients']
        # Group by Medications 
        Medications_counts = df['Medications'].value_counts().reset_index()
        Medications_counts.columns = ['Medications', 'Number_of_patients']
        # Group by A1c% and count the occurrences
        a1c_counts = df['A1c (%)'].value_counts().reset_index()
        a1c_counts.columns = ['A1c (%)', 'Number_of_patients']
        # Display the charts in columns
        cl1, cl2 = st.columns(2)
        with cl1:
            fig1 = px.pie(age_countx, names='Age_count', values='Count', hole=0.5, title='Age'
                      # added category_orders to sort donut chart by Age_Count labels #
                      ,category_orders={'Age_count':["Age between 1-20 ", "Age between 21-30 ", "Age between 31-40 ", "Age between 41-50 ", "Age between 51-60 ", "Age between 61-80 "] }
                     )
        #fig1.layout()
            st.write(fig1)
        with cl2:
            fig2 = px.pie(sex_counts, names='Sex', values='Count', title='Sex')
            st.write(fig2)
        c21, c22 = st.columns(2)
        with c21:
            custom_colors = ['darkblue', 'lightblue', 'lightgreen', 'lightcoral', 'pink']
            fig3 = px.bar(ethnicity_counts, x='Ethnicity', y='Number_of_patients', color='Ethnicity', title='Number of Patients by Ethnicity', color_discrete_sequence=custom_colors)
            st.plotly_chart(fig3)
        with c22:
            # fig4 = px.histogram(df,x='Age', y='Medications', title='Medications vs Age')
            custom_colors = ['lightblue', 'lightgreen','yellow','lightyellow', 'lightcoral', 'pink']
            fig4 = px.bar(Medications_counts,x='Medications', y='Number_of_patients', color='Medications', title='Patients vs Medications ', color_discrete_sequence=custom_colors)
            st.plotly_chart(fig4)
        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            fig5 = px.histogram(a1c_counts, x='A1c (%)',y='Number_of_patients',title='A1c% vs Number of patients')
            st.write(fig5)
        with fig_col2:
            fig6 = px.scatter(df, x='Age', y='Total Cholesterol (mg/dL)', color='Sex', title='Total Cholesterol vs Age')
            st.write(fig6)

    openai_api_key = st.secrets["OPENAI_API_KEY"]
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()



    uploaded_file = st.file_uploader(
        "Upload a Data file",
        type=list(file_formats.keys()),
        help="Various File formats are Support",
        on_change=clear_submit,
    )

    if uploaded_file:
        df = load_data(uploaded_file)
        if df is None:
            st.stop()
    if "messages" not in st.session_state or st.sidebar.button("Clear conversation history"):
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:

        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(placeholder="What is this data about?"):
        st.session_state.messages.append({"role": "user", "content": prompt+" and save  df_filtered as a csv file"})
        st.chat_message("user").write(prompt)

        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        llm = ChatOpenAI(
            temperature=0, model="gpt-4", openai_api_key=openai_api_key, streaming=True
        )

        pandas_df_agent = create_pandas_dataframe_agent(
            llm,
            df,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            #handle_parsing_errors=True,
            allow_dangerous_code=True
        )
        with st.chat_message("assistant"):
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            response = pandas_df_agent.run(st.session_state.messages, callbacks=[st_cb])
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)
        df=pd.read_csv('/home/sharanya/AI_env/clinical_records/df_filtered.csv')
        chart_display()
        st.dataframe(data=df)
        st.info(len(df)) 
    