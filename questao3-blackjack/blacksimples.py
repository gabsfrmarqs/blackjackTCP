import random
import socket
import pickle

# Define the deck of cards
suits = ['Copas', 'Ouro', 'Paus', 'Espadas']
ranks = [
    'Dois', 'Tres', 'Quatro', 'Cinco', 'Seis', 'Sete', 'Oito', 'Nove', 'Dez',
    'Valete', 'Dama', 'Rei', 'As'
]

# Create a dictionary to represent card values
card_values = {
    'Dois': 2,
    'Tres': 3,
    'Quatro': 4,
    'Cinco': 5,
    'Seis': 6,
    'Sete': 7,
    'Oito': 8,
    'Nove': 9,
    'Dez': 10,
    'Valete': 10,
    'Dama': 10,
    'Rei': 10,
    'As': 11
}


# Function to initialize and shuffle the deck
def initialize_deck():
  deck = [{'Rank': rank, 'Suit': suit} for rank in ranks for suit in suits]
  random.shuffle(deck)
  return deck


# Function to calculate the total value of a hand
def calculate_hand_value(hand):
  value = sum(card_values[card['Rank']] for card in hand)
  # Adjust for Aces
  for card in hand:
    if card['Rank'] == 'As' and value > 21:
      value -= 10
  return value


# Function to display a hand
def display_hand(hand):
  for card in hand:
    print(f"{card['Rank']} de {card['Suit']}")

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

data = conn.recv(TAMANHO_BUFFER)
received = pickle.loads(data)
print("Nome do jogador:", received)

player_name = received

print(
    "Bem vindo ao Blackjack (21) via TCP. Você é o servidor, agindo como dealer."
)
print(
    "Quando um comando for solicitado, digite 'hit' para pedir mais uma carta ou 'stand' para finalizar sua jogada."
)

deck = initialize_deck()



# Deal initial cards to the player and dealer
player_hand = [deck.pop(), deck.pop()]
dealer_hand = [deck.pop(), deck.pop()]

conn.send(pickle.dumps(player_hand))
conn.send(pickle.dumps(dealer_hand))

print("Mão do jogador:")
display_hand(player_hand)

print("\nMão do dealer:")
print(
    f"Face up card: \n{dealer_hand[0]['Rank']} de {dealer_hand[0]['Suit']}")

while True: #será usado também para conexão e recebimento de mensagens
  player_value = calculate_hand_value(player_hand)
  if player_value == 21:
    print("Blackjack! Player venceu!")
    break
  elif player_value > 21:
    print("Estouro! Player perdeu.")
    break

  action = input("\n'hit', 'stand' ou 'chat'? ").lower()
  if action == 'chat':
    message_to_send = input("Sua mensagem: ")
    conn.send(message_to_send.encode("utf-8"))
  elif action == 'hit':
    player_hand.append(deck.pop())
    print("\nMão do Player:")
    display_hand(player_hand)
  elif action == 'stand':
    dealer_value = calculate_hand_value(dealer_hand)
    while dealer_value < 17:
      dealer_hand.append(deck.pop())
      dealer_value = calculate_hand_value(dealer_hand)

    print("\nMão do Dealer:")
    display_hand(dealer_hand)

    if dealer_value > 21:
      print("Dealer estourou! Player venceu!")
    elif dealer_value > player_value:
      print("Dealer ganhou.")
    elif dealer_value < player_value:
      print("Você ganhou!")
    else:
      print("Empate!")

    break
  else:
    print("Inválido. Digite 'hit', 'stand' ou 'chat'.")
