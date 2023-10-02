import random
import socket
import pickle
import json

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

def sum_hand(hand):
    total_value = 0
    num_aces = 0  # Count the number of Aces in the hand

    for card in hand:
        rank = card['Rank']
        total_value += card_values[rank]

        if rank == 'As':
            num_aces += 1

    # Adjust for Aces if the total value exceeds 21
    while num_aces > 0 and total_value > 21:
        total_value -= 10  # Deduct 10 for each Ace (changes Ace's value from 11 to 1)
        num_aces -= 1

    return total_value

#FUNÇÃO MAIN

TCP_IP = '192.168.100.103'
TCP_PORTA = 42107
TAMANHO_BUFFER = 1024

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((TCP_IP, TCP_PORTA))

print(
    "Bem vindo ao Blackjack (21) via TCP. Você é o cliente, agindo como player."
)
print(
    "Quando um comando for solicitado, digite 'hit' para pedir mais uma carta ou 'stand' para finalizar sua jogada."
)

player_name = input("Insira seu nome de jogador: ")
cliente.send(pickle.dumps(player_name))

#received_data = cliente.recv(1024)  # Adjust the buffer size as needed
#received_tuple = pickle.loads(received_data)
#print("Received tuple:", received_tuple)

deck = initialize_deck()

# Deal initial cards to the player and dealer
# Receive the serialized data
data_received = cliente.recv(TAMANHO_BUFFER)

# Unpickle the entire data
received_data = pickle.loads(data_received)
print(received_data)

# Access player_hand and dealer_hand
player_hand = received_data['player_hand']
dealer_hand = received_data['dealer_hand']

print("Mão do jogador:")
display_hand(player_hand)

#print("\nMão do dealer:")
#print(f"Face up card: \n{dealer_hand[0]['Rank']} de {dealer_hand[0]['Suit']}")

while True: #será usado também para conexão e recebimento de mensagens
  player_value = calculate_hand_value(player_hand)
  dealer_value = calculate_hand_value(dealer_hand)
  if player_value == 21:
  
    print("\nMão do Player:")
    display_hand(player_hand)
    print(f"Soma {player_name}: {sum_hand(player_hand)}")
    
    print("\nMão do Dealer:")
    display_hand(dealer_hand)
    print(f"Soma dealer: {sum_hand(dealer_hand)}")
    print(f"Blackjack! {player_name} venceu!")
    break
  elif player_value > 21:
    print("\nMão do Player:")
    display_hand(player_hand)
    print(f"Soma {player_name}: {sum_hand(player_hand)}")
    
    print("\nMão do Dealer:")
    display_hand(dealer_hand)
    print(f"Soma dealer: {sum_hand(dealer_hand)}")
    print(f"Estouro! {player_name} perdeu.")
    break

  action = None
  action = input("\n'hit', 'stand' ou 'chat'? ").lower()
  if action == 'chat':
    message = input("Sua mensagem: ")
    envio = (action,message)
    cliente.send(pickle.dumps(envio))
    
    data = cliente.recv(TAMANHO_BUFFER)
    received_data = pickle.loads(data)

    #Access player_hand and dealer_hand
    player_hand = received_data['player_hand']
    dealer_hand = received_data['dealer_hand']
  
  elif action == 'hit':
    envio = (action,None)
    cliente.send(pickle.dumps(envio))
   
    data = cliente.recv(TAMANHO_BUFFER)
    received_data = pickle.loads(data)

    #Access player_hand and dealer_hand
    player_hand = received_data['player_hand']
    dealer_hand = received_data['dealer_hand']
    
    
    print("\nMão do Player:")
    display_hand(player_hand)
    print(f"Soma: {sum_hand(player_hand)}")
        
  
  elif action == 'stand':
    envio = (action,None)
    cliente.send(pickle.dumps(envio))
    dealer_playing = True
    while dealer_playing == True:
        data = cliente.recv(TAMANHO_BUFFER)
        dealer_action = pickle.loads(data)
        if dealer_action[0] == "chat":
            print(f"Mensagem do dealer: {dealer_action[1]}")
        elif dealer_action[0] == "hit":
            print(f"Dealer usou 'hit'")
            print(f"+{dealer_action[1]['Rank']} de {dealer_action[1]['Suit']}")
        elif dealer_action[0] == "stand":
            print(f"Dealer usou 'stand'!")
            dealer_playing = False
            
  else:
    print("Inválido. Digite 'hit', 'stand' ou 'chat'.")
    envio = ("invalido",None)
    cliente.send(pickle.dumps(envio))
    
    
  #print("aqui chega")
  data = cliente.recv(TAMANHO_BUFFER)
  #print("data")
  received_data = pickle.loads(data)
  #print("aqui não")
    

    #Access player_hand and dealer_hand
  player_hand = received_data['player_hand']
  dealer_hand = received_data['dealer_hand']
            
  
