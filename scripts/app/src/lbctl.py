import argparse
import subprocess
import sys
import json
import pandas as pd
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.alert import Alert
import time
from tqdm import tqdm, trange
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from termcolor import colored
from decouple import config
import mysql_connection
cnx = mysql_connection.mydb
cursor = cnx.cursor()

color_out = "green"
color_key = "yellow"
color_value = "blue"
color_analizando = "yellow"
color_error = "red"
color_warning = "yellow"

def main():
    options = webdriver.FirefoxOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')

    parser = argparse.ArgumentParser(
        prog="lbctl",
        usage='lbctl <command> [flags]',
        description="Liburutegia control ('lbctl') provisions and manages local Liburutegia containers optimized for production workflows.",
        epilog='Use "lbctl --help" for more information about a given command.'
    )
    parser.add_argument("command", help='An ("status", "update", "reset", "stop", "find") command is needed, for default is status', type=str, default='status', nargs='?')
    parser.add_argument("-t", '--title', help='Search by TITLE, example (lbctl find -t="title") or (lbctl find --title="title")', type=str)
    parser.add_argument("-a", '--author', help='Search by AUTHOR, example (lbctl find -a="author") or (lbctl find --author="author")', type=str)
    parser.add_argument("-i", '--isbn', help='Search by ISBN, example (lbctl find -i="isbn") or (lbctl find --isbn="isbn")')
    parser.add_argument("-c", '--container', help="The following arguments are required: Container name")
    args = parser.parse_args()

    if args.command == "find" or (args.command == "help" and args.container == "find"):
        parser_find = argparse.ArgumentParser(
            prog="lbctl find",
            usage='lbctl find [flags]',
            description="Search book data on the web"
        )
        parser_find.add_argument("-t", '--title', help='Search by TITLE, example (lbctl find -t="title") or (lbctl find --title="title")', type=str)
        parser_find.add_argument("-a", '--author', help='Search by AUTHOR, example (lbctl find -a="author") or (lbctl find --author="author")', type=str)
        parser_find.add_argument("-i", '--isbn', help='Search by ISBN, example (lbctl find -i="isbn") or (lbctl find --isbn="isbn")')
        args_find, _ = parser_find.parse_known_args()
        if not all(v is None for v in vars(args_find).values()):
            # Si alguno de los valores no es None, se proporcionaron argumentos válidos
            # Llamada find Book
            driver = webdriver.Remote(
                command_executor='http://{}:4444/wd/hub'.format(config('WEBDRIVER_HOST')),
                options=options
            )
            initContainer(args, parser_find, driver)
        else:
            # No se proporcionaron argumentos válidos, imprimir ayuda
            parser_find.print_help()
    else:
        driver = webdriver.Remote(
                command_executor='http://{}:4444/wd/hub'.format(config('WEBDRIVER_HOST')),
            options=options
        )

        # Llamada init Container
        initContainer(args, parser_find, driver)


def capitalizar_palabras(cadena, excepciones=["de"]):
    palabras = cadena.split()
    palabras_mayusculas = []
    for i, palabra in enumerate(palabras):
        if palabra.lower() not in excepciones:
            palabra = palabra.lower()
            palabra = palabra.capitalize()
        else:
            palabra = palabra.lower()
        if i == 0:
            palabra = palabra.capitalize()
        palabras_mayusculas.append(palabra)
    return ' '.join(palabras_mayusculas)

def conection_database(data):
    try:
        title = data[0]['title']
        print("RECIVO title => ", title)
    except (IndexError, KeyError):
        print("Error al acceder al title en los datos recibidos.")
    try:
        author = data[0]['author']
        print("RECIVO author => ", author)
    except (IndexError, KeyError):
        print("Error al acceder al author en los datos recibidos.")
    try:
        editorial = data[0]['editorial']
        print("RECIVO editorial => ", editorial)
    except (IndexError, KeyError):
        print("Error al acceder al editorial en los datos recibidos.")
    try:
        isbn = data[0]['isbn']
        print("RECIVO ISBN => ", isbn)
    except (IndexError, KeyError):
        print("Error al acceder al ISBN en los datos recibidos.")
    try:
        type = data[0]['category']
        print("RECIVO type => ", type)
    except (IndexError, KeyError):
        print("Error al acceder al type en los datos recibidos.")
    try:
        language = data[0]['language']
        print("RECIVO language => ", language)
    except (IndexError, KeyError):
        print("Error al acceder al language en los datos recibidos.")
    
    with tqdm(total=100, desc="\033[33mRealizando operaciones en la Base de datos....\033[0m") as pbar:
        # al final del ciclo for, puedes imprimir el mensaje de conexión
        print("\033[32mConectado a la base de datos.\033[0m")
        pbar.update(50)

        query = "SELECT * FROM users"
        cursor.execute(query)
        pbar.update(50)        
    # with tqdm(total=10, desc="\033[33mGuardando datos....\033[0m") as pbar:
    #     try:
    #         add_book = ("INSERT INTO books "
    #                     "(title, author, editorial, isbn, type, language) "
    #                     "VALUES (%s, %s, %s, %s, %s, %s)")
    #         data_book = (title, author, editorial, isbn, type, language)

    #         cursor.execute(add_book, data_book)
    #         cnx.commit()
    #     except Exception as e:
    #         print("Error al guardar los datos:", e)
    #         cnx.rollback()
    #     finally:
    #         cursor.close()
    #         cnx.close()

    #     pbar.update(10)

