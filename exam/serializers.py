from rest_framework.serializers import ModelSerializer, Serializer
from .models import Assessment, AssessmentResult


class ExamSerializer(ModelSerializer):

    class Meta:
        model = Assessment
        exclude = ('candidates', 'examiner')


class ExamCreateSerializer(ModelSerializer):

    class Meta:
        model = Assessment
        fields = '__all__'


class ExamResultListSerializer(ModelSerializer):

    class Meta:
        model = AssessmentResult
        fields = '__all__'


class ExamResultDetailSerializer():
    pass
