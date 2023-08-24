from django.contrib import admin
from .models import Question, QuestionOption, QuestionGrade

# Register your models here.
admin.site.register(Question)
admin.site.register(QuestionOption)
admin.site.register(QuestionGrade)
