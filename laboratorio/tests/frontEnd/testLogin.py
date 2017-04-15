__author__ = 'asistente'
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

host = "http://localhost:8000/";

class testLogin(TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)

    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        self.browser.get(host+'laboratorio/')
        self.assertIn('Laboratorio Uniandes', self.browser.title)

    #def atest_title(self):
     #   self.browser.get(self.baseUrl)
      #  self.assertIn('Laboratorio Uniandes', self.browser.title)
