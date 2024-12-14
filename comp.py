import random
from sklearn.naive_bayes import MultinomialNB
import numpy as np 

class Comp:
    def __init__(self):
        self.history = []
        self.model = MultinomialNB()
        self.trained = False

    def make_decision(self):
        if not self.trained or len(self.history) < 2:
            return random.choice(['Rock', 'Paper', 'Scissors'])
        
        recent_moves = np.array([self.history[-1]]).reshape(-1, 1)
        #prediction = self.model.predict(recent_moves)
        predicted_move = self.model.predict(recent_moves)[0]

        return ['Rock', 'Paper', 'Scissors'][(predicted_move + 1) % 3]
    
    def learn(self, player_move):
        move_map = {'Rock': 0, 'Paper': 1, 'Scissors': 2}
        if player_move in move_map:
            self.history.append(move_map[player_move])
        
        if len(self.history) > 5:
            x = np.array(self.history[:-1]).reshape(-1, 1)

            y = np.array(self.history[1:])
            self.model.fit(x, y)
            self.trained = True