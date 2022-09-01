from otree.api import *
import json


doc = """
Elicitation belief app
"""


class C(BaseConstants):
    NAME_IN_URL = 'prediction'
    PLAYERS_PER_GROUP = None

    def PREDICTION_QUESTIONS():

        return [
            dict(
        q="What will be the temperature (°F) in New York City at noon on the 10th of September, 2022?",
        min=60,
        step=10,
        nb_bins=11,
        unit="°"),
            dict(
        q="20 years from now, what will be the temperature (°F) in New York City at noon on the 10th of September, 2042?",
        min=60,
        step=10,
        nb_bins=11,
        unit="°"
            )
        ]

    NUM_ROUNDS = len(PREDICTION_QUESTIONS())


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    data = models.StringField()
    history = models.LongStringField(initial="[]")
    min = models.IntegerField(label="Min value of the x axis")
    max = models.IntegerField(label="Max value of the x axis")
    nb_bins = models.IntegerField(label="Number of bins", min=2)


def creating_session(subsession: Subsession):
    if 'interface' in subsession.session.config:
        for player in subsession.get_players():
            player.interface = subsession.session.config["interface"]
            player.participant.interface = player.interface
    else:
        import itertools
        interfaces = itertools.cycle(["ours", "number","bins","metaculus"])
        for player in subsession.get_players():
            player.interface = next(interfaces)
            player.participant.interface = player.interface

# PAGES

class End(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


class Prediction(Page):
    form_model = 'player'
    form_fields = ["min","max","nb_bins"]

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            prediction_questions = C.PREDICTION_QUESTIONS()[player.round_number-1]["q"],
        )

    @staticmethod
    def error_message(player, values):
        if values['max'] <= values['min']:
            return 'Max value should be superior to Min value!'

    @staticmethod
    def is_displayed(player: Player):
        return player.session.config["self"] == True

class Distributions(Page):

    form_model = 'player'
    form_fields = []

    timer_text = 'Time left to make your prediction:'

    @staticmethod
    def get_timeout_seconds(player):
        if player.session.config["timeout"]:
            return 90

    @staticmethod
    def live_method(player, data):
        history = json.loads(player.history)
        history.append(data["history"])
        player.history = json.dumps(history)
        player.data = json.dumps(data["history"]["data"])

    @staticmethod
    def before_next_page(player, timeout_happened):
        pass
#        if timeout_happened:
#            player.timeout = True


    @staticmethod
    def js_vars(player):
        if not player.session.config["self"]:
            player.min = C.PREDICTION_QUESTIONS()[player.round_number-1]["min"]
            player.nb_bins = C.PREDICTION_QUESTIONS()[player.round_number-1]["nb_bins"]
            player.max = C.PREDICTION_QUESTIONS()[player.round_number-1]["min"]+C.PREDICTION_QUESTIONS()[player.round_number-1]["step"]*(C.PREDICTION_QUESTIONS()[player.round_number-1]["nb_bins"]-1)
            print(player.max)

        return dict(
            interface = player.participant.interface,
            prediction = True,
            yMax = 1,
            min = player.min,
            step = (player.max-player.min)/(player.nb_bins-1),
            nb_bins = player.nb_bins,
            xUnit = C.PREDICTION_QUESTIONS()[player.round_number-1]["unit"],
            min_timeout=30,
        )

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            prediction_questions = C.PREDICTION_QUESTIONS()[player.round_number-1]["q"],
            interface=player.participant.interface,
        )

page_sequence = [Prediction,Distributions,End]
