import joblib
import json
import pickle
import numpy as np
from random import randint
from random import choice
from typing import Dict, Tuple, List
import random
random.seed(2)
with open("model.sav", 'rb') as file:
    regressor = joblib.load(file)
with open('batsman.json', 'r') as fp:
    batsman_dictionary = json.load(fp)
with open('bowler.json', 'r') as fp:
    bowler_dictionary = json.load(fp)
with open('ct.pkl', 'rb') as f:
    ct = pickle.load(f)
with open('sc_X.pkl', 'rb') as f:
    sc_X = pickle.load(f)
with open('sc_y.pkl', 'rb') as f:
    sc_y = pickle.load(f)
std_scaling = 5


class Player:
    def __init__(self, name):
        self.name = name
        if name in batsman_dictionary:
            self.bats = True
            self.batting_stats = batsman_dictionary[name][:-2]
            self.batting_balls_average = batsman_dictionary[name][-2]
            self.batting_balls_std = batsman_dictionary[name][-1]
        else:
            self.bats = False
        if name in bowler_dictionary:
            self.bowls = True
            self.bowling_stats = bowler_dictionary[name][:-2]
            self.bowling_overs_average = bowler_dictionary[name][-2]
            self.bowling_overs_std = bowler_dictionary[name][-1]
        else:
            self.bowls = False
        self.balls_batted = 0
        self.overs_bowled = 0

    def set_balls_batted(self) -> None:
        if not self.bats:
            return 0
        balls = round(np.random.normal(self.batting_balls_average,
                                       self.batting_balls_std/std_scaling))
        balls = max(min(balls, 77), 0)
        self.balls_batted = balls

    def set_overs_bowled(self) -> None:
        if not self.bowls:
            return 0
        overs = round(np.random.normal(self.bowling_overs_average,
                                       self.bowling_overs_std/std_scaling))
        overs = max(min(overs, 4), 0)
        self.overs_bowled = overs

    def increase_balls_faced(self) -> int:
        if self.bats and self.balls_batted < 77:
            self.balls_batted += 1
            return 1
        return 0

    def decrease_balls_faced(self) -> int:
        if self.bats and self.balls_batted > 0:
            self.balls_batted -= 1
            return 1
        return 0

    def increase_overs_bowled(self) -> int:
        if self.bowls and self.overs_bowled < 4:
            self.overs_bowled += 1
            return 1
        return 0

    def decrease_overs_bowled(self) -> int:
        if self.bowls and self.overs_bowled > 0:
            self.overs_bowled -= 1
            return 1
        return 0

    def __str__(self):
        return self.name


class Team:
    def __init__(self, players: List[Player]):
        self.players = players

    def predict_batting_distribution(self) -> None:
        for player in self.players:
            player.set_balls_batted()
        difference = 120 - sum(player.balls_batted for player in self.players)
        while difference:
            if difference > 0:
                difference -= self.players[randint(0, 10)
                                           ].increase_balls_faced()
            else:
                difference += self.players[randint(0, 10)
                                           ].decrease_balls_faced()

    def predict_bowling_distribution(self) -> None:
        for player in self.players:
            player.set_overs_bowled()
        difference = 20 - sum(player.overs_bowled for player in self.players)
        while difference:
            if difference > 0:
                difference -= self.players[randint(0, 10)
                                           ].increase_overs_bowled()
            else:
                difference += self.players[randint(0, 10)
                                           ].decrease_overs_bowled()

    def batting_distribution(self) -> Dict[Player, int]:
        return {player: player.balls_batted for player in self.players if player.balls_batted > 0}

    def bowling_distribution(self) -> Dict[Player, int]:
        return {player: player.overs_bowled*6 for player in self.players if player.overs_bowled > 0}


