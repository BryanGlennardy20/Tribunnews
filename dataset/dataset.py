import pandas as pd
import random
import csv

# membaca file pertama
df1 = pd.read_csv('./datasetFile/dataset kata.csv')

# membaca file kedua
df2 = pd.read_csv('./datasetFile/dataset kata luluh.csv')

# membaca file ketiga
df3 = pd.read_csv('./datasetFile/dataset kata konjungsi.csv')

# membaca file keempat
df4 = pd.read_csv('./datasetFile/dataset kata tambahan.csv')

# menggabungkan keempat file
df = pd.concat([df1, df2, df3, df4], ignore_index=True)

#tambahkan kolom baru dengan nama 'label' dan isi dengan nilai 'correct'
df['label'] = 'correct'

#hapus nilai kosong dan duplikat
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

# menuliskan hasilnya ke dalam file output
df.to_csv('dataset kata benar.csv', index=False)



def generate_typo(word):
    
    # generate typo tipe 1: penggandaan huruf secara acak
    if len(word) >= 1:
        # pilih indeks huruf yang akan digandakan secara acak
        rand_idx = random.randint(0, len(word) - 1)
        
        # selama idx mengarah ke tanda strip maka idx random akan di generate terus
        while word[rand_idx] == '-':
            rand_idx = random.randint(0, len(word) - 1)

        # masukkan indeks yang dipilih kedalam variabel letter
        letter = word[rand_idx]

        # kembalikan kata dengan huruf yang telah digandakan
        typo1 = word[:rand_idx + 1] + letter + word[rand_idx + 1:]
    else:
        typo1 = None

    
    # generate typo tipe 2: menukar posisi 2 huruf secara acak
    if len(word) >= 3:
        # generate satu bilangan acak antara 1 dan panjang kata dikurangi 1
        rand_idx1 = random.randint(1, len(word) - 1)
        
        # selama index berada di posisi terakhir kata, menuju ke tanda strip atau berada 1 posisi di belakang tanda strip
        while rand_idx1 == len(word) - 1 or word[rand_idx1] == '-' or word[rand_idx1 + 1] == '-':
            rand_idx1 = random.randint(1, len(word) - 1)
        
        rand_idx2 = rand_idx1 + 1

        # menukar posisi dari 2 huruf berdasarkan index yang telah dihasilkan
        typo2 = word[:rand_idx1] + word[rand_idx2] + word[rand_idx1] + word[rand_idx2 + 1:]
    else:
        typo2 = None

    # generate typo tipe 3: menghapus satu huruf secara acak
    if len(word) >= 3:
        # generate random idx
        rand_idx = random.randint(1, len(word) - 1)
        
        # jika index menuju ke tanda strip
        while word[rand_idx] == '-':
            rand_idx = random.randint(1, len(word) - 1)
            
        # hapus huruf pada indeks yang dihasilkan secara acak
        typo3 = word[:rand_idx] + word[rand_idx+1:]
    else:
        typo3 = None

    
    # generate typo tipe 4: mengganti satu huruf dengan huruf lain secara acak
    if len(word) >= 2:
        # memilih indeks acak pada kata, kecuali indeks pertama
        selected_index = random.randint(1, len(word) - 1)
        
        while word[selected_index] == '-':
            selected_index = random.randint(1, len(word) - 1)

        # memilih huruf acak untuk typo
        typo_char = chr(random.randint(97, 122)) # karakter huruf kecil ASCII antara a dan z

        # memeriksa apakah huruf acak sama dengan huruf pada indeks yang akan diganti
        while typo_char == word[selected_index]:
            typo_char = chr(random.randint(97, 122))

        # mengganti karakter pada indeks yang dipilih dengan huruf typo
        typo4 = word[:selected_index] + typo_char + word[selected_index + 1:]
    else:
        typo4 = None
        
    # membuat list kosong dengan nama generatedTypos
    generatedTypos = []
    
    # memasukkan typo1, typo2, typo3, dan typo4 kedalam list jika tidak none
    if typo1 is not None:
        generatedTypos.append(typo1)
    if typo2 is not None:
        generatedTypos.append(typo2)
    if typo3 is not None:
        generatedTypos.append(typo3)
    if typo4 is not None:
        generatedTypos.append(typo4)
        
    # return list generatedTypos
    return generatedTypos

# membaca data dari file dataset kata benar.csv
with open('./dataset kata benar.csv', 'r') as wordData:
    reader = csv.reader(wordData)
    next(reader) # melewatkan baris pertama
    data = list(reader)

# melakukan generate typo pada setiap kata
typos = []
for row in data:
    word = row[0]
    typo_list = generate_typo(word)
    
    # membuat list berisi typo dan label incorrect
    for typo in typo_list:
        typo_data = [typo, "incorrect"]
        typos.append(typo_data)


# menuliskan hasil typo ke dalam file baru
with open('dataset kata typo.csv', 'w', newline='') as output_file:
    writer = csv.writer(output_file)
    writer.writerows(typos)

# membaca file pertama
df1 = pd.read_csv('./dataset kata benar.csv')

# membaca file kedua
df2 = pd.read_csv('./dataset kata typo.csv', header=None, names=['word', 'label'])

# menghapus baris duplikat dan nilai kosong pada df2
df2.drop_duplicates(inplace=True)
df2.dropna(inplace=True)

# Membuat list untuk menyimpan indeks baris yang akan dihapus pada df2
rows_to_drop = []

# Mengiterasi setiap baris pada df2
for index, row in df2.iterrows():
    word = row['word']
    
    # Mencari baris data pada df2 yang memiliki kata yang sama dengan df1 dan berlabel 'incorrect'
    if (word in df1['word'].values):
        rows_to_drop.append(index)

# Menghapus baris data yang sesuai dengan indeks yang ada pada rows_to_drop
df2 = df2.drop(rows_to_drop)

# menggabungkan kedua file
df = pd.concat([df1, df2], ignore_index=True)

# menuliskan hasilnya ke dalam file output
df.to_csv('dataset kata benar dan typo.csv', index=False)