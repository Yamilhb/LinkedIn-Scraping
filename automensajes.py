from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # Para esperar a que el html cargue antes de acceder.
from selenium.webdriver.support import expected_conditions as EC # La condición que estamos esperando.
from selenium.webdriver.common.by import By # Para manejar ciertos elementos del html.
from selenium.webdriver.common.keys import Keys
import time
import sys
import pandas as pd

name = sys.argv[1]
clave = sys.argv[2]
data = pd.read_csv(f'./data/{sys.argv[3]}')
mis_names = data['mis_names'].values
#print(len(mis_names),mis_names, mis_names[0])
#print(f'usuario: {name}\npass: {clave}')
# ACCEDEMOS A NUESTRA CUENTA
driver = webdriver.Chrome()

# INICIALIZAMOS EL NAVEGADOR
driver.get('https://www.linkedin.com/')

# Esperar a que la página se cargue completamente

# Introduzco usuario.
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                       'input#session_key')))\
    .send_keys(name)

# Introduzco clave.
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                       'input#session_password')))\
    .send_keys(clave)

# Pulso.
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                       '//*[@id="main-content"]/section[1]/div/div/form/div[2]/button')))\
    .click()

time.sleep(10)

# Capturo el objeto buscador.
busqueda =WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    'input[aria-label="Search"]')))

# Recorro el listado de nombres.
for nombre in mis_names:

    # Busco perfiles.
    busqueda.send_keys('') # Escribo nombre.
    busqueda.send_keys(nombre) # Escribo nombre.
    busqueda.send_keys(Keys.RETURN) # Ejecuto búsqueda.

    time.sleep(3)
    
    # Busco el botón de conectar.
    boton_mensaje = driver.find_elements(By.TAG_NAME, "button")
    try:
        boton_mensaje = [x for x in boton_mensaje if x.text == 'Connect']
    except:
        boton_mensaje = []
    if len(boton_mensaje)>=1:
        try:
            boton_mensaje = boton_mensaje[0]

            # Uso el nombre que usé en la búsqueda.
            nombre_amensajado = nombre

            # Envío invitación.
            if boton_mensaje is not None:
                boton_mensaje.click()

                # Hago click en añadir un mensaje a la invitación.
                WebDriverWait(driver, 5)\
                    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                    'button.artdeco-button artdeco-button--muted artdeco-button--2 artdeco-button--secondary ember-view mr1'.replace(' ', '.'))))\
                    .click()
                # Escribo el mensaje.
                WebDriverWait(driver, 5)\
                    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                    'textarea.ember-text-area ember-view connect-button-send-invite__custom-message mb3'.replace(' ','.'))))\
                    .send_keys(f'Hola {nombre_amensajado.split(" ")[0]}!\nSoy parte del equipo de Bci Labs y e invito a seguirnos: https://www.linkedin.com/company/bci-labs/\n\
Podrás explorar tendencias en innovación y nuestras última iniciativas\nUn saludo!')
                #Envío la invitación con el mensaje.
                WebDriverWait(driver, 5)\
                    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                    'button.artdeco-button artdeco-button--2 artdeco-button--primary ember-view ml1'.replace(' ', '.'))))\
                    .click()
        #    driver.back()
            
            del(nombre_amensajado)
        except:
            boton_mensaje = None

    busqueda.clear()
    del(boton_mensaje)
    print(nombre)
        


input("Presiona Enter para continuar después de interactuar con el perfil...")

