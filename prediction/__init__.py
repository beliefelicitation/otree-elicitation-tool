from otree.api import *
import json


doc = """
Elicitation belief app
"""


class C(BaseConstants):
    NAME_IN_URL = 'prediction'
    PLAYERS_PER_GROUP = None

    PREDICTION_QUESTIONS = [
        dict(
            q="What will be the temperature (°F) in New York City at noon on the 10th of September, 2022?",
            min=60,
            step=10,
            nb_bins=11,
            unit="°",
        ),
        dict(
            q="20 years from now, what will be the temperature (°F) in New York City at noon on the 10th of September, 2042?",
            min=60,
            step=10,
            nb_bins=11,
            unit="°",
        ),
    ]

    NUM_ROUNDS = len(PREDICTION_QUESTIONS)


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
    session = subsession.session
    if 'interface' in session.config:
        for player in subsession.get_players():
            player.interface = session.config["interface"]
            player.participant.interface = player.interface
    else:
        import itertools

        interfaces = itertools.cycle(["ours", "number", "bins", "metaculus"])
        for player in subsession.get_players():
            player.interface = next(interfaces)
            player.participant.interface = player.interface


# PAGES


class End(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


class Prediction(Page):
    # TODO: Chris comment: shouldn't this page be called 'Configuration'?
    # and rename the 'self' session config param to 'configuration'? etc

    form_model = 'player'
    form_fields = ["min", "max", "nb_bins"]

    @staticmethod
    def is_displayed(player: Player):
        session = player.session
        return session.config["self"] == True

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            prediction_questions=C.PREDICTION_QUESTIONS[player.round_number - 1]["q"],
        )

    @staticmethod
    def error_message(player, values):
        if values['max'] <= values['min']:
            return 'Max value should be superior to Min value!'


class Distributions(Page):

    timer_text = 'Time left to make your prediction:'

    @staticmethod
    def get_timeout_seconds(player):
        session = player.session
        if session.config["timeout"]:
            return 90

    @staticmethod
    def live_method(player, data):
        history = json.loads(player.history)
        history.append(data["history"])
        player.history = json.dumps(history)
        player.data = json.dumps(data["history"]["data"])

    @staticmethod
    def js_vars(player: Player):
        session = player.session
        participant = player.participant

        pq = C.PREDICTION_QUESTIONS[player.round_number - 1]
        if not session.config["self"]:
            player.min = pq["min"]
            player.nb_bins = pq["nb_bins"]
            player.max = pq["min"] + pq["step"] * (pq["nb_bins"] - 1)

        return dict(
            interface=participant.interface,
            prediction=True,
            yMax=1,
            min=player.min,
            step=(player.max - player.min) / (player.nb_bins - 1),
            nb_bins=player.nb_bins,
            xUnit=pq["unit"],
            min_timeout=30,
        )

    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        pq = C.PREDICTION_QUESTIONS[player.round_number - 1]
        return dict(
            prediction_questions=pq["q"],
            interface=participant.interface,
        )


page_sequence = [Prediction, Distributions, End]
