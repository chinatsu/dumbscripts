import random


class Yatzy:
    def __init__(self):
        self.rolls = 0
        self.hand = []
        self.score = {}

    def roll(self):
        if self.rolls == 3:
            print("You've rolled this hand 3 times already.")
            return
        self.hand = self.hand + [random.randint(1,6) for _ in range(5 - len(self.hand))]
        self.rolls += 1

    def hold(self, numbers):
        new_hand = []
        old_hand = self.hand
        for number in numbers:
            if not number in old_hand:
                print("You do not have {} in your hand.".format(number))
                return
            else:
                old_hand.remove(number)
                new_hand.append(number)
        self.hand = new_hand

    def is_yahtzee(self):
        return sum(x for x in self.hand if self.hand.count(x) >= 5) > 0

    def play(self):
        for x in random.sample([1, 2, 3, 4, 5, 6], 6):
            for _ in range(3):
                self.roll()
                self.hold([x] * self.hand.count(x))
                if self.is_yahtzee():
                    break
            self.rolls = 0
            self.score[x] = self.hand.count(x)

for x in range(1, 100000):
    y = Yatzy()
    y.play()
