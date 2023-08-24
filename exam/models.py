from django.db import models
from django.conf import settings


class Assessment(models.Model):
    examiner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='assessments', on_delete=models.CASCADE)
    candidates = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='AssessmentResult',
        through_fields=('assessment', 'candidate'), related_name='tests')
    total_mark = models.IntegerField()
    title = models.CharField(max_length=255)
    instruction = models.TextField(null=True)
    duration = models.DurationField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    no_of_questions = models.IntegerField()
    exam_code = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.title


class AssessmentResult(models.Model):
    assessment = models.ForeignKey(
        Assessment, on_delete=models.CASCADE, related_name='results')
    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="results")
    started = models.BooleanField(default=False)
    submitted = models.BooleanField(default=False)
    date_started = models.DateTimeField(default=None, null=True)
    date_submitted = models.DateTimeField(default=None, null=True)
    score = models.IntegerField(default=0)

    class Meta:
        unique_together = ['assessment', 'candidate']

    def __str__(self) -> str:
        return f"{self.candidate}: {self.assessment.title}"
