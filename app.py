from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import re
import string
import nltk
import difflib
import pickle


app = Flask(__name__, template_folder='index')

# function

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        text = request.form['text']

        trained_model = pickle.load(open('./pickle/trained_model.pkl', 'rb'))

        model = trained_model['model']

        vectorizer = trained_model['vectorizer']

        artikel_berita = text

        factory = StopWordRemoverFactory()
        stopword = factory.create_stop_word_remover()
        stopwordRemover = stopword.remove(artikel_berita)

        
        # Menghapus karakter diluar ASCII Table
        removeEncodedChar = ''.join(i for i in stopwordRemover if ord(i) < 128)

        # Menghapus angka
        regexReplacement = re.sub('\d+', '', removeEncodedChar)

        # Mengubah teks berita menjadi lowercase
        lowercase = regexReplacement.lower()

        # Menghapus spasi di awal dan akhir artikel berita
        trimming = lowercase.strip()

        # Menghapus tanda baca kecuali strip
        removePunctuation = trimming.translate(str.maketrans("", "", string.punctuation.replace('-', '')))
        
        # Tokenisasi teks
        tokens = nltk.word_tokenize(removePunctuation)

        data_test = tokens

        data_test = vectorizer.transform(data_test)

        # Melakukan prediksi
        pred = model.predict(data_test) #msh salah

        # Load the data
        df_correct = pd.read_csv('./dataset/dataset kata benar.csv')
        df_correction = df_correct['word'].values

        typo_word = []
        words_correction = []
        salah_tik = []
        counter = 1

        for index in range(len(tokens)):
          
            if pred[index] == 'incorrect':
                typo_word.append(f"{counter}. Kata {tokens[index].upper()} adalah typo.")
                counter += 1

                salah_tik.append(tokens[index])
                
                correction = tokens[index]

                # Alasan mengapa digunakan n sebesar 15 adalah agar koreksi kata benar yang diinginkan dapat masuk kedalam saran yang dihasilkan.
                matches = difflib.get_close_matches(correction, df_correction, n=15, cutoff=0.85)
                
                words = []
                
                for idx in range(len(matches)):
                    if '-' in tokens[index]:
                        if matches[idx][0] == tokens[index][0]:
                            words.append(matches[idx])
                    else:
                        if matches[idx][0] == tokens[index][0]:
                            if len(matches[idx]) == len(tokens[index]) or len(matches[idx]) == len(tokens[index]) - 1 or len(matches[idx]) == len(tokens[index]) + 1:
                                words.append(matches[idx])
                
                if words != []:
                    correction = f"Saran koreksi kata yang benar dari kata {tokens[index].upper()} adalah {', '.join(words)}."
                    words_correction.append(correction)
                    print(words_correction)
                else:
                    words_correction.append('Saran koreksi kata yang benar tidak ditemukan')
                    print(words_correction)

        
        return render_template('result.html', typo_word = typo_word, words_correction = words_correction, artikel_berita = artikel_berita, salah_tik = salah_tik)
       
    return render_template('home.html')