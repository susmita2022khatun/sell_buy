import buyer

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

buyer_prefs = {
    'min': [200, 30],  # Min values for each issue
    'max': [300, 48],  # Max values for each issue
    'weights': [0.8, 0.2],  # Weights for each issue
    'type': ["cost", "benefit"],  # Issue types: "cost" and "benefit"
    'pap': [0.2, 0.2]  # PAP values for each issue
}

# Concession speeds for the buyer's side
c = buyer.ConcessionSpeed(no_of_buyer, no_of_seller, buyer_prefs['weights']).buyer_end()

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
            buyer.OfferValue(buyer_prefs['min'][i], buyer_prefs['max'][i], turn, no_of_rounds, [c[i]], buyer_prefs['type'][i], offer_value).type_cast()
            for i in range(len(buyer_prefs['min']))
        ]
    else:
        current_offer_value = [
            buyer.OfferValue(buyer_prefs['min'][i], buyer_prefs['max'][i], turn, no_of_rounds, [c[i]], buyer_prefs['type'][i], offer_value[i]).type_cast()
            for i in range(len(buyer_prefs['min']))
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
    while not counter or len(counter) != len(buyer_prefs['min']):
        counter_input = input("Enter counters for each issue separated by space: ").split()
        counter = list(map(float, counter_input))
        if len(counter) != len(buyer_prefs['min']):
            print(f"Please enter exactly {len(buyer_prefs['min'])} counter values.")

    print(f"\nDebugging NSP for Turn {turn}:")

    nsp_counter_offer = buyer.NumericalScore(
        buyer_prefs['min'], buyer_prefs['max'], counter,
        buyer_prefs['weights'], turn, no_of_rounds, buyer_prefs['pap'], buyer_prefs['type']
    ).nsp_count()
    
    print(f"NSP for counter offer: {nsp_counter_offer}")

    # NEXT ROUND OFFER: Generate the next round's offer
    next_round_offer = [
        buyer.OfferValue(buyer_prefs['min'][i], buyer_prefs['max'][i], turn, no_of_rounds, [c[i]], buyer_prefs['type'][i], current_offer_value[i]).type_cast()
        for i in range(len(buyer_prefs['min']))
    ]
    
    # NSP for the next round offer
    nsp_next_round = buyer.NumericalScore(
        buyer_prefs['min'], buyer_prefs['max'], next_round_offer,
        buyer_prefs['weights'], turn, no_of_rounds, buyer_prefs['pap'], buyer_prefs['type']
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
