# General import section
import streamlit as st  # streamlit backend
import matplotlib.pyplot as plt
import seaborn as sns
# Importing specific plots
from Visualization.visualization import Heatmap
from Data_Preview import utils
import numpy as np
import pandas as pd
import os
#from Data_Visulization import utils
def main(data_obj):
    """Data Preview main

    :param data_obj: DataObject instance
    :param data_obj: DataObject instance
    :type data_obj: __main__.DataObject
    """
    st.header("Data Visualization")


    if 'initial.csv' not in os.listdir('Smoothing_and_Filtering'):
        st.markdown("Please upload data through side bar `Upload Data` page!")
    else:

        # df_analysis = pd.read_csv('data/2015.csv')
        df_analysis = pd.read_csv('Smoothing_and_Filtering/initial.csv')
        st.write(df_analysis.head())

# Main
if __name__ == "__main__":
    main()