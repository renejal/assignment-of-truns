from main import Main
import sys
import json
from utils.optimizerParameters import OptimizerParamets
sys.path.append("..")

request  = open("dataset/real_dataset.json")
request = json.load(request)
Main(request)

def main():
    request  = open("app/request.json")
    data = json.load(request)
    Main(data)
