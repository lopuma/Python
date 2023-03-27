import argparse
import subprocess
import sys
import requests
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.alert import Alert
import time
import pandas as pd
from tqdm import tqdm
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from termcolor import colored

def main():
    options = webdriver.FirefoxOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')

    driver = webdriver.Remote(
        command_executor='http://192.168.1.19:4444/wd/hub',
        options=options
    )
    parser = argparse.ArgumentParser(
        prog="lbctl",
        usage='lbctl <command> [flags]',
        description="Liburutegia control ('lbctl') provisions and manages local Liburutegia containers optimized for production workflows.",
        epilog='Use "lbctl --help" for more information about a given command.'
    )
    parser.add_argument("command", help='An ("status", "update", "reset", "stop", "find") command is needed, for default is status', type=str, default='status', nargs='?')
    parser.add_argument("-t", '--title', help="Buscar por titulo")
    parser.add_argument("-a", '--author', help="Buscar por author")
    parser.add_argument("-i", '--isbn', help="Buscar por isbn")
    parser.add_argument("-c", '--container', help="The following arguments are required: Container name")
    args = parser.parse_args()
    
    # Llamada init Container
    initContainer(args, parser, driver)

def add_book_bd(data):
    print("Qué libro desea añadir a la BD?")
    for i, book in enumerate(data):
        print(f"[{i+1}] {book['Title']} de {book['Author']}")

    choice = int(input("Ingrese el número de la opción que desea: "))
    selected_book = data[choice-1]
    print(f"\n Has selecionado la opcion {selected_book}")
    # Aquí puedes agregar el código para añadir el libro seleccionado a la BD


def scraping(driver, element):
    loading_message = "Extrayendo datos..."
    with tqdm(total=1, desc=loading_message, bar_format='{percentage:3.0f}%|{bar}|') as pbar:
        try:
            # Navegar a la página web
            driver.get('https://www.casadellibro.com/')

            # Aceptar cookies si se muestran
            try:
                cookies_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler')))
                cookies_button.click()
            except TimeoutException:
                pass

            # Esperar hasta que se muestre el primer input
            input_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[3]/div[1]/div[1]/input')))
            if input_element.is_displayed() and input_element.is_enabled():
                input_element.click()
                boton_element = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[3]/div[1]/div[1]/button')
                boton_element.click()
            else:
                print("El elemento no está disponible para interactuar.")
                driver.quit()

            # Escribir texto en el segundo input
            input2_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/section/header/div/div/input')))
            if input2_element.is_displayed() and input2_element.is_enabled():
                input2_element.send_keys(element)
                driver.implicitly_wait(5)

                # Esperar hasta que los artículos estén disponibles
                try:
                    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'section.ebx-grid.ebx-empathy-x__grid')))
                except TimeoutException:
                    try:
                        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div.ebx-sliding-panel__scroll')))
                    except TimeoutException:
                        element = None

                if element:
                    articles = element.find_elements(By.TAG_NAME, "article")
                else:
                    articles = []
            else:
                print("El elemento no está disponible para interactuar.")
                driver.quit()
            pbar.update(1)
        except:
            pbar.close()
            raise

    articles_data = []
    id = 0
    if articles:
        for article in articles:
            try:
                title = article.find_element(By.CSS_SELECTOR, ".ebx-result-title a").text.strip()
                title_utf8 = title.encode('utf-8')
            except NoSuchElementException:
                print("No se pudo encontrar el elemento del título")
            try:
                author = article.find_element(By.CSS_SELECTOR, ".ebx-result-authors").text.strip()
            except NoSuchElementException:
                print("No se pudo encontrar el elemento del autor")
            try:
                link = article.find_element(By.CSS_SELECTOR, ".ebx-result-title a").get_attribute('href')
            except NoSuchElementException:
                print("No se pudo encontrar el elemento del enlace")
            try:
                other = article.find_element(By.CSS_SELECTOR, ".ebx-result-binding-type").text.strip()
            except NoSuchElementException:
                print("No se pudo encontrar el elemento de otra informacion")
            id+=1
            article_data = {"ID": id, "Title": title, "Author": author, "View": link, "Other": other}
            articles_data.append(article_data)
            
            total_elements = len(articles_data)
            #Convertir la lista a formato JSON
        json_books = json.dumps(articles_data, indent=2, ensure_ascii=False)

        #Imprimir la lista de libros en formato JSON
        print('\n',json_books,'\n')
        print(f"{colored('El total de libros encontrados es :',  'green', attrs=['bold'])} {colored(total_elements, 'yellow')}")
        add_book_bd(articles_data)
    else :
        print("No se pudo encontrar el elemento deseado")
    ##Cerramos session en selenium
    time.sleep(5)
    driver.quit()

def findBook(data, driver):
    title = data[0] if data[0] is not None else ''
    author = data[1] if data[1] is not None else ''
    isbn = data[2] if data[2] is not None else ''
    element = ' '.join([title, author, isbn])
    parser_find = argparse.ArgumentParser(
        prog="lbctl find",
        usage='lbctl find [flags]',
        description="Search book data on the web"
    )
    parser_find.add_argument("-t", '--title', help='Search by TITLE, example (lbctl find -t="title") or (lbctl find --title="title")')
    parser_find.add_argument("-a", '--author', help='Search by AUTHOR, example (lbctl find -a="author") or (lbctl find --author="author")')
    parser_find.add_argument("-i", '--isbn', help='Search by ISBN, example (lbctl find -i="isbn") or (lbctl find --isbn="isbn")')
    color_out = "green"
    color_key = "yellow"
    color_value = "blue"
    if (title == '' and author == '' and isbn == ''):
        parser_find.print_help()
        driver.quit()
    else:
        print(f"{colored('El libro a buscar es', color_out, attrs=['bold'])} ==> {colored('Title: ', color_key)} -> {colored(title, color_value)}, {colored('Author:', color_key)} -> {colored(author, color_value)}, {colored('isbn:', color_key)} -> {colored(isbn, color_value)}")
        scraping(driver, element)

def initContainer(args, parser, driver):
    match args.command:
        case "update":
            print(f"El comando que ejecutas es 1 : {args.command} y el contenedor : {args.container}")
        case "stop":
            print(f"El comando que ejecutas es 2 : {args.command} y el contenedor : {args.container}")
        case "restart":
            print(f"El comando que ejecutas es 3 : {args.command} y el contenedor : {args.container}")
        case "find":
            flags = []
            flags.append(args.title)
            flags.append(args.author)
            flags.append(args.isbn)
            findBook(flags, driver)
        case _:
            print(f"El comando que ejecutas es 4 : {args.command} y el contenedor : {args.container}")
            #    result = subprocess.run(['docker', '-H', 'unix:///var/run/docker.sock', 'ps'], stdout=subprocess.PIPE)
            #    print(result.stdout.decode('utf-8'))

if __name__=='__main__':
    main()