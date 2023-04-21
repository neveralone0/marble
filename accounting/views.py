from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import *
from .models import User


class RegisterUser(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        srz_data = self.serializer_class(data=request.data, partial=True)
        if srz_data.is_valid():
            print(srz_data)
            # print(srz_data.errors)
            print(srz_data.validated_data)
            srz_data.create(srz_data.validated_data)
            user = User.objects.get(username=srz_data.validated_data['username'])
            refresh = RefreshToken.for_user(user)
            return Response({'msg': 'true',
                             'refresh': str(refresh),
                             'access': str(refresh.access_token)})


class LoginUser(APIView):
    def post(self, request):
        phone_number = request.data['username']
        password = request.data['password']
        check_for_user = User.objects.get(username=phone_number)
        if not check_for_user:
            return Response({'msg': 'register first!'}, status=status.HTTP_400_BAD_REQUEST)
        check = check_password(password, check_for_user.password)
        if not check:
            return Response({'msg': 'wrong password!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.get(username=phone_number)
            refresh = RefreshToken.for_user(user)
            return Response({'msg': 'true',
                             'refresh': str(refresh),
                             'access': str(refresh.access_token)})


class Testi(APIView):
    def get(self, request):
        return Response({'msg': 'im your response'})


class GetUsers(APIView):
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.all()
        srz_data = self.serializer_class(instance=users, many=True)
        return Response(srz_data.data)


class ValidateToken(APIView):
    permission_classes = [IsAuthenticated, ]
    def get(self, request):
            return Response({'msg': 'true'})


class YourProfile(APIView):
    serializer_class = UserResponceSerialilzer
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        posts = User.objects.get(id=request.user.id)
        srz_data = self.serializer_class(instance=posts)
        return Response(srz_data.data)


class UpdateProfile(APIView):
    serializer_class = ProfileUpdateSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        srz_data = self.serializer_class(data=request.data)
        if srz_data.is_valid():
            user = User.objects.get(id=request.user.id)
            user.profile.delete()
            srz_data.update(instance=user, validated_data=srz_data.validated_data)
            return Response({'msg': 'profile updated'}, status=status.HTTP_201_CREATED)
        print(srz_data.errors)
        return Response(srz_data.errors)
