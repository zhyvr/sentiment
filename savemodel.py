import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

df =pd.read_csv("data/output.csv")
df = df.dropna()

df['sentiment'] = df['sentiment'].replace({'positive': 1, 'negative': -1})

x = df['sentence']
y = df['sentiment']

vectorizer = CountVectorizer()
x_train_vectorized = vectorizer.fit_transform(x)

model = LogisticRegression()
model.fit(x_train_vectorized, y)


# Save the model and vectorizer to disk
filename = 'model.pkl'
pickle.dump((model, vectorizer), open(filename, 'wb'))
