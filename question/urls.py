from django.urls import path
from .views import (
    RetrieveUpdateDestroyQuestionAPIView,
    ListCreateOptionAPIView,
    ListCreateQuestionAPIView,
    RetrieveUpdateDeleteOptionView
)

urlpatterns = [
    path("", ListCreateQuestionAPIView.as_view()),
    path("options/<int:pk>/", RetrieveUpdateDeleteOptionView.as_view()),
    path("<int:pk>/", RetrieveUpdateDestroyQuestionAPIView.as_view()),
    path("<int:pk>/options/", ListCreateOptionAPIView.as_view()),
]
