from datetime import datetime
from matplotlib import collections
import collections
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.core.fromnumeric import shape
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error as MSE
from typing import NamedTuple
import seaborn as sn
import streamlit as st #streamlit backend


class NN_TimeSeries_Reg:
    """Neural Network Time Series Regressor Class:

    This Class contains the methods used for Neural Network Regression using MLP Regressor for Timeseries data 

    Class input parameters:

    :param df: The input data frame
    :type df: Pandas DataFrame
    :param NN_Inputs: Tuple of parameters for the Regressor clarified by the user
    :type NN_Inputs: Named Tuple
    :param dependant_var_index: The index of the target column in the df for the Regression
    :type dependant_var_index: int
    :param time_index: The index of the column with timeseries data in the df
    :type time_index: int

    

    Class Output Parameters:

    :param y_pred: The resulting output of the Regression test
    :type y_pred: float 
    :param y_actual: The expected output of the Regression test
    :type y_actual: float 
    :param length: The length of the output of the Regression test set
    :type length: int 
    :param mean_squared_error: The MSE of the y_pred with respect to the y_actual
    :type mean_squared_error: float 
    :param Train_score: Model Score (R^2) on the Training data
    :type Train_score: float 
    :param test_score: Model Score (R^2) on the Testing data  
    :type test_score: float
    :param model: The MLP Regressor model created using the specified inputs
    :type model: MLPRegressor
    :param group_object: Output array of the list of unique values in a specified column for grouping
    :type group_object: dataframe
    :param Error_message: Error message if an exception was encountered during the processing of the code
    :type Error_message: str
    :param flag: internal flag for marking if an error occurred while processing a previous method
    :type flag: bool
    """
    y_pred:                     float # resulting output
    y_actual:                   float # expected output
    length:                     int   # length of y_test
    mean_squared_error:         float # mean square error
    Train_score:                float  
    X_test:                     float
    test_score:                 float
    model:                      MLPRegressor
    Error_message:              str
    flag:                       bool
    group_object:               np.ndarray

    dependant_var_index =0
    time_index=0
    #self.NN_Inputs = Regressor_Inputs
    # = Regressor_Outputs
    flag=False
    Error_message='No Error occurred in the processing'
    
    df:pd.DataFrame # original dataframe
    internal_df:pd.DataFrame   # Internal Df

    #Constructor
    #External inputs are the Data frame object, the Named Tuple of NN_Inputs, the index of the dependant variable in the Data frame
    # And the index of the column containing date time information
    def __init__(self,df,NN_Inputs,dependant_var_index,time_index):
        """Class Constructor:

        :param df: The input data frame
        :type df: Pandas DataFrame
        :param NN_Inputs: Tuple of parameters for the Regressor clarified by the user
        :type NN_Inputs: Named Tuple
        :param dependant_var_index: The index of the target column in the df for the Regression
        :type dependant_var_index: int
        :param time_index: The index of the column with timeseries data in the df
        :type time_index: int
        """
        self.df=df
        self.NN_Inputs=NN_Inputs
        self.time_index=time_index
        self.k=dependant_var_index
        # if the group falg is not true, that means that the user wants to use the entire dataframe 
        if self.NN_Inputs.group !=True:
            self.internal_df=self.df
            self.internal_df=self.internal_df.dropna()
            self.internal_df.drop_duplicates(keep='first',inplace=True) 
            self.features()
    
    def listing(self,i):
        """Method for Creating unique values list:

        This method takes a column index and outputs a dataframe with the list of unique values in this specific column in order for the user to choose a group to run the regression on.

        :param i: Unique Values column index
        :type i: int
        """
        try:
            self.col_name=self.df.columns[i]
            self.group_object=collections.Counter(self.df[self.col_name])
            self.group_object = pd.DataFrame.from_dict(self.group_object, orient='index').reset_index()
            print(self.group_object.head(6))
        except Exception as e:
            self.Error_message='Error in Handling Method: ' + str(e)
            self.flag=True

    def group(self,i):
        """Grouping method:

        This method gets an index of the value the user wants to group the data on from the list of unique values created by the listing method, It then creates the dataframe subset with this group only for the regression to use.


        :param i: index of the group identifier
        :type i: int
        """
        try:
            self.internal_df=self.df.loc[self.df[self.col_name]==self.group_object.iloc[i,0]]
            self.internal_df=self.internal_df.dropna()
            self.internal_df.drop_duplicates(keep='first',inplace=True) 
            self.features()
            print(self.internal_df.head(5))
        except Exception as e:
            self.Error_message='Error in Handling Method: ' + str(e)
            self.flag=True
    

    def features(self):
        """Extracting features method:
        This method deals with Internal_df parameter in the Class, It extracts datetime information from datetime column into 6 separate columns for "Year,Month,Day,Hour,Minute,Second".

        This method is called internally in one of 2 separate places:
            1. During the Class Instance Creation if the user doesn't wish to group data based on a specific value in a column.
            2. In the grouping method after the creation of the subset dataframe based on the specific group identifier if the grouping flag is True.
          
        After these features are extracted the data is reshuffled and then split into X and Y dataframes with the X being the 6 columns including datetime information and the Y the target column for the regression.

        The X,Y dataframes are then fed to the "Regressor" Method.
        """
        try:
            
            nxm=shape(self.internal_df)
            n=nxm[0]
            m=nxm[1]
            df2=self.internal_df.columns[self.time_index]
            date_time_column=self.internal_df[[df2]]
            X=np.ndarray(shape=(n,6),dtype=float, order='F')
            #for l in range (0,6):
            for a in range(0,n):
                #date_time_obj = datetime.strptime(date_time_column.iloc[a,0], '%m/%d/%Y %H:%M')

                date_time_obj = date_time_column.iloc[a,0]
                year=date_time_obj.year
                month=date_time_obj.month
                day=date_time_obj.day
                hour=date_time_obj.hour
                minute=date_time_obj.minute
                second=date_time_obj.second
                X[a,0]=year
                X[a,1]=month
                X[a,2]=day
                X[a,3]=hour
                X[a,4]=minute
                X[a,5]=second


                #X[a,l]=date_time_obj[a]
            #X=np.ndarray(shape=(n,m),dtype=int, order='F')
        


            Y=np.ndarray(shape=(n,1), dtype=float, order='F')
            Y[:,0]=self.internal_df.iloc[:,self.k]

            y_t=np.ravel(Y)
            df_internal=pd.DataFrame(data=X,columns=["Year","Month","Day", "Hour","Minute","Second"])
            df_internal=pd.concat([df_internal,pd.DataFrame(y_t,columns=["y"])],axis=1)
            df1=df_internal.sample(frac=1,random_state=1).reset_index(drop=True)

            #cyc=pd.DataFrame(data=x,columns=["Year","Month","Day", "Hour","Minute","Second"])
            
            self.X_new=df1.drop(['y'],axis=1)
            self.Y_new=df1.y
        except Exception as e:
            self.Error_message='Error in Handling Method: ' + str(e)
            self.flag=True
        
    def Regressor(self):
        """ 
        Regressor Creation Method:

        This method splits the data into train and test sets, then creates the MLP regressor based on the user inputs from NN_Inputs Named Tuple.
        
        The data is Normalized using MinMaxScaler() and then the method fits the model and returns some metrics for the performance of the model on the test and train data sets.

        :return: Modified set of class parameters
        
        """

        if (self.flag) !=True:
            try:

                X_train, self.X_test, y_train, self.y_actual= train_test_split(self.X_new,self.Y_new,test_size=self.NN_Inputs.test_size,shuffle=False, random_state=109)
                self.model = MLPRegressor(hidden_layer_sizes = self.NN_Inputs.hidden_layers,
                                    activation = self.NN_Inputs.activation_fun, solver = self.NN_Inputs.solver_fun,
                                    max_iter = self.NN_Inputs.Max_iterations,alpha= 0.01, early_stopping=True, learning_rate= 'constant', learning_rate_init= 0.1, random_state= 1, tol= 0.01, verbose= False)
                from sklearn.preprocessing import MinMaxScaler
                scaler = MinMaxScaler()
                X_train_norm = scaler.fit_transform(X_train)
                X_test_norm = scaler.fit_transform(self.X_test)

                self.model.fit(X_train_norm,y_train)
                self.Train_score= self.model.score(X_train_norm,y_train)
                self.test_score= self.model.score(X_test_norm,self.y_actual)
                #coeff=self.model.coefs_


                self.y_pred = self.model.predict(X_test_norm)

                y_pred = np.ndarray.tolist(self.y_pred)
                self.length = len(y_pred)

                #Mean squared error and accuracy
                self.mean_squared_error = MSE(self.y_actual,
                self.y_pred)
            except Exception as e:
                self.Error_message= 'Error in Regressor Creation: ' + str(e)
                self.flag=True
                st.warning(self.Error_message)
                print(self.Error_message)

                self.Train_score= 'Refer To error in Regressor Creation'
                self.test_score= 'Refer To error in Regressor Creation'
                

                self.y_actual='Refer To error in Regressor Creation'
                self.y_pred = 'Refer To error in Regressor Creation'

                self.y_pred = 'Refer To error in Regressor Creation'
                self.length = 'Refer To error in Regressor Creation'
                
                #Mean squared error and accuracy
                self.mean_squared_error = 'Refer To error in Regressor Creation'
        else:
            print(self.Error_message)

            st.warning(self.Error_message)
            self.Train_score= 'Refer To error in Handling Method'
            self.test_score= 'Refer To error in Handling Method'
            #self.coeff=self.model.coefs_

            self.y_actual='Refer To error in Handling Method'
            self.y_pred = 'Refer To error in Handling Method'

            self.y_pred = 'Refer To error in Handling Method'
            self.length = 'Refer To error in Handling Method'
            
            #Mean squared error and accuracy
            self.mean_squared_error = 'Refer To error in Handling Method'


    def printing(self):
        """Printing Outputs:

        This method prints the chosen metrics to the user after the model is trained and fitted.

        The metrics are:
            1. Model R2 Score on the Training Data
            2. Model R2 Score on the Testing Data
            3. Length of the output array
            4. Root Mean Squared Error 
        """
        #Printing the chosen metrics
        if (self.flag) != True:
            self.Error_message= ' No Error Occurred during prcoessing of the code'
        
        try:
            

            # print('Error Message           ', self.Error_message)
            # #print('expected output:        ', self.y_actual)
            # #print('Predicted Output:       ', self.y_pred)
            # print('Model R2 score on the Training Data: ',  self.Train_score)
            # print('Model R2 score on the Testing Data: ',  self.test_score)

            # print('Root Mean Square error:      ',  round((self.mean_squared_error)**(0.5),8))
            # print('length of output array: ',  self.length)
            st.warning(self.Error_message)
            cc1, cc2 = st.columns(2)
            with cc1:
                # st.metric('Expected output:        ', self.NN_Outputs.y_actual)
                # st.write('Predicted Output:       ', self.NN_Outputs.y_pred)
                st.metric('Model score (R2) on the Training Data:',  round(self.Train_score, 8))
                st.metric('Model score (R2) on the Testing Data:',  round(self.test_score, 8))
            with cc2:
                #st.write('Classification Report: ')
                st.metric('Length of output array: ',  self.length)
                st.metric('RMSE: ',  round((self.mean_squared_error)**(0.5),8))
        except Exception as e:
            self.Error_message = 'Error while printing outputs: ' +str(e)
            self.flag=True
            #print(self.Error_message)
            st.warning(self.Error_message)
        #print('coeff: ',.coeff )

    def plotting(self):
        """Plotting Method:

        This method plots the scatter plot of the predicted vs Expected output to visualize the quality of the regression
        """
        #Plotting a 2D plot of the Regression output with external input i being the field of which we want to plot as x-axis
        if self.flag != True:
            try:
                # fig = plt.figure()
                # ax1 = fig.add_subplot(111)

                # ax1.scatter(self.X_test[:,i],self.y_pred, s=10, c='r', marker="o", label='Predicted')
                # ax1.scatter(self.X_test[:,i],self.y_actual, s=10, c='b', marker="o", label='actual')
                # ax1.set_xlabel (self.df.columns[i])
                # ax1.set_ylabel  (self.df.columns[self.k])   
                # ax1.legend()
                # plt.show()
                df=pd.DataFrame({'y_test':self.y_actual,'y_pred':self.y_pred})
                fig = plt.figure(figsize=(10, 4))
                sn.scatterplot(x='y_test',y='y_pred',data=df,label='Real Prediction')
                sn.lineplot(x='y_test',y='y_test',data=df,color='red',alpha=0.5,label='Optimal Prediction')
                plt.title('Expected vs Predicted Output')
                plt.legend()
                plt.show()
                st.pyplot(fig)
            except Exception as e:
                self.Error_message='Error in Plotting Method: ' + str(e)
                self.flag=True
                st.warning(self.Error_message)

