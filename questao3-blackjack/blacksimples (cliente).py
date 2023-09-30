import random

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


# Function to play a round of Blackjack
def play_blackjack():
  deck = initialize_deck()

  # Deal initial cards to the player and dealer
  player_hand = [deck.pop(), deck.pop()]
  dealer_hand = [deck.pop(), deck.pop()]

  print("Mão do jogador:")
  display_hand(player_hand)

  print("\nMão do dealer:")
  print(f"Face up card: {dealer_hand[0]['Rank']} de {dealer_hand[0]['Suit']}")

  while True:
    player_value = calculate_hand_value(player_hand)
    if player_value == 21:
      print("Blackjack! Player venceu!")
      break
    elif player_value > 21:
      print("Estouro! Player perdeu.")
      break

    action = input("\n'hit' ou 'stand'? ").lower()
    if action == 'chat':
      print('não implementado puta')
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


print(
    "Bem vindo ao Blackjack (21) via TCP. O Player agirá como cliente, enquanto o Dealer será o servidor."
)
print(
    "O Dealer terá sempre uma carta escondida do jogador. Todas as cartas do jogador estarão visíveis."
)
print(
    "Quando um comando for solicitado, digite 'hit' para pedir mais uma carta ou 'stand' para finalizar sua jogada."
)

play_blackjack()
