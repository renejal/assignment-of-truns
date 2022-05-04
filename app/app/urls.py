from django.contrib import admin
from django.urls import path
from app.views import CSVUploadHandler

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'csv-upload/',CSVUploadHandler.as_view(), name='csv-upload'),
    # path('',index)
]
