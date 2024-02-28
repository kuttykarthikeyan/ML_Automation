import streamlit as st
import pandas as pd
import os

if "no_of_csv" not in st.session_state:
    st.session_state.no_of_csv = 1

# Identify target variable types
# Identification feature type
def class_identification(column_name):
        if column_name in df.columns:
            unique_values_count = df[column_name].nunique()
            flag=0
            try :
                str(df.iloc[0:1,'column_name'])
                flag=1
            except ValueError:
                flag=0

            if unique_values_count < len(df)/2:
                #  suggesting classification
                target_type = "Categorical"
            elif flag==1:
                target_type='Categorical'
            
            else:
                #  assume regression
                target_type = "Numerical"
            
            return target_type
        
#Navigation/Side bar

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
        
        #current dataset name
        idependent_df=df.drop(target_variable, axis=1)
        
        class_of_target=class_identification(target_variable)
        if class_of_target=='Categorical':
            st.write("A Classification Problem")
        else:
            st.write('A Regression Problem')
        idependent_columns=st.multiselect("enter the columns",idependent_df.columns)
        
        class_type_of_coloumn=dict()
        for names in idependent_columns:
            #contains the type(Catogorical/Regression) of independent features
            class_type_of_coloumn[names]=class_identification(names)
            
        print(class_type_of_coloumn)
        
if choice=='Preprocessing':
    st.dataframe(df)
    
if choice=='Model Fitting':
    pass
if choice=='Download':
    pass

