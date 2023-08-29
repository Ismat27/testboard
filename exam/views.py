from django.utils import timezone
from django.conf import settings
import jwt
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import ExamSerializer
from .models import Assessment, AssessmentResult,\
    AssessmentLogin, AssessmentToken, Result
from .serializers import ExamSerializer, ExamCreateSerializer,\
    ExamResultListSerializer, ExamTokenSerializer
from .permissions import ExamOwnerPermission, ExamResultPermission
from question.models import Question, QuestionGrade
from question.serializers import QuestionSerializer

EXAM_TOKEN_SECRET = settings.EXAM_TOKEN_SECRET


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
        username = data.get("username")
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
            encoded_token = jwt.encode({
                "exam_code": assessment.exam_code,
                "exam_id": assessment.pk,
                "username": username,
                "exp": expires,
            }, EXAM_TOKEN_SECRET, algorithm="HS256")
            token = AssessmentToken.objects.create(
                token=encoded_token,
                login=login,
                expires=expires
            )
            return Response({"token": token.token, }, status=200)
        except:
            return Response({"message": "incorrect credentials"}, status=400)


class StartExam(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        items = Question.objects.filter(assessment_id=pk)
        return items

    def list(self, request, *args, **kwargs):
        authorization = request.headers.get("Authorization")
        exam_token = authorization
        if not exam_token:
            return Response({"message": "exam token is missing"}, status=400)
        try:
            decoded_token = jwt.decode(
                exam_token, EXAM_TOKEN_SECRET, algorithms=['HS256'])
            username = decoded_token["username"]
            exam_code = decoded_token["exam_code"]
            login = AssessmentLogin.objects.get(
                username=username, assessment__exam_code=exam_code)
        except:
            return Response({"message": "invalid or expired token"}, status=400)
        # check if exam is still ongoing
        assessment_id = kwargs.get("pk")
        assessment = Assessment.objects.filter(id=assessment_id).first()
        if not assessment:
            return Response({"message": "invalid credentials"}, status=400)
        if not assessment.is_ongoing:
            return Response({"message": "assessment is closed or not started"}, status=403)
        # check if candidate has not submitted
        result = Result.objects.filter(
            candidate_credential__username=username).first()
        if result:
            if result.submitted:
                return Response({"message": "result submitted"}, status=403)
        else:
            result = Result.objects.create(
                submitted=False,
                started=True,
                date_started=timezone.now(),
                candidate_credential=login,
                score=0
            )
        return super().list(request, *args, **kwargs)
