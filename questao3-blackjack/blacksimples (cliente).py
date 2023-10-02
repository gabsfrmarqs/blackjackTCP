import socket

def main():
    host = '192.168.100.103'
    porta = 12343

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, porta))
    print(f"Conectado a {host}:{porta}")

    try:
        while True:
            mensagem = cliente.recv(1024).decode()
            print(mensagem)

            origem = input("Digite a coordenada da peça a ser movida (linha,coluna): ")
            destino = input("Digite a coordenada de destino (linha,coluna): ")

            cliente.sendall(origem.encode())
            cliente.sendall(destino.encode())

            resposta = cliente.recv(1024).decode()
            print(resposta)

    except KeyboardInterrupt:
        print("Conexão encerrada.")
        cliente.close()

if __name__ == "__main__":
    main()
