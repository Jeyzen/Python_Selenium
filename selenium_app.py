from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
import os
import pandas as pd
import time
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

class SeleniumApp:
    def __init__(self, progress_label):
        self.progress_label = progress_label

    def setUp(self):
        options = webdriver.ChromeOptions()
        service = Service(r'driver\chromedriver.exe')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def login(self, driver):
        load_dotenv()
        user = os.getenv('DB_USER')
        password = os.getenv('DB_PASSWORD')
        driver.get('https://url.com')
        wait = WebDriverWait(driver, 10)
        driver.find_element(By.XPATH, "//input[@id='txtUsuario']").send_keys(user)
        driver.find_element(By.XPATH, "//input[@id='txtClave']").send_keys(password)
        try:
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        finally:
            driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def data_dict(self):
        df_url = pd.read_excel(r'db\database.xlsx', sheet_name="URL")
        item_url = df_url.set_index('Product_ID').to_dict()
        product_url = item_url['Product_URL']
        return product_url

    def process(self, driver, product_url):
        df_main = pd.read_excel(r'db\database.xlsx', sheet_name="MAIN")
        total_rows = len(df_main)
        for index, row in df_main.iterrows():
            id = row['Product_ID']
            price = row['Product_PRICE']
            url = product_url[id]
            driver.get(url)
            Price_field = driver.find_element(By.XPATH, "//input[@id='txtPrecioPesos']")
            Price_field = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='txtPrecioPesos']")))
            Price_field.clear()
            Price_field.send_keys(price)
            driver.find_element(By.XPATH, "//span[normalize-space()='Guardar']").click()
            try:
                element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Sí']")))
            except Exception as e:
                messagebox.showerror('Error', f'Error en la carga de datos: {e}')
            finally:
                driver.find_element(By.XPATH, "//span[normalize-space()='Sí']").click()
                progress = (index + 1) / total_rows * 100
                self.progress_label.config(text=f'Estado de ejecución: {progress:.2f}%')

        end_time = time.time()
        execution_time = end_time - self.start_time
        messagebox.showinfo('Proceso completado', f'Tiempo de ejecución: {execution_time:.2f} segundos')

    def run(self):
        self.start_time = time.time()
        driver = self.setUp()
        self.login(driver)
        product_url = self.data_dict()
        self.process(driver, product_url)