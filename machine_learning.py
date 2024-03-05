import streamlit as st
import pandas as pd
import pickle
from interface_app import *

def identify_classification_regression(target_df):
    unique_values_count = target_df.nunique()[0]
    if unique_values_count < len(target_df) / 2:
        return "Classification"
    else:
        return "Regression"

def machine_learning(df_2, target_df):
    df = pd.concat([df_2, target_df], axis=1)
    target_type = identify_classification_regression(target_df)
    
    if target_type == 'Classification':
        if st.button("Run Modelling"): 
            from pycaret.classification import setup, compare_models, pull, save_model
            setup(df, target=target_df.columns[0])
            setup_df = pull()
            st.dataframe(setup_df)
            best_model = compare_models()
            compare_df = pull()
            save_model(best_model, 'best_model.pkl')  # Saving model to a file
            st.dataframe(compare_df)
    else:
        from pycaret.regression import setup, compare_models, pull, save_model
        if st.button("Run Modelling"): 
            setup(df, target=target_df)
            setup_df = pull()
            st.dataframe(setup_df)
            best_model = compare_models()
            compare_df = pull()
            save_model(best_model, 'best_model.pkl')  # Saving model to a file
            st.dataframe(compare_df)

    # Add a download button for the best model
    if st.button("Download Best Model"):
        model_filename = 'best_model.pkl'
        with open(model_filename, 'rb') as file:
            model = file.read()
        st.download_button(
            label="Download Model",
            data=model,
            file_name=model_filename,
            mime="application/octet-stream"
        )



