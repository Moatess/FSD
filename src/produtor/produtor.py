import socket
import threading
import os

from src.produtor.produtor_rest import start_produtor_rest
from src.produtor.registo_gestor import iniciar_registo_gestor


class Produtor:
    def __init__(self, stock_file='/Users/joaofernandes/PycharmProjects/FSD/src/Stock.txt'):
            self.stock_file = stock_file
            self.stock = {}
            self.lock = threading.Lock()  # Para controlar o acesso ao stock
            self.carregar_stock()

    def carregar_stock(self):
        if os.path.exists(self.stock_file):
            print(f"A carregar o stock a partir de {self.stock_file}...")
            with open(self.stock_file, 'r') as f:
                for linha in f:
                    linha = linha.strip()
                    if linha:  # Verifica se a linha não está vazia
                        try:
                            categoria, produto, preco, quantidade = linha.split('|')
                            if categoria not in self.stock:
                                self.stock[categoria] = {}
                            self.stock[categoria][produto] = {
                                'preco': float(preco),
                                'quantidade': int(quantidade)
                            }
                        except ValueError as e:
                            print(f"Erro ao processar a linha: {linha}. Erro: {e}")
        else:
            print("Ficheiro de stock não encontrado. A criar stock vazio.")

    def listar_produtos(self, categorias):
        produtos_disponiveis = {}
        for categoria in categorias:
            if categoria in self.stock:
                produtos_disponiveis[categoria] = self.stock[categoria]
        return produtos_disponiveis

    def comprar_produto(self, categoria, produto, quantidade):
        with self.lock:  #  com isto só um Marketplace faz alteração no stock de cada vez
            if categoria in self.stock and produto in self.stock[categoria]:
                if self.stock[categoria][produto]['quantidade'] >= quantidade:
                    self.stock[categoria][produto]['quantidade'] -= quantidade
                    return f"Compra bem-sucedida de {quantidade} unidades de {produto}."
                else:
                    return "Quantidade insuficiente."
            else:
                return "Produto ou categoria não encontrados."

def handle_marketplace_connection(conn, addr, produtor):
    print(f"Conectado ao Marketplace: {addr}")
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"Recebido: {data}")
            parts = data.split('|')

            if parts[0] == 'LISTAR':
                categorias = parts[1].split(',')
                resposta = produtor.listar_produtos(categorias)
                conn.send(str(resposta).encode())

            elif parts[0] == 'COMPRAR':
                categoria = parts[1]
                produto = parts[2]
                quantidade = int(parts[3])
                resposta = produtor.comprar_produto(categoria, produto, quantidade)
                conn.send(resposta.encode())

            else:
                conn.send("Comando inválido.".encode())

    finally:
        conn.close()

def start_produtor():
    servidor_produtor = Produtor()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('10.8.0.12', 7012))
    server_socket.listen(5)
    print("Produtor a aguardar conexões...")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_marketplace_connection, args=(conn, addr, servidor_produtor))
        thread.start()


if __name__ == '__main__':
    # Carrega o stock e inicia o Produtor Socket
    servidor_produtor = Produtor()
    threading.Thread(target=start_produtor).start()


