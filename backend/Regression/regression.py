import datetime
import pandas as pd
import numpy as np
import streamlit as st
from .Regression_final import Regressor
from .MLP_Regressor import NN_Regressor, Regressor_Inputs
from .MLP_TimeSeries import NN_TimeSeries_Reg, Regressor_Inputs_TS
from .Regression_Group4 import Regression
from .TimeSeries_Final import Timeseries, rf_Inputs
import os
import json
# Machine Learning
import matplotlib.pyplot as plt
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier, ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.metrics import confusion_matrix
# Custom classes 
from .utils import isNumerical

def main(data_obj):
    """Regression main 

    :param data_obj: DataObject instance.
    :type data_obj: __main__.DataObject
    
    """

    st.header('Regression')

    with st.expander("How to use", expanded=True):
        st.markdown("""
                    Here the User can choose Regression Method and parameters for each different regressor:
                    1. Choose Regressor type and weather it is time series regression or not?
                    2. Choose Target Column for the regression
                    3. Modify Regressor inputs and click submit to run regression and output results
                    """)

    try:
        #var_read = pd.read_csv("Smoothing_and_Filtering//Preprocessing dataset.csv", index_col=None, parse_dates=True, date_parser = pd.to_datetime)
        var_read = pd.read_csv("data//AfterDataprep.csv", index_col=None, parse_dates=True, date_parser = pd.to_datetime)
        rg_df = var_read
        for col in rg_df.columns:
            if rg_df[col].dtype == 'object':
                try:
                    rg_df[col] = pd.to_datetime(rg_df[col])
                except ValueError:
                    pass

    except:
        rg_df = data_obj.df.copy()
        for col in rg_df.columns:
            if rg_df[col].dtype == 'object':
                try:
                    rg_df[col] = pd.to_datetime(rg_df[col])
                except ValueError:
                    pass

        st.error("""You did not smooth of filter the data.
                     Please go to 'Smoothing and filtering' and finalize your results.
                     Otherwise, the default dataset would be used!
                     """)

    st.write(
        '<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;}</style>', unsafe_allow_html=True)

    # Main data classification method radio selector
    rg_method = st.radio(label='Regression Method', options=['Neural Networks',
                                                             'ML Regression and Claaification',
                                                             'Other Methods'])




    # Selected 'Neural Networks'
    if rg_method == 'Neural Networks':
        rg_nn_radio = st.radio(label = 'Neural Network',
                             options = ['Standard','Timeseries'])

        st.dataframe(rg_df)
        st.write(rg_df.shape)
        st.download_button(label="Download data as CSV",
                data=rg_df.to_csv(index=False),
                file_name='Preprocessed Dataset.csv',
                mime='text/csv')

        if rg_nn_radio == 'Standard':

            with st.container():

                # Input settings header
                st.subheader('Select input settings')

                cc1, cc2, cc3 = st.columns(3)

                # Input variables/widgets for the 1st column
                with cc1:
                    tt_proportion = st.slider('Portion of test data', 0.0, 1.0, 0.2, 0.05)
                    iteration_num = st.slider('Number of iterations', 100, 5000, 200, 50)
                    norm_bool = st.checkbox('Normalize data?')

                # Input variables/widgets for the 2nd column
                with cc2:
                    columns_list = list(rg_df.columns)
                    selected_column = st.selectbox("Column to regress:", columns_list)
                    col_idx = rg_df.columns.get_loc(selected_column)

                    solver_fun1 = ("lbfgs", "sgd", "adam")
                    selected_solver = st.selectbox("Solver:", solver_fun1)

                    activation_fun1 = ("identity", "logistic", "tanh", "relu")
                    selected_function = st.selectbox("Activation function:", activation_fun1)

                # Input variables/widgets for the 3rd column
                with cc3:
                    number_hl = st.slider('Hidden layers:', 1, 5, 2, 1)

                    a = [] #

                    for i in range(number_hl):
                        a.append(st.number_input(f'Number of neurons in hidden layer {i+1}:', 1, 600, 1, 1, key=i))

            with st.container():

                # Submit button
                with st.form(key="Youssef"):
                    submit_button = st.form_submit_button(label='Submit')

                    # Circle animation for code execution 
                    if submit_button:
                        with st.spinner("Training models..."):

                            # Class instance for further input
                            NN_inputs = Regressor_Inputs(tt_proportion,
                                                    selected_function,
                                                    tuple(a),
                                                    selected_solver,
                                                    iteration_num,
                                                    norm_bool
                                                    )

                            # Class instance/method for Neural Networks execution
                            RegressorMLP = NN_Regressor(rg_df, NN_inputs, col_idx)

                            RegressorMLP.Regressor()
                            RegressorMLP.printing()
                            RegressorMLP.plotting()


    # Selected 'Neural Networks TS (Youssef)'
        if rg_nn_radio == 'Timeseries':

            with st.expander("How to use", expanded=True):
                st.markdown("""
                    Here you need to choose if you want to group the data set based on a unique value in a specific column and then run the regression for this filtered data only. 
                    
                    If you don't group data then timeseries regression will be done on the whole dataset.
                    """)

            with st.container():

                # Input settings header
                st.subheader('Select input settings')

                cc1, cc2, cc3 = st.columns(3)


                # Input variables/widgets for the 1st column
                try:
                    with cc1:
                        tt_proportion = st.slider('Portion of test data', 0.0, 1.0, 0.2, 0.05)

                        solver_fun1 = ("lbfgs", "sgd", "adam")
                        selected_solver = st.selectbox("Solver:", solver_fun1)

                        activation_fun1 = ("identity", "logistic", "tanh", "relu")
                        selected_function = st.selectbox("Activation function:", activation_fun1)

                        group_bool = st.checkbox('Group data?')

                    # Input variables/widgets for the 2nd column
                    with cc2:
                        iteration_num = st.slider('Number of iterations', 100, 5000, 200, 50)

                        columns_list = list(rg_df.select_dtypes(exclude=['object', 'datetime']).columns)
                        selected_column = st.selectbox("Column to regress:", columns_list)
                        col_idx = rg_df.columns.get_loc(selected_column)

                        unique_columns_list = list(rg_df.select_dtypes(exclude=['datetime']).columns)
                        unique_selected_column = st.selectbox("Filter uniques:", unique_columns_list)
                        unique_col_idx = rg_df.columns.get_loc(unique_selected_column)


                        tm_columns_list = list(rg_df.select_dtypes(include=['datetime']).columns)
                        time_column = st.selectbox("Select a time column:", tm_columns_list)
                        tm_col_idx = rg_df.columns.get_loc(time_column)


                    # Input variables/widgets for the 3rd column
                    with cc3:
                        number_hl = st.slider('Hidden layers:', 1, 5, 3, 1)

                        a = []

                        for i in range(number_hl):
                            a.append(st.number_input(f'Number of neurons in hidden layer {i+1}:', 1, 600, 10, 1, key=i))
                except KeyError as e:
                    st.error("Are you sure this dataset has a time column?")
                    st.stop()


            with st.container():



                # Class instance for further input
                NN_inputs_TS = Regressor_Inputs_TS(tt_proportion,
                                        selected_function,
                                        tuple(a),
                                        selected_solver,
                                        iteration_num,
                                        group_bool
                                        )

                # Class instance/method for Neural Networks execution
                Regressor_TS = NN_TimeSeries_Reg(rg_df, NN_inputs_TS, col_idx, tm_col_idx)

                if group_bool:
                    # Section subheader
                    st.subheader('Additional user inputs')
                    Regressor_TS.listing(unique_col_idx)
                    #st.dataframe(Regressor_TS.group_object)
                    selected_group = Regressor_TS.group_object['index']
                    sel = st.selectbox("Select an element for groupping:", selected_group)
                    sel_idx = selected_group[selected_group == sel].index[0]

                # Submit button
                with st.form(key="Youssef"):
                    submit_button = st.form_submit_button(label='Submit')



                    # Circle animation for code execution
                    if submit_button:
                        with st.spinner("Training models..."):

                            if group_bool:
                                Regressor_TS.group(sel_idx)
                            Regressor_TS.Regressor()
                            Regressor_TS.printing()
                            Regressor_TS.plotting()


    # Selected 'Random Forest'
    if rg_method == 'ML Regression and Claaification':
        st.write("ML Regression and Claaification")
         # Load the data
        if 'main_data.csv' not in os.listdir('data'):
            st.markdown("Please upload data through `Upload Data` page!")
        else:
            data = pd.read_csv('data/main_data.csv')

         # Create the model parameters dictionary 
        params = {}

        # Use two column technique 
        col1, col2 = st.columns(2)

        # Design column 1 
        y_var = col1.radio("Select the variable to be predicted (y)", options=data.columns)

        # Design column 2 
        X_var = col2.multiselect("Select the variables to be used for prediction (X)", options=data.columns)

        # Check if len of x is not zero 
        if len(X_var) == 0:
            st.error("You have to put in some X variable and it cannot be left empty.")

        # Check if y not in X 
        if y_var in X_var:
            st.error("Warning! Y variable cannot be present in your X-variable.")

        # Option to select predition type 
        pred_type = st.radio("Select the type of process you want to run.", 
                            options=["Regression", "Classification"], 
                            help="Write about reg and classification")

        # Add to model parameters 
        params = {
                'X': X_var,
                'y': y_var, 
                'pred_type': pred_type,
        }

        # if st.button("Run Models"):

        st.write(f"**Variable to be predicted:** {y_var}")
        st.write(f"**Variable to be used for prediction:** {X_var}")
        
        # Divide the data into test and train set 
        X = data[X_var]
        y = data[y_var]

        # Perform data imputation 
        # st.write("THIS IS WHERE DATA IMPUTATION WILL HAPPEN")
        
        # Perform encoding
        X = pd.get_dummies(X)

        # Check if y needs to be encoded
        if not isNumerical(y):
            le = LabelEncoder()
            y = le.fit_transform(y)
            
            # Print all the classes 
            st.write("The classes and the class allotted to them is the following:-")
            classes = list(le.classes_)
            for i in range(len(classes)):
                st.write(f"{classes[i]} --> {i}")
        

        # Perform train test splits 
        st.markdown("#### Train Test Splitting")
        size = st.slider("Percentage of value division",
                            min_value=0.1, 
                            max_value=0.9, 
                            step = 0.1, 
                            value=0.8, 
                            help="This is the value which will be used to divide the data for training and testing. Default = 80%")

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=size, random_state=42)
        st.write("Number of training samples:", X_train.shape[0])
        st.write("Number of testing samples:", X_test.shape[0])

        # Save the model params as a json file
        with open('data/metadata/model_params.json', 'w') as json_file:
            json.dump(params, json_file)

        ''' RUNNING THE MACHINE LEARNING MODELS '''
        if pred_type == "Regression":
            st.write("Running Regression Models on Sample")

            # Table to store model and accurcy
            # Test options and evaluation metric
            num_folds = 10
            seed = 7
            scoring = 'accuracy'
            model_r2 = []
            model_r2.append(('LR', LogisticRegression()))
            model_r2.append(('LDA', LinearDiscriminantAnalysis()))
            model_r2.append(('KNN', KNeighborsClassifier()))
            model_r2.append(('CART', DecisionTreeClassifier()))
            model_r2.append(('NB', GaussianNB()))
            model_r2.append(('SVM', SVC()))

            results = []
            names = []
            maxvalue=[]

            st.write("Find the Accuracy using Mean and Standard Deviation")
            for name, model in model_r2:
                kfold = KFold(n_splits=num_folds, random_state=seed, shuffle=True)
                cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)
                results.append(cv_results)
                names.append(name)
                #st.write(maxvalue)
                msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
                maxvalue.append(cv_results.mean())
                st.write(msg)
            res_max=max(maxvalue)
            max_pos=maxvalue.index(res_max)
            st.write("Maximum value of Mean in Regression Algo is ",names[max_pos],res_max)
            #st.write("Maximum Value of Mean is ",res_max)
            #st.write("So will go with maximum value, before that we will go with Normalize of data and Evaluate Algo")
            # Compare Algorithms
            fig = pyplot.figure()
            fig.suptitle('Scaled Algorithm Comparison')
            ax = fig.add_subplot(111)
            pyplot.boxplot(results)
            ax.set_xticklabels(names)
            st.pyplot(fig)
            pyplot.show()
            #######
            if names[max_pos] == "LR":
                st.subheader("Logistic Regression Model")
                Lkfold = KFold(n_splits=2, random_state=22, shuffle=True)
                Lmodel = LogisticRegression()
                st.write("Accuracy Check for Logistic as per spot check of Algo")
                scoring = 'accuracy'
                results = cross_val_score(Lmodel, X_train, y_train, cv=Lkfold, scoring=scoring)
                st.write("Accuracy: %.3f (%.3f)" % (results.mean(), results.std()))
                st.write("prediction on test data")
                ns_probs = [0 for _ in range(len(y_test))]
                Lmodel.fit(X_train, y_train)
                predicted = Lmodel.predict(X_test)
                # preds = np.argmax(predicted, axis=1)
                st.write("Accuracy {0:.2f}%".format(100 * accuracy_score(predicted, y_test)))
                st.write(confusion_matrix(y_test, predicted))
                #plot_confusion_matrix(estimator=Lmodel, X=X_test, y_true=y_test,display_labels=["False", "True"])
                #st.pyplot(fig)
                st.write(classification_report(y_test, predicted))
                ########
                #######
            if names[max_pos] == "LDA":
                 st.subheader("Linear Discrement Analysis")
                 Lkfold = KFold(n_splits=2, random_state=22, shuffle=True)
                 Lmodel = LinearDiscriminantAnalysis()
                 st.write("Accuracy Check for LDA as per spot check of Algo")
                 scoring = 'accuracy'
                 results = cross_val_score(Lmodel, X_train, y_train, cv=Lkfold, scoring=scoring)
                 st.write("Accuracy: %.3f (%.3f)" % (results.mean(), results.std()))
                 st.write("prediction on test data")
                 ns_probs = [0 for _ in range(len(y_test))]
                 Lmodel.fit(X_train, y_train)
                 predicted = Lmodel.predict(X_test)
                 # preds = np.argmax(predicted, axis=1)
                 st.write("Accuracy {0:.2f}%".format(100 * accuracy_score(predicted, y_test)))
                 st.write(confusion_matrix(y_test, predicted))
                 # plot_confusion_matrix(estimator=Lmodel, X=X_test, y_true=y_test,display_labels=["False", "True"])
                 # st.pyplot(fig)
                 st.write(classification_report(y_test, predicted))
                 ########
            if names[max_pos] == "KNN":
                st.subheader("K-Nearest Neighbors Regression")
                Lkfold = KFold(n_splits=2, random_state=22, shuffle=True)
                Kmodel = KNeighborsRegressor()
                st.write("Accuracy Check for KNN as per spot check of Algo")
                scoring = 'neg_mean_squared_error'
                results = cross_val_score(Kmodel, X_train, y_train, cv=Lkfold, scoring=scoring)
                st.write("Negative Mean Squared Error: %.3f (%.3f)" % (results.mean(), results.std()))
                st.write("Predicting and checking the accuracy")
                Kmodel.fit(X_train, y_train)
                predicted = Kmodel.predict(X_test)
                st.write("Next, we'll check the model prediction accuracy.")
                score = Kmodel.score(X_test, y_test)
                st.write("Score is ", score)
                mse = mean_squared_error(y_test, predicted)
                st.write("Mean Squared Error:", mse)
                rmse = math.sqrt(mse)
                st.write("Root Mean Squared Error:", rmse)
                st.write("Finally, we'll plot the predicted result.")
                #fig=plt.scatter(X_test, y_test, s=5, color="blue", label="original")
                #plt.plot(x_ax, predicted, lw=1.5, color="red", label="predicted")
                #st.plotly_chart(fig)
            if names[max_pos] == "CART":
                st.subheader("Classification and Regression Tree")
                Lkfold = KFold(n_splits=2, random_state=22, shuffle=True)
                Cmodel = DecisionTreeRegressor()
                st.write("Accuracy Check for CART as per spot check of Algo")
                scoring = 'neg_mean_squared_error'
                results = cross_val_score(Cmodel, X_train, y_train, cv=Lkfold, scoring=scoring)
                st.write("Negative Mean Squared Error: %.3f (%.3f)" % (results.mean(), results.std()))
                st.write("Predicting and checking the accuracy")
                Cmodel.fit(X_train, y_train)
                predicted = Cmodel.predict(X_test)
                st.write("Next, we'll check the model prediction accuracy.")
                score = Cmodel.score(X_test, y_test)
                st.write("Score is ", score)
                mse = mean_squared_error(y_test, predicted)
                st.write("Mean Squared Error:", mse)
                rmse = math.sqrt(mse)
                st.write("Root Mean Squared Error:", rmse)
                st.write("Finally, we'll plot the predicted result.")
            if names[max_pos] == "NB":
                st.subheader("Naive Bayes Model")
                Lkfold = KFold(n_splits=2, random_state=22, shuffle=True)
                Lmodel = GaussianNB()
                st.write("Accuracy Check for Naive Bayes as per spot check of Algo")
                scoring = 'accuracy'
                results = cross_val_score(Lmodel, X_train, y_train, cv=Lkfold, scoring=scoring)
                st.write("Accuracy: %.3f (%.3f)" % (results.mean(), results.std()))
                st.write("prediction on test data")
                ns_probs = [0 for _ in range(len(y_test))]
                Lmodel.fit(X_train, y_train)
                predicted = Lmodel.predict(X_test)
                # preds = np.argmax(predicted, axis=1)
                st.write("Accuracy {0:.2f}%".format(100 * accuracy_score(predicted, y_test)))
                st.write(confusion_matrix(y_test, predicted))
                # plot_confusion_matrix(estimator=Lmodel, X=X_test, y_true=y_test,display_labels=["False", "True"])
                # st.pyplot(fig)
                st.write(classification_report(y_test, predicted))
            if names[max_pos] == "SVM":
                st.subheader("Support Vector Machine Model")
                Lkfold = KFold(n_splits=2, random_state=22, shuffle=True)
                Lmodel = SVC()
                st.write("Accuracy Check for Support Vector Machine as per spot check of Algo")
                scoring = 'accuracy'
                results = cross_val_score(Lmodel, X_train, y_train, cv=Lkfold, scoring=scoring)
                st.write("Accuracy: %.3f (%.3f)" % (results.mean(), results.std()))
                st.write("prediction on test data")
                ns_probs = [0 for _ in range(len(y_test))]
                Lmodel.fit(X_train, y_train)
                predicted = Lmodel.predict(X_test)
                # preds = np.argmax(predicted, axis=1)
                st.write("Accuracy {0:.2f}%".format(100 * accuracy_score(predicted, y_test)))
                st.write(confusion_matrix(y_test, predicted))
                # plot_confusion_matrix(estimator=Lmodel, X=X_test, y_true=y_test,display_labels=["False", "True"])
                # st.pyplot(fig)
                st.write(classification_report(y_test, predicted))

            st.subheader("Evaluate Algorithms: Standardize/Normalize data")
            st.write("To avoid data leakage when we transform the data. A good way to avoid leakage is to use pipelines")
            st.write("standardize the data and build the model for each fold in the cross-validation test harness.")
            st.write("That way we can get a fair estimation of how each model with standardized data might perform on unseen data.")
            st.subheader("Standardize the dataset")
            pipelines = []
            pipelines.append(('ScaledLR', Pipeline([('Scaler', StandardScaler()), ('LR', LogisticRegression())])))
            pipelines.append(
                ('ScaledLDA', Pipeline([('Scaler', StandardScaler()), ('LDA', LinearDiscriminantAnalysis())])))
            pipelines.append(('ScaledKNN', Pipeline([('Scaler', StandardScaler()), ('KNN', KNeighborsClassifier())])))
            pipelines.append(
                ('ScaledCART', Pipeline([('Scaler', StandardScaler()), ('CART', DecisionTreeClassifier())])))
            pipelines.append(('ScaledNB', Pipeline([('Scaler', StandardScaler()), ('NB', GaussianNB())])))
            pipelines.append(('ScaledSVM', Pipeline([('Scaler', StandardScaler()), ('SVM', SVC())])))
            results = []
            names = []
            maxvalue=[]
            st.write("Find the Accuracy using Mean and Standard Deviation")
            for name, model in pipelines:
                kfold = KFold(n_splits=num_folds, random_state=seed, shuffle=True)
                cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)
                results.append(cv_results)
                names.append(name)
                msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
                maxvalue.append(cv_results.mean())
                st.write(msg)
            res_max = max(maxvalue)
            max_pos = maxvalue.index(res_max)
            st.write("Maximum value of Mean in Regression Algo is ", names[max_pos], res_max)
            st.write("Compare Algorithms After Normalized of data")
            fig = pyplot.figure()
            fig.suptitle('Scaled Algorithm Comparison After Standardize/Normalize data')
            ax = fig.add_subplot(111)
            pyplot.boxplot(results)
            ax.set_xticklabels(names)
            st.pyplot(fig)
            pyplot.show()
            st.subheader("  Ensemble Methods   ")
            st.write(" evaluate four different ensemble machine learning")
            st.write(" algorithms, two boosting and two bagging methods:")
            st.write(" 1. Boosting Methods: AdaBoost (AB) and Gradient Boosting (GBM).")
            st.write(" 2. Bagging Methods: Random Forests (RF) and Extra Trees (ET).")

            st.write("Ensembles taking mean and standard deviation to get accuracy ")
            ensembles = []
            ensembles.append(('AB', AdaBoostClassifier()))
            ensembles.append(('GBM', GradientBoostingClassifier()))
            ensembles.append(('RF', RandomForestClassifier()))
            ensembles.append(('ET', ExtraTreesClassifier()))
            results = []
            names = []
            maxvalue=[]
            for name, model in ensembles:
                kfold = KFold(n_splits=num_folds, random_state=seed, shuffle=True)
                cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring=scoring)
                results.append(cv_results)
                names.append(name)
                msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
                maxvalue.append(cv_results.mean())
                st.write(msg)
            res_max = max(maxvalue)
            max_pos = maxvalue.index(res_max)
            st.write("Maximum value of Mean in Ensemble Algo is ", names[max_pos], res_max)
            fig = pyplot.figure()
            fig.suptitle('Ensemble Algorithm Comparison')
            ax = fig.add_subplot(111)
            pyplot.boxplot(results)
            ax.set_xticklabels(names)
            st.pyplot(fig)
            pyplot.show()

            # Save one of the models
            #if dt_r2 > lr_r2:
                # save decision tree 
                #joblib.dump(dt_model, 'data/metadata/model_reg.sav')
            #else:
                #joblib.dump(lr_model, 'data/metadata/model_reg.sav')

            # Make a dataframe of results 
            #results = pd.DataFrame(model_r2, columns=['Models', 'R2 Score']).sort_values(by='R2 Score', ascending=False)
            #st.dataframe(results)
        
        if pred_type == "Classification":
            st.write("Running Classfication Models on Sample")

            # Table to store model and accurcy 
            model_acc = []

            # Linear regression model 
            lc_model = LogisticRegression()
            lc_model.fit(X_train, y_train)
            lc_acc = lc_model.score(X_test, y_test)
            model_acc.append(['Linear Regression', lc_acc])

            # Decision Tree model 
            dtc_model = DecisionTreeClassifier()
            dtc_model.fit(X_train, y_train)
            dtc_acc = dtc_model.score(X_test, y_test)
            model_acc.append(['Decision Tree Regression', dtc_acc])

            # Save one of the models 
            if dtc_acc > lc_acc:
                # save decision tree 
                joblib.dump(dtc_model, 'data/metadata/model_classification.sav')
            else: 
                joblib.dump(lc_model, 'data/metadata/model_classificaton.sav')

            # Make a dataframe of results 
            results = pd.DataFrame(model_acc, columns=['Models', 'Accuracy']).sort_values(by='Accuracy', ascending=False)
            st.dataframe(results)


        

    ################## Group 4

    if rg_method == 'Other Methods':
        """_summary_
        Args:
            data_obj (_type_): _description_
        """

        # Displaying the Dataframe
        st.dataframe(rg_df)
        # Displaying the shape of the Dataframe
        st.write(rg_df.shape)
        # Button for downloading the Dataframe
        st.download_button(label="Download data as CSV",
                    data=rg_df.to_csv(index=False),
                    file_name='Preprocessed Dataset.csv',
                    mime='text/csv')

        # creating a copy of the current dataframe
        rg_df = data_obj.df.copy()
        # Using this Dataframe to create an instance of the Regression class
        regg_obj = Regression(rg_df)

        for col in rg_df.columns:
            if rg_df[col].dtype == 'object':
                try:
                    rg_df[col] = pd.to_datetime(rg_df[col])
                except ValueError:
                    pass

        st.write(
            '<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;}</style>',
            unsafe_allow_html=True)


        with st.container():
            # Creating three columns for Data Description
            c1, c2, c3 = st.columns(3)

            # Left Column shows the data types of every column
            with c1:
                st.subheader("Dataframe's datatypes")
                st.dataframe(rg_df.dtypes.astype(str))

            # Middle Column shows the correlation heatmap (the correlation matrix shows a "stair" structure)
            with c2:
                st.subheader("Correlation heatmap")
                regg_obj.plot_heatmap_correlation()
            # Right Column shows a description of the internal stored Dataframe (using the pd.Dataframe.describe() function)
            with c3:
                st.subheader("Dataframe description")
                st.dataframe(regg_obj.get_dataframe_description())

        # Creating the second row of the page
        with st.container():
            st.subheader('Select input settings')
            # Creating three columns for the Model Inputs
            cc1, cc2, cc3 = st.columns(3)

            # In the left column are input option for the preparation of the dataset
            with cc1:
                tt_proportion = st.slider('Portion of test data', 0.0, 1.0, 0.2, 0.05)
                del_dup = st.checkbox('Deleting duplicates?')
                scale = st.checkbox('Scale data?')
                del_na = st.checkbox('Get rid of N/A values?')

            # In the middel column is the chosen target column
            with cc2:
                columns_list = list(rg_df.columns)
                selected_column = st.selectbox("Column to regress:", columns_list)

            # In the right column is the selected regression method
            with cc3:
                regression_list = ["Support Vector Machine Regression", "Elastic Net Regression","Ridge Regression",
                                "Linear Regression","Stochastic Gradient Descent Regression"]
                selected_regressor = st.selectbox("Select a regression method:", regression_list)
                # Depending on the selected regression method are different options to setup
                # Following options are given for the Support Vector Machine:
                if selected_regressor == "Support Vector Machine Regression":
                    # Kernel to be selected
                    kernel_list = ['linear', 'poly', 'rbf', 'sigmoid', 'precomputed']
                    selected_kernel = st.selectbox("Kernel:", kernel_list)
                    # Degree (Degree of the polynomial kernel function) to be selected
                    degree_default = 3
                    degree_value = st.number_input('Degree of the polynomial kernel function', 1, 10, degree_default, 1)
                    # svmNumber to be selected (An upper bound on the fraction of training errors and a lower bound of the fraction of
                    # support vectors, should be in the interval (0, 1), defaults to 0.5)
                    svmNumber_default = 0.5
                    svmNumber_value = st.slider('SVM Number', 0.0, 1.0, svmNumber_default, 0.1)
                    # Maximal number of Iterations to be selected
                    # if -1 = no limit
                    maxIterations_default = -1
                    maxIterations_value = st.number_input('Maximum of Iterations', -1, 1000, maxIterations_default, 1)

                # Optional regression method
                if selected_regressor == "Elastic Net Regression":
                    pass

                # Following options are given for the Support Vector Machine:
                if selected_regressor == "Ridge Regression":
                    # Solver to be selected
                    # defaults to 'auto'
                    solver_list = ['auto', 'svd', 'cholesky', 'lsqr', 'sparse_cg', 'sag', 'saga', 'lbfgs']
                    selected_solver = st.selectbox("Solver:", solver_list)

                    # Maximum number of iterations for conjugate gradient solver, defaults to 15000
                    maxIterations_default = 15000
                    maxIterations_value = st.number_input('Maximum of Iterations', 1, 50000, maxIterations_default, 100)

                # Optional regression method
                if selected_regressor == "Linear Regression":
                        pass

                # Following options are given for the Stochastic Gradient Descent Regression:
                if selected_regressor == "Stochastic Gradient Descent Regression":
                    # The maximum number of passes over the training data, defaults to 1000
                    maxIterations_default = 1000
                    maxIterations_value = st.number_input('Maximum of Iterations', 1, 10000, maxIterations_default, 100)


        with st.container():
            # The last row
            cc1, cc2, cc3= st.columns([1,2,2])
            # Scaling the dataframe and storing it in a separated Datframe for later usage
            rg_df_norm = (rg_df - np.min(rg_df)) / (np.max(rg_df) - np.min(rg_df))
            regg_obj_norm = Regression(rg_df_norm)

            with cc1:
                st.subheader('Model Training')
                submit_button = st.button(label='Train Model')

                if submit_button:
                    with st.spinner("Training models..."):
                        try:
                            if selected_regressor == "Support Vector Machine Regression":
                                ################# Support Vector Machine Regression with the internal Dataset
                                # Splitting the internal Dataset in a train and test portion
                                regg_obj.split_train_test(label_target=selected_column,
                                                        testsize=tt_proportion,
                                                        random_state=0,
                                                        deleting_na=del_na,
                                                        scaling=scale,
                                                        deleting_duplicates=del_dup)
                                # Building the Support Vector Machine Regression with the internal Dataset
                                st.session_state.model,st.session_state.model_string = regg_obj.build_regression("Support Vector Machine Regression ",
                                                        kernel=selected_kernel,
                                                        degree=degree_value,
                                                        svmNumber=svmNumber_value,
                                                        maxIterations=maxIterations_value)
                                # Outputting the regression plot and regression metrics
                                st.session_state.fig = regg_obj.plot_regression_1()
                                #################
                                # Splitting the scaled Dataset in a train and test portion
                                regg_obj_norm.split_train_test(label_target=selected_column,
                                                        testsize=tt_proportion,
                                                        random_state=0,
                                                        deleting_na=del_na,
                                                        scaling=False,
                                                        deleting_duplicates=del_dup)
                                # Building the Support Vector Machine Regression with the scaled Dataset
                                regg_obj_norm.build_regression("Support Vector Machine Regression ",
                                                        kernel=selected_kernel,
                                                        degree=degree_value,
                                                        svmNumber=svmNumber_value,
                                                        maxIterations=maxIterations_value)
                                # Outputting the Sensitivity plot on the scaled Dataset
                                st.session_state.fig_norm = regg_obj_norm.MainEffectsPlot()

                            if selected_regressor == "Elastic Net Regression":
                                ###################### Elastic Net Regression with the internal Dataset
                                # Splitting the internal Dataset in a train and test portion
                                regg_obj.split_train_test(label_target=selected_column,
                                                        testsize=tt_proportion,
                                                        random_state=0,
                                                        deleting_na=del_na,
                                                        scaling=scale,
                                                        deleting_duplicates=del_dup)
                                # Building the Elastic Net Regression with the internal Dataset
                                st.session_state.model,st.session_state.model_string = regg_obj.build_regression("Elastic Net Regression ")
                                # Outputting the regression plot and regression metrics
                                st.session_state.fig = regg_obj.plot_regression_1()
                                ######################
                                regg_obj_norm.split_train_test(label_target=selected_column,
                                                        testsize=tt_proportion,
                                                        random_state=0,
                                                        deleting_na=del_na,
                                                        scaling=False,
                                                        deleting_duplicates=del_dup)
                                regg_obj_norm.build_regression("Elastic Net Regression ")
                                # Outputting the Sensitivity plot on the scaled Dataset
                                st.session_state.fig_norm = regg_obj_norm.MainEffectsPlot()

                            if selected_regressor == "Ridge Regression":
                                ###################### Ridge Regression with the internal Dataset
                                # Splitting the internal Dataset in a train and test portion
                                regg_obj.split_train_test(label_target=selected_column,
                                                        testsize=tt_proportion,
                                                        random_state=0,
                                                        deleting_na=del_na,
                                                        scaling=scale,
                                                        deleting_duplicates=del_dup)
                                # Building the Ridge Regression with the internal Dataset
                                st.session_state.model,st.session_state.model_string = regg_obj.build_regression("Ridge Regression ",
                                                        max_iter=maxIterations_value,
                                                        solver=selected_solver)
                                # Outputting the regression plot and regression metrics
                                st.session_state.fig = regg_obj.plot_regression_1()
                                ######################
                                # Splitting the scaled Dataset in a train and test portion
                                regg_obj_norm.split_train_test(label_target=selected_column,
                                                        testsize=tt_proportion,
                                                        random_state=0,
                                                        deleting_na=del_na,
                                                        scaling=False,
                                                        deleting_duplicates=del_dup)
                                # Building the Ridge Regression with the scaled Dataset
                                regg_obj_norm.build_regression("Ridge Regression ",
                                                        max_iter=maxIterations_value,
                                                        solver=selected_solver)
                                # Outputting the Sensitivity plot on the scaled Dataset
                                st.session_state.fig_norm = regg_obj_norm.MainEffectsPlot()

                            if selected_regressor == "Linear Regression":
                                ###################### Linear Regression with the internal Dataset
                                # Splitting the internal Dataset in a train and test portion
                                regg_obj.split_train_test(label_target=selected_column,
                                                        testsize=tt_proportion,
                                                        random_state=0,
                                                        deleting_na=del_na,
                                                        scaling=scale,
                                                        deleting_duplicates=del_dup)
                                # Building the Linear Regression with the internal Dataset
                                st.session_state.model,st.session_state.model_string = regg_obj.build_regression("Linear Regression ")
                                # Outputting the regression plot and regression metrics
                                st.session_state.fig = regg_obj.plot_regression_1()
                                ###################### Linear Regression with the scaled Dataset
                                # Splitting the scaled Dataset in a train and test portion
                                regg_obj_norm.split_train_test(label_target=selected_column,
                                                        testsize=tt_proportion,
                                                        random_state=0,
                                                        deleting_na=del_na,
                                                        scaling=False,
                                                        deleting_duplicates=del_dup)
                                # Building the Linear Regression with the scaled Dataset
                                regg_obj_norm.build_regression("Linear Regression ")
                                # Outputting the Sensitivity plot on the scaled Dataset
                                st.session_state.fig_norm = regg_obj_norm.MainEffectsPlot()

                            if selected_regressor == "Stochastic Gradient Descent Regression":
                                ###################### Stochastic Gradient Descent Regression with the internal Dataset
                                # Splitting the internal Dataset in a train and test portion
                                regg_obj.split_train_test(label_target=selected_column,
                                                        testsize=tt_proportion,
                                                        random_state=0,
                                                        deleting_na=del_na,
                                                        scaling=scale,
                                                        deleting_duplicates=del_dup)
                                # Building the Stochastic Gradient Descent Regression with the internal Dataset
                                st.session_state.model,st.session_state.model_string = regg_obj.build_regression("Stochastic Gradient Descent Regression ",
                                                        max_iter=maxIterations_value)
                                # Outputting the regression plot and regression metrics
                                st.session_state.fig = regg_obj.plot_regression_1()
                                ######################
                                # Splitting the scaled Dataset in a train and test portion
                                regg_obj_norm.split_train_test(label_target=selected_column,
                                                        testsize=tt_proportion,
                                                        random_state=0,
                                                        deleting_na=del_na,
                                                        scaling=False,
                                                        deleting_duplicates=del_dup)
                                # Building the Stochastic Gradient Descent Regression with the scaled Dataset
                                regg_obj_norm.build_regression("Stochastic Gradient Descent Regression ",
                                                        max_iter=maxIterations_value)
                                # Outputting the Sensitivity plot on the scaled Dataset
                                st.session_state.fig_norm = regg_obj_norm.MainEffectsPlot()


                        except ValueError as e:
                            st.error("Please check if you selected a dataset and column suitable for the regression "
                                     "model.\n Remember that the regression model only works with numerical data")
                try:
                    # Outputting the Regression Methods metrics
                    st.metric(st.session_state.model_string[0]+str(" --> RMSE"),st.session_state.model_string[1])
                    st.metric(st.session_state.model_string[0]+str(" --> R2-Score"),st.session_state.model_string[2])
                except AttributeError as e:
                    pass

            with cc2:
                st.subheader('Model Graphs')
                try:
                    # Plotting the Regresssion Plot
                    st.caption("Actual- vs Expected Target Value")
                    st.pyplot(st.session_state.fig)
                    # Plotting the Sensitivity Plot
                    st.caption("Main Effects Plot")
                    st.pyplot(st.session_state.fig_norm)
                except:
                    pass

            with cc3:
                # This Column creates the Ability for the User
                # to use the trained model to make a prediction
                st.subheader('Model Prediction')
                columns_list = list(rg_df.columns)
                parameter = []

                for i , column in enumerate(columns_list):
                    if not column == selected_column:
                        parameter.append(st.number_input(label=column,
                                                        min_value=0.0,
                                                        max_value=100.0,
                                                        value=0.0,
                                                        step=1.0))

                submit_button = st.button(label='Predict')
                if submit_button:
                    try:
                        prediction = st.session_state.model.predict(pd.DataFrame([parameter]))
                        st.metric("Prediction of "+selected_column,round(prediction[0],4))
                    except:
                        st.write("No model found!")




if __name__ == "__main__":
   main()