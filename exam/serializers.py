from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from .models import Assessment, AssessmentResult, AssessmentToken, AssessmentLogin


class ExamSerializer(ModelSerializer):

    class Meta:
        model = Assessment
        exclude = ('candidates', 'examiner')


class ExamCreateSerializer(ModelSerializer):

    class Meta:
        model = Assessment
        exclude = ('candidates', 'examiner')


class ExamResultListSerializer(ModelSerializer):

    class Meta:
        model = AssessmentResult
        fields = '__all__'


class ExamResultDetailSerializer():
    pass


class ExamTokenSerializer(Serializer):
    code = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)

    def create(self, validated_data):

        return super().create(validated_data)

    def save(self, **kwargs):
        return super().save(**kwargs)

    class Meta:
        fields = "__all__"


class ExamLoginCredientialSerializer(ModelSerializer):

    class Meta:
        model = AssessmentLogin
        exclude = ["assessment"]
