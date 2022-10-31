from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path("upload_file",upload_file, name="upload_file")
]
