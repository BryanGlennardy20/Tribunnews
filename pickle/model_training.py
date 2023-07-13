import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer

# Deklarasi Dataset
df = pd.read_csv('../dataset/dataset kata benar dan typo.csv')

df.to_numpy()

# Deklarasi Dataset
training_data = df['word'].values
training_label = df['label'].values

# Deklarasi (X) dan label (y)
X = training_data
y = training_label

# Menggunakan CountVectorizer untuk mengubah teks menjadi vektor
vectorizer = CountVectorizer(analyzer='char', ngram_range=(1, 3))
X_vectorized = vectorizer.fit_transform(X)

# Melatih model Random Forest
rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf = rf.fit(X_vectorized, y)

# Simpan model dan vectorizer dalam satu objek
model_data = {
    'model': rf,
    'vectorizer': vectorizer
}

# Save the trained model to a file using pickle
filename = 'trained_model.pkl'
pickle.dump(model_data, open(filename, 'wb'))
