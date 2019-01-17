from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from otomasyondb import Veritabani
import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
from sklearn.linear_model import SGDClassifier

class Yapayzeka():


    def veritabanigetir(self):
        DATABASE=Veritabani().db["sayfalars"]
        coll=DATABASE.find({},{"_id": 0,"url":0})
        return coll

    def learn(self):
        docs_new = ['beslenme c vitamininin önemi', 'tarım ve köy işleri başkanlığı altın faiz',"Münbiç şehir merkezinde bugün (16 Ocak) vuku bulan bombalı saldırıda ABD askeri personeli ve sivil can kaybı meydana geldiği üzüntüyle öğrenilmiştir. Bu menfur terör eylemini şiddetle kınıyoruz. ","Hazine ve Maliye Bakanı Berat Albayrak'ın imzasıyla yayımlanan genelge ile kamu idarelerinin kiraladığı taşınmazlarının kira artış oranlarının belirlenmesinde ve yeni yapacağı taşınmaz kiralamalarında uyacağı esaslar yer aldı. Genelgeye göre; kamu idarelerinin kiraladığı taşınmazların kira artışları, artışın yapılacağı ayda yayımlanan Tüketici Fiyatları Endeksi'nin(TÜFE) 12 aylık ortalamasına göre yüzde değişim oranını geçmeyecek şekilde yapılacak. Söz konusu yüzde değişim oranının negatif çıkması halinde kira bedelinde bir değişiklik yapılmayacak ","kanser hastlarında yeni laç üretimi ","sabit transfer yörüngesine gitmek","spacex","recep tayyip erdoğan","orkun uçar","ibm","necip fazıl kısakürek kitapları","diyet kitapları ve faizle ilgili elifle konuşuyordum","faiz"]
        df = pd.DataFrame(list(self.veritabanigetir()))
        df['data'] = [" ".join(data) for data in df['data'].values]
        df["target"] = [" ".join(target) for target in df['target'].values]
        pipeline = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf', MultinomialNB(), )])
        predicted=pipeline.fit(df["data"], df["target"]).predict(docs_new)
        print(df.shape)

        print(predicted)
        plt.xlabel('tahminler')
        plt.ylabel('etiketler')
        plt.title('Tahmin ortalaması')
        plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
        plt.grid(True)
        plt.plot(predicted,np.arange(0,13))
        plt.show()
        # ['s a g l i k' 'e k o n o m i' 'b i l i m - t e k n o l o j i'
        #  'e k o n o m i' 's a g l i k' 'b i l i m - t e k n o l o j i'
        #  'b i l i m - t e k n o l o j i' 'e k o n o m i' 'y a s a m'
        #  'b i l i m - t e k n o l o j i' 'k u l t u r - s a n a t' 's a g l i k'
        #  # 'e k o n o m i']
        # ['y a s a m' 'e k o n o m i' 'b i l i m - t e k n o l o j i'
        #  'e k o n o m i' 's a g l i k' 'b i l i m - t e k n o l o j i'
        #  'b i l i m - t e k n o l o j i' 'e k o n o m i' 'y a s a m' 'y a s a m'
        #  'y a s a m' 'y a s a m' 'e k o n o m i']

if __name__ == "__main__":
    orn=Yapayzeka()
    orn.learn()