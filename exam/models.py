from django.db import models
from django.conf import settings
from django.utils import timezone


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

    @property
    def not_started(self):
        return self.start_date > timezone.now()

    @property
    def is_ended(self):
        return timezone.now() > self.end_date

    @property
    def is_ongoing(self):
        return (not self.not_started) and (not self.is_ended)


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


class AssessmentLogin(models.Model):
    assessment = models.ForeignKey(
        Assessment, on_delete=models.CASCADE, related_name='logins')
    username = models.CharField(max_length=255)
    password = models.TextField()

    class Meta:
        unique_together = ['assessment', 'username']

    def __str__(self) -> str:
        return self.username

    def is_taken(self):
        if self.result:
            return True
        return False


class AssessmentToken(models.Model):
    expires = models.DateTimeField()
    login = models.OneToOneField(
        AssessmentLogin, on_delete=models.CASCADE, related_name='token')
    token = models.TextField()

    def is_expire(self):
        return timezone.now() > self.expires


class Result(models.Model):
    started = models.BooleanField(default=False)
    submitted = models.BooleanField(default=False)
    date_started = models.DateTimeField(default=None, null=True)
    date_submitted = models.DateTimeField(default=None, null=True)
    score = models.IntegerField(default=0)
    candidate_credential = models.OneToOneField(
        AssessmentLogin, on_delete=models.CASCADE, related_name='crediential')
