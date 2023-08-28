from django.urls import path
from .views import (
    ExamListCreateAPIView, ExamResultsAPIView,
    ExamResultAPIView, ExamRetrieveUpdateDestroyAPIView,
    ExamLoginAPIView
)

urlpatterns = [
    path('assessments/', ExamListCreateAPIView.as_view()),
    path('assessments/<int:pk>/', ExamRetrieveUpdateDestroyAPIView.as_view()),
    path('assessments/<int:item_id>/results', ExamResultsAPIView.as_view()),
    path('results/<int:pk>/', ExamResultAPIView.as_view()),
    path('assessments/login/', ExamLoginAPIView.as_view())
]
