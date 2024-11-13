from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.urls import reverse

from django.contrib.auth.models import User

from rent_booking_apps.users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['id', 'user']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'profile_url']
        read_only_fields = ['username', 'email']

    def update(self, instance, validated_data):
        profile_data = validated_data.get('profile', {})
        profile_serializer = ProfileSerializer(
            instance.profile,
            data=profile_data,
            partial=True
        )
        if profile_serializer.is_valid():
            profile_serializer.save()
        return instance

    def get_profile_url(self, obj) -> str:
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(
                reverse('user-detail', kwargs={'pk': obj.pk})
            )
        return None


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'email': {
                'required': True,
                'allow_blank': False,
                'validators': [UniqueValidator(queryset=User.objects.all())]
            },
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'email': {
                'required': True,
                'allow_blank': False
            },
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }
