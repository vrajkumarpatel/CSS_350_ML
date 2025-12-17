
import pandas as pd
from imblearn.over_sampling import SMOTE

df = pd.read_csv('cuisines.csv')

feature_df = df.drop(['cuisine', 'Unnamed: 0', 'rice', 'garlic', 'ginger'], axis=1)
labels_df = df.cuisine

oversample = SMOTE()
transformed_feature_df, transformed_label_df = oversample.fit_resample(feature_df, labels_df)

transformed_df = pd.concat([transformed_label_df, transformed_feature_df], axis=1, join='outer')
transformed_df.to_csv("cleaned_cuisines.csv")
