from django.urls import path
from .views import ProjectCreate, ProjectDetail, ContributorCreate, ContributorDetail, IssueCreate, IssueDetail, CommentCreate, CommentDetail
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', ProjectCreate.as_view()),
    path('<int:pk>/', ProjectDetail.as_view()),
    path('<int:project_id>/users/', ContributorCreate.as_view()),
    path('<int:project_id>/users/<int:user_id>/', ContributorDetail.as_view()),
    path('<int:project_id>/issues/', IssueCreate.as_view()),
    path('<int:project_id>/issues/<int:issue_id>/', IssueDetail.as_view()),
    path('<int:project_id>/issues/<int:issue_id>/comments/',
         CommentCreate.as_view()),
    path('<int:project_id>/issues/<int:issue_id>/comments/<int:id>/',
         CommentDetail.as_view()),
]
"""
urlpatterns = format_suffix_patterns(urlpatterns)
    {"email": "ichter.g@gmail.com","password": "159951aA*"}
    """
