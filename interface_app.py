import streamlit as st
import pandas as pd
import os



def is_empty_file_size(filename):

  return os.path.getsize(filename) < 3



if os.path.exists('independent_data.csv'):
    if not is_empty_file_size('independent_data.csv'):
        df_2=pd.read_csv('independent_data.csv')
    else:
        df_2=pd.Dataframe()
        
if os.path.exists('regression_data.csv'):
    if not is_empty_file_size('regression_data.csv'):
        regression_df=pd.read_csv('regression_data.csv')
    else:
        regression_df=pd.DataFrame()
        
if os.path.exists('encoding_needed_data.csv'):
    if not is_empty_file_size('encoding_needed_data.csv'):
        encoding_needed_df=pd.read_csv('encoding_needed_data.csv')
    else:
        encoding_needed_df=pd.DataFrame()
        
if os.path.exists('encoding_not_needed_data.csv'):
    if not is_empty_file_size('encoding_not_needed_data.csv'):
        encoding_not_needed_df=pd.read_csv('encoding_not_needed_data.csv')
    else:
        encoding_not_needed_df=pd.DataFrame()

if "no_of_csv" not in st.session_state:
    st.session_state.no_of_csv = 1
# Initialize dictionaries to store information
target_info = {}
independent_info = {}
selected_columns_info = []

# Function to identify column types
def identify_classification_regression(column_name, df):
    unique_values_count = df[column_name].nunique()

    if unique_values_count < len(df) / 2:
        return "Classification"
    else:
        return "Regression"

#to check encoding is required or not
def need_enconding_or_not(column_name,df):
        try:
            int(df.loc[:0,column_name])
            return 'Not Needed'
        except ValueError:
            return 'Needed'
     
# Sidebar navigation
with st.sidebar:
    independent_info = {}
    st.title("Automated machine learning")
    choice = st.radio("Navigation", ["Upload", "Preprocessing", "Model Fitting", "Download"])

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

        target_variable = st.selectbox("Enter the target column", df.columns)
        
        # Store target variable type in dictionary
        target_type = identify_classification_regression(target_variable, df)
        target_info[target_variable] = target_type

        independent_df = df.drop(target_variable, axis=1)
        
        selected_columns = st.multiselect("Select independent columns", independent_df.columns)
        
        # Store independent variable types in dictionary
        for column in selected_columns:
            column_type = identify_classification_regression(column, df)
            independent_info[column] = column_type
            if column_type == "Classification":
                independent_info[f"{column}_encoding"] = need_enconding_or_not(column,df)
            else:
                independent_info[f"{column}_encoding"] = "Not Needed"

        # Store selected columns
        selected_columns_info = selected_columns
        
        to_be_removed_columns=[]
        
        press=st.button('Click here to continue')
        if press:
            for i in df.columns:
                if i not in selected_columns_info:
                    to_be_removed_columns.append(i)
            df_2=pd.DataFrame()
            regression_df=pd.DataFrame()
            classification_df=pd.DataFrame()
            encoding_needed_df=pd.DataFrame()
            encoding_not_needed_df=pd.DataFrame()
            
            df_2=df.drop(to_be_removed_columns,axis=1)
            
            for i in df_2.columns:
                if independent_info[i]=='Regression':
                    regression_df[i]=df_2[i]
                else:
                    classification_df[i]=df_2[i]
             
            for i in classification_df.columns:
                if independent_info[i+'_encoding']=='Needed':
                    encoding_needed_df[i]=classification_df[i]
                else:
                    encoding_not_needed_df[i]=classification_df[i]
    
            df_2.to_csv("independent_data.csv",index=None)
            regression_df.to_csv("regression_data.csv",index=None)
            encoding_needed_df.to_csv("encoding_needed_data.csv",index=None)
            encoding_not_needed_df.to_csv("encoding_not_needed_data.csv",index=None)

if choice == 'Preprocessing':
    
    #removal of null values in categorical datasets
    if not encoding_needed_df.empty:
        for i in encoding_needed_df.columns:
            mode_value = encoding_needed_df[i].mode()[0]

    # Fill the missing values with mode
            encoding_needed_df[i].fillna(mode_value, inplace=True)
            df_2[i]=encoding_needed_df[i]
            
    if not encoding_not_needed_df.empty:
        for i in encoding_not_needed_df.columns:
            mode_value = encoding_not_needed_df[i].mode()[0]

    # Fill the missing values with mode
            encoding_not_needed_df[i].fillna(mode_value, inplace=True)
            df_2[i]=encoding_not_needed_df[i]
        st.dataframe(encoding_not_needed_df)
        
    

if choice == 'Model Fitting':
    pass

if choice == 'Download':
    pass