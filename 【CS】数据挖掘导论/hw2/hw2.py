#environment: datamining
import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression  
from sklearn.svm import SVC
from sklearn.metrics import precision_score
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("house-prices-advanced-regression-techniques/train.csv")

#------------------------------------------------------task1------------------------------------------------------
# train-validation split
train, validation = train_test_split(df, train_size=0.8)
train.to_csv("hw2/train_num.csv")
validation.to_csv("hw2/validate_num.csv")

#------------------------------------------------------task2------------------------------------------------------
# multi-variable linear regression
dfTrain = pd.read_csv("hw2/train_num.csv")
dfValidation = pd.read_csv("hw2/validate_num.csv")

X_train = dfTrain.select_dtypes(include=[int, float])       #select numbers in train_num
X_train.drop(labels=['SalePrice'], axis=1, inplace=True)
X_train.drop(labels=['Id'], axis=1, inplace=True)           #不知道为什么多出来的1列，删掉好了
y_train = dfTrain['SalePrice']
X_test = dfValidation.select_dtypes(include=[int, float])   #select numbers in validation_num
X_test.drop(labels=['SalePrice'], axis=1, inplace=True)
X_test.drop(labels=['Id'], axis=1, inplace=True)            #不知道为什么多出来的1列，删掉好了
y_test = dfValidation['SalePrice'] 

X_train = X_train.apply(lambda x: x.fillna(x.mean()),axis=0)
X_test = X_test.apply(lambda x: x.fillna(x.mean()),axis=0)

feature_cols = X_train.columns.tolist()

#fit model
linreg = LinearRegression()  
model = linreg.fit(X_train, y_train)      
zip(feature_cols, linreg.coef_)      
y_pred = linreg.predict(X_test) 

#MAE&MSE
y = np.array(y_test)
y_hat = np.array(y_pred)
MSE = metrics.mean_squared_error(y, y_hat)
MAE = metrics.mean_absolute_error(y, y_hat)
print("MSE: " + str(MSE))
print("MAE: " + str(MAE))

#------------------------------------------------------task3------------------------------------------------------
# prepare discrete input
X_train = dfTrain.select_dtypes(include=[int, float])  ##select numbers in train_num
X_test = dfValidation.select_dtypes(include=[int, float])  ##select numbers in validation_num

classLabel = []
for i in range(len(X_train['SalePrice'])):
    classLabel.append(int(X_train['SalePrice'][i] // 100000) + 1) 
X_train.drop(labels=['SalePrice'], axis=1, inplace=True)
X_train.drop(labels=['Unnamed: 0'], axis=1, inplace=True)      #不知道为什么多出来的1列，删掉好了
y_train = classLabel
classLabel = []
for i in range(len(X_test['SalePrice'])):
    classLabel.append(int(X_test['SalePrice'][i] // 100000) + 1)  
X_test.drop(labels=['SalePrice'], axis=1, inplace=True)
X_test.drop(labels=['Unnamed: 0'], axis=1, inplace=True)        #不知道为什么多出来的1列，删掉好了
y_test = classLabel

X_train = X_train.apply(lambda x: x.fillna(x.mean()), axis=0)
X_test = X_test.apply(lambda x: x.fillna(x.mean()), axis=0)

#svm: linear kernal, SVM precision: 0.8253424657534246
clf = SVC(C=9, kernel='linear', decision_function_shape='ovr')
clf.fit(X_train, y_train)
y_predict = clf.predict(X_test)
print( "SVM with linear kernel precision: ", clf.score(X_test, y_test))

##svm: rbf kernal, SVM precision: 0.7054794520547946
clf = SVC(C=9, kernel='rbf', decision_function_shape='ovr')
clf.fit(X_train, y_train)
y_predict = clf.predict(X_test)
print( "SVM with rbf kernel precision: ", clf.score(X_test, y_test))

##logistic regression: 0.7157534246575342
classfier = LogisticRegression()
classfier.fit(X_train, y_train)
LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                   intercept_scaling=1, l1_ratio=None, max_iter=100,
                   multi_class='warn', n_jobs=None, penalty='l2',
                   random_state=None, solver='warn', tol=0.0001, verbose=0,
                   warm_start=False)
y_predict = classfier.predict(X_test)
print( "Logistic Regression precision: ", precision_score(y_test, y_predict, average='micro'))