from rest_framework import serializers
from .models import Project

from users.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        read_only_fields = ['id', 'author_user_id']
        fields = ['id', 'title', 'description', 'type', 'author_user_id']
