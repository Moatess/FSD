import socket
import threading

# Estrutura de produtos do Produtor
produtos = {
    "Frutas": {"morangos": 100, "pera": 50},
    "Legumes": {"tomate": 75, "alface": 20}
}


def listar_produtos(categorias):
    resposta = {}
    for categoria in categorias:
        if categoria in produtos:
            resposta[categoria] = produtos[categoria]
    return resposta


def comprar_produto(nome_produto, quantidade):
    for categoria in produtos:
        if nome_produto in produtos[categoria]:
            if produtos[categoria][nome_produto] >= quantidade:
                produtos[categoria][nome_produto] -= quantidade
                return f"Produto {nome_produto} comprado com sucesso!\n"
            else:
                return "Quantidade inválida. Por favor, verifique o estoque disponível e tente novamente.\n"
    return "Produto inexistente. Por favor, verifique o nome do produto e tente novamente.\n"


def enviar_resposta(cliente, mensagem):
    cliente.sendall((mensagem + "\npedido: ").encode('utf-8'))


def atender_cliente(cliente):
    try:
        enviar_resposta(cliente, "Bem-vindo ao servidor do Produtor! O que deseja consultar?\n")

        while True:
            pedido = cliente.recv(1024).decode('utf-8').strip()  # Decodificar usando 'utf-8'
            if not pedido:
                break

            print(f"Pedido recebido: {pedido}")

            partes_pedido = pedido.split(";")
            if len(partes_pedido) != 2:
                mensagem_erro = (
                    "Pedido inválido. Esperava-se o formato:\n"
                    "LISTA_PRODUTOS;<categoria1,categoria2,...> ou\n"
                    "COMPRAR_PRODUTO;<nome_produto,quantidade>\n"
                    "Por favor, corrija e tente novamente.\n"
                )
                enviar_resposta(cliente, mensagem_erro)
                continue

            acao, parametros = partes_pedido

            if acao == "LISTA_PRODUTOS":
                categorias = parametros.split(",")
                resposta = listar_produtos(categorias)
            elif acao == "COMPRAR_PRODUTO":
                parametros = parametros.split(",")
                if len(parametros) != 2:
                    resposta = (
                        "Pedido inválido. Esperava-se o formato:\n"
                        "COMPRAR_PRODUTO;<nome_produto,quantidade>\n"
                        "Por favor, corrija e tente novamente.\n"
                    )
                else:
                    nome_produto, quantidade = parametros
                    resposta = comprar_produto(nome_produto.strip(), int(quantidade.strip()))
            else:
                resposta = (
                    "Ação inválida. As ações válidas são:\n"
                    "LISTA_PRODUTOS e COMPRAR_PRODUTO.\n"
                    "Por favor, corrija e tente novamente.\n"
                )

            print(f"Resposta enviada: {resposta}")
            enviar_resposta(cliente, str(resposta))
    except Exception as e:
        print(f"Erro: {e}")
        enviar_resposta(cliente, f"Erro: {e}\nPor favor, tente novamente.")
    finally:
        print("Cliente desconectado")
        cliente.close()


def iniciar_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(('localhost', 12345))
    servidor.listen()

    print("Servidor Produtor esperando conexões...")

    while True:
        cliente, endereco = servidor.accept()
        print(f"Conexão estabelecida com: {endereco}")
        threading.Thread(target=atender_cliente, args=(cliente,)).start()


iniciar_servidor()
