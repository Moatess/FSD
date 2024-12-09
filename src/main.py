import threading
from src.produtor.produtor import start_produtor
from src.produtor.produtor_rest import start_produtor_rest
from src.marketplace.marketplace import start_marketplace
from src.marketplace.marketplace_rest import MarketplaceREST

def menu_principal():
    while True:
        print("\n============== Menu Principal ==============")
        print("1. Iniciar Produtor Socket")
        print("2. Iniciar Produtor REST")
        print("3. Iniciar Marketplace REST")
        print("4. Iniciar Marketplace Socket")
        print("q. Sair")
        escolha = input("\nEscolha uma opção: ")

        if escolha == '1':
            print("\nIniciando Produtor Socket...")
            threading.Thread(target=start_produtor).start()
        elif escolha == '2':
            print("\nIniciando Produtor REST...")
            start_produtor_rest()
        elif escolha == '3':
            print("\nIniciando Marketplace REST...")
            marketplace_rest = MarketplaceREST()
            marketplace_rest.run()
        elif escolha == '4':
            print("\nIniciando Marketplace Socket...")
            start_marketplace()
        elif escolha.lower() == 'q':
            print("\nA sair...")
            break
        else:
            print("\nOpção inválida. Tente novamente.")

if __name__ == '__main__':
    menu_principal()