def add_book_bd(data, driver):
    time.sleep(2)
    link_book = data['view']
    title = capitalizar_palabras(data['title'])
    author = capitalizar_palabras(data['author'])
    driver.get(link_book)
    
    data_category = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, './/*[@id="breadcrumbs"]/div/div[2]/div[5]/a/span')))
    category = capitalizar_palabras(data_category.text)
    
    xpaths = ['//*[@id="app"]/div[1]/main/div/div/div/div[4]/div/div[3]',
            '//*[@id="app"]/div[1]/main/div/div/div/div[6]/div/div[3]',
            '//*[@id="app"]/div[1]/main/div/div/div/div[7]/div/div[3]']

    # lista para almacenar los resultados
    resultados = []

    # comenzar el bucle de búsqueda de datos
    with tqdm(total=100, desc="\033[33m\nAnalizando datos....\033[0m") as pbar:
        # buscar los datos en cada xpath que aún no se haya comprobado
        for xpath in xpaths:
            try:
                data_sheet = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                if data_sheet is not None:
                    rows = data_sheet.find_elements(By.XPATH, './/div[@class="row text-body-2 no-gutters"]')

                    # crear un diccionario vacío para almacenar los datos de la ficha técnica
                    tech_specs = {}
                     # iterar sobre cada fila de la tabla y extraer el nombre y valor correspondientes
                    for row in rows:
                        name = row.find_element(By.XPATH, './/span/strong').text
                        value = row.find_element(By.XPATH, './/div[@class="col col-6"][2]/span')
                        tech_specs[name] = value.text

                    isbn = ''
                    idioma = ''
                    editorial = ''

                    try:
                        isbn = tech_specs['ISBN:']
                    except KeyError:
                        isbn = ""

                    try:
                        idioma = tech_specs['Idioma:']
                    except KeyError:
                        idioma = ""

                    try:
                        editorial = tech_specs['Editorial:']
                    except KeyError:
                        editorial = ""
                    
                    # imprimir los datos de la ficha técnica
                    if isbn not in [r.get('isbn', '') for r in resultados]:
                        print("RR => ", isbn)
                        resultados.append({'isbn': isbn, 'language': capitalizar_palabras(idioma), 'editorial': capitalizar_palabras(editorial), 'title': title, 'author': author, 'category': category})
                    
                    pbar.update(100)
                    break
            except TimeoutException:
                pass
    if data_sheet is None:
        print("No se pudo encontrar la hoja técnica")
    else:    
        if len(resultados) == 0:
            print("No se encontraron resultados")
        else:
            print("Antes de la BD => ", resultados)
            conection_database(resultados)

def select_book(data, df, driver):
    total_elements = len(df)
    print("\n------------------------------------------------------------------------------------------------------------------------")
    print("------------------------------------------------- LIBROS DISPONIBLES ---------------------------------------------------")
    print("------------------------------------------------------------------------------------------------------------------------")
    print('\n',df,'\n')
    print("\n\t\t", colored("[X]   Salir", color_error), "\n")
    print(f"{colored('El total de libros encontrados es :',  color_out, attrs=['bold'])} {colored(total_elements, color_key)}")
    while True:
        user_input = input("\nIngrese el ID de la opción que desea o X para salir: ")
        if user_input.lower() == "x":
            print("\n\t", colored('Cerrando session....', color_error))
            return None
        try:
            choice = int(user_input)
            for book in data:
                if book["ID"] == choice:
                    book_data  = {'view': book['view'], 'title': book['title'], 'author': book['author']}
                    add_book_bd(book_data , driver)
                    return choice
        except ValueError:
            print("\n\t" , colored(f"La opción {user_input} no es válida. Por favor, ingrese un número entre ", color_error) + colored("0", color_out) + colored(f" y {len(data) - 1}", color_out) + colored(" o ",color_error) + colored("X ", color_warning) + colored("para salir.", color_error))

