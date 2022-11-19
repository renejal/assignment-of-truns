import json
from utils.optimizerParameters import OptimizerParamets
    
def main():
    request  = open("app/request.json")
    filesNames = json.load(request)
    OptimizerParamets("NSGA-II", filesNames.get("filesNames"))
main()