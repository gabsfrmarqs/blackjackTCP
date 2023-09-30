import socket

TCP_IP = '192.168.100.103'
TCP_PORTA = 42107
TAMANHO_BUFFER = 1024

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
servidor.bind((TCP_IP, TCP_PORTA))
servidor.listen(1)

print(f"Servidor disponível na porta {TCP_PORTA} e escutando.....")

conn, addr = servidor.accept()
print('Endereço conectado:', addr)

while True:
    data = conn.recv(TAMANHO_BUFFER)
    
    if not data:
        break  #S
   
    print("Mensagem recebida:", data.decode("utf-8"))

    #Verifica se a conexão fechará
    if data.decode("utf-8").strip() == "QUIT":
        print("Cliente QUITou. Fechando conexao.")
        conn.close()
        servidor.close()  # Close the server socket
        exit(0)

    #Manda resposta
    message_to_send = input("Sua mensagem: ")
    conn.send(message_to_send.encode("utf-8"))
    if message_to_send == "QUIT":
        print("Servidor QUITou. Fechando conexao.")
        conn.close()
        break

#Fecha o servidor
servidor.close()
