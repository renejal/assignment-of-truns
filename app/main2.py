import json
from utils.optimizerParameters import OptimizerParamets


    
def main():
    request  = open("app/request.json")
    filesNames = json.load(request)
    OptimizerParamets("NSGAII", filesNames.get("filesNames"))

    
main()