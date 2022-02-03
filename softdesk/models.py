from django.db import models
from users.models import User
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status


class Project(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(max_length=1500, blank=True, default='')
    type = models.CharField(max_length=100, blank=True)
    author_user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='projects', on_delete=models.CASCADE)


class Issue(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(max_length=1500, blank=True, default='')
    tag = models.CharField(max_length=100, blank=True, default='')
    priority = models.CharField(max_length=100, blank=True, default='')
    status = models.CharField(max_length=100, blank=True, default='')

    author_user_id = models.ForeignKey(
        User, related_name='issues_created', on_delete=models.CASCADE)
    assignee_user_id = models.ForeignKey(
        User, related_name='issues_assigned', on_delete=models.SET_NULL, null=True)
    project_id = models.ForeignKey(
        Project, related_name='issues', on_delete=models.CASCADE)


class Comment(models.Model):
    description = models.TextField(max_length=1500, blank=True, default='')
    created_time = models.DateTimeField(auto_now_add=True)

    author_user_id = models.ForeignKey(
        User, related_name='comments_created', on_delete=models.CASCADE)
    issue_id = models.ForeignKey(
        Issue, related_name='comments', on_delete=models.CASCADE)


class Contributor(models.Model):
    user = models.ForeignKey(
        User, related_name='contributions', on_delete=models.CASCADE)
    project = models.ForeignKey(
        Project, related_name='contributors', on_delete=models.CASCADE)
    # permission = models.ChoiceField()
    role = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        pass
        #        unique_together = ('user_id', 'project_id')
