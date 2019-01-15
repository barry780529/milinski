from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random

class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']

    def vars_for_template(self):
        group = self.group
        player = self.player
        return {
            # cumulative group cintribution before this round showing in contribute page
            'cum_group_contribution_sofar': sum([g.total_contribution for g in group.in_previous_rounds()]),
            #  cumulative participant cintribution before this round showing in contribute page
            'cum_participant_contribution_sofar': sum([p.temp_payoff for p in player.in_previous_rounds()])
        }


class RoundWaitPage(WaitPage):#Any code you define here will be executed once all players have arrived at the wait page.
    def after_all_players_arrive(self):#The action while all players have made choices
        group = self.group
        players = group.get_players()
        contributions = [p.contribution for p in players]#each player's contribution in the round
        group.total_contribution = sum(contributions)#the group contribution in the round

        for p in players:
            p.temp_payoff = Constants.endowment - p.contribution#players' payoff in the round

class ResultWaitPage(WaitPage):
    def is_displayed(self):#"Result" page only shows at 3th round
        return self.round_number == Constants.num_rounds
    def after_all_players_arrive(self):
        group = self.group
        players = group.get_players()
        #cum_total_contribution=group.cum_total_contribution
        if group.cum_total_contribution() < Constants.threshold:# whether cumulative group contribution exceeds threshold
            if random.randint(0, 9) < Constants.disaster_prob*10:#random draw of the probaility of catastrophe
                group.catastrophe = True
                for p in players:
                    p.payoff = 0# if catastrophe happens, everyone's payoff is zero
            else:
                group.catastrophe = False# no catastrophe
                for p in players:
                    p.payoff = p.cumulate_payoff()# if catastrophe does not happens, everyone's payoff  ramains  the same
        else:
            group.catastrophe = False# no catastrophe
            for p in players:
                p.payoff = p.cumulate_payoff() # if catastrophe does not happens, everyone's payoff  ramains  the same


class EachRound(Page):
    pass


class Results(Page):
    def is_displayed(self):#"Result" page only shows at 3th round
        return self.round_number == Constants.num_rounds

#define page sequence
page_sequence = [
    Contribute,
    RoundWaitPage,
    EachRound,
    ResultWaitPage,
    Results
]
