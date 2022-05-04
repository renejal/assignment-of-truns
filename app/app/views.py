from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import JSONParser


class CSVUploadHandler(APIView):
    def get(self, request: Request) -> Response:
        print("get")
        return Response({}, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        print("post",Request.data)
        return Response({}, status=status.HTTP_201_CREATED)