def scraping(element, driver):
    articles = []
    with tqdm(total=3) as pbar:
        try:
            driver.get('https://www.casadellibro.com/')
            try:
                cookies_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler')))
                try:
                    cookies_button.click()
                    pbar.update(1)
                except NoSuchElementException:
                    pass
            except TimeoutException:
                pass
            driver.implicitly_wait(5)
            try:
                input_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[3]/div[1]/div[1]/input')))
                input_element.click()
                driver.implicitly_wait(5)
                boton_element = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[3]/div[1]/div[1]/button')
                boton_element.click()
                pbar.update(1)
            except TimeoutException:
                print(colored('El elemento no está disponible para interactuar.', color_error))
                pass
            except ElementClickInterceptedException:
                print(colored('El elemento está oculto y no se puede hacer clic en él.', color_error))
                pass
            driver.implicitly_wait(5)
            try:
                input2_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="empathy-x"]/header/div/div/input')))
                input2_element.send_keys(element)
                driver.implicitly_wait(5)
                try:
                    element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'section.ebx-grid.ebx-empathy-x__grid')))
                except TimeoutException:
                    try:
                        element = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'div.ebx-sliding-panel__scroll')))
                    except TimeoutException:
                        element = None
                time.sleep(3)
                if element:
                    articles = element.find_elements(By.TAG_NAME, "article")
                    pbar.update(1)
                else:
                    articles = []
            except TimeoutException:
                print(colored('El elemento no está disponible para interactuar.', color_warning))
        except:
            pbar.close()
            raise
    list_articles_data = []
    id = 0
    if articles:
        for article in articles:
            try:
                title = article.find_element(By.CSS_SELECTOR, ".ebx-result-title a").text.strip()
            except NoSuchElementException:
                print(colored('No se pudo encontrar el elemento del título.', color_warning))
                title = ''
            try:
                author = article.find_element(By.CSS_SELECTOR, ".ebx-result-authors").text.strip()
            except NoSuchElementException:
                print(colored('No se pudo encontrar el elemento del autor.', color_warning))
                author = ''
            try:
                link = article.find_element(By.CSS_SELECTOR, ".ebx-result-title a").get_attribute('href')
            except NoSuchElementException:
                print(colored('No se pudo encontrar el elemento del enlace.', color_warning))
                link = ''
            try:
                other = article.find_element(By.CSS_SELECTOR, ".ebx-result-binding-type").text.strip()
            except NoSuchElementException:
                print(colored('No se pudo encontrar el elemento de otra informacion.', color_warning))
                other = ''
            
            dict_article_data = {}
            if any([len(title)>0, len(author)>0, len(link)>0, len(other)>0]):
                dict_article_data["ID"] = id
                dict_article_data["title"] = title
                dict_article_data["author"] = author
                dict_article_data["view"] = link
                dict_article_data["other"] = other
                
                list_articles_data.append(dict_article_data)
                dict_articles_data = {}
            id+=1
        for d in list_articles_data:
            for k, v in d.items():
                dict_articles_data.setdefault(k, []).append(v)
        df = pd.DataFrame.from_dict(dict_articles_data)
        print("\n\033[33mCargando datos....\033[0m")
        for i in trange(10, unit="s", unit_scale=0.1, unit_divisor=1):
            time.sleep(0.2)
        select_book(list_articles_data, df, driver)
    else :
        print(colored('No se pudo encontrar el elemento deseado.', color_error))

    #Cerramos session en selenium
    time.sleep(5)
    driver.quit()

def findBook(data, driver, parser_find):
    title   = data[0] if data[0] is not None else ''
    author  = data[1] if data[1] is not None else ''
    isbn    = data[2] if data[2] is not None else ''
    data_element = ' '.join([title, author, isbn])
    
    if (title == '' and author == '' and isbn == ''):
        parser_find.print_help()
        driver.quit()
    else:
        print("\n" + f"{colored('El libro a buscar es', color_key, attrs=['bold'])} --> {colored('Title: ', color_key)} --> {colored(title, color_value)}, {colored('Author:', color_key)} --> {colored(author, color_value)}, {colored('isbn:', color_key)} --> {colored(isbn, color_value)}")
        print("\033[33m\nBuscando datos....\033[0m")
        scraping(data_element, driver)            

def initContainer(args, parser_find, driver):
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
            findBook(flags, driver, parser_find)
        case _:
            print(f"El comando que ejecutas es 4 : {args.command} y el contenedor : {args.container}")
            #    result = subprocess.run(['docker', '-H', 'unix:///var/run/docker.sock', 'ps'], stdout=subprocess.PIPE)
            #    print(result.stdout.decode('utf-8'))

if __name__=='__main__':
    main()