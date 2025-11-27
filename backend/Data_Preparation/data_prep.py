# General import section
import pandas as pd  # to work with dataframes
import streamlit as st  # streamlit backend
import numpy as np  # to work with numerical arrays
import os  # to work with files
#st.set_option('deprecation.showPyplotGlobalUse', False)
from matplotlib import pyplot as plt
from streamlit_autorefresh import \
    st_autorefresh  # library for autorefresher https://libraries.io/pypi/streamlit-autorefresh
import seaborn as sns  # to work with plots
def import_dset(data_obj):
    """Checking if the processed dataset already exist, then current dataframe will be equal to that.
       If it's not, initial dataframe will be generated into initial.csv file, and current dataframe will be equal to initial.

    :param data_obj: DataObject instance
    :type data_obj: __main__.DataObject
    :return: pandas dataframe object
    :rtype: pandas.core.frame.DataFrame
    """

    try:
        a = pd.read_csv('Smoothing_and_Filtering//Filtered Dataset.csv', index_col=None)
        if a.equals(data_obj.df) == False:
            current_df = a
        else:
            current_df = data_obj.df
            current_df.to_csv("Smoothing_and_Filtering//initial.csv", index=False)
    except:
        current_df = data_obj.df
        current_df.to_csv("Smoothing_and_Filtering//initial.csv", index=False)

    return current_df


def main(data_obj):
    """Data Preparation main

    :param data_obj: DataObject instance
    :type data_obj: __main__.DataObject
    """    """"""

    # Header
    st.header("Data Preparation")
    st.info("""
               Here you can rename and/or drop columns.
               \nA field "Column to delete" is a multi-selector. You can choose more than one column to delete at once. 
               \nDon't forget to press 'Submit' each time to apply changes!
            """)

    # Dataframe assignement from data object
    current_df = import_dset(data_obj)

    # Reset dataframe
    if st.sidebar.button("Reset dataframe to the initial one"):
        current_df = pd.read_csv('Smoothing_and_Filtering//initial.csv', index_col=None)
        # Check if file exists and remove it if it does
        if os.path.isfile("Smoothing_and_Filtering//Filtered Dataset.csv"):
            os.remove("Smoothing_and_Filtering//Filtered Dataset.csv")
        st.sidebar.success("Success!")

    cc1, cc2 = st.columns(2)
    cc3, cc4 = st.columns(2)
    cc5, cc6 = st.columns(2)
    cc7, cc8 = st.columns(2)

    # Display current dataframe
    with cc1:
        st.write("Dataframe display:")
        st.write(current_df)
    # The form for renaming columns
    with cc2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        with st.form(key="form"):
            # Selecting the column to change
            col_to_change = st.selectbox("Column to change", current_df.columns)
            new_col_name = st.text_input("New name", value="")
            submit_button = st.form_submit_button(label='Submit changes')

        # Submitting changes
        if submit_button:
            current_df = current_df.rename(columns={col_to_change: new_col_name})
            current_df.to_csv("Smoothing_and_Filtering//Filtered Dataset.csv", index=False)
            st_autorefresh(interval=50, limit=2, key="fizzbuzzcounter")

            # The form for deleting columns
    with cc3:
        st.write(" ")
        st.write(" ")
        st.write(" ")

        # Selecting the columns to delete
        with st.form(key="form1"):
            col_to_delete = st.multiselect('Columns to delete', current_df.columns)
            submit_button1 = st.form_submit_button(label='Submit changes')

        # Submitting changes
        if submit_button1:
            current_df = current_df.drop(columns=col_to_delete)
            current_df.to_csv("Smoothing_and_Filtering//Filtered Dataset.csv", index=False)
            st_autorefresh(interval=50, limit=2, key="fizzbuzzcounter")
    df=current_df
    with cc4:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write("Dataframe Shape")
        st.write(df.shape)
        st.write("Dataframe Types")
        st.write(df.dtypes)
        st.write("Dataframe Info")
        st.write(df.describe())
        #st.write("Dataframe Describe include object")
        #st.write(df.describe(include='object'))

        # Find columns with null values greater than 0
        columns_with_null = df.columns[df.isnull().sum() > 0].tolist()

        # Calculate sum and mean of null values for columns with nulls > 0
        null_info = {}
        for col in columns_with_null:
            null_sum = df[col].isnull().sum()
            null_mean = df[col].mean()
            null_median = df[col].median()
            null_mode = df[col].mode()
            null_unique=df[col].unique()
            null_desc = df[col].describe()
            null_info[col] = {'Null Sum': null_sum, 'Null Mean': null_mean, 'Null Median': null_median,'Null_Mode':null_mode, 'Unique': null_unique,'Description': null_desc}

        st.write("Sum, Mean, Median, Mode, Unique and Describe of Columns with  nulls > 0:")
        for col, info in null_info.items():
            st.write(f"Column '{col}':")
            st.write(info)
    with cc5:
        # Horizontal styling of radio buttons
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;}</style>',
                 unsafe_allow_html=True)

        # Main data preparation method radio selector
        dp_method = st.radio(label='Null Value Imputation Method', options=['NoImpute','ImputeMean', 'ImputeMode', 'ImputeMedian'])

        if dp_method == 'ImputeMean':
            for col in columns_with_null:
                col_mean = df[col].mean()
                df[col].fillna(col_mean, inplace=True)

        st.write("DataFrame after filling NaN values with mean:")
        st.write(df.isnull().sum())
    with cc6:
        st.write("Heat Map to show the null values")
        fig, ax = plt.subplots()  # solved by add this line
        ax = sns.heatmap(data=df.isnull(), cbar=False)
        st.pyplot(fig)
        plt.savefig('docs/no_nullvalue.png')
        st.write("Checking for outlier")
        df.plot(kind='box', figsize=(12, 10), subplots=True, layout=(4, 3))
        st.pyplot(plt.show())
    with cc7:
        st.write(" ")
        st.write(" ")
        st.write("Select the outliers column you want to remove. After visiting the form, press 'Submit' to apply changes!")

        # Selecting the columns to delete
        with st.form(key="form6"):
            col_to_delete = st.multiselect('Columns to delete', df.columns)
            submit_button5 = st.form_submit_button(label='Submit changes')

        # Submitting changes
        if submit_button5:
            df = df.drop(columns=col_to_delete)
            df.to_csv("Smoothing_and_Filtering//Filtered Dataset.csv", index=False)
            st_autorefresh(interval=50, limit=2, key="fizzbuzzcounter")
        df1 = df
        st.write("Data After dropping columns:")
        st.write(df1)
    with cc8:
        st.write("Encoding categorical variables")
        # Encoding categorical variables
        with st.form(key="form8"):
            col_encoding = st.selectbox('Select Categorical Column', df1.columns)
            col=df1[col_encoding].unique()

            submit_button8 = st.form_submit_button(label='Submit changes')
        # Submitting changes
        if submit_button8:
            st.write(col.shape[0])
            for i in range(col.shape[0]):
                #st.write(df1[col_encoding].unique()[i])
                df1[col_encoding].replace(df1[col_encoding].unique()[i], i, inplace=True)
                df1.to_csv("Smoothing_and_Filtering//Filtered Dataset.csv", index=False)
        st_autorefresh(interval=50, limit=2, key="fizzbuzzcounter1")
        st.write("Data After encoding categorical variables:")
        st.write(df1)
        df1.to_csv("data/AfterDataprep.csv", index=False)





# Main
if __name__ == "__main__":
    main()