from rest_framework import generics
from .permissions import IsOwner, IsOwnerOrContributorReadOnly
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, ContributorCreateSerializer, IssueCreateSerializer, IssueSerializer, CommentCreateSerializer, CommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.authentication import TokenAuthentication, SessionAuthentication


class ProjectCreate(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerOrContributorReadOnly,)

    def perform_create(self, serializer):
        return serializer.save(author_user_id=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(author_user_id=user.id)
        contributions = Contributor.objects.filter(user=user)
        for c in contributions:
            queryset = queryset | Project.objects.filter(id=c.project.id)
        return queryset.order_by('id')


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrContributorReadOnly,)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj


class ContributorCreate(generics.ListCreateAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorCreateSerializer
    permission_classes = (IsAuthenticated, IsOwner,)
    lookup_field = 'project_id'

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.kwargs['project_id'])
        self.check_object_permissions(self.request, project)

        if serializer.is_valid():
            return serializer.save(project=project)
        return Response(status=409)

    def get_queryset(self):
        project = Project.objects.get(id=self.kwargs['project_id'])
        self.check_object_permissions(self.request, project)
        if not project:
            raise NotFound()
        return self.queryset.filter(project=project)


class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.

    @api_view(["POST","GET","PUT","DELETE"])
    @permission_classes([IsAuthenticated])
    """

    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]:  # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)
        return obj


class ContributorDetail(generics.RetrieveDestroyAPIView, MultipleFieldLookupMixin):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'project_id'
    lookup_fields = ['project_id', 'pk']

    def get_queryset(self, *args, **kwargs):
        queryset = Contributor.objects.all()
        return queryset.filter(project_id=self.kwargs['project_id'], user_id=self.kwargs['user_id'])


class IssueCreate(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueCreateSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrContributorReadOnly,)
    lookup_field = 'issue_id'

    def perform_create(self, serializer):
        project = Project.objects.get(id=self.kwargs['project_id'])
        self.check_object_permissions(self.request, project)
        if serializer.is_valid():
            return serializer.save(project_id=project, author_user_id=self.request.user)
        return Response(status=409)

    def get_queryset(self):
        project = Project.objects.get(id=self.kwargs['project_id'])
        self.check_object_permissions(self.request, project)
        return self.queryset.filter(project_id=project)


class IssueDetail(generics.RetrieveUpdateDestroyAPIView, MultipleFieldLookupMixin):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrContributorReadOnly,)
    lookup_field = 'issue_id'
    lookup_fields = ['project_id', 'issue_id']

    def get_queryset(self):
        project = Project.objects.get(id=self.kwargs['project_id'])
        self.check_object_permissions(self.request, project)
        return self.queryset.filter(project_id=self.kwargs['project_id'])

    def get_object(self):
        project = Project.objects.get(id=self.kwargs['project_id'])
        self.check_object_permissions(self.request, project)
        obj = get_object_or_404(self.get_queryset(),
                                pk=self.kwargs['issue_id'])
        return obj


class CommentCreate(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrContributorReadOnly,)
    lookup_field = 'issue_id'

    def perform_create(self, serializer):
        issue = Issue.objects.get(id=self.kwargs['issue_id'])
        project = issue.project_id
        self.check_object_permissions(self.request, project)
        user = self.request.user
        if serializer.is_valid():
            return serializer.save(issue_id=issue, author_user_id=user)
        return Response(status=409)

    def get_queryset(self, *args, **kwargs):
        issue = Issue.objects.get(id=self.kwargs['issue_id'])
        project = issue.project_id
        self.check_object_permissions(self.request, project)
        return self.queryset.filter(issue_id=self.kwargs['issue_id'])


class CommentDetail(generics.RetrieveUpdateDestroyAPIView, MultipleFieldLookupMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrContributorReadOnly,)
    lookup_field = 'id'
    lookup_fields = ['issue_id', 'id']

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(issue_id=self.kwargs['issue_id'])

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(),
                                pk=self.kwargs['id'])
        return obj
