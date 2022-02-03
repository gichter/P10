from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment
from users.models import User


from users.serializers import UserSerializer


class ContributorMinimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user', 'role']


class ContributorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project', 'role']
        lookup_field = 'project'


class ProjectSerializer(serializers.ModelSerializer):
    contributors = ContributorMinimalSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        read_only_fields = ['id', 'author_user_id']
        fields = ['id', 'title', 'description',
                  'type', 'author_user_id', 'contributors']


class ContributorCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributor
        read_only_fields = ['id', 'project']
        fields = ['id', 'user', 'project', 'role']


class IssueCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        read_only_fields = ['id', 'project_id']
        fields = ['id', 'title', 'description', 'tag', 'priority',
                  'status', 'author_user_id', 'assignee_user_id', 'project_id']


class IssueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issue
        read_only_fields = ['id', 'project_id']
        fields = ['id', 'title', 'description', 'tag', 'priority',
                  'status', 'author_user_id', 'assignee_user_id', 'project_id']


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        read_only_fields = ['id', 'issue_id', 'author_user_id']
        fields = ['id', 'description', 'created_time',
                  'author_user_id', 'issue_id']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        read_only_fields = ['id', 'issue_id', 'author_user_id']
        fields = ['id', 'description', 'created_time',
                  'author_user_id', 'issue_id']
