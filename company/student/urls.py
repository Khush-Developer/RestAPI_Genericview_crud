from django.urls import path
from .views import StudentApi,StudentCreateApi,StudentUpdateApi,StudentDeleteApi

urlpatterns = [
    path('stu',StudentApi.as_view()),
    path('stu/create',StudentCreateApi.as_view()),
    path('stu/upd/<int:pk>',StudentUpdateApi.as_view()),
    path('stu/dlt/<int:pk>',StudentDeleteApi.as_view()),
]
