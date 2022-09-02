import random
import environ

JSON_SITES_DATA = "app/dataset/sites.json"
JSON_VIGILANTES_DATA = "app/dataset/vigilantes.json"
#result
PATH_RESULTS="dataset/results/"
#Nsga2 Constant
INFINITE_POSITIVE = 100000000000000
INFINITE_NEGATIVE = -100000000000000
# Gras Constant

# SETTINGS=random.seed(0) #SEED
env1 = environ.Env(
    SETTINGS=(int, random.seed(0)), #SEED
    MAX_TOTAL_WEEKS=(int, 4), 
    WINDOWS_RANDOM_THE_VIGILANTS_ORDER_FOR_SITE=(int, 5),
    MISSING_FITNESS_VALUE=(int, 1),
    ASSIGNED_VIGILANTES_FITNESS_VALUE=(int, 1),
    DISTANCE_FITNESS_VALUE=(int, 1), 
    EXTRA_HOURS_FITNESS_VALUE=(int, 1),
    AMOUNT_POBLATION_TO_CREATE = (int, 5),
    #NUMBER ITERACTION FOR THA SELECCION OF RANDOM COMPONENTE IN THE CROOSIN
    #NSGA2 
    NUM_PARENTS_OF_ORDERED_POPULATION=(float, 0.5),
    NUM_OBJECTIVE=(int, 4),  # 0 -3 = 4 objetive
    MAX_EFOS=(int, 10), 
    NUM_SOLUTION=(int, 10),
    NUMBER_OF_CHILDREN_GENERATE=(int, 10),
    NUMBER_ITERATION_SELECTION_COMPONENTE=(int, 10),
    NUMBER_OF_CHILDREN_FOR_PARENTS=(int, 2),  # se negera 2 hijos por cadas dos padres
    RESTRICTED_LIST_AMOUNT_COMPONENT=(int, 5),
    SIZE_POPULATION=(int, 10),  # Tamaño de la poblacion final
    NUMBER_OBJECTIVE_AT_OBTIMIZATE=(int, 4),
    #Results
    #PorcetanjeSolution
    MISSING_SHIFT_PROBABILITY = (int, 50),
    ASSIGNED_VIGILANTES_PROBABILITY = (int, 30),
    EXTRA_HOURS_PROBABILITY = (int, 15),
    DISTANCE_GRASP_PROBABILITY = (int, 5),
    #PorcetanjeCrossingNsgaii
    MISSING_SHIFT_CROSSING_PROBABILITY = (int, 1),
    ASSIGNED_VIGILANTES_CROSSING_PROBABILITY = (int, 1),
    EXTRA_HOURS_CROSSING_PROBABILITY = (int, 1),
    DISTANCE_CROSSING_PROBABILITY = (int, 97),
    #PorcetanjeTweaksGRASP
    MISSING_SHIFT_TWEAK_PROBABILITY = (int, 50),
    ASSIGNED_VIGILANTES_TWEAK_PROBABILITY = (int, 30),
    EXTRA_HOURS_TWEAK_PROBABILITY = (int, 15),
    DISTANCE_TWEAK_PROBABILITY = (int, 5),
)
env2 = environ.Env(
    SETTINGS=(int, random.seed(0)),
    MAX_TOTAL_WEEKS=(int, 4), 
    WINDOWS_RANDOM_THE_VIGILANTS_ORDER_FOR_SITE=(int, 5),
    MISSING_FITNESS_VALUE=(int, 100),
    ASSIGNED_VIGILANTES_FITNESS_VALUE=(int, 20),
    DISTANCE_FITNESS_VALUE=(int, 1), 
    EXTRA_HOURS_FITNESS_VALUE=(int, 5),
    #NUMBER ITERACTION FOR THA SELECCION OF RANDOM COMPONENTE IN THE CROOSIN
    #NSGA2 
    NUM_OBJECTIVE=(int, 4),  # 0 -3 = 4 objetive
    MAX_EFOS=(int, 10), 
    NUM_SOLUTION=(int, 20),
    NUMBER_OF_CHILDREN_GENERATE=(int, 20),
    NUMBER_ITERATION_SELECTION_COMPONENTE=(int, 10),
    NUMBER_OF_CHILDREN_FOR_PARENTS=(int, 2),  # se negera 2 hijos por cadas dos padres
    RESTRICTED_LIST_AMOUNT_COMPONENT=(int, 10),
    SIZE_POPULATION=(int, 10),  # Tamaño de la poblacion final
    NUMBER_OBJECTIVE_AT_OBTIMIZATE=(int, 4),
    #Results
    #PorcetanjeSolution
    MISSING_SHIFT_PROBABILITY = (int, 50),
    ASSIGNED_VIGILANTES_PROBABILITY = (int, 30),
    EXTRA_HOURS_PROBABILITY = (int, 15),
    DISTANCE_GRASP_PROBABILITY = (int, 5),
    #PorcetanjeTweaksGRASP
    MISSING_SHIFT_TWEAK_PROBABILITY = (int, 50),
    ASSIGNED_VIGILANTES_TWEAK_PROBABILITY = (int, 30),
    EXTRA_HOURS_TWEAK_PROBABILITY = (int, 15),
    DISTANCE_TWEAK_PROBABILITY = (int, 5)
)
env3 = environ.Env(
    SETTINGS=(int, random.seed(0)), #SEED
    MAX_TOTAL_WEEKS=(int, 4), 
    WINDOWS_RANDOM_THE_VIGILANTS_ORDER_FOR_SITE=(int, 5),
    MISSING_FITNESS_VALUE=(int, 1),
    ASSIGNED_VIGILANTES_FITNESS_VALUE=(int, 1),
    DISTANCE_FITNESS_VALUE=(int, 1), 
    EXTRA_HOURS_FITNESS_VALUE=(int, 1),
    AMOUNT_POBLATION_TO_CREATE = (int, 5),
    #NUMBER ITERACTION FOR THA SELECCION OF RANDOM COMPONENTE IN THE CROOSIN
    #NSGA2 
    NUM_OBJECTIVE=(int, 4),  # 0 -3 = 4 objetive
    MAX_EFOS=(int, 10), 
    NUM_SOLUTION=(int, 20),
    NUMBER_OF_CHILDREN_GENERATE=(int, 20),
    NUMBER_ITERATION_SELECTION_COMPONENTE=(int, 10),
    NUMBER_OF_CHILDREN_FOR_PARENTS=(int, 2),  # se negera 2 hijos por cadas dos padres
    RESTRICTED_LIST_AMOUNT_COMPONENT=(int, 10),
    SIZE_POPULATION=(int, 11),  # Tamaño de la poblacion final
    NUMBER_OBJECTIVE_AT_OBTIMIZATE=(int, 4),
     #PorcetanjeTweaksGRASP
    MISSING_SHIFT_CROSSING_PROBABILITY = (int, 1),
    ASSIGNED_VIGILANTES_CROSSING_PROBABILITY = (int, 1),
    EXTRA_HOURS_CROSSING_PROBABILITY = (int, 1),
    DISTANCE_CROSSING_PROBABILITY = (int, 97),
    #Results
    #PorcetanjeSolution
    MISSING_SHIFT_PROBABILITY = (int, 1),
    ASSIGNED_VIGILANTES_PROBABILITY = (int, 1),
    EXTRA_HOURS_PROBABILITY = (int, 1),
    DISTANCE_GRASP_PROBABILITY = (int, 97),
    #PorcetanjeTweaksGRASP
    MISSING_SHIFT_TWEAK_PROBABILITY = (int, 1),
    ASSIGNED_VIGILANTES_TWEAK_PROBABILITY = (int, 1),
    EXTRA_HOURS_TWEAK_PROBABILITY = (int, 1),
    DISTANCE_TWEAK_PROBABILITY = (int, 97),
)
# envirom exect