class Regressor_Inputs_TS(NamedTuple):
        """
        This class is used to parse inputs from the user into this Named Tuple structure for easy use inside the NN_TimeSeries_Reg class.

        Below is a description of the Named Tuple Elements:

        """
        
        test_size:              float  ;""" Test size percentage"""
        activation_fun:         tuple  ;""" Activation function selection"""
        hidden_layers:          tuple  ;""" Size of hidden layer and number of neurons in each layer"""
        solver_fun:             tuple  ;""" Solver function selection"""
        Max_iterations:         int    ;""" Number of Maximum iterations"""
        group:                  bool   ;""" Flag to know if you want to do grouping on the data or not """

# parking_data = pd.read_csv("D:\MAIT\OOP\Datasets\TimeSeries\dataset.csv",',')

# activation_fun1 = ("identity", "logistic", "tanh", "relu")
# solver_fun1 = ("lbfgs", "sgd", "adam")
# hidden_layers3=(100,20)

# Inputs= Regressor_Inputs_TS(0.1,activation_fun1[3],hidden_layers3,solver_fun1[0],2000,True)

# Regressor1=NN_TimeSeries_Reg(parking_data,Inputs,2,3)

# #X=input("Enter Column number you want to list: ")
# #a=int(X)
# Regressor1.listing(1)
# #print(Regressor1.group_object.iloc[10,0])
# Regressor1.group(2)


# Regressor1.Regressor()
# Regressor1.printing()
# Regressor1.plotting()



#x,y,Y=features(df,0,1)

#print(x[0:15,:])



    
