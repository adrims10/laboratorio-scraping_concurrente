from bs4 import BeautifulSoup 
import requests 
import pandas as pd
import numpy as np 
from time import sleep
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.support.ui import Select  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException 
import random as ra
import asyncio
import aiohttp

df = pd.read_csv("datos_con_geoposicion.csv", index_col = 0)

def extraer_codigo_estacion():
    driver = webdriver.Chrome(executable_path='/ruta/a/chromedriver')

    # URL de ejemplo para el código de estación
    url_wunder = "https://www.wunderground.com/weather/es/alcorcon"
    driver.get(url_wunder)
    driver.maximize_window()

    # Manejar cookies
    iframe_cookies = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="sp_message_iframe_1165301"]'))
    )
    driver.switch_to.frame(iframe_cookies)
    try:
        driver.implicitly_wait(5)
        driver.find_element(By.CSS_SELECTOR, "#notice > div.message-component.message-row.cta-buttons-container > div.message-component.message-column.cta-button-column.reject-column > button").click()
    except:
        print("No encuentro el botón de cookies")
    driver.switch_to.default_content()
    sleep(3)

    # Obtener el código de estación
    datos = driver.find_element(By.CSS_SELECTOR, "#inner-content > div.region-content-top > lib-city-header > div:nth-child(1) > div > div > a.station-name")
    url = datos.get_attribute("href")
    url_temp = url.split("?")
    code_station = url_temp[0].rsplit('/', 1)[-1]
    print(code_station)

    driver.quit()
    return code_station

# Función asíncrona para solicitar datos históricos
async def fetch_history_data(session, url):
    async with session.get(url) as response:
        return await response.text()

# Función principal para extraer datos históricos
async def extraer_datos_historicos(code_station):
    url_wunder = f"https://www.wunderground.com/history/daily/es/alcorcon/date/{code_station}"
    async with aiohttp.ClientSession() as session:
        html = await fetch_history_data(session, url_wunder)
        soup = BeautifulSoup(html, 'html.parser')

        # Extraer la tabla de datos
        tabla = soup.select_one("#main-page-content > div > div > div > lib-history > div.history-tabs > lib-history-table > div > div > div > table > tbody")
        print(tabla.text)

        # Procesar los datos de la tabla
        datos = tabla.text.split('\n')
        print(datos)
        df = pd.DataFrame(datos)
        print(df)

# Ejecutar la extracción de datos
async def main():
    code_station = extraer_codigo_estacion()
    await extraer_datos_historicos(code_station)

# Ejecutar la función principal
# Función para extraer el código de la estación
def extraer_codigo_estacion():
    driver = webdriver.Chrome(executable_path='/ruta/a/chromedriver')
    url_wunder = "https://www.wunderground.com/weather/es/alcorcon"
    driver.get(url_wunder)
    driver.maximize_window()
    
    iframe_cookies = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="sp_message_iframe_1165301"]'))
    )
    driver.switch_to.frame(iframe_cookies)
    try:
        driver.implicitly_wait(5)
        driver.find_element(By.CSS_SELECTOR, "#notice > div.message-component.message-row.cta-buttons-container > div.message-component.message-column.cta-button-column.reject-column > button").click()
    except:
        print("No encuentro el botón de cookies")
    driver.switch_to.default_content()
    sleep(3)

    datos = driver.find_element(By.CSS_SELECTOR, "#inner-content > div.region-content-top > lib-city-header > div:nth-child(1) > div > div > a.station-name")
    url = datos.get_attribute("href")
    url_temp = url.split("?")
    code_station = url_temp[0].rsplit('/', 1)[-1]
    print(code_station)
    
    driver.quit()
    return code_station

# Función asíncrona para solicitar datos históricos
async def fetch_history_data(session, url):
    async with session.get(url) as response:
        return await response.text()

# Función principal para extraer datos históricos
async def extraer_datos_historicos(code_station):
    url_wunder = f"https://www.wunderground.com/history/daily/es/alcorcon/date/{code_station}"
    async with aiohttp.ClientSession() as session:
        html = await fetch_history_data(session, url_wunder)
        soup = BeautifulSoup(html, 'html.parser')

        tabla = soup.select_one("#main-page-content > div > div > div > lib-history > div.history-tabs > lib-history-table > div > div > div > table > tbody")
        print(tabla.text)

        datos = tabla.text.split('\n')
        print(datos)
        df = pd.DataFrame(datos)
        print(df)

# Ejecutar la extracción de datos
async def main():
    code_station = extraer_codigo_estacion()
    await extraer_datos_historicos(code_station)

# Ejecutar la función principal
if __name__ == "__main__":
    asyncio.run(main())