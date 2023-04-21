from rest_framework import serializers

from posts.serializers import Base64ImageField
from .models import User


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def create(self, data):
        user_obj = User.objects.create_user(**data)
        return user_obj

    # class Meta:
    #     model = User
    #     fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'profile')


class UserResponceSerialilzer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField('get_profile')

    def get_profile(self, instance):
        return instance.profile.url

    class Meta:
        model = User
        fields = ['profile', ]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    profile = Base64ImageField(
        max_length=None, use_url=True, required=False
    )

    class Meta:
        model = User
        fields = ('profile', )
