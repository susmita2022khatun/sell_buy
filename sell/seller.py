class ConcessionSpeed:
    """
    Class to calculate concession speeds for buyers and sellers based on weights.
    """
    def __init__(self, no_of_buyer, no_of_seller, weights):
        self.no_of_buyer = no_of_buyer
        self.no_of_seller = no_of_seller
        self.weights = weights

    def buyer_end(self):
        """
        Calculate the buyer's concession speed based on the number of buyers and sellers.
        """
        if self.no_of_seller == 0:
            raise ValueError("Seller count cannot be zero")
        return [(float(self.no_of_buyer / self.no_of_seller)) + float(weight) for weight in self.weights]
    
    def seller_end(self):
        """
        Calculate the seller's concession speed based on the number of sellers and buyers.
        """
        if self.no_of_buyer == 0:
            raise ValueError("Buyer count cannot be zero")
        return [(float(self.no_of_seller / self.no_of_buyer)) + float(weight) for weight in self.weights]


class OfferValue:
    """
    Class to compute the offer values based on concession speed, turn, and issue type (cost or benefit).
    """
    def __init__(self, min_val, max_val, turn, no_of_rounds, concess_speed, issue_type, offer_value):
        self.min_val = min_val
        self.max_val = max_val
        self.turn = turn
        self.issue_type = issue_type
        self.no_of_rounds = no_of_rounds
        self.concess_speed = concess_speed
        self.offer_value = offer_value if offer_value is not None else []

    def exponentiation(self, base, exponents):
        """
        Raises the base to the power of each value in the exponents list.
        """
        return [pow(base, exp) for exp in exponents]  

    def calculate_k_turn(self):
        """
        Calculates K-turn for current round based on concession speed.
        """
        if self.no_of_rounds == 0:
            raise ValueError("Number of rounds cannot be zero")
        return self.exponentiation(float(self.turn / self.no_of_rounds), self.concess_speed)

    def multiply_corresponding(self, left, right):
        """
        Multiplies corresponding elements from two lists.
        """
        return [num1 * num2 for num1, num2 in zip(left, right)]

    def cost_type_issue(self):
        """
        Calculates offer for a cost-type issue.
        """
        if self.turn == 1:
            return self.max_val - self.multiply_corresponding(self.calculate_k_turn(), [self.max_val - self.min_val])[0]
        else:
            return self.offer_value - self.multiply_corresponding(self.calculate_k_turn(), [self.offer_value - self.min_val])[0]

    def benefit_type_issue(self):
        """
        Calculates offer for a benefit-type issue.
        """
        if self.turn == 1:
            return self.min_val + self.multiply_corresponding(self.calculate_k_turn(), [self.max_val - self.min_val])[0]
        else:
            return self.offer_value + self.multiply_corresponding(self.calculate_k_turn(), [self.max_val - self.offer_value])[0]

    def type_cast(self):
        """
        Determines the issue type (cost or benefit) and returns the corresponding calculated value.
        """
        if self.issue_type == "cost":
            return self.cost_type_issue()
        elif self.issue_type == "benefit":
            return self.benefit_type_issue()


class NumericalScore:
    """
    Class to compute the numerical score (NSP) for an offer based on issue values, weights, and issue type.
    """
    def __init__(self, min_val, max_val, offer_value, weights, turn, no_of_rounds, pap, issue_type):
        self.min_val = min_val
        self.max_val = max_val
        self.issue_type = issue_type
        self.offer_value = offer_value
        self.weights = weights
        self.turn = turn
        self.no_of_rounds = no_of_rounds
        self.pap = pap

    def dot_product(self, a, b):
        """
        Computes the dot product of two lists.
        """
        return sum(num1 * num2 for num1, num2 in zip(a, b))

    def ns_cost_type_issue(self, min_i, max_i, offer_i, i):
        """
        Calculates the numerical score for a cost-type issue.
        """
        if self.turn == self.no_of_rounds:
            self.min_val[i] = (1 - self.pap[i]) * self.min_val[i]
        if self.max_val[i] == self.min_val[i]:
            raise ValueError("Invalid reservation values")
        return float((offer_i - min_i) / (max_i - min_i))
        
    def ns_benefit_type_issue(self, min_i, max_i, offer_i, i):
        """
        Calculates the numerical score for a benefit-type issue.
        """
        if self.turn == self.no_of_rounds:
            self.max_val[i] = (1 + self.pap[i]) * self.max_val[i]
        if self.max_val[i] == self.min_val[i]:
            raise ValueError("Invalid reservation values")
        return float((max_i - offer_i) / (max_i - min_i))
    
    def nsp_count(self):
        """
        Calculates the weighted numerical score for all issues.
        """
        ns = []
        for i in range(len(self.min_val)):
            if self.issue_type[i] == "cost":
                ns.append(self.ns_cost_type_issue(self.min_val[i], self.max_val[i], self.offer_value[i], i))
            elif self.issue_type[i] == "benefit":
                ns.append(self.ns_benefit_type_issue(self.min_val[i], self.max_val[i], self.offer_value[i], i))
        return self.dot_product(ns, self.weights)
