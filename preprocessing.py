from interface_app import *
import streamlit as st
from sklearn.preprocessing import LabelEncoder

def preprocessing(df_2,regression_df,encoding_needed_df,encoding_not_needed_df):
    #removal of null values in categorical datasets
    number_rows=df_2.shape[0]
    if not encoding_needed_df.empty:
        for i in encoding_needed_df.columns:
            if encoding_needed_df.isnull().sum()[i]>number_rows/4:
                unique=encoding_not_needed_df[i].unique()
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