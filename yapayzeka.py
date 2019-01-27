from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from otomasyondb import Veritabani
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import HashingVectorizer
import numpy as np
from sklearn.linear_model import SGDClassifier
import pickle
import os
import time
from joblib import dump,load

class Yapayzeka():

    def veritabanigetir(self):
        DATABASE = Veritabani().db["sayfalars"]
        coll = DATABASE.find({}, {"_id": 0, "url": 0})
        return coll
    def save_model(self):

        df = pd.DataFrame(list(self.veritabanigetir()))
        df['data'] = [" ".join(data) for data in df['data'].values]
        df["target"] = [" ".join(target) for target in df['target'].values]
        pipeline = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf', MultinomialNB(),)])
        predicted = pipeline.fit(df["data"], df["target"])
        pcdump = pickle.dump(predicted,open("model.sav","wb"))
        return pcdump


    def predict_from_model(self):
        docs_new = ['beslenme c vitamininin önemi', 'tarım ve köy işleri başkanlığı altın faiz',
                    "Münbiç şehir merkezinde bugün (16 Ocak) vuku bulan bombalı saldırıda ABD askeri personeli ve sivil can kaybı meydana geldiği üzüntüyle öğrenilmiştir. Bu menfur terör eylemini şiddetle kınıyoruz. ",
                    "Hazine ve Maliye Bakanı Berat Albayrak'ın imzasıyla yayımlanan genelge ile kamu idarelerinin kiraladığı taşınmazlarının kira artış oranlarının belirlenmesinde ve yeni yapacağı taşınmaz kiralamalarında uyacağı esaslar yer aldı. Genelgeye göre; kamu idarelerinin kiraladığı taşınmazların kira artışları, artışın yapılacağı ayda yayımlanan Tüketici Fiyatları Endeksi'nin(TÜFE) 12 aylık ortalamasına göre yüzde değişim oranını geçmeyecek şekilde yapılacak. Söz konusu yüzde değişim oranının negatif çıkması halinde kira bedelinde bir değişiklik yapılmayacak ",
                    "kanser hastlarında yeni laç üretimi ", "sabit transfer yörüngesine gitmek", "spacex",
                    "recep tayyip erdoğan", "orkun uçar", "ibm", "necip fazıl kısakürek kitapları",
                    "diyet kitapları ve faizle ilgili elifle konuşuyordum", "faiz",
                    "domates fiyatları son on yılın en yüksek rakamını gördü",
                    "kış aylarında gribe yakalanma olasılığı artıyor",
                    "çikolata almaya karar verdim"]
        docs_new2=["beslenme c vitamininin önemi",]
        path=os.getcwd()
        files=os.listdir(path)
        if "model.sav" in files:
            timestart=time.time()
            loaded_model = pickle.load(open("model.sav","rb"))
            predicted2 = loaded_model.predict(docs_new)
            timeend=time.time()
            print("geçen zaman:  ", timeend-timestart)
            for i in enumerate(zip(predicted2, docs_new),1):
                print("tahmin:  ",i)
        else:
            print("kayıtlı değil")
            timestart=time.time()
            saved_model=self.save_model()
            model=pickle.load(open("model.sav","rb"))
            predicted2 = model.predict(docs_new2)
            timeend=time.time()
            print("geçen zaman:  ", timeend-timestart)

            for i in enumerate(zip(predicted2, docs_new), 1):
                print("tahmin:  ", i)
        # plt.xlabel('tahminler')
        # plt.ylabel('etiketler')
        # plt.title('Tahmin ortalaması')
        # plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
        # plt.grid(True)
        # plt.plot(np.arange(0, 16), predicted2)
        # plt.show()
        # [1's a g l i k' 2'e k o n o m i' 3'b i l i m - 4t e k n o l o j i'
        #  5'e k o n o m i' 6's a g l i k' 7'b i l i m - t e k n o l o j i'
        #  8'b i l i m - t e k n o l o j i' 9'e k o n o m i' 10'y a s a m'
        #  11'b i l i m - t e k n o l o j i' 12'k u l t u r - s a n a t' 13's a g l i k'
        #  14'e k o n o m i']
        # [1'y a s a m' 2'e k o n o m i' 3'b i l i m - t e k n o l o j i'
        #  4'e k o n o m i' 5's a g l i k' 6'b i l i m - t e k n o l o j i'
        #  7'b i l i m - t e k n o l o j i' 8'e k o n o m i' 9'y a s a m' 10'y a s a m'
        #  11'y a s a m' 12'y a s a m' 13'e k o n o m i']


if __name__ == "__main__":
    orn = Yapayzeka()
    orn.predict_from_model()
