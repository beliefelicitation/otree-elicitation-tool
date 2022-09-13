from os import environ


SESSION_CONFIGS = [
    dict(
        name='drag_self',
        display_name="Drag and drop interface (player set min,max,nbins)",
        app_sequence=['prediction'],
        beta=False,
        interface="ours",
        timeout=False,
        num_demo_participants=1,
        self=True
    ),
    dict(
        name='drag',
        display_name="Drag and drop interface",
        app_sequence=['prediction'],
        beta=False,
        interface="ours",
        timeout=False,
        num_demo_participants=1,
        self=False
    ),
    dict(
        name='elicitation_belief_number_timeout_self',
        display_name="Number-input interface (player set min,max,nbins)",
        app_sequence=['prediction'],
        beta=False,
        interface="number",
        timeout=False,
        num_demo_participants=1,
        self=True
    ),
    dict(
        name='elicitation_belief_number_timeout',
        display_name="Number-input interface",
        app_sequence=['prediction'],
        beta=False,
        interface="number",
        timeout=False,
        num_demo_participants=1,
        self=False
    ),
    dict(
        name='elicitation_belief_slider_not_norm_timeout_self',
        display_name="Slider-input interface (player set min,max,nbins)",
        app_sequence=['prediction'],
        beta=False,
        interface="bins",
        timeout=False,
        num_demo_participants=1,
        self=True
    ),
    dict(
        name='elicitation_belief_slider_not_norm_timeout',
        display_name="Slider-input interface",
        app_sequence=['prediction'],
        beta=False,
        interface="bins",
        timeout=False,
        num_demo_participants=1,
        self=False
    ),
    dict(
        name='elicitation_belief_metaculus_timeout_self',
        display_name="The metaculus normal distribution (player set min,max,nbins)",
        app_sequence=['prediction'],
        beta=False,
        interface="metaculus",
        timeout=False,
        num_demo_participants=1,
        self=True
    ),
    dict(
        name='elicitation_belief_metaculus_timeout',
        display_name="The metaculus normal distribution",
        app_sequence=['prediction'],
        beta=False,
        interface="metaculus",
        timeout=False,
        num_demo_participants=1,
        self=False
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']
PARTICIPANT_FIELDS = ["interface"]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.5,  doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = False

ROOMS = [
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')



DEMO_PAGE_INTRO_HTML = """
<p><strong>Aim of the paper</strong></p>
<p>We think that a belief elicitation interface should:
<ul><li>be <strong>easy to understand</strong>;</li><li>allow for <strong>all sort of beliefs</strong>, from simple point estimates to bimodal distributions and more, without imposing any structure;</li><li>manage <strong>not to get in the way</strong> of subjects;</li><li><strong>help subjects</strong> easily express what they believe;</li><li>be <strong>fast</strong>, <strong>responsive</strong>, and <strong>accurate</strong>.</li></ul>
There are several interfaces out there.</p>
<a class="btn btn-primary" href="https://beliefelicitation.github.io/">Go to the project website</a>
"""


SECRET_KEY = environ.get('OTREE_SECRET_KEY') or 'kbohidoecdoatukacaanqthanapanhanan'

INSTALLED_APPS = ['otree']
