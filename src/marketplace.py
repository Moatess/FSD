import socket


def conectar_ao_produtor():
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(('localhost', 12345))  # IP e porta do Produtor

        # Enviar pedido para o Produtor (exemplo: listar produtos)
        cliente.sendall(b"LISTA_PRODUTOS;Frutas,Legumes")

        # Receber resposta do Produtor
        resposta = cliente.recv(1024)
        if resposta:
            print(f"Resposta do Produtor (listar produtos): {resposta.decode()}")

        # Enviar pedido de compra para o Produtor
        cliente.sendall(b"COMPRAR_PRODUTO;morangos,10")

        resposta = cliente.recv(1024)
        if resposta:
            print(f"Resposta do Produtor (compra produto): {resposta.decode()}")

    except ConnectionResetError:
        print("Erro de conexão: Conexão foi redefinida pelo servidor.")
    except ConnectionRefusedError:
        print("Erro de conexão: Não foi possível conectar ao servidor. Verifique se o servidor está funcionando.")
    except socket.error as erro:
        print(f"Erro de socket: {erro}")
    finally:
        cliente.close()


# Executar o teste de conexão e compra
conectar_ao_produtor()
