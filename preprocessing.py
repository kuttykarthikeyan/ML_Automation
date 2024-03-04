from interface_app import *
import streamlit as st
from sklearn.preprocessing import LabelEncoder

def identify_classification_regression_in_target(target_df):
    unique_values_count = target_df.nunique()[0]

    if unique_values_count < len(target_df) / 2:
        return "Classification"
    else:
        return "Regression"

def need_enconding_or_not_of_target(target_df):
    try:
        int(target_df.iloc[0,0])
        return 'Not Needed'
    except ValueError:
        return 'Needed'
    
def target_variable_preprocessing(target_df):
    target_name=target_df.columns[0]
    st.write(target_name)
    number_rows=target_df.shape[0]
    if identify_classification_regression_in_target(target_df)=='Classification':
        if need_enconding_or_not_of_target(target_df)=='Needed':
            if target_df.isnull().sum()[0]>number_rows/4:
                unique=target_df.unique()
                mode_value=str(unique[0])+str(unique[1])
                
            else:
                
                mode_value = target_df.mode()[target_name][0]

    # Fill the missing values with mode
            target_df.fillna(mode_value, inplace=True)
            #performing label encoder
            encoder = LabelEncoder()
            encoder.fit(target_df)
            target_df = pd.DataFrame(encoder.transform(target_df),columns=target_df.columns)
            
        else:
            if target_df.isnull().sum()[0]>number_rows/4:
                mode_value=-999 
            else:
                mode_value = target_df.mode()[target_name][0]

            target_df.fillna(mode_value, inplace=True)
            
    else:
        mean_value = target_df.mean()[0]
        # Fill the missing values with mean
        target_df.fillna(mean_value, inplace=True)
        
        
    return target_df

def preprocessing(df_2,regression_df,encoding_needed_df,encoding_not_needed_df):
    #removal of null values in categorical datasets
    number_rows=df_2.shape[0]
    if not encoding_needed_df.empty:
        for i in encoding_needed_df.columns:
            if encoding_needed_df.isnull().sum()[i]>number_rows/4:
                unique=encoding_needed_df[i].unique()
                mode_value=str(unique[0])+str(unique[1])
                
            else:
                mode_value = encoding_needed_df[i].mode()[0]

    # Fill the missing values with mode
            encoding_needed_df[i].fillna(mode_value, inplace=True)
    #performing label encoder
            encoder = LabelEncoder()
            encoder.fit(encoding_needed_df[i])
            encoding_needed_df[i] = encoder.transform(encoding_needed_df[i])
            
            df_2[i]=encoding_needed_df[i]
    st.dataframe(df_2)
            
    if not encoding_not_needed_df.empty:
        for i in encoding_not_needed_df.columns:
            if encoding_not_needed_df.isnull().sum()[i]>number_rows/4:
                mode_value=-999 
            else:
                mode_value = encoding_not_needed_df[i].mode()[0]

            encoding_not_needed_df[i].fillna(mode_value, inplace=True)
            df_2[i]=encoding_not_needed_df[i]
            
    #for regresion data 
    #null values replaced with mean
    st.write(regression_df.isnull().sum())
    if not regression_df.empty:
        for i in regression_df.columns:
                mean_value = regression_df.mean()[i]
                # Fill the missing values with mean
                regression_df[i].fillna(mean_value, inplace=True)
                df_2[i]=regression_df[i]
    st.write(regression_df.isnull().sum())
    
    return(df_2,regression_df,encoding_needed_df,encoding_not_needed_df)