from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import KNeighborsClassifier
from mpl_toolkits.mplot3d import Axes3D
import pymongo
from otomasyondb import Veritabani
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import HashingVectorizer
import numpy as np
# from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
# from sklearn.feature_selection import f_classif
from sklearn import svm
from sklearn.model_selection import train_test_split
import pickle
import os
import time
import timeit
import random
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.metrics import accuracy_score
from gensim.sklearn_api import Text2BowTransformer
import gensim
from gensim.sklearn_api import W2VTransformer
# from joblib import dump, load
from sklearn.neural_network import MLPClassifier
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.naive_bayes import BernoulliNB
# from sklearn.naive_bayes import GaussianNB
# from sklearn.neural_network import MLPClassifier
# from sklearn.preprocessing import FunctionTransformer
# from mlxtend.preprocessing import DenseTransformer
from sklearn.ensemble import GradientBoostingClassifier
# from sklearn import tree
from gensim.models import Word2Vec

# from matplotlib.colors import ListedColormap
# from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
# from scipy.sparse import csr_matrix,csc_matrix
# from sklearn.linear_model import LassoLars
from sklearn.ensemble import VotingClassifier
# from sklearn.neighbors import RadiusNeighborsClassifier
# from sklearn.neighbors import KNeighborsClassifier
from TurkishStemmer import TurkishStemmer as tust
from sklearn.ensemble import RandomForestClassifier
# from sklearn import preprocessing
# from sklearn.multiclass import OneVsRestClassifier
# from sklearn.multiclass import OneVsOneClassifier
from joblib import Parallel, delayed
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis


class Yapayzeka():

    def veritabanigetir(self):
        DATABASE = Veritabani().db["sayfalars"]
        # DATABASE.create_index([("target","text")])
        # coll=DATABASE.aggregate([{"$group":{"_id":"$target"}}])
        # for i in coll:
        #     print(i)

        coll = DATABASE.find({"$and": [
            {"target": {"$nin": ["turkiye", "dunya", "gundem","magazin","spor","cevre","medya","egitim"]}},
            {"data": {"$gt": []}},
            {"target": {"$in": ["yasam", "ekonomi",
                                "bilim-teknoloji",
                                "kultur-sanat",
                                "saglik"],
                        }},

        ]}, {"_id": 0, "url": 0})



        # print(type(coll),coll.count())
        # coll = DATABASE.find({"target":{"$nin":["turkiye","dunya","gundem"]}}, {"_id": 0, "url": 0})

        return coll

    def split_model(self):
        df = pd.DataFrame(list(self.veritabanigetir()))

        data = df['data'] = [" ".join(data) for data in df['data'].values]
        df["target"] = [" ".join(target) for target in df['target'].values]

        target = np.array(df["target"])
        X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.21, random_state=97)


        return X_train, X_test, y_train, y_test

    def plot_model(self):
        pass

    def save_model(self):
        X_train1, X_test, y_train, y_test = self.split_model()
        stemmed = []
        ps = tust()
        for i in X_train1:
            stem = ps.stem(i)
            stemmed.append(stem)
        X_train = stemmed
        pipeline = Pipeline(steps=[
            ('vect', CountVectorizer()),
            ('tfidf', LatentDirichletAllocation(n_jobs=3, verbose=1, learning_method="batch")),
            ('clf', RandomForestClassifier(verbose=2,n_jobs=3),)])


        predicted = pipeline.fit(X_train, y_train)
        pcdump = pickle.dump(predicted, open("deneme.sav", "wb"))
        return pcdump

    def start_model(self):
        Parallel(n_jobs=3, verbose=1)(delayed(self.predict_from_model()))

    def predict_from_model(self):

        X_train, X_test, y_train, y_test = self.split_model()
        # y_test = self.split_model()[3]
        docs_new = ['beslenme c vitamininin önemi', 'tarım ve köy işleri başkanlığı altın faiz',
                    "Münbiç şehir merkezinde bugün (16 Ocak) vuku bulan bombalı saldırıda ABD askeri personeli ve sivil can kaybı meydana geldiği üzüntüyle öğrenilmiştir. Bu menfur terör eylemini şiddetle kınıyoruz. ",
                    "Hazine ve Maliye Bakanı Berat Albayrak'ın imzasıyla yayımlanan genelge ile kamu idarelerinin kiraladığı taşınmazlarının kira artış oranlarının belirlenmesinde ve yeni yapacağı taşınmaz kiralamalarında uyacağı esaslar yer aldı. Genelgeye göre; kamu idarelerinin kiraladığı taşınmazların kira artışları, artışın yapılacağı ayda yayımlanan Tüketici Fiyatları Endeksi'nin(TÜFE) 12 aylık ortalamasına göre yüzde değişim oranını geçmeyecek şekilde yapılacak. Söz konusu yüzde değişim oranının negatif çıkması halinde kira bedelinde bir değişiklik yapılmayacak ",
                    "kanser hastlarında yeni laç üretimi ", "sabit transfer yörüngesine gitmek", "spacex",
                    "recep tayyip erdoğan", "orkun uçar", "ibm", "necip fazıl kısakürek kitapları",
                    "diyet kitapları ve faizle ilgili elifle konuşuyordum", "faiz",
                    "domates fiyatları son on yılın en yüksek rakamını gördü",
                    "kış aylarında gribe yakalanma olasılığı artıyor",
                    "irtifa ayarları,ve bilgisayar"]
        docs_new2 = ["beslenme c vitamininin önemi", ]
        path = os.getcwd()
        files = os.listdir(path)
        model = "deneme.sav"
        if model in files:
            self.save_model()
            timestart = timeit.default_timer()
            loaded_model = pickle.load(open(model, "rb"))
            predicted2 = loaded_model.predict(X_test)
            predicted3 = loaded_model.predict(docs_new)

            for i in enumerate(zip(predicted3, docs_new), 1):
                print("tahmin   ", i)
            for i in enumerate(zip(predicted2[-40:], X_test[-40:]), 1):
                print("tahmin:  ", i)
            timeend = time.time()
            print("Tahmin skoru :         %", 100 * accuracy_score(y_test, predicted2),
                  "  doğruluk oranına ulaşılmıştır...")
            print("Toplam öğrenme zamanı:  ", timeit.default_timer() - timestart, " saniye sürdü.")
        else:
            print("{0} öğrenim modeli bilinmiyor.eğitim başlatıldı...".format(model))
            timestart = timeit.default_timer()
            saved_model = self.save_model()
            model = pickle.load(open(model, "rb"))
            predicted2 = model.predict(X_test)

            for i in enumerate(zip(predicted2[-20:], X_test[-20:]), 1):
                print("tahmin:  ", i)
            timeend = time.time()
            print("Tahmin skoru : %", 100 * accuracy_score(y_test, predicted2), " doğruluk oranına ulaşılmıştır.")
            print("geçen zaman:  ", timeit.default_timer() - timestart)
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

