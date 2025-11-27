# General import section
import pandas as pd  # to work with dataframes
import streamlit as st  # streamlit backend
import numpy as np  # to work with numerical arrays
import os  # to work with files
from matplotlib import pyplot as plt
from streamlit_autorefresh import \
    st_autorefresh  # library for autorefresher https://libraries.io/pypi/streamlit-autorefresh
import seaborn as sns  # to work with plots
from Utils import utils  # to work with numerical arrays
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
    st.header("EDA For Data")
    st.info("""
              EDA for Data
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

    # Display current dataframe
    with cc1:
        st.write("Dataframe display:")
        st.write(current_df)
    with cc2:
        st.write(" ")
        st.write(" ")
        st.write(" ")

        # Selecting the columns to delete
        st.write("Delete the column that contaiing id or other irrelevant information. After visiting the form, press 'Submit' to apply changes!")
        with st.form(key="form1"):
            col_to_delete = st.multiselect('Columns to delete', current_df.columns)
            submit_button1 = st.form_submit_button(label='Submit changes')

        # Submitting changes
        if submit_button1:
            current_df = current_df.drop(columns=col_to_delete)
            current_df.to_csv("Smoothing_and_Filtering//Filtered Dataset.csv", index=False)
            st_autorefresh(interval=50, limit=2, key="fizzbuzzcounter")
        df=current_df
    with cc3:
        st.write("Draw Chart for Data")
        cols = pd.read_csv('data/metadata/column_type_desc.csv')
        df_analysis= current_df.copy()
        df_visual = df_analysis.copy()
        Categorical, Numerical, Object = utils.getColumnTypes(cols)
        cat_groups = {}
        unique_Category_val = {}

        for i in range(len(Categorical)):
            unique_Category_val = {Categorical[i]: utils.mapunique(df_analysis, Categorical[i])}
            cat_groups = {Categorical[i]: df_visual.groupby(Categorical[i])}

        category = st.selectbox("Select Category ", Categorical + Object)

        sizes = (df_visual[category].value_counts() / df_visual[category].count())

        labels = sizes.keys()

        maxIndex = np.argmax(np.array(sizes))
        explode = [0] * len(labels)
        explode[int(maxIndex)] = 0.1
        explode = tuple(explode)

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False, startangle=0)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_title('Distribution for Categorical Column - ' + (str)(category))
        st.pyplot(fig1)

        corr = df_analysis.corr(method='pearson')

        fig2, ax2 = plt.subplots()
        mask = np.zeros_like(corr, dtype=bool)
        mask[np.triu_indices_from(mask)] = True
        # Colors
        cmap = sns.diverging_palette(240, 10, as_cmap=True)
        sns.heatmap(corr, mask=mask, linewidths=.5, cmap=cmap, center=0, ax=ax2)
        ax2.set_title("Correlation Matrix")
        st.pyplot(fig2)
        #category.astype("str")
        categoryObject = st.selectbox("Select " + (str)(category), unique_Category_val[category])
        st.write(cat_groups[category].get_group(categoryObject).describe())
        colName = st.selectbox("Select Column ", Numerical)

        st.bar_chart(cat_groups[category].get_group(categoryObject)[colName])

        ## Code base to drop redundent columns


#main
if __name__ == "__main__":
    main()
