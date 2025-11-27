# General import section
import streamlit as st  # streamlit backend

# Importing specific plots
from Visualization.visualization import Heatmap
from Data_Preview import utils
import numpy as np
import pandas as pd
import os

def main(data_obj):
    """Data Preview main

    :param data_obj: DataObject instance
    :type data_obj: __main__.DataObject
    """
    st.header("Change Column Data Type")
    # Load the uploaded data
    if 'main_data.csv' not in os.listdir('data'):
        st.markdown("Please upload data through `Upload Data` page!")
    else:
        data = pd.read_csv('data/main_data.csv')
        st.dataframe(data)

        # Read the column meta data for this dataset
        col_metadata = pd.read_csv('data/metadata/column_type_desc.csv')

        ''' Change the information about column types
                    Here the info of the column types can be changed using dropdowns.
                    The page is divided into two columns using beta columns 
                '''
        st.markdown("#### Change the information about column types")

        # Use two column technique
        col1, col2 = st.columns(2)

        global name, type
        # Design column 1
        name = col1.selectbox("Select Column", data.columns)

        # Design column two
        current_type = col_metadata[col_metadata['column_name'] == name]['type'].values[0]
        print(current_type)
        column_options = ['numerical', 'categorical', 'object']
        current_index = column_options.index(current_type)

        type = col2.selectbox("Select Column Type", options=column_options, index=current_index)

        st.write("""Select your column name and the new type from the data.
                            To submit all the changes, click on *Submit changes* """)

        if st.button("Change Column Type"):
            # Set the value in the metadata and resave the file
            # col_metadata = pd.read_csv('data/metadata/column_type_desc.csv')
            st.dataframe(col_metadata[col_metadata['column_name'] == name])

            col_metadata.loc[col_metadata['column_name'] == name, 'type'] = type
            col_metadata.to_csv('data/metadata/column_type_desc.csv', index=False)

            st.write("Your changes have been made!")
            st.dataframe(col_metadata[col_metadata['column_name'] == name])


        st.markdown("**Column Name**-**Type**")

        for i in range(col_metadata.shape[0]):
            st.write(f"{i + 1}. **{col_metadata.iloc[i]['column_name']}** - {col_metadata.iloc[i]['type']}")
        col_metadata.to_csv('data/metadata/column_type_desc.csv', index=False)
