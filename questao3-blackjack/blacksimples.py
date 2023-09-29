import random
vai toma no cu seu lixo humano

# Define the deck of cards
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']

# Create a dictionary to represent card values
card_values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
               'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

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
        if card['Rank'] == 'Ace' and value > 21:
            value -= 10
    return value

# Function to display a hand
def display_hand(hand):
    for card in hand:
        print(f"{card['Rank']} of {card['Suit']}")

# Function to play a round of Blackjack
def play_blackjack():
    deck = initialize_deck()

    # Deal initial cards to the player and dealer
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    print("Player's hand:")
    display_hand(player_hand)

    print("\nDealer's hand:")
    print(f"Face up card: {dealer_hand[0]['Rank']} of {dealer_hand[0]['Suit']}")

    while True:
        player_value = calculate_hand_value(player_hand)
        if player_value == 21:
            print("Blackjack! You win!")
            break
        elif player_value > 21:
            print("Bust! You lose.")
            break

        action = input("\nDo you want to 'hit' or 'stand'? ").lower()
        if action == 'hit':
            player_hand.append(deck.pop())
            print("\nPlayer's hand:")
            display_hand(player_hand)
        elif action == 'stand':
            dealer_value = calculate_hand_value(dealer_hand)
            while dealer_value < 17:
                dealer_hand.append(deck.pop())
                dealer_value = calculate_hand_value(dealer_hand)

            print("\nDealer's hand:")
            display_hand(dealer_hand)

            if dealer_value > 21:
                print("Dealer busts! You win!")
            elif dealer_value > player_value:
                print("Dealer wins.")
            elif dealer_value < player_value:
                print("You win!")
            else:
                print("It's a tie!")

            break
        else:
            print("Invalid action. Please enter 'hit' or 'stand'.")

if __name__ == "__main__":
    play_blackjack()

