import pandas as import pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv('data/preprocess_data.csv')
df = df.drop(columns=['Unnamed: 0', 'num_followers', 'num_comments', 'num_likes', 'post_description',
                       'clean_post_description'])
df['sentiment'] = df['sentiment'].replace({'neutral': 0,'positive': 1, 'negative': -1})
df['media_type'] = df['media_type'].replace({'Photo': 0,'Video': 1})

df['Day_week'] = LabelEncoder().fit_transform(df['Day_week'])

df = pd.concat([df, pd.get_dummies(df['pr_activity'])], axis=1)
df = df.drop(columns=['pr_activity', 'Modèle', 'influencer'])

def processing_data(X):
    X['sentiment'] = X['sentiment'].replace({'neutral': 0,'positive': 1,'negative': -1})
    X['media_type'] = X['media_type'].replace({'Photo': 0,'Video': 1})
    return np.c_[X['sentiment'].values,X['media_type'].values,
                  
transformer_var = FunctionTransformer(
    lambda df: processing_data(df)
)                
cols = ['num_posts', 'num_followings','year', 'month', 'day', 'hour',
        'num_words','polarity','subjectivity','dominant_topic', 'perc_contribution',
        'ER']
                 
df = pd.concat([df, pd.get_dummies(df['pr_activity'])],axis=1)
df = df.drop(columns = ['pr_activity','Modèle','influencer'])

transformer = make_column_transformer(
    (transformer_var, ['sentiment', 'media_type']),
    (LabelEncoder(), ['Day_week']),
    (OneHotEncoder(drop = first), ['pr_activity']),
    ('passthrough', cols),
)

pipe = make_pipeline(
    transformer,
    StandardScaler(),
    RandomForestRegressor()
) 
def get_estimator():
    return pipe