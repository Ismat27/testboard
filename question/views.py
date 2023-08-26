from rest_framework import generics, exceptions
from .models import Question, QuestionGrade, QuestionOption
from .serializers import QuestionSerializer, QuestionOptionSerializer
from .permissions import IsCandidate, IsExaminer, IsExaminerOption
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class ListCreateQuestionAPIView(generics.ListCreateAPIView):
    permission_classes = [
        IsAuthenticated,
        (IsCandidate | IsExaminer | IsAdminUser)
    ]
    serializer_class = QuestionSerializer

    def get_queryset(self):
        query_params = self.request.query_params
        assessment_id = query_params.get("assessment_id", None)
        if not assessment_id:
            raise exceptions.ParseError("assessment id is missing")
        try:
            items = Question.objects.filter(assessment=assessment_id)
            return items
        except:
            raise exceptions.ParseError("invalid exam id")

    def get_permissions(self):
        return super().get_permissions()

    def get_serializer_class(self):
        return super().get_serializer_class()


class RetrieveUpdateDestroyQuestionAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [
        IsAuthenticated,
        (IsCandidate | IsExaminer | IsAdminUser)
    ]
    serializer_class = QuestionSerializer
    lookup_field = "pk"
    queryset = Question.objects.all()

    def get_object(self):
        return super().get_object()


class ListCreateOptionAPIView(generics.ListCreateAPIView):
    serializer_class = QuestionOptionSerializer

    def get_queryset(self):
        question_id = self.kwargs.get("pk")
        options = QuestionOption.objects.filter(question=question_id)
        return options

    def perform_create(self, serializer):
        try:
            question_id = self.kwargs.get("pk")
            return serializer.save(question_id=question_id)
        except:
            raise exceptions.ParseError("invalid question id")


class RetrieveUpdateDeleteOptionView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionOptionSerializer
    permission_classes = [IsAuthenticated, (IsAdminUser | IsExaminerOption)]
    queryset = QuestionOption.objects.all()


class GradeQuestion(generics.CreateAPIView):

    def perform_create(self, serializer):
        grade = QuestionGrade.objects.update_or_create()
        return super().perform_create(serializer)
