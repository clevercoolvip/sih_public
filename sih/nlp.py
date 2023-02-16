import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import re
nltk.download("stopwords")
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import os


def preprocessing(df, textField, target):
    data = df[textField]
    preprocessed_data = []
    for i in range(len(data)):
        d1 = re.sub('[^a-zA-z]', ' ', str(data[i]))
        d2 = d1.lower()
        tokens = d2.split()
        stemming = PorterStemmer()
        stemmed = [stemming.stem(word) for word in tokens if word not in set(stopwords.words('english'))]
        preprocessed_data.append(stemmed)
    dataframe = pd.DataFrame({"Preprocessed":preprocessed_data, "Label":target})
    dataframe.to_csv("result.csv", index=False)
    path = os.getcwd()
    # print(f"Result saved to {path}")
    dic = {
        "Shape":dataframe.shape,
        "Features":("Regular Expresssion", "Small Case", "Tokenization", "Stemming"),
        "Encoding":textField,
        "Path":path
    }
    return preprocessed_data, dataframe, dic


def bagOfWords(data, textField, target):    
    data = data[textField]
    v = CountVectorizer()
    df_cv = v.fit_transform(data)
    df = pd.DataFrame(df_cv.toarray())
    df["Label"] = target
    df.to_csv("result.csv", index=False)
    path = os.getcwd()
    # print(f"Result saved to {path}")
    dic = {
        "Shape":df.shape,
        "Features":("Vector count"),
        "Encoding":textField,
        "Path":path
    }
    return df_cv.toarray(), df, dic
