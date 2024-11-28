import seller

def get_user_input(prompt, expected_type):
    while True:
        try:
            return expected_type(input(prompt))
        except ValueError:
            print(f"Invalid input! Please enter a valid {expected_type.__name__}.")

no_of_buyer = 1
no_of_seller = 1
no_of_rounds = 10

nsp_counter_offer = 0
nsp_current_offer = 0


seller_prefs = {
    'min': [250, 24],  # Min values for each issue
    'max': [400, 36],  # Max values for each issue
    'weights': [0.7, 0.3],  # Weights for each issue
    'type': ["cost", "benefit"],  # Issue types: "cost" and "benefit"
    'pap': [0.3, 0.2]  # PAP values for each issue
}

# Concession speeds for the buyer's side
c = seller.ConcessionSpeed(no_of_buyer, no_of_seller, seller_prefs['weights']).buyer_end()

turn = 1
offer_value = None

# Loop through each round of negotiation
while turn < no_of_rounds:
    print(f"\nTurn {turn}")
    
                                 #########################
                                 #     INITIALIZATION    #
                                 #########################
    
    if(turn ==1):
        current_offer_value = [
            seller.OfferValue(seller_prefs['min'][i], seller_prefs['max'][i], turn, no_of_rounds, [c[i]], seller_prefs['type'][i], offer_value).type_cast()
            for i in range(len(seller_prefs['min']))
        ]
    else:
        current_offer_value = [
            seller.OfferValue(seller_prefs['min'][i], seller_prefs['max'][i], turn, no_of_rounds, [c[i]], seller_prefs['type'][i], offer_value[i]).type_cast()
            for i in range(len(seller_prefs['min']))
        ]
        
    print(f"Offer: {current_offer_value}")
    
        
                                 #########################
                                 #    ROUND ACCEPTANCE   #
                                 #########################
 

    st = input("Offer accepted? (y/n): ").strip().lower()
    if st == 'y':
        offer_value = current_offer_value
        break

    turn += 1
        
                                 #########################
                                 #  COUNTER OFFER INPUT  #
                                 #########################
 

    counter = None
    while not counter or len(counter) != len(seller_prefs['min']):
        counter_input = input("Enter counters for each issue separated by space: ").split()
        counter = list(map(float, counter_input))
        if len(counter) != len(seller_prefs['min']):
            print(f"Please enter exactly {len(seller_prefs['min'])} counter values.")

    print(f"\nDebugging NSP for Turn {turn}:")

    nsp_counter_offer = seller.NumericalScore(
        seller_prefs['min'], seller_prefs['max'], counter,
        seller_prefs['weights'], turn, no_of_rounds, seller_prefs['pap'], seller_prefs['type']
    ).nsp_count()
    
    print(f"NSP for counter offer: {nsp_counter_offer}")

    # NEXT ROUND OFFER: Generate the next round's offer
    next_round_offer = [
        seller.OfferValue(seller_prefs['min'][i], seller_prefs['max'][i], turn, no_of_rounds, [c[i]], seller_prefs['type'][i], current_offer_value[i]).type_cast()
        for i in range(len(seller_prefs['min']))
    ]
    
    # NSP for the next round offer
    nsp_next_round = seller.NumericalScore(
        seller_prefs['min'], seller_prefs['max'], next_round_offer,
        seller_prefs['weights'], turn, no_of_rounds, seller_prefs['pap'], seller_prefs['type']
    ).nsp_count()
    
    print(f"Next round offer: {next_round_offer}")
    print(f"NSP for next round offer: {nsp_next_round}")

    # Compare NSP values
    if nsp_counter_offer >= nsp_next_round:
        print("Counter offer accepted.")
        offer_value = counter
        break

    offer_value = next_round_offer

print("\nFinal offer values across rounds:", offer_value)

# If negotiation reaches the last round, evaluate the final offers
if turn == no_of_rounds:

    print(f"Final NSP for current offer: {nsp_current_offer}")
    print(f"Final NSP for counter offer: {nsp_counter_offer}")

    if nsp_counter_offer >= nsp_current_offer:
        print("Final counter offer accepted.")
    else:
        print("Final offer rejected.")