class Match:
    def __init__(self, team_a: Team, team_b: Team):
        self.team_a = team_a
        self.team_b = team_b
        self.bowler_a_to_batsman_b = {}
        self.bowler_b_to_batsman_a = {}

    def process_balls(self) -> None:
        self.team_a.predict_batting_distribution()
        self.team_a.predict_bowling_distribution()
        self.team_b.predict_batting_distribution()
        self.team_b.predict_bowling_distribution()

    def distribute_balls(self) -> None:
        team_a_batting_distribution = self.team_a.batting_distribution()
        team_b_batting_distribution = self.team_b.batting_distribution()
        team_a_bowling_distribution = self.team_a.bowling_distribution()
        team_b_bowling_distribution = self.team_b.bowling_distribution()
        assert(sum(team_a_batting_distribution.values()) == 120)
        assert(sum(team_b_batting_distribution.values()) == 120)
        assert(sum(team_a_bowling_distribution.values()) == 120)
        assert(sum(team_b_bowling_distribution.values()) == 120)
        n_balls_at_a_time = 4
        for bowler in team_a_bowling_distribution:
            while team_a_bowling_distribution[bowler]:
                batsman = choice(list(team_b_batting_distribution.keys()))
                balls = randint(1, min(
                    team_b_batting_distribution[batsman], team_a_bowling_distribution[bowler], n_balls_at_a_time))
                team_b_batting_distribution[batsman] -= balls
                team_a_bowling_distribution[bowler] -= balls
                if not team_b_batting_distribution[batsman]:
                    del team_b_batting_distribution[batsman]
                self.bowler_a_to_batsman_b[(bowler, batsman)] = self.bowler_a_to_batsman_b.get(
                    (bowler, batsman), 0) + balls
        for bowler in team_b_bowling_distribution:
            while team_b_bowling_distribution[bowler]:
                batsman = choice(list(team_a_batting_distribution.keys()))
                balls = randint(1, min(
                    team_a_batting_distribution[batsman], team_b_bowling_distribution[bowler], n_balls_at_a_time))
                team_a_batting_distribution[batsman] -= balls
                team_b_bowling_distribution[bowler] -= balls
                if not team_a_batting_distribution[batsman]:
                    del team_a_batting_distribution[batsman]
                self.bowler_b_to_batsman_a[(bowler, batsman)] = self.bowler_b_to_batsman_a.get(
                    (bowler, batsman), 0) + balls

    def predict(self) -> Tuple[Dict[str, List[int]]]:
        final_batsman_a_stats = {i[1].name: [0, 0]
                                 for i in self.bowler_b_to_batsman_a}
        final_bowler_a_stats = {i[0].name: [0, 0]
                                for i in self.bowler_a_to_batsman_b}
        final_batsman_b_stats = {i[1].name: [0, 0]
                                 for i in self.bowler_a_to_batsman_b}
        final_bowler_b_stats = {i[0].name: [0, 0]
                                for i in self.bowler_b_to_batsman_a}
        for bowler, batsman in self.bowler_a_to_batsman_b:
            balls = self.bowler_a_to_batsman_b[(bowler, batsman)]
            bowler_values = bowler_dictionary[bowler.name][:-2]
            batsman_values = batsman_dictionary[batsman.name][:-2]
            data = [[batsman.name]+bowler_values + batsman_values + [balls]]
            data = np.array(ct.transform(data))
            data[:, 527:] = sc_X.transform(data[:, 527:])
            y_pred = regressor.predict(data)
            try:
                predicted = [max(round(sc_y.inverse_transform([i])[0]), 0)
                             for i in y_pred]
            except:
                predicted = [max(round(sc_y.inverse_transform(i)[0]), 0)
                             for i in y_pred]
            final_batsman_b_stats[batsman.name][0] += predicted[0]
            final_bowler_a_stats[bowler.name][0] += predicted[0]
            final_batsman_b_stats[batsman.name][1] += balls
            final_bowler_a_stats[bowler.name][1] += balls
        for bowler, batsman in self.bowler_b_to_batsman_a:
            balls = self.bowler_b_to_batsman_a[(bowler, batsman)]
            bowler_values = bowler_dictionary[bowler.name][:-2]
            batsman_values = batsman_dictionary[batsman.name][:-2]
            data = [[batsman.name]+bowler_values + batsman_values + [balls]]
            data = np.array(ct.transform(data))
            data[:, 527:] = sc_X.transform(data[:, 527:])
            y_pred = regressor.predict(data)
            try:
                predicted = [max(round(sc_y.inverse_transform([i])[0]), 0)
                             for i in y_pred]
            except:
                predicted = [max(round(sc_y.inverse_transform(i)[0]), 0)
                             for i in y_pred]
            final_batsman_a_stats[batsman.name][0] += predicted[0]
            final_bowler_b_stats[bowler.name][0] += predicted[0]
            final_batsman_a_stats[batsman.name][1] += balls
            final_bowler_b_stats[bowler.name][1] += balls
        return final_batsman_a_stats, final_bowler_a_stats, final_batsman_b_stats, final_bowler_b_stats


def get_prediction(team_a: List[str], team_b: List[str]) -> Tuple[Dict[str, List[int]]]:
    """
    Takes 2 lists of player names as input.
    Returns 4 dictionaries, 2 for batting, 2 for bowling
    batting_dictionary : dictionary[player_name] = [runs_made, balls_faced]
    bowling_dictionary : dictionary[player_name] = [runs_conceded, balls_bowled]
    """
    team_a = Team([Player(name) for name in team_a])
    team_b = Team([Player(name) for name in team_b])
    match = Match(team_a, team_b)
    match.process_balls()
    match.distribute_balls()
    final_batsman_a_stats, final_bowler_a_stats, final_batsman_b_stats, final_bowler_b_stats = match.predict()
    total_a = sum(i[0] for i in final_batsman_a_stats.values())
    total_b = sum(i[0] for i in final_batsman_b_stats.values())
    return final_batsman_a_stats, final_bowler_a_stats, final_batsman_b_stats, final_bowler_b_stats, total_a, total_b


if __name__ == "__main__":
    team_a = [
        'Q de Kock',
        'RG Sharma',
        'SA Yadav',
        'Ishan Kishan',
        'KA Pollard',
        'HH Pandya',
        'KH Pandya',
        'TA Boult',
        'JJ Bumrah',
        'RD Chahar',
        '11th player?'
    ]
    team_b = [
        'WP Saha',
        'DA Warner',
        'MK Pandey',
        'J Bairstow',
        'V Shankar',
        'JO Holder',
        'Rashid Khan',
        'B Kumar',
        'T Natarajan',
        'S Nadeem',
        '11th player?'
    ]
    final_batsman_a_stats, final_bowler_a_stats, final_batsman_b_stats, final_bowler_b_stats = get_prediction(
        team_a, team_b)
    print('Batsman Team A')
    for i in final_batsman_a_stats:
        print(i, final_batsman_a_stats[i][0],
              'in', final_batsman_a_stats[i][1])
    print('Total =', sum(i[0] for i in final_batsman_a_stats.values()))
    print('Bowlers Team B')
    for i in final_bowler_b_stats:
        print(i, final_bowler_b_stats[i][0], 'conceded in',
              final_bowler_b_stats[i][1]//6, 'overs')
    print('*'*100)
    print('Batsman Team B')
    for i in final_batsman_b_stats:
        print(i, final_batsman_b_stats[i][0],
              'in', final_batsman_b_stats[i][1])
    print('Bowlers Team A')
    for i in final_bowler_a_stats:
        print(i, final_bowler_a_stats[i][0], 'conceded in',
              final_bowler_a_stats[i][1]//6, 'overs')
    print('Total =', sum(i[0] for i in final_batsman_b_stats.values()))
