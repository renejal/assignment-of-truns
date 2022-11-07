import random
import environ

MAX_TOTAL_WEEKS = 0
MAX_TIME_DURATION = 2000#1day
PATH_RESULTS = "app/dataset/results/"

NUMBER_OBJECTIVE_AT_OBTIMIZATE = 4
#TODO RENOMBRAR ESTA VARIABLE PORQUE NO SE ENTIENDE
WINDOWS_RANDOM_THE_VIGILANTS_ORDER_FOR_SITE = 5
#VALUE TO APPLY TO EACH INFRACTION IN A OBJETIVE
MISSING_FITNESS_VALUE =  100
ASSIGNED_VIGILANTES_FITNESS_VALUE = 100
DISTANCE_FITNESS_VALUE= 100
EXTRA_HOURS_FITNESS_VALUE = 10

#Nsga2 Constants
INFINITE_POSITIVE = 100000000000000
INFINITE_NEGATIVE = -100000000000000

SEEDS = [722, 829, 616, 923, 150, 317, 101, 747, 75, 920, 870, 700, 338, 483, 573, 103,362,444,323,625,655,934,209,989,565,488,453,886,533,266 ]

env1 = environ.Env(
    #GENERAL
    SETTINGS = (int, random.seed(0)), #SEED
    
    #Probability to choose a objective to optimize in one solution
    MISSING_SHIFT_PROBABILITY = (int, 25),
    ASSIGNED_VIGILANTES_PROBABILITY = (int, 25),
    EXTRA_HOURS_PROBABILITY = (int, 25),
    DISTANCE_GRASP_PROBABILITY = (int, 25),

    #NSGAII
    #PARAMETERS
    MAX_EFOS_NSGAII =(int, 100), 
    POPULATION_AMOUNT_NSGAII = (int, 10),
    NUM_PARENTS_OF_ORDERED_POPULATION=(float, 0.5), # numero de padres se se tomaran en cuenta de la lista ordenada de soluciones
    NUMBER_OF_CHILDREN_GENERATE= (int, 2),
    NUMBER_ITERATION_SELECTION_COMPONENTE=(int, 10),
    #PorcetanjeCrossingNsgaii
    MISSING_SHIFT_CROSSING_PROBABILITY = (int, 50),
    ASSIGNED_VIGILANTES_CROSSING_PROBABILITY = (int, 30),
    EXTRA_HOURS_CROSSING_PROBABILITY = (int, 15),
    DISTANCE_CROSSING_PROBABILITY = (int, 5),
    
    #GRASP CONFIG
    #PARAMETERS
    MAX_EFOS_GRASP =  (int, 10),
    POPULATION_AMOUNT_GRASP = (int, 20),
    COMPONENTS_AMOUNT_GRASP =  (int, 50),
    RESTRICTED_LIST_AMOUNT_COMPONENT_GRASP =  (int, 5),
    TWEAK_AMOUNT_REPETITIONS_GRASP =  (int, 30),
    #PorcetanjeTweaksGRASP
    MISSING_SHIFT_TWEAK_PROBABILITY = (int, 25),
    ASSIGNED_VIGILANTES_TWEAK_PROBABILITY = (int, 25),
    EXTRA_HOURS_TWEAK_PROBABILITY = (int, 25),
    DISTANCE_TWEAK_PROBABILITY = (int, 25)
)

# envirom exect
env = env1

#GENERAL
SETTINGS = env("SETTINGS")
# SEED = env("SEED")
#Probability to choose a objective to optimize in one solution
MISSING_SHIFT_PROBABILITY = env("MISSING_SHIFT_PROBABILITY")
ASSIGNED_VIGILANTES_PROBABILITY = env("ASSIGNED_VIGILANTES_PROBABILITY")
EXTRA_HOURS_PROBABILITY = env("EXTRA_HOURS_PROBABILITY")
DISTANCE_GRASP_PROBABILITY = env("DISTANCE_GRASP_PROBABILITY")


#NSGA2 
MAX_EFOS_NSGAII = env("MAX_EFOS_NSGAII")
POPULATION_AMOUNT_NSGAII = env("POPULATION_AMOUNT_NSGAII")
NUM_PARENTS_OF_ORDERED_POPULATION = env("NUM_PARENTS_OF_ORDERED_POPULATION")
NUMBER_ITERATION_SELECTION_COMPONENTE = env("NUMBER_ITERATION_SELECTION_COMPONENTE")
NUMBER_OF_CHILDREN_GENERATE = env("NUMBER_OF_CHILDREN_GENERATE")
#PorcetanjeCrossigNsgaii
MISSING_SHIFT_CROSSING_PROBABILITY = env("MISSING_SHIFT_CROSSING_PROBABILITY")
ASSIGNED_VIGILANTES_CROSSING_PROBABILITY = env("ASSIGNED_VIGILANTES_CROSSING_PROBABILITY")
EXTRA_HOURS_CROSSING_PROBABILITY = env("EXTRA_HOURS_CROSSING_PROBABILITY")
DISTANCE_CROSSING_PROBABILITY = env("DISTANCE_CROSSING_PROBABILITY")

#GRASP CONFIG
#PARAMETERS
MAX_EFOS_GRASP = env("MAX_EFOS_GRASP")
POPULATION_AMOUNT_GRASP = env("POPULATION_AMOUNT_GRASP")
COMPONENTS_AMOUNT_GRASP = env("COMPONENTS_AMOUNT_GRASP")
RESTRICTED_LIST_AMOUNT_COMPONENT_GRASP = env("RESTRICTED_LIST_AMOUNT_COMPONENT_GRASP")
TWEAK_AMOUNT_REPETITIONS_GRASP = env("TWEAK_AMOUNT_REPETITIONS_GRASP")
#PorcetanjeTweaksGRASP
MISSING_SHIFT_TWEAK_PROBABILITY = env("MISSING_SHIFT_TWEAK_PROBABILITY")
ASSIGNED_VIGILANTES_TWEAK_PROBABILITY = env("ASSIGNED_VIGILANTES_TWEAK_PROBABILITY")
EXTRA_HOURS_TWEAK_PROBABILITY = env("EXTRA_HOURS_TWEAK_PROBABILITY")
DISTANCE_TWEAK_PROBABILITY = env("DISTANCE_TWEAK_PROBABILITY")