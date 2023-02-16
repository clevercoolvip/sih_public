"""
This Python File Consists of Functions to perform Automatic feature Selection 

"""
import os,cv2
import numpy as np
import pandas as pd
from sklearn.feature_selection import VarianceThreshold,SelectKBest,f_regression,f_classif
from sklearn.preprocessing import  MinMaxScaler
from statistics import mean
#from . import  dataCleaner
from sih.Cleaner import dataCleaner

class AutoFeatureSelection: 
    
    def dropHighCorrelationFeatures(X):
        """
        param1: pandas DataFrame

        return: pandas DataFrame

        Function calculates Mutual Correlation of the passed dataframe,
        and drop one of the feature which are highly correlated to each other,
        """
        cor_matrix = X.corr()
        upper_tri = cor_matrix.where(np.triu(np.ones(cor_matrix.shape),k=1).astype(np.bool))
        to_drop = [column for column in upper_tri.columns if any(upper_tri[column] > 0.95)]
        if to_drop!=[]: return X.drop(to_drop, axis=1)
        else: return X
            
    def dropConstantFeatures(X):
        """
        param1: pandas DataFrame
        return: pandas DataFrame
        
        Funciton drops column with low variance/constant values in the field.
        VarianceThreshold function is utilized to filter out such columns from the DataFrame
        and once all such columns are dropped if exists return the dataframe.
        """
        cols=X.columns
        constant_filter = VarianceThreshold(threshold=0).fit(X)
        constcols=[col for col in cols if col not in cols[constant_filter.get_support()]]
        if(constcols!=[]): X.drop(constcols,axis=1,inplace=True)
        return X

    def MainScore(resultscore,dict_class):

        """
        param1: dictionary - feature importance scores 
        param2: Class Object - Dictionary class

        return: dictionary 

        Function calculate and filter dictionary on the basis on the existence of Categorical feature(String type features).
        first the function check whether the dataset had any String categorical feature using previously stored Boolean Class variable .
        If String Categorical feature  exist return aggregate score for the actually features and return it.
        else return passed feature score.
        """
        #average on categorical features
        if(dict_class.ObjectExist):
            objList=dict_class.ObjectList
            for i in objList:
                resultscore[i]=mean(list(dict(filter(lambda item: i in item[0], resultscore.items())).values()))
            #resulting dictionary  
            res = dict()
            for key, val in resultscore.items():
                if not any(ele+"_" in key for ele in objList): res[key] = val
            return res
        else: return resultscore

    #feature importance calculator
    def get_feature_importance(X,Y,score_func,dict_class):
        """
        param1: pandas DataFrame X Features
        param2: pandas Series/Dataframe target dataset
        param3: Sklearn.feature_selection function 
        param4: Class Object of Dictionary Class

        return: pandas DataFrame

        Working:

        Function  Selects Feature on the basis of feature importance using f_classif or f_regression function.
        Feature importance score generated using SelectKBest Function is then Scaled in range of 0 to 1, using MinMaxScaler function
        To manage feature from one hot encoding if any categorical feature exists MainScore function returns an average/mean score for the appropirate feature.
        if the dataframe has less then equal to 2 features return orignal dataframe. else return a short listed dataframe on the basis of 
        categorical features.
        """
        if(X.shape[1]<3):
            dict_class.feature_importance=None
            return X
        else:
            fit = SelectKBest(score_func=score_func, k=X.shape[1]).fit(X,Y)
            dfscores,dfcolumns = pd.DataFrame(fit.scores_),pd.DataFrame(X.columns)
            df = pd.concat([dfcolumns,dfscores],axis=1)
            df.columns = ['features','Score'] 
            df['Score']=MinMaxScaler().fit_transform(np.array(df['Score']).reshape(-1,1))
            main_score=AutoFeatureSelection.MainScore(dict(df.values),dict_class)
            return AutoFeatureSelection.GetAbsoluteList(main_score,X,dict(df.values),dict_class)
    
    def GetAbsoluteList(resdic,dataframe,impmain,dict_class):

        """
        param1: Dictionary
        param2: pandas.DataFrame
        param3: Dictionary

        return: pandas.DataFrame
        """
        keylist=[]
        imp_dict={}
        for key, value in resdic.items():
            if value < 0.01: 
                for key_2 in impmain.keys():
                    if key in key_2:
                        keylist.append(key_2)
            else: imp_dict[key]=value
            
        result_df=dataframe.drop(keylist,axis=1)
        dict_class.feature_importance=imp_dict
        return result_df

    def FeatureSelection(dataframe,target):
        """
        param1: pandas DataFrame
        param2: target column name
        param3: Class object
        
        return : pandas dataframe

        Function starting with performing data cleaning process of the data by calling dataCleaner funciton.
        On the Basis of problem type either Classification or Regression assigns scoring function for feature selection.
        perform a subset for feature set and target set.
        Pass the Feature set/independent features through feature selection process has follow:
            1. Droping Constant Features
            2. Droping Highly Correlated features
            3. Droping Columns on basis of Feature Importance Criteria.
        and finally return List of features to utilize ahead for processing and model training.
        """
        df=dataCleaner(dataframe,dataframe.drop(target,axis=1).columns.to_list(),target)
        #score_func=f_classif if(dict_class.getdict()['problem']["type"]=='Classification') else f_regression
        X=df.drop(target,axis=1)
        Y=df[target]
        X=AutoFeatureSelection.dropConstantFeatures(X)
        X=AutoFeatureSelection.dropHighCorrelationFeatures(X) #if not disable_colinearity else X
        #X=AutoFeatureSelection.get_feature_importance(X,Y,score_func,dict_class)
        #featureList=AutoFeatureSelection.getOriginalFeatures(X.columns.to_list(),dict_class)
        #dict_class.addKeyValue('features',{'X_values':featureList,'Y_values':target})
        return X,Y

    def getOriginalFeatures(featureList,dict_class):
        """
        param1: List
        param2: Class object
        
        return: List

        Function check whether Object type data exists using Class Variable.
        if exists shorts/filters list of feature on the basis of feature importance list.
        and return filtered List of features
        """
        if(dict_class.ObjectExist):
            res,res2= [],[]#List
            for val in featureList: #filter for String categorical field existence.
                if not any(ele+"_" in val for ele in dict_class.ObjectList): res.append(val)
            res=res+dict_class.ObjectList
            for v in res:# filter for Selected String categorical
                if not any (v in ele for ele in featureList): res2.append(v)
            # filter to consider the features
            res3=[i for i in res if i not in res2]
            return res3 
        else: return featureList

    def image_processing(data,targets,resize,dict_class):
        """
        param1: String
        param2: List
        param3: Class object
        return: pandas.DataFrame

        Function return dataframe object which consist of image data and the target.
        """
        training_data,label_mapping=AutoFeatureSelection.create_training_data(data,targets,resize)
        dict_class.original_label=label_mapping
        original_shape=[len(training_data)]
        original_shape.extend(list(training_data[0][0].shape))
        dict_class.original_shape=original_shape
        dict_class.addKeyValue('cleaning',{"resize":resize})
        df = pd.DataFrame(training_data, columns=['image', 'label'])
        return df

    def create_training_data(data,target,resize):
        """
        param1: String
        param2: List
        return: Tuple : (List,dict)

        Function read each image from the provided source and creates a training data whether each image data is mapped with its target label.
        """
        training_data=[]
        label_mapping={}
        for category in target:
            path=os.path.join(data, category)
            class_num=target.index(category)
            label_mapping[class_num]=category
            for img in os.listdir(path):
                try:
                    img_array=cv2.imread(os.path.join(path,img))
                    img_array=cv2.cvtColor(img_array,cv2.COLOR_BGR2RGB)
                    new_array=cv2.resize(img_array,(resize,resize))
                    training_data.append([new_array,class_num])
                except Exception as e:
                    pass
        return (training_data,label_mapping)

    def get_reshaped_image(training_data):
        """
        param1:numpy.array
        return: tuple :(numpy.array,numpy.array)

        Function return required feature and target in a flatten image and label for training 
        """
        lenofimage = len(training_data)
        X, y = [], []
        for categories, label in training_data:
            X.append(categories)
            y.append(label)
        X = np.array(X).reshape(lenofimage,-1)
        y = np.array(y)
        return (X,y)