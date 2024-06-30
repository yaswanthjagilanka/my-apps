import json
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pandas as pd




def query_and_matching(path,query):
    df = pd.read_parquet(path+'topics_LDA.parquet', engine='fastparquet')
    words = initial_query_process(query)
    topicid = topicid_getter(df,words)
    id_out = id_getter(path,topicid)
    finaldf,final_json = json_getter(path,id_out)
    return finaldf,final_json


def initial_query_process(test):
    words = test.split(" ")
    words = [word.lower() for word in words]
    data = [word for word in words if not word in set(stopwords.words('english'))]
    lemmmatizer=WordNetLemmatizer()
    words = [lemmmatizer.lemmatize(word.lower()) for word in data if word not in set(stopwords.words('english'))]
    return words


def topicid_getter(df,words):
    topic = []
    for index, row in df.iterrows():
        weight = 0
        for t in words:
            try:
                arg = row['words_in_topic'].index(t)
                weight+= row['termWeights'][arg]
            except ValueError:
                pass
        topic.append(weight)
    topicid = topic.index(max(topic)) + 1
    return topicid

def id_getter(path,topicid):
    df1 = pd.read_parquet(path+'transformed_LDA_TopicDist.parquet', engine='fastparquet')
    topic = ["topic"+str(i) for i in range(1,21)]
    df1[topic] = pd.DataFrame(df1['topicDistribution.values'].tolist())
    id_out = list(df1.sort_values(['topic'+str(topicid)], ascending=[False]).index)
    return id_out[:15]

def json_getter(path,id_out):
    df = pd.read_parquet(path+'trans_sub_df.parquet', engine='fastparquet')
    df_new = df[['id','title','abstract','authors','Year']]
    dfout = df_new.iloc[id_out]
    dfout.abstract = dfout.abstract.apply(lambda x:x.replace("\n"," "))
    dfout.title = dfout.title.apply(lambda x:x.replace("\n"," "))
    return dfout,dfout.to_json(orient="records")