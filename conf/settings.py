import random
JSON_SITES_DATA = "dataset/sites2.json"
JSON_VIGILANTES_DATA = "dataset/vigilantes3.json"
MAX_TOTAL_WEEKS = 4
WINDOWS_RANDOM_THE_VIGILANTS_ORDER_FOR_SITE = 5
SEED = 0
SETTINGS=random.seed(SEED)
MISSING_FITNESS_VALUE = 10
ASSIGNED_VIGILANTES_FITNESS_VALUE = 10
DISTANCE_FITNESS_VALUE= 1
EXTRA_HOURS_FITNESS_VALUE = 1
#NUMBER ITERACTION FOR THA SELECCION OF RANDOM COMPONENTE IN THE CROOSIN
NUMBER_ITERATION_SELECTION_COMPONENTE = 10
NUMBER_OF_CHILDREN_GENERATE = 11 # se generarn 11 hijos para tener en cuenta y de estos se toma el mejor
NUMBER_OF_CHILDREN_FOR_PARENTS= 2 # se negera 2 hijos por cadas dos padres
RESTRICTED_LIST_AMOUNT_COMPONENT = 10

