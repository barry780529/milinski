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
            'cum_group_contribution_sofar': sum([g.total_contribution for g in group.in_previous_rounds()]),
            'cum_participant_contribution_sofar': sum([p.payoff for p in player.in_previous_rounds()])
        }


class RoundWaitPage(WaitPage):#Any code you define here will be executed once all players have arrived at the wait page.
    def after_all_players_arrive(self):#The action while all players have made choices
        group = self.group
        players = group.get_players()
        # group.num_Round = group.num_Round+1#round counter
        # group.old_num_Round = group.num_Round-1
        contributions = [p.contribution for p in players]#each player's contribution in the round
        group.total_contribution = sum(contributions)#the group contribution in the round

        for p in players:
            #p.cumulate_contribution += p.contribution
            p.payoff = Constants.endowment - p.contribution#players' payoff in the round
            #p.cumulate_payoff = p.cumulate_payoff+p.payoff#players' cumulative payoff

class ResultWaitPage(WaitPage):
    def is_displayed(self):#"Result" page only shows at 3th round
        return self.round_number == Constants.num_rounds
    def after_all_players_arrive(self):
        group = self.group
        players = group.get_players()
        #cum_total_contribution=group.cum_total_contribution
        if group.cum_total_contribution() < Constants.threshold:# whether cumulative group contribution exceeds threshold
            if random.randint(0, 9) < Constants.disaster_prob*10:#random draw for 90% catastrophe
                group.catastrophe = True
                for p in players:
                    p.final_payoff = 0# if catastrophe happens, everyone's payoff is zero
            else:
                group.catastrophe = False# no catastrophe
                for p in players:
                    p.final_payoff = p.cumulate_payoff()# if catastrophe happens, everyone's payoff is zero
        else:
            group.catastrophe = False# no catastrophe
            for p in players:
                p.final_payoff = p.cumulate_payoff()  # if catastrophe happens, everyone's payoff is zero


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
