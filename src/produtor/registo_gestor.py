import threading
import requests
import time

GESTOR_URL = 'http://193.136.11.170:5001/produtor'
PRODUTOR_IP = '192.168.1.71'
PRODUTOR_PORTA = 1194
PRODUTOR_NOME = 'JOAO_PL6_GRUPO3'

def registar_produtor_periodicamente():

    while True:
        try:
            response = requests.post(GESTOR_URL, json={
                "ip": PRODUTOR_IP,
                "porta": PRODUTOR_PORTA,
                "nome": PRODUTOR_NOME
            })
            if response.status_code in [200, 201]:
                print("Produtor REST registado com sucesso no Gestor.")
            else:
                print("Erro ao registar o Produtor REST no Gestor:", response.status_code)
        except Exception as e:
            print("Erro ao conectar ao Gestor de Produtores:", e)
        time.sleep(300)  # Regista de novo a cada 5 minutos

def iniciar_registo_gestor():

    print("Iniciando registo no Gestor de Produtores...")
    registo_thread = threading.Thread(target=registar_produtor_periodicamente)
    registo_thread.start()
