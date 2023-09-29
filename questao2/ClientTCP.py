import socket

TCP_IP = '192.168.100.135'
TCP_PORTA = 42107
TAMANHO_BUFFER = 1024

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((TCP_IP, TCP_PORTA))

MENSAGEM = "placeholder"

while MENSAGEM != "QUIT" and MENSAGEM != "quit":
    MENSAGEM = input("Sua mensagem: ")

    #Manda mensagem
    cliente.send(MENSAGEM.encode('UTF-8'))

    #Recebe dados
    data = cliente.recv(TAMANHO_BUFFER)

    if data.decode('UTF-8') == "QUIT":
        print("Servidor QUITou. Fechando conexao.")
        cliente.close()
        exit()
    else:
        print("Recebeu:", data.decode('UTF-8'))

#Fecha a conexão se digitar QUIT
if MENSAGEM == "QUIT" or MENSAGEM == "quit":
    print("Cliente QUITou. Fechando conexao.")
    cliente.close()  #Fecha a conexão
