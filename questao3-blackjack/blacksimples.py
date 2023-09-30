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
  sum = 0
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

data_to_send = {
    'player_hand': player_hand,
    'dealer_hand': dealer_hand
}

serialized_data = pickle.dumps(data_to_send)

conn.send(serialized_data)

#print("Mão do jogador:")
#display_hand(player_hand)

print("\nMão do dealer:")
display_hand(dealer_hand)

while True: #será usado também para conexão e recebimento de mensagens
  player_value = calculate_hand_value(player_hand)
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

##ação do jogador PLAYER
  data = conn.recv(TAMANHO_BUFFER)
  player_action = pickle.loads(data)


  #action = input("\n'hit', 'stand' ou 'chat'? ").lower()
  if player_action[0] == 'chat':
    print(f"Mensagem do {player_name}: {player_action[1]}")
    data_to_send = {
    'player_hand': player_hand,
    'dealer_hand': dealer_hand
}

    serialized_data = pickle.dumps(data_to_send)

    conn.send(serialized_data)
    
  elif player_action[0] == 'hit':
    carta_poppada = deck.pop()
    player_hand.append(carta_poppada)
    print(f"\n{player_name} usou 'hit'!")
    print(f"+{carta_poppada['Rank']} de {carta_poppada['Suit']}")
    #print("Mão do Player:") 
    #display_hand(player_hand)
    #print(f"Soma: {sum_hand(player_hand)}")
    data_to_send = {
    'player_hand': player_hand,
    'dealer_hand': dealer_hand
}

    serialized_data = pickle.dumps(data_to_send)

    conn.send(serialized_data)
    
  elif player_action[0] == 'stand':
    dealer_playing = True
    print(f"\n{player_name} usou 'stand'!")
    while dealer_playing:
      dealer_action = input("\n'hit', 'stand' ou 'chat'? ").lower()
      if dealer_action == "chat":
        message = input("Sua mensagem: ")
        envio = (dealer_action,message)
        conn.send(pickle.dumps(envio))
        
      elif dealer_action == "hit":
        
        carta_poppada_dealer = deck.pop()
        dealer_hand.append(carta_poppada_dealer)
        print(f"\nDealer usou 'hit'!\nMão do Dealer:")
        display_hand(dealer_hand)
        print(f"Soma: {sum_hand(dealer_hand)}")
        envio = (dealer_action,carta_poppada_dealer)
        #print(f"DEBUG: {carta_poppada}")
        conn.send(pickle.dumps(envio))
        
      elif dealer_action == "stand":
        envio = (dealer_action,None)
        conn.send(pickle.dumps(envio))
        dealer_playing = False
      
    dealer_value = calculate_hand_value(dealer_hand)


    data_to_send = {
    'player_hand': player_hand,
    'dealer_hand': dealer_hand
}

    serialized_data = pickle.dumps(data_to_send)

    conn.send(serialized_data)
    
    """
    print(f"\n{player_name} usou 'stand'!\nMão do Dealer:")
    display_hand(dealer_hand)
    print(f"Soma: {sum_hand(dealer_hand)}")
    """
    
    #display_hand(dealer_hand)
    
    if dealer_value > 21:
            print(f"\nVocê estourou! {player_name} venceu!")
    elif dealer_value > player_value:
        
        print(f"\nDealer ganhou! {player_name} perdeu.")
    elif dealer_value < player_value:
        print(f"\n{player_name} ganhou!\nVocê perdeu.")
    else:
        print("Empate!")
    dealer_playing = False
    
    
    

    break
  else:
    print("Inválido. Digite 'hit', 'stand' ou 'chat'.")


"""
while True: #será usado também para conexão e recebimento de mensagens
  player_value = calculate_hand_value(player_hand)
  if player_value == 21:
    print("Blackjack! Player venceu!")
    break
  elif player_value > 21:
    print("Estouro! Player perdeu.")
    break

    data = conn.recv(TAMANHO_BUFFER)
    action = pickle.loads(data)
    #print("Jogador tirou:", received)

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

"""
