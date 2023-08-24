from django.db import models
from django.conf import settings
from exam.models import Assessment


class Question(models.Model):
    assessment = models.ForeignKey(
        Assessment, on_delete=models.CASCADE, related_name='questions')
    content = models.TextField()
    point = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Assessment Questions'

    def __str__(self) -> str:
        return self.content


class QuestionOption(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='options')
    is_active = models.BooleanField(default=True)
    is_answer = models.BooleanField()
    content = models.TextField()
    point = models.IntegerField(default=1)

    def __str__(self) -> str:
        return self.content


class QuestionGrade(models.Model):
    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    selected_options = models.ManyToManyField(QuestionOption)

    class Meta:
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'

    def __str__(self):
        return self.point_obtained

    @property
    def point_obtained(self):
        points = 0
        answers = self.selected_options.all()
        if len(answers) == 0:
            return points
        for i in answers:
            points += i.point
        return points
