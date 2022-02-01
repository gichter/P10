from django.db import models
from users.models import User


class Projects(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(max_length=1500, blank=True, default='')
    type = models.CharField(max_length=100, blank=True)
    author_user_id = models.ForeignKey(
        User, related_name='projects', on_delete=models.CASCADE)


class Issues(models.Model):
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
        Projects, related_name='issues', on_delete=models.CASCADE)


class Comments(models.Model):
    description = models.TextField(max_length=1500, blank=True, default='')
    created_time = models.DateTimeField(auto_now_add=True)

    author_user_id = models.ForeignKey(
        User, related_name='comments_created', on_delete=models.CASCADE)
    issue_id = models.ForeignKey(
        Issues, related_name='comments', on_delete=models.CASCADE)