env = env1
SETTINGS = env("SETTINGS")
MAX_TOTAL_WEEKS = env("MAX_TOTAL_WEEKS")
WINDOWS_RANDOM_THE_VIGILANTS_ORDER_FOR_SITE = env("WINDOWS_RANDOM_THE_VIGILANTS_ORDER_FOR_SITE")
# SEED = env("SEED")
SETTINGS = env("SETTINGS")
MISSING_FITNESS_VALUE = env("MISSING_FITNESS_VALUE")
ASSIGNED_VIGILANTES_FITNESS_VALUE = env("ASSIGNED_VIGILANTES_FITNESS_VALUE")
DISTANCE_FITNESS_VALUE = env("DISTANCE_FITNESS_VALUE")
EXTRA_HOURS_FITNESS_VALUE = env("EXTRA_HOURS_FITNESS_VALUE")
AMOUNT_POBLATION_TO_CREATE = env("AMOUNT_POBLATION_TO_CREATE")

#NUMBER ITERACTION FOR THA SELECCION OF RANDOM COMPONENTE IN THE CROOSIN
#NSGA2 
NUM_PARENTS_OF_ORDERED_POPULATION = env("NUM_PARENTS_OF_ORDERED_POPULATION")
NUM_OBJECTIVE = env("NUM_OBJECTIVE")
MAX_EFOS = env("MAX_EFOS")
NUM_SOLUTION = env("NUM_SOLUTION")
NUMBER_OF_CHILDREN_GENERATE = env("NUMBER_OF_CHILDREN_GENERATE")
NUMBER_ITERATION_SELECTION_COMPONENTE = env("NUMBER_ITERATION_SELECTION_COMPONENTE")
NUMBER_OF_CHILDREN_FOR_PARENTS = env("NUMBER_OF_CHILDREN_FOR_PARENTS")
RESTRICTED_LIST_AMOUNT_COMPONENT = env("RESTRICTED_LIST_AMOUNT_COMPONENT")
SIZE_POPULATION = env("SIZE_POPULATION")
NUMBER_OBJECTIVE_AT_OBTIMIZATE = env("NUMBER_OBJECTIVE_AT_OBTIMIZATE")
#Results,
#PorcetanjeSolution
MISSING_SHIFT_PROBABILITY = env("MISSING_SHIFT_PROBABILITY")
ASSIGNED_VIGILANTES_PROBABILITY = env("ASSIGNED_VIGILANTES_PROBABILITY")
EXTRA_HOURS_PROBABILITY = env("EXTRA_HOURS_PROBABILITY")
DISTANCE_GRASP_PROBABILITY = env("DISTANCE_GRASP_PROBABILITY")
#PorcetanjeCrossigNsgaii
MISSING_SHIFT_CROSSING_PROBABILITY = env("MISSING_SHIFT_CROSSING_PROBABILITY")
ASSIGNED_VIGILANTES_CROSSING_PROBABILITY = env("ASSIGNED_VIGILANTES_CROSSING_PROBABILITY")
EXTRA_HOURS_CROSSING_PROBABILITY = env("EXTRA_HOURS_CROSSING_PROBABILITY")
DISTANCE_CROSSING_PROBABILITY = env("DISTANCE_CROSSING_PROBABILITY")
#PorcetanjeTweaksGRASP
MISSING_SHIFT_TWEAK_PROBABILITY = env("MISSING_SHIFT_TWEAK_PROBABILITY")
ASSIGNED_VIGILANTES_TWEAK_PROBABILITY = env("ASSIGNED_VIGILANTES_TWEAK_PROBABILITY")
EXTRA_HOURS_TWEAK_PROBABILITY = env("EXTRA_HOURS_TWEAK_PROBABILITY")
DISTANCE_TWEAK_PROBABILITY = env("DISTANCE_TWEAK_PROBABILITY")