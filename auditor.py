import urllib.request as request
import requests  # Para realizar peticiones HTTP
from bs4 import BeautifulSoup  # Para extraer datos de archivos HTML
import re
from colorama import init, Fore, Style  # Para agregar color a los strings en la consola

init(autoreset=True)

# Definimos la URL de la pagina a la que auditaremos
protocol = "http://"
enter_url = input('Enter URL: ')  # Pedimos la URL en formato de nombre de dominio y dominio
url = protocol + enter_url  # Concatenamos el protocolo a la URL entrante

response = requests.get(url)  # Creamos un objeto Response en base a la peticion a la URL
bs = BeautifulSoup(response.text, 'html.parser')  # Extraemos el HTML y lo parseamos


# Verificacion de certificado SSL en base a la respuesta (HTTP o HTTPS)
def https_check():
    print(Fore.YELLOW + 'HTTPS Validation')

    ''' Llamamos a la clase Request de urllib.request y le pasamos la URL como parametro 
    para posteriormente usar la funcion urlopen sobre '''

    req = request.Request(url)
    result = request.urlopen(req)
    new_url = result.geturl()
    print('\nHTTP or HTTPS url result:', Fore.CYAN + new_url)


# Peso de la pagina web
def webpage_weight():
    print(Fore.YELLOW + 'Weight of page')

    site = request.urlopen(url)
    file = open('out.txt', 'wb')  # Creamos un archivo donde guardaremos toda lainformacion del sitio
    file.write(site.read())  # Escribimos la lectura de la pagina en el archivo
    site.close()
    file.close()

    file = open('out.txt', 'r')
    weight = len(file.read())  # Medimos el peso del archivo y lo guardamos en una variable
    print('\nWebsite weight:', Fore.CYAN + str(weight), Fore.CYAN + 'kB')
    if weight < 35000:
        print(Fore.GREEN + 'The size of the website is optimal')
    else:
        print(Fore.RED + 'The size of the website is not optimal')
    file.close()

    file = open('out.txt', 'w')  # Limpiamos el archivo out para que no quede registro
    file.close()


# Verificacion de la etiquta title en el head
def title_check():
    print(Fore.YELLOW + 'Title validation')

    title = bs.html.head.title.string

    if title is not None:
        title_characters = len(bs.html.head.title.string)
        print('\nThe title of page is:', '"' + Fore.CYAN + title + Fore.RESET + '"')
        print('Title size is:', Fore.CYAN + str(title_characters), Fore.CYAN + 'characters')
        if 70 < title_characters < 55:
            print(Fore.GREEN + 'The title has an optimal size')
        else:
            print(Fore.RED + 'The title does not have an optimal size')
    else:
        print(Style.BRIGHT + Fore.RED + 'The page does not have a title!!')


# Verificacion de numero de caracteres en la meta descripcion
def desciption_check():
    print(Fore.YELLOW + 'Size of the description')

    description = bs.find('meta', attrs={'name': 'description'})  # Busqueda tag/attrs, si no encuentra lo que le
    # pedimos nos retorna un tipo None

    if description is not None:  # Validacion de la busqueda
        description_content = description.get('content')  # Optener el valor de content dentro del tag que buscamos
        characters_number = len(description.get('content'))  # Conteo de caracteres del content
        print('\nDescription of page is:', '"' + Fore.CYAN + description_content + Fore.RESET + '"')
        print('\nDescription size of page is:', Fore.CYAN + f'{characters_number} characters')
        if 155 > characters_number > 50:
            print(Fore.GREEN + 'Optimal description size')
        else:
            print(Fore.RED + 'The description does not have an optimal size')
    else:
        print(Style.BRIGHT + Fore.RED + '\nThe page does not have a description!!')


# Palabras clave mas usadas
def keywords_check():
    print(Fore.YELLOW + 'Keyword verification')

    keywords = bs.find('meta', attrs={'name': 'keywords'})

    if keywords is not None:
        keywords_in_page = keywords.get('content')
        words = keywords_in_page.split()  # Division de la cadena por caracter especifico, por defecto un espacio
        print('\nMost used keywords on the page:')
        print()
        for word in words:
            print(f'- {word}:', Fore.CYAN + str(len(bs.find_all(text=re.compile(word)))))

    else:
        print(Style.BRIGHT + Fore.RED + '\nThe page does not have a keywords!!')


