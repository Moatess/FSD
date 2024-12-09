from flask import Flask, jsonify, request
import threading
import os
import time

from src.produtor.registo_gestor import iniciar_registo_gestor


class ProdutorREST:
    def __init__(self, stock_file='/Users/joaofernandes/PycharmProjects/FSD/src/Stock Produtor Rest.txt'):
        self.stock_file = stock_file
        self.stock = self.carregar_stock()
        self.app = Flask(__name__)
        self._configurar_rotas()

    def carregar_stock(self):
        stock = {}
        if os.path.exists(self.stock_file):
            with open(self.stock_file, 'r') as f:
                for linha in f:
                    linha = linha.strip()
                    if linha:
                        try:
                            categoria, produto, preco, quantidade = linha.split('|')
                            if categoria not in stock:
                                stock[categoria] = {}
                            stock[categoria][produto] = {
                                'preco': float(preco),
                                'quantidade': int(quantidade)
                            }
                        except ValueError:
                            print(f"Erro ao processar a linha: {linha}")
        else:
            print(f"Ficheiro de stock não encontrado: {self.stock_file}. Criando um stock vazio.")
        return stock

    def _configurar_rotas(self):

        @self.app.route('/categorias', methods=['GET'])
        def listar_categorias():
            categorias = list(self.stock.keys())
            return jsonify(categorias), 200

        @self.app.route('/produtos', methods=['GET'])
        def listar_produtos_por_categoria():
            categoria = request.args.get('categoria')
            if categoria in self.stock:
                produtos = [
                    {
                        "categoria": categoria,
                        "produto": produto,
                        "quantidade": detalhes["quantidade"],
                        "preco": f"{detalhes['preco']}€"
                    }
                    for produto, detalhes in self.stock[categoria].items()
                ]
                return jsonify(produtos), 200
            else:
                return jsonify("1: Categoria Inexistente"), 404

        @self.app.route('/comprar/<produto>/<int:quantidade>', methods=['GET'])
        def comprar_produto(produto, quantidade):
            for categoria, produtos in self.stock.items():
                if produto in produtos:
                    if produtos[produto]["quantidade"] >= quantidade:
                        produtos[produto]["quantidade"] -= quantidade
                        return jsonify("Produtos comprados"), 200
                    else:
                        return jsonify("2: Quantidade indisponível"), 404
            return jsonify("1: Produto inexistente"), 404

    def run(self):
        self.app.run(host='0.0.0.0', port=1194)


def start_produtor_rest():
    iniciar_registo_gestor()
    produtor_rest = ProdutorREST()
    rest_thread = threading.Thread(target=produtor_rest.run)
    rest_thread.start()




