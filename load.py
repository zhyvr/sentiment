import pickle

# Load the saved model and vectorizer
filename = 'model.pkl'
loaded_model, loaded_vectorizer = pickle.load(open(filename, 'rb'))

# Example usage: transform new sentences and predict sentiment
new_sentence = ["زۆر ڕقم لێتە"]
new_sentence_vectorized = loaded_vectorizer.transform(new_sentence)
predicted_sentiment = loaded_model.predict(new_sentence_vectorized)

print(predicted_sentiment[0])