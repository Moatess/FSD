from flask import Flask, jsonify, request
import threading
import requests
import time

GESTOR_URL = 'http://193.136.11.170:5001/produtor'

class MarketplaceREST:
    def __init__(self):
        self.produtores_rest = []

    def atualizar_produtores_periodicamente(self):

        while True:
            try:
                response = requests.get(GESTOR_URL)
                if response.status_code == 200:
                    self.produtores_rest = response.json()
            except Exception as e:
                print(f"Erro ao atualizar produtores REST: {e}")
            time.sleep(300)  # Atualizar a cada 5 minutos

    def selecionar_produtor(self):
        if not self.produtores_rest:
            print("\nNenhum produtor REST disponível no momento.")
            return None
        print("\nProdutores REST disponíveis no Gestor de Produtores:")
        for i, produtor in enumerate(self.produtores_rest, 1):
            print(f"{i}. {produtor['ip']} (Nome: {produtor['nome']}, Porta: {produtor['porta']})")
        while True:
            escolha = input("\nEscolha o número do produtor para se ligar ou 'q' para sair: ")
            if escolha.lower() == 'q':
                return None
            if escolha.isdigit() and 1 <= int(escolha) <= len(self.produtores_rest):
                return self.produtores_rest[int(escolha) - 1]
            print("\nOpção inválida. Tente novamente.")

    def listar_categorias(self, produtor):
        url = f"http://{produtor['ip']}:{produtor['porta']}/categorias"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                categorias = response.json()
                print("\nCategorias disponíveis:", ', '.join(categorias))
                return categorias
            else:
                print("\nErro ao listar categorias. Código:", response.status_code)
                return []
        except Exception as e:
            print("\nErro ao conectar ao produtor:", e)
            return []

    def listar_produtos_por_categoria(self, produtor, categoria):
        url = f"http://{produtor['ip']}:{produtor['porta']}/produtos?categoria={categoria}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                produtos = response.json()
                print("\nProdutos disponíveis:")
                for produto in produtos:
                    print(f"- {produto['produto']} (Preço: {produto['preco']}€, Quantidade: {produto['quantidade']})")
                return produtos
            else:
                print("\nErro ao listar produtos. Código:", response.status_code)
                return []
        except Exception as e:
            print("\nErro ao conectar ao produtor:", e)
            return []

    def comprar_produto(self, produtor, produto, quantidade):
        url = f"http://{produtor['ip']}:{produtor['porta']}/comprar/{produto}/{quantidade}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("\nCompra realizada com sucesso!")
            else:
                print("Erro ao realizar compra. Código:", response.status_code)
        except Exception as e:
            print("Erro ao conectar ao produtor:", e)

    def menu_produtor(self, produtor):

        while True:
            print(f"\n==============     Marketplace ligado ao ({produtor['ip']})   ============")
            print("1. Listar Categorias")
            print("2. Listar Produtos por Categoria")
            print("3. Comprar Produto")
            print("b. Voltar ao Menu Principal")
            escolha = input("Escolha uma opção: ")
            if escolha == '1':
                self.listar_categorias(produtor)
            elif escolha == '2':
                categorias = self.listar_categorias(produtor)
                if categorias:
                    categoria = input("\nEscolha uma categoria: ")
                    if categoria in categorias:
                        self.listar_produtos_por_categoria(produtor, categoria)
                    else:
                        print("Categoria inválida.")
            elif escolha == '3':
                produto = input("\nNome do produto: ")
                quantidade = input("Quantidade: ")
                if quantidade.isdigit():
                    self.comprar_produto(produtor, produto, int(quantidade))
                else:
                    print("Quantidade inválida.")
            elif escolha.lower() == 'b':
                break
            else:
                print("Opção inválida. Tente novamente.")

    def menu_principal(self):

        while True:
            print("\n==============     Menu Principal do Marketplace Rest Do Grupo 6 PL3   ============\n")
            print("1. Selecionar Produtor REST")
            escolha = input("\nEscolha uma opção: ")
            if escolha == '1':
                produtor = self.selecionar_produtor()
                if produtor:
                    self.menu_produtor(produtor)
            else:
                print("Opção inválida. Tente novamente.")

    def run(self):
        threading.Thread(target=self.atualizar_produtores_periodicamente).start()
        self.menu_principal()


if __name__ == '__main__':
    marketplace_rest = MarketplaceREST()
    marketplace_rest.run()
