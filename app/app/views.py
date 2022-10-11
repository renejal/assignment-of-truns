from main import Main
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
import sys
from utils.optimizerParameters import OptimizerParamets
sys.path.append("..")


class CSVUploadHandler(APIView):

    def get(self, request: Request) -> Response:
        converted_request = Request(request._request, parsers=[JSONParser()]).data
        algorithm = converted_request.get("algorithm")
        filesNames = converted_request.get("filesNames")
        OptimizerParamets(algorithm, filesNames)
        return Response({}, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        converted_request = Request(request._request, parsers=[JSONParser()])
        Main(converted_request.data)
        return Response({}, status=status.HTTP_201_CREATED)
