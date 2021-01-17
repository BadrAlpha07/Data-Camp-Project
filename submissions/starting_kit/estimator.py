from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, LabelEncoder, StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor


def processing_data(X):
    
    X['media_type'] = X['media_type'].replace({'Photo':0,'Video':1})
    X["Day_week"] = LabelEncoder().fit_transform(X['Day_week'])
    
    X["clean_post_description"] = X["post_description"].apply(nlp_pre_processing.pre_process)
    X['polarity'] = X['clean_post_description'].apply(nlp_pre_processing.polarity)
    X['sentiment'] = X['polarity'].apply(nlp_pre_processing.sentiment)
    X['sentiment'] = X['sentiment'].replace({'neutral':0,'positive':1,'negative':-1})
    X["num_hashtags"] = X["post_description"].apply(nlp_pre_processing.hashtags_num)
    X["num_ref"] = X["post_description"].apply(nlp_pre_processing.ref_num)
    X_topic_sents_keywords = nlp_pre_processing.LDAmodel(X.clean_post_description,passes=2,
                                   num_topics=5,
                                   workers = 2,
                                  re_train=False)
    X = pd.concat([X, X_topic_sents_keywords], axis=1)
 
    return np.c_[X['sentiment'].values,X['media_type'].values,
                X['Day_week'].values, X['polarity'].values,
                X['num_hashtags'].values,X['num_ref'].values,
                X['dominant_topic'].values,X['perc_contribution'].values]
                  

transformer_var = FunctionTransformer(
    lambda df: processing_data(df)
)
                 
cols = ['num_posts', 'num_followings','year', 'month', 'day', 'hour',
        'num_words']
                 

transformer = make_column_transformer(
    (transformer_var, ['media_type', 'post_description','Day_week']),
    (OneHotEncoder(), ['pr_activity']),
    ('passthrough', cols),
)

pipe = make_pipeline(
    transformer,
    StandardScaler(),
    RandomForestRegressor()
)
    
def get_estimator():
    return pipe