from django.urls import path
from .views import ProjectCreate, ProjectDetail
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', ProjectCreate.as_view()),
    path('<int:pk>', ProjectDetail.as_view()),
    path('<int:pk>/users', ProjectDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
