from django.urls import path
from .views import ProjectCreate, ProjectDetail, ContributorCreate, ContributorDelete, IssueCreate, IssueDelete, CommentCreate, CommentDelete
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', ProjectCreate.as_view()),
    path('<int:pk>', ProjectDetail.as_view()),
    path('<int:project_id>/users', ContributorCreate.as_view()),
    path('<int:project_id>/users/<int:user_id>', ContributorDelete.as_view()),
    path('<int:project_id>/issues', IssueCreate.as_view()),
    path('<int:project_id>/issues/<int:id>', IssueDelete.as_view()),
    path('<int:project_id>/issues/<int:issue_id>/comments', CommentCreate.as_view()),
    path('<int:project_id>/issues/<int:issue_id>/comments/<int:id>',
         CommentDelete.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
