import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import warnings
warnings.filterwarnings("ignore")

"""
different models are build based on percentage split 70-30% on the merged data
70% data is used to build a model and 30% data is used for testing the model
algorithm used: KNN, SVM, XGBoost, Random forest, Logistic Regression, Decision Tree, and
Naive Bayes 
-----------
input:
    features
    target class
-----------    
output:    
    %accuracy of the test set of each model
-----------    
citation:
https://pythonprogramminglanguage.com/machine-learning-classifier/    
"""
class ModelBuild:

    def __init__(self, keyword):
        df_finance = pd.read_csv("./data/new"+keyword+".csv")
        # print(df_finance.head(5))

        features=pd.DataFrame()
        features['positive_score']=df_finance['positive_score']
        features['negative_score']=df_finance['negative_score']
        features['neutral_score']=df_finance['neutral_score']
        features['open_price']=df_finance['open_price']
        features['close_price']=df_finance['close_price']
        features['high_price']=df_finance['high_price']
        features['low_price']=df_finance['low_price']
        features['volume']=df_finance['volume']
        features['total_words']=df_finance['total_words']
        features['total_hashtag']=df_finance['total_hashtag']
        #print(features)

        target=pd.DataFrame()
        target['class_label']=df_finance['class_label']
        #print(target)

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(features, target, test_size=0.30, random_state=42)
        #print(x_test)

        newfeatures = features
        newfeatures.drop(["high_price", "low_price", "volume", "total_words", "total_hashtag"], axis=1, inplace=True)
        # print(newfeatures)
        self.m_train, self.m_test, self.n_train, self.n_test = train_test_split(newfeatures, target, test_size=0.30, random_state=42)

    # Classify the predicted result
    @staticmethod
    def classify(pred_val):
        if pred_val == 0:
            return "Neutral"
        elif pred_val == -1:
            return "Down"
        else:
            return "Up"

    # KNN model
    def KNN_Model(self, test_feature):
        knn = KNeighborsClassifier(n_neighbors=2)
        knn.fit(self.x_train, self.y_train)
        pred = knn.predict(test_feature)[0]
        accuracy_per = str(round((accuracy_score(self.y_test, knn.predict(self.x_test)) * 100), 2))
        print("KNN model (%)accuracy: " + accuracy_per)
        print("KNN classifies test data: " + ("Down" if pred == -1 else "Up"))
        #print(pred)
        pred_result = ModelBuild.classify(pred)
        resultList = ['KNN', accuracy_per, pred_result]
        return resultList

    # Naive Bayes
    def NB_Model(self, test_feature):
        nb=GaussianNB()
        nb.fit(self.x_train, self.y_train)
        accuracy_per = str(round((accuracy_score(self.y_test,nb.predict(self.x_test)) * 100), 2))
        pred = nb.predict(test_feature)[0]
        print("Naive bayes model (%)accuracy: " + accuracy_per)
        print("Naive bayes classifies test data: " + ("Down" if pred == -1 else "Up"))
        pred_result = ModelBuild.classify(pred)
        resultList = ['Naive Bayes', accuracy_per, pred_result]
        return resultList

    # Logistic Regression
    def Logist_Model(self, test_feature):
        logisticRegr=LogisticRegression()
        logisticRegr.fit(self.x_train, self.y_train)
        predictions=logisticRegr.predict(test_feature)
        predictions=np.where(predictions=='Larceny',1,predictions)
        predictions=predictions.reshape(1,-1)
        accuracy_per = str(round((logisticRegr.score(self.x_test, self.y_test) * 100), 2))
        print("Logistic model (%)accuracy: " + accuracy_per)
        print("Logistic classifies test data: " + ("Down" if predictions == -1 else "Up"))
        pred_result = ModelBuild.classify(predictions)
        resultList = ['Logistic Regression', accuracy_per, pred_result]
        return resultList

    # SVM algorithms
    def SVM_Model(self, test_feature):
        # kernel = ["linear","rbf","ploy"]
        svclassifier = SVC(kernel='linear')
        svclassifier.fit(self.m_train, self.n_train)
        n_pred = svclassifier.predict(test_feature)
        accuracy_per = str(round((accuracy_score(self.n_test, svclassifier.predict(self.m_test)) * 100), 2))
        print("SVM model (%)accuracy: " + accuracy_per)
        print("SVM classifies test data: " + ("Down" if n_pred == -1 else "Up"))
        pred_result = ModelBuild.classify(n_pred)
        resultList = ['SVM', accuracy_per, pred_result]
        return resultList

    # Decision tree classifier
    def DecisionTree_Model(self, test_feature):
        decisionClassifier = DecisionTreeClassifier()
        decisionClassifier = decisionClassifier.fit(self.m_train, self.n_train)
        n_pred = decisionClassifier.predict(test_feature)
        accuracy_per = str(round((accuracy_score(self.n_test, decisionClassifier.predict(self.m_test))*100), 2))
        print("Decision Tree model (%)accuracy: ", accuracy_per)
        print("Decision Tree classifies test data: " + ("Down" if n_pred == -1 else "Up"))
        pred_result = ModelBuild.classify(n_pred)
        resultList = ['Decision Tree', accuracy_per, pred_result]
        return resultList

    # Ensembles algorithm using XGBoost(a boosting algorithm)
    def XGBoost_Model(self, test_feature):
        xgboost = XGBClassifier()
        xgboost.fit(self.m_train,self.n_train)
        xg_pred = xgboost.predict(test_feature)
        accuracy_per = str(round((accuracy_score(self.y_test, xgboost.predict(self.m_test))*100), 2))
        print("XGBoost model (%)accuracy: ", accuracy_per)
        print("XGBoost classifies test data: " + ("Down" if xg_pred == -1 else "Up"))
        pred_result = ModelBuild.classify(xg_pred)
        resultList = ['XGBoost', accuracy_per, pred_result]
        return resultList

    # Random Forest ensemble classifier
    def Rand_Model(self, test_feature):
        randomForest = RandomForestClassifier(n_estimators=100)
        randomForest.fit(self.m_train,self.n_train)
        f_pred=randomForest.predict(test_feature)
        accuracy_per = str(round((accuracy_score(self.n_test, randomForest.predict(self.m_test))*100), 2))
        print("Random forest model (%)accuracy: ", accuracy_per)
        print("Random forest classifies test data: " + ("Down" if f_pred == -1 else "Up"))
        pred_result = ModelBuild.classify(f_pred)
        resultList = ['Random Forest', accuracy_per, pred_result]
        return resultList
