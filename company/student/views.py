from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .serializer import StudentSerializer,loginserializer
from .models import Student
from django.contrib.auth.hashers import make_password,check_password
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
class StudentApi(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentCreateApi(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentUpdateApi(generics.RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDeleteApi(generics.DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class RegistrationAPIView(generics.CreateAPIView):
    queryset= Student.objects.all()
    serializer_class = StudentSerializer

    def post(self,request):
        data=request.POST.copy()
        password= data.get('password')
        data['password'] =make_password(password)
        serializer = self.get_serializer(data= data)
        serializer.is_valid(raise_exception = True)
        student= serializer.save()
        refresh =RefreshToken.for_user(student)
        token ={
            'refresh':str(refresh),
            'access':str(refresh.access_token),
        }
        return Response(token)
    

class LoginAPIView(generics.CreateAPIView):
    serializer_class= loginserializer
    def post(self, request):
        serializers =self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception = True)

        student_email=serializers.validated_data['student_email']
        password=serializers.validated_data['password']
        try:
            student= Student.objects.get(student_email=student_email)
        except Student.DoesNotExist:
            return Response({'error':'Invalid Email. '},status=400)
        if not check_password(password,student.password):
            return Response({'error':'Invalid password. '},status=400)
        refresh =RefreshToken.for_user(student)
        response_data ={
            'email':student_email,
            'access_token':str(refresh.access_token),
        }
        return Response(response_data)
    