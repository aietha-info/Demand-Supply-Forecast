import streamlit as st
import os


def main():
    """Automate the ML flow for data preprocessing till Model Deployment.
    """
    st.header("Welcome")
    st.subheader("Do the Complete Automate ML flow")
    st.write("""
             Follow the below to get smooth flow for end to end implementation

             It allows you to:
             - Upload your own datasets
             - Data Description
             - Rename and drop columns within them
             - Change the Data type of column
             - Data Preprocessing
             - Smooth, filter and interpolate
             - EDA
             - Perform advanced machine learning with customizable parameters on you data
             - Model Building
             - Visualize and download the results
             - Validate ML pipeline
             """)
    st.subheader("App Navigation")
    st.markdown("""
                0. **Welcome:** Start the Journey for ML and AI
                1. **Data Preview:**  You can have a look at your dataset in general and spot some correlations between the features
                2. **Data Preparation:** Drop and/or rename single/multiple columns, don't forget to submit changes
                3. **Column Modification:** Change the Data type of column for Dependent and Independent variable, don't forget to submit changes
                4. **Data Preprocessing:** Do the label encoding for categorical variable and fill the missing value, submit the changes
                5. **Smoothing and Filtering:** Use a multitude of tools to trim or adjust your data to increase its quality. Don't forget to save and finalize the results! Even if you didn't change anything.
                6. **EDA:** EDA using the pandas proffilling and other python library
                7. **Classification:** You can perform several classification methods (e.g. Random Forest) and get results as visualization and datasheet.  
                8. **Regression:** Predict the next data points using Neural Networks, Random Forest and other algorithms
                9. **Model Deployment:** Save the model file in case of neural network save the weights file also
                10. **Test the Model:** Load the saved model and do the predication on test data
                11. **Deploy the Model on Azure Cloud:** Deploy the Model on Azure cloud 
                12. **Create Pipeline using ML flow for Automate:** Automate the process using MLops
                13. **Create Pipeline on Azure Cloud for Automate:** Automate the process using MLops on Cloud
                
                
                
               
                """)
    st.info("Follow the sequence for entire process for ML model!")
    #st.subheader("Source code")
    #st.markdown(
     #   "It can be found via navigating to the menu in the top right corner and pressing 'View App Source' or by using [this link](https://github.com/Aonic7/Dashboard-Streamlit).")

    # To delete leftover files from the previous runs
    if os.path.isfile("Smoothing_and_Filtering//Preprocessing dataset.csv"):
        os.remove("Smoothing_and_Filtering//Preprocessing dataset.csv")

    if os.path.isfile("Smoothing_and_Filtering//Filtered Dataset.csv"):
        os.remove("Smoothing_and_Filtering//Filtered Dataset.csv")

    if os.path.isfile("Smoothing_and_Filtering//initial.csv"):
        os.remove("Smoothing_and_Filtering//initial.csv")