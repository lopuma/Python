# -*- coding: utf-8 -*-
from sys import maxsize
from selenium import webdriver
import pandas as pd
import csv
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import time

home = Path.home()

# Opciones de navegación
options =  webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--disable-extensions')

driver = webdriver.Chrome(Path(home, 'Alvaro','Desarrollo','Python','auto','chromedriver'), chrome_options=options)

#Abrir el explorador
driver.get('http://192.168.122.89/login')


user = "admin@mail.com"
password = "admin"

# Por eso tengo que esperar que aparezca 
input_user = WebDriverWait(driver, 10).until(
  EC.presence_of_element_located((By.XPATH, '//input[@name="email"]'))
)
input_pass = driver.find_element(By.XPATH, '//input[@name="password"]')

# Escribo mi usuario input
input_user.send_keys(user)

# Escribo mi contrasena en el input
input_pass.send_keys(password)

# Obtengo el boton de login
login_button = driver.find_element(By.XPATH, '//input[@id="btnLogin"]')
# Le doy click
login_button.submit()
try:
  with open('data.csv', encoding='utf-8') as file:
    data = csv.reader(file, delimiter=',')
    next(file)
    for linea in data:
        dataEmail = linea[0]
        dataUser = linea[1]
        dataFullname = linea[2]
        dataRol = linea[3]
        dataPass = linea[4]
        driver.get('http://192.168.122.89/register')
        input_email = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[3]/form/div/div[2]/div[1]/input'))
        )
        input_username = driver.find_element(By.XPATH, '//div[@class="Singin"]//input[@name="username"]')
        input_fullname = driver.find_element(By.XPATH, '//div[@class="Singin"]//input[@name="fullname"]')
        input_password = driver.find_element(By.XPATH, '//div[@class="Singin"]//input[@name="pass"]')
        input_passwordRepeat = driver.find_element(By.XPATH, '//div[@class="Singin"]//input[@name="passRepeat"]')
        #Select
        select = Select(driver.find_element_by_name('rol'))
        select.select_by_value(dataRol)

        input_email.send_keys(dataEmail)
        input_username.send_keys(dataUser)
        input_fullname.send_keys(dataFullname)
        input_password.send_keys(dataPass)
        input_passwordRepeat.send_keys(dataPass)
        btnAddUser = driver.find_element(By.XPATH, '//*[@id="btnAccept"]').submit()
        time.sleep(1)
  driver.close();
except():
  print("No such file or directory.\nTry again.")
  driver.close()

