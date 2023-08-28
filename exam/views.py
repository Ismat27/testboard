from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import ExamSerializer
from .models import Assessment, AssessmentResult, AssessmentLogin, AssessmentToken
from .serializers import ExamSerializer, ExamCreateSerializer,\
    ExamResultListSerializer, ExamTokenSerializer
from .permissions import ExamOwnerPermission, ExamResultPermission
from question.models import Question, QuestionGrade
from question.serializers import QuestionSerializer


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


class ExamCredentialCreateAPIView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        assessment_id = self.kwargs.get("pk")
        serializer.save(assessment_id=assessment_id,
                        **serializer.validated_data)


class ExamLoginAPIView(generics.CreateAPIView):
    serializer_class = ExamTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        code = data.pop("code")
        try:
            login = AssessmentLogin.objects.get(
                assessment__exam_code=code, **data)
            assessment = login.assessment
            if not assessment.is_ongoing:
                return Response({"message": "assessment is closed or not started"}, status=403)
            existing_token = AssessmentToken.objects.filter(
                login=login).first()
            if existing_token:
                if existing_token.is_expire():
                    return Response({"message": "Your session has ended"}, status=403)
                return Response({"token": existing_token.token}, status=200)
            current_time = timezone.now()
            expires = assessment.duration + current_time
            if (expires > assessment.end_date):
                expires = assessment.end_date
            token = AssessmentToken.objects.create(
                token="generate hashed token",
                login=login,
                expires=expires
            )
            return Response({"token": token.token, }, status=200)
            # create token
        except:
            return Response({"message": "incorrect credentials"}, status=400)


class StartExam(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        items = Question.objects.filter(id=pk)
        return items

    def list(self, request, *args, **kwargs):
        authorization = self.headers.get("Authorization", {})
        exam_token = authorization.get("exam_token", None)
        if not exam_token:
            return Response({"message": "exam token is missing"}, status=400)
        # check if token has not expired
            # check if exam is still ongoing
            # check if candidate has not submitted
            #  decode token to obtain candidate record
        return super().list(request, *args, **kwargs)
