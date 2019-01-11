from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Pei-Hsun Hsieh'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Public_Goods'
    players_per_group = 3 #number of players
    num_rounds = 3#The round here is the repeat process, so only one
    endowment = c(4)# endowment for each round
    threshold = c(18) #The threshold to prevent a catastrophe
    Total_endowment=endowment*players_per_group #obtaining endowment during all rounds
    disaster_prob = 0.9 #the probability to lose all payoff if not satisfy the thresholdor , can be 0.5 and 0.1 in other conditions

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()#define group contribution in the round
    def cum_total_contribution(self):# define cumulative group contribution
        return sum([g.total_contribution for g in self.in_all_rounds()])
    catastrophe = models.BooleanField()#define whether catastrophe happens, the value is TRUE or FALSE

class Player(BasePlayer):
    contribution = models.CurrencyField(
        choices=currency_range(c(0), c(4), c(2))
        # this gives:
        # [$0.00, $2.00, $4,00]
    )
    def cumulate_contribution(self):#return players' cumulative contribution
        return sum([p.contribution for p in self.in_all_rounds()])
    payoff = models.CurrencyField()#define players' payoff in the round
    def cumulate_payoff (self):#define players' cumulative payoff
        return sum([p.payoff for p in self.in_all_rounds()])
    final_payoff = models.CurrencyField()#the realized payoff
    def contribution_each_player_round(self):# return a list regarding to other players' contribution in each round
        history = []
        for other_player in self.get_others_in_group():
            each_round = []
            for pr in other_player.in_previous_rounds():
                each_round.append(pr.contribution)
            history.append(each_round)
        transpose_history=map(list, zip(*history))
        #print('History matrix',history)
        return transpose_history
