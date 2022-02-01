from rest_framework import mixins, generics
from rest_framework.decorators import api_view
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from .models import Project
from .serializers import ProjectSerializer

from users.models import User

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class ProjectCreate(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(author_user_id=self.request.user)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
