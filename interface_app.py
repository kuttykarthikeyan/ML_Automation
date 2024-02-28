import streamlit as st
import pandas as pd
import os

if "no_of_csv" not in st.session_state:
    st.session_state.no_of_csv = 1

# Identify target variable types have chaai
def class_identification(column_name):
        if column_name in df.columns:
            unique_values_count = df[column_name].nunique()
            data_type = df[column_name].dtype

            if unique_values_count < len(df):
                #  suggesting classification
                target_type = "Classification"
            elif data_type == "object":
                # suggesting classification
                target_type = "Classification"
            else:
                #  assume regression
                target_type = "Regression"
            
            return target_type

with st.sidebar:
    st.title("Automated machine learning")
    choice=st.radio("Navigation",["Upload","Preprocessing","Model Fitting","Download"])
if choice == "Upload":
    st.title("ML Automation")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        folder_path = "./datasets"
        filename, extension = os.path.splitext(uploaded_file.name)
        file_name = f"dataset_{st.session_state.no_of_csv}{extension}"
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        df = pd.read_csv(uploaded_file)
        st.session_state.no_of_csv += 1

        target_variable = st.selectbox("Enter the target column",df.columns)
        idependent_df=df.drop(target_variable, axis=1)
        #current dataset name
        idependent_columns=st.multiselect("enter the columns",idependent_df.columns)
        
       
        
        

        
if choice=='Preprocessing':
    st.dataframe(df)
    
if choice=='Model Fitting':
    pass
if choice=='Download':
    pass

