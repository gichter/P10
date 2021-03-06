from rest_framework import serializers
from .models import User
from softdesk.models import Project
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(
            username=attrs['email'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError('Incorrect email or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}


class UserSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Project.objects.all())

    class Meta:
        model = User
        read_only_fields = ['id', 'projects']
        fields = ['id', 'first_name', 'last_name',
                  'email', 'password', 'projects']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class UserCreateSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        read_only_fields = ['id', 'projects']
        fields = ['id', 'first_name', 'last_name',
                  'email', 'password', 'projects']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
