# General import section
import pandas as pd  # to work with dataframes
import streamlit as st  # streamlit backend
from io import StringIO  # to read data files as .csv correctly
import os

import Regression.machine_learning  # to work with files

# Streamlit main page configuration
st.set_page_config(page_title="ML Process Automation",
                   page_icon=None,
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items=None)
import numpy as np
from Utils import utils
# App import
import Welcome_Page
import Data_Preview
import Data_Preparation
import Data_Visulization
import Smoothing_and_Filtering
import Change_Column_Datatype
import EDA
import Regression
import Classification
import ML_Pipeline
import Model_Build



# Data object class
class DataObject():
    """
    Data object class holds a dataframe and its byte size.
    """

    def __init__(self, df=None, filesize=None):
        """The constructor for DataObject class

        :param df: pandas dataframe object, defaults to None
        :type df: pandas.core.frame.DataFrame, optional
        :param filesize: byte size of pandas dataframe, defaults to None
        :type filesize: numpy.int32, optional
        """
        self.df = df
        self.filesize = filesize


# Interface class
class Interface():
    """
    Interface class contains a file picker and a side bar. It also handles the import of a data object.
    """

    def __init__(self):
        """The constructor for Interface class.
        """
        pass

    def side_bar(cls, dt_obj):
        """Sidebar configuration and file picker

        :param dt_obj: pandas dataframe object
        :type dt_obj: pandas.core.frame.DataFrame
        """
        # Accepts .csv and .data
        filename = st.sidebar.file_uploader("Upload a data file", type=(["csv", "data"]))
        if filename is not None:  # file uploader selected a file
            try:  # most datasets can be read using standard 'read_csv'
                dt_obj.df = pd.read_csv(filename, sep=';|,', engine='python')
                dt_obj.filesize = dt_obj.df.size

                #############################################
                numeric_cols = dt_obj.df.select_dtypes(include=np.number).columns.tolist()
                categorical_cols = list(set(list(dt_obj.df.columns)) - set(numeric_cols))

                # Save the columns as a dataframe or dictionary
                columns = []

                # Iterate through the numerical and categorical columns and save in columns
                columns = utils.genMetaData(dt_obj.df)

                # Save the columns as a dataframe with categories
                # Here column_name is the name of the field and the type is whether it's numerical or categorical
                columns_df = pd.DataFrame(columns, columns=['column_name', 'type'])
                columns_df.to_csv('data/metadata/column_type_desc.csv', index=False)
                dt_obj.df.to_csv('data/main_data.csv', index=False)

                # Display columns
                st.markdown("**Column Name**-**Type**")
                for i in range(columns_df.shape[0]):
                    st.write(f"{i + 1}. **{columns_df.iloc[i]['column_name']}** - {columns_df.iloc[i]['type']}")

                st.markdown("""The above are the automated column types detected by the application in the data. 
                        In case you wish to change the column types, head over to the **Column Change** section. """)





                ######


            except:  # due to a different encoding some datafiles require additional processing
                filename.seek(0)
                filename = filename.read()
                filename = str(filename, 'utf-8')
                filename = StringIO(filename)
                # now the standard 'read_csv' should work
                dt_obj.df = pd.read_csv(filename, sep=';', decimal=',', index_col=False)
                dt_obj.filesize = dt_obj.df.size

            # Side bar navigation menu with a select box
            menu = ['Welcome Page', 'Data Preview', 'Change Column Datatype', 'Data Preparation', 'Data Visualization','Smoothing and filtering',
                    'EDA','Classification', 'Regression', 'Model_Build','ML_Pipeline']
            navigation = st.sidebar.selectbox(label="Select menu", options=menu)

            # Apps

            # Landing page
            if navigation == 'Welcome Page':
                with st.container():
                    Welcome_Page.welcome()

            # Runs 'Data Preview' app
            if navigation == 'Data Preview':
                with st.container():
                    Data_Preview.data_preview(dt_obj)

            # Runs 'Data Preparation' app
            if navigation == 'Data Preparation':
                with st.container():
                    Data_Preparation.data_prep(dt_obj)

            # Runs 'Change Cloumn Type' app
            if navigation == 'Change Column Datatype':
                with st.container():
                   Change_Column_Datatype.change_column_type(dt_obj)

           #Run EDA app
            if navigation == 'EDA':
                with st.container():
                    EDA.eda(dt_obj)


            # Runs 'Regression' app
            if navigation == 'Regression':
               with st.container():
                   Regression.regression(dt_obj)
                   

            # Runs 'Classification' app
            if navigation == 'Classification':
               with st.container():
                   Classification.classification(dt_obj)

            # Runs 'Model_Build' app
            if navigation == 'Model_Build':
               with st.container():
                   Model_Build.model_build(dt_obj)

            # Runs 'ML_Pipeline' app
            if navigation == 'ML_Pipeline':
               with st.container():
                   ML_Pipeline.ml_pipeline(dt_obj)
           # Runs 'Smoothing and filtering' app
            if navigation == 'Smoothing and filtering':
               Smoothing_and_Filtering.smoothing_and_filtering(dt_obj)

            # Runs 'Data Visulization' app
            if navigation == 'Data Visualization':
               with st.container():
                   Data_Visulization.data_visulization(dt_obj)

        # Initial welcome page when there is no file selected
        else:
            Welcome_Page.welcome()
            # It deletes Preprocessing and initial datasets from the last run
            #if os.path.isfile("Smoothing_and_Filtering//Preprocessing dataset.csv"):
             #   os.remove("Smoothing_and_Filtering//Preprocessing dataset.csv")
            #if os.path.isfile("Smoothing_and_Filtering//initial.csv"):
             #   os.remove("Smoothing_and_Filtering//initial.csv")


def main():
    """
    Main and its Streamlit configuration
    """

    # Creating an instance of the original dataframe data object
    data_main = DataObject()
    # Creating an instance of the main interface
    interface = Interface()
    interface.side_bar(data_main)


# Run Main
if __name__ == '__main__':
    main()