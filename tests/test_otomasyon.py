from typing import Any, Union

import pytest
# from kivy.app import App
# from kivy.graphics import Mesh, Color
# from kivy.graphics.tesselator import Tesselator, WINDING_ODD, TYPE_POLYGONS
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.gridlayout import GridLayout
# from kivy.logger import Logger
# from kivy.uix.textinput import TextInput
# from kivy.config import Config
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.widget import Widget
# from kivy.core.window import Window
# from kivy.uix.popup import Popup
# from kivy.uix.label import Label
from urllib.error import URLError, HTTPError
import tempfile

# import asyncio
# import pickle
# import urllib
from bs4 import BeautifulSoup as bs
# from kivy.core.clipboard import Clipboard
# from kivy.uix.screenmanager import ScreenManager,Screen
# from kivy.uix.bubble import Bubble
# from kivy.properties import ObjectProperty,StringProperty
from urllib.request import Request

from _pytest._code import ExceptionInfo

from otomasyondb import Veritabani
# from kivy.config import Config
import urllib
# from kivy.lang.builder import Builder
# import threading
# import time
# import pathlib
# from kivy.app import App
# from kivy.lang import Builder
# from kivy.factory import Factory
# from kivy.animation import Animation
# from kivy.clock import Clock, mainthread
# from kivy.uix.gridlayout import GridLayout
# from kivy.tests.common import GraphicUnitTest
# from otom import WebSayfa
from otom import SayfaGetir,WebSayfa
from otomasyondb import Veritabani

class Test_SayfaGetir():

    @pytest.fixture
    def sayfa_fixture(self): #sadece sayfayı getirir,request ile .bs kullanılmaz.
        orn = SayfaGetir()
        path = str("https://python-3-patterns-idioms-test.readthedocs.io/en/latest/UnitTesting.html")
        sayfa = orn.get_page(path)
        return sayfa

    def test_get_page(self,sayfa_fixture):
        sayfa=sayfa_fixture
        assert sayfa

    def test_check_page(self,sayfa_fixture):
        assert sayfa_fixture.headers is not None

    def test_check_error_url(self):
        orn = SayfaGetir()
        path = str("https://python-3-patterns-idigoms-test.readthedocs.io/en/latest/UnitTesting.html")
        with pytest.raises(Exception):
            orn.get_page(path)

    def test_check_read_page(self):
        orn=SayfaGetir()
        path = str("http://www.blankwebsite.com/")
        sayfa = orn.read_check_page(path)
        assert sayfa is True

    @pytest.fixture()
    def sayfa_read_fixture(self):
        orn=SayfaGetir()
        path = str("https://www.bilim.org/kilogram-amper-kelvin-ve-mol-yeniden-tanimlandi/")
        sayfa=orn.read_page(path)
        return sayfa

    def test_read_page(self):
        orn=SayfaGetir()
        path = str("https://python-3-patterns-idioms-test.readthedocs.io/en/latest/UnitTesting.html")
        sayfa=orn.read_page(path)
        assert sayfa

    def test_page_write_file(self,sayfa_read_fixture):
        with open("test.txt","w+") as tst:
            tst.write(sayfa_read_fixture)

    def test_async_page_request(self,sayfa_read_fixture):
        orn=WebSayfa()
        asayfa=orn.sayfa_asenkron("https://www.bilim.org/kilogram-amper-kelvin-ve-mol-yeniden-tanimlandi/")
        with open("test2.txt","w+") as tst:
            assenk=tst.write(sayfa_read_fixture)
        with open("test3.txt","w+") as tst:
            assenk2=tst.write(asayfa)
        assert assenk2 == assenk

    def test_database_add(self):
        orn=Veritabani()
        orn.sayfa_ekle(({"veri","43"}))
        sayfacoll=orn.veritabani()
        sorgu=sayfacoll.get_collection("sayfalar").find_one({"sayfa_adı":"veri"})
        if "veri" in sorgu:
            assert sorgu == {"veri","43"}

    def test_database_get(self): # veritabanı testleri
        orn=Veritabani()
        orn.sayfa_ekle(({"veri","43"}))
        sayfa=orn.sayfa_getir("veri")
        sayfa2=orn.sayfa_getir(("sayfa_adı","veri"))
        print(sayfa)
        print(sayfa2)
        sayfacoll = orn.veritabani()
        sorgu = sayfacoll.get_collection("sayfalar").find_one({"sayfa_adı": "veri"})
        assert sayfa == sorgu and sayfa2 == sorgu

