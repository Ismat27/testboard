from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import ExamSerializer
from .models import Assessment, AssessmentResult
from .serializers import ExamSerializer, ExamCreateSerializer, ExamResultListSerializer
from .permissions import ExamOwnerPermission, ExamResultPermission


class ExamListCreateAPIView(generics.ListCreateAPIView):
    queryset = Assessment.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return super().get_queryset()
        items = Assessment.objects.filter(examiner=user)
        return items

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ExamCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        return serializer.save(examiner=self.request.user)


class ExamRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assessment.objects.all()
    lookup_field = 'pk'
    permission_classes = [ExamOwnerPermission]
    serializer_class = ExamSerializer


class ExamResultsAPIView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ExamResultListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return AssessmentResult.objects.filter(assessment=item_id)
        item_id = self.kwargs.get('item_id')
        items = AssessmentResult.objects.filter(assessment=item_id)
        return items


class ExamResultAPIView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    permission_classes = [ExamResultPermission]
    queryset = AssessmentResult.objects.all()
    serializer_class = ExamResultListSerializer

    def get_object(self):
        return super().get_object()