# Verificacion de atributo alt en etiquetas img
def img_check():
    print(Fore.YELLOW + 'Alt img verification')

    print()
    alt = bs.find_all('img', attrs={'alt': ''})

    if alt is not None:
        for image in alt:
            print(Fore.RED + 'This image has no Alt:', Fore.CYAN + image['src'])
    else:
        print(Fore.GREEN + 'This page has no images without Alt')  # Issue #001: No valida si no hay img sin alt.


# Verificacion si la pagina posee H1
def h1_check():
    print(Fore.YELLOW + 'H1 verification')

    h1 = bs.find_all('h1')  # Busqueda de todos los tag h1

    if h1 is not None:
        h1_count = len(h1)  # Conteo de la busqueda
        if h1_count == 1:
            print(Fore.GREEN + '\nThe page has an H1')
        else:
            print(Fore.RED + '\nThe page has more than one H1')
    else:
        print(Style.BRIGHT + Fore.RED + '\nThe page does not have a H1!!')


# Verificacion si la pagina posee Favicon
def favicon_check():
    print(Fore.YELLOW + 'Favicon verification')

    favicon = bs.find('link', attrs={'rel': 'icon' or 'shorcut icon'})  # Indicamos que encuentre un valor u otro

    if favicon is not None:
        print(Fore.GREEN + '\nThe page has favicon')
    else:
        print(Fore.RED + '\nThe page does not have a favicon!!')


# Verificacion si la pagina posee google analitics
def analytics_check():
    print(Fore.YELLOW + 'Analytics verification')

    analytics = bs.find('script', string='ga.src')  # Busqueda especifica de un string dentro de un tag

    if analytics is not None:
        print(Fore.GREEN + '\nThe page has google analytics')
    else:
        print(Fore.RED + '\nThe page does not have google analytics')


# Verificacion del idioma de la pagina
def lang_check():
    print(Fore.YELLOW + 'Lang verification')

    lang = bs.find('html')['lang']  # Indicamos que busque en html a lang y su valor lo pase a la variable

    if lang is not None:
        print('\nThe language of the page is:', Fore.CYAN + lang)
    else:
        print(Style.BRIGHT + Fore.RED + '\nThe page does not have a lang attrs!!')


# Verificacion del Charset
def charset_check():
    print(Fore.YELLOW + 'Charset verification')

    charset = bs.find('meta')['charset']

    if charset is not None:
        print('\nThe charset of the page is:', Fore.CYAN + charset)
    else:
        print(Style.BRIGHT + Fore.RED + '\nThe page does not have a charset attrs!!')


# Verificacion si la pagina posee  viewport
def viewport_check():
    print(Fore.YELLOW + 'Viewport verification')

    viewport = bs.find('meta', attrs={'name': 'viewport'})

    if viewport is not None:
        print(Fore.GREEN + '\nThe page has viewport')
    else:
        print(Style.BRIGHT + Fore.RED + '\nThe page does not have a viewport!!')


#  Ejecuntamos e imprimimos en la consola
print(Style.BRIGHT + Fore.YELLOW + '\nSEO audit starting...')
print('\n--------------------------------------------------------------')
https_check()
print('--------------------------------------------------------------')
webpage_weight()
print('--------------------------------------------------------------')
title_check()
print('--------------------------------------------------------------')
desciption_check()
print('--------------------------------------------------------------')
keywords_check()
print('--------------------------------------------------------------')
img_check()
print('--------------------------------------------------------------')
h1_check()
print('--------------------------------------------------------------')
favicon_check()
print('--------------------------------------------------------------')
analytics_check()
print('--------------------------------------------------------------')
lang_check()
print('--------------------------------------------------------------')
charset_check()
print('--------------------------------------------------------------')
viewport_check()
print('--------------------------------------------------------------')
print(Style.BRIGHT + Fore.YELLOW + '\nSEO audit completed!')
