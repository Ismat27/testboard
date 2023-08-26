from rest_framework import serializers
from .models import Question, QuestionOption


class QuestionIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ["id"]


class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ["question",]
        model = QuestionOption
        extra_kwargs = {
            "is_answer": {"write_only": True},
        }


class QuestionSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True)

    class Meta:
        fields = "__all__"
        model = Question

    def create(self, validated_data):
        options = validated_data.pop("options")
        question = Question.objects.create(**validated_data)
        for option in options:
            QuestionOption.objects.create(question=question, **option)
        return question
