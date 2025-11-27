# Import necessary libraries
import json
import joblib
import numpy as np
import math
import pandas as pd
import streamlit as st

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


# Custom classes 
from .utils import isNumerical
import os

def app():
    """This application helps in running machine learning models without having to write explicit code 
    by the user. It runs some basic models and let's the user select the X and y variables. 
    """
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
