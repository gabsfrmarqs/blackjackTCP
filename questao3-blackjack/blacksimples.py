import socket

# Inicialização do tabuleiro de Damas
def inicializar_tabuleiro():
    tabuleiro = [[' ' for _ in range(8)] for _ in range(8)]
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 1:
                if i < 3:
                    tabuleiro[i][j] = 'O'
                elif i > 4:
                    tabuleiro[i][j] = 'X'
    return tabuleiro

# Função para imprimir o tabuleiro
def imprimir_tabuleiro(tabuleiro):
    print("  0 1 2 3 4 5 6 7")
    for i in range(8):
        print(i, end=' ')
        for j in range(8):
            print(tabuleiro[i][j], end=' ')
        print()

# Função para verificar se um movimento é válido
def movimento_valido(tabuleiro, jogador, origem, destino):
    x1, y1 = origem
    x2, y2 = destino

    if tabuleiro[x2][y2] != ' ':
        return False

    if jogador == 'X':
        if x2 - x1 == 1 and abs(y2 - y1) == 1:
            return True
        elif x2 - x1 == 2 and abs(y2 - y1) == 2 and tabuleiro[(x1 + x2) // 2][(y1 + y2) // 2] == 'O':
            return True
    elif jogador == 'O':
        if x1 - x2 == 1 and abs(y2 - y1) == 1:
            return True
        elif x1 - x2 == 2 and abs(y2 - y1) == 2 and tabuleiro[(x1 + x2) // 2][(y1 + y2) // 2] == 'X':
            return True

    return False

# Função principal do servidor
def main():
    host = '192.168.100.103'
    porta = 12343

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, porta))
    servidor.listen(1)
    print(f"Servidor ouvindo em {host}:{porta}")

    jogador_atual = 'X'
    tabuleiro = inicializar_tabuleiro()

    while True:
        cliente, endereco = servidor.accept()
        print(f"Jogador {jogador_atual} conectado de {endereco}")

        try:
            while True:
                imprimir_tabuleiro(tabuleiro)
                cliente.sendall(str(tabuleiro).encode())
                origem = cliente.recv(1024).decode()
                destino = cliente.recv(1024).decode()

                origem = tuple(map(int, origem.split(',')))
                destino = tuple(map(int, destino.split(',')))

                if movimento_valido(tabuleiro, jogador_atual, origem, destino):
                    tabuleiro[destino[0]][destino[1]] = tabuleiro[origem[0]][origem[1]]
                    tabuleiro[origem[0]][origem[1]] = ' '
                    cliente.sendall("Movimento válido".encode())

                    # Trocar de jogador
                    jogador_atual = 'O' if jogador_atual == 'X' else 'X'
                else:
                    cliente.sendall("Movimento inválido. Tente novamente.".encode())

        except ConnectionResetError:
            print(f"Jogador {jogador_atual} desconectado.")
            cliente.close()

if __name__ == "__main__":
    main()
