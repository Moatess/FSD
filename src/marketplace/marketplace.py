import socket


def listar_produtos(sock, categorias):
    try:
        mensagem = f"LISTAR|{','.join(categorias)}"
        sock.send(mensagem.encode())
        resposta = sock.recv(1024).decode()
        print("Produtos disponíveis:", resposta)
    except socket.error as e:
        print(f"Erro ao comunicar com o servidor: {e}")


def comprar_produto(sock, categoria, produto, quantidade):
    if quantidade <= 0:
        print("Erro: Quantidade inválida. Deve ser maior que 0.")
        return
    mensagem = f"COMPRAR|{categoria}|{produto}|{quantidade}"
    sock.send(mensagem.encode())
    resposta = sock.recv(1024).decode()
    print("Resposta à compra:", resposta)


def start_marketplace():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(('10.8.0.12', 7012))
        print("Conectado ao Produtor.")
    except ConnectionRefusedError:
        print("Erro: Não foi possível conectar ao Produtor.")
        return

    while True:
        print("1. Listar Produtos")
        print("2. Comprar Produto")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            categorias = input("Insira as categorias (separadas por vírgulas): ").split(',')
            listar_produtos(sock, categorias)
        elif opcao == '2':
            categoria = input("Categoria: ")
            produto = input("Produto: ")
            quantidade = int(input("Quantidade: "))
            comprar_produto(sock, categoria, produto, quantidade)
        else:
            print("Opção inválida.")

if __name__ == '__main__':
    start_marketplace()
