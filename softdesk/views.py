from rest_framework import generics, mixins
from django.db.models.signals import post_save
from django.conf import settings
from .models import Project, Contributor, Issue, Comment
from users.models import User
from .serializers import ProjectSerializer, ContributorSerializer, ContributorCreateSerializer, IssueCreateSerializer, IssueSerializer, CommentCreateSerializer, CommentSerializer
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from rest_framework import status

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


class ProjectCreate(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        return serializer.save(author_user_id=self.request.user)

    def get_queryset(self):
        user = self.request.user
        print(user)
        return self.queryset.filter(author_user_id=user.id)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ContributorCreate(generics.ListCreateAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorCreateSerializer
    lookup_field = 'project_id'

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.kwargs['project_id'])
        if serializer.is_valid():
            return serializer.save(project=project)
        return Response(status=409)

    def get_queryset(self):
        project = Project.objects.get(id=self.kwargs['project_id'])
        return self.queryset.filter(project=project)


class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """

    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]:  # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class ContributorDelete(generics.RetrieveDestroyAPIView, MultipleFieldLookupMixin):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    lookup_field = 'project_id'
    lookup_fields = ['project_id', 'user_id']

    def get_queryset(self, *args, **kwargs):
        queryset = Contributor.objects.all()
        return queryset.filter(project_id=self.kwargs['project_id'], user_id=self.kwargs['user_id'])


class IssueCreate(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueCreateSerializer
    lookup_field = 'issue_id'

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.kwargs['project_id'])
        if serializer.is_valid():
            return serializer.save(project_id=project)
        return Response(status=409)

    def get_queryset(self):
        project = Project.objects.get(id=self.kwargs['project_id'])
        return self.queryset.filter(project_id=project)


class IssueDelete(generics.RetrieveUpdateDestroyAPIView, MultipleFieldLookupMixin):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    lookup_field = 'id'
    lookup_fields = ['project_id', 'id']

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(project_id=self.kwargs['project_id'])


class CommentCreate(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    lookup_field = 'issue_id'

    def perform_create(self, serializer):
        issue = Issue.objects.get(id=self.kwargs['issue_id'])
        user = self.request.user
        if serializer.is_valid():
            return serializer.save(issue_id=issue, author_user_id=user)
        return Response(status=409)


class CommentDelete(generics.RetrieveUpdateDestroyAPIView, MultipleFieldLookupMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'
    lookup_fields = ['issue_id', 'id']

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(issue_id=self.kwargs['issue_id'])
