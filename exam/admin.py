from django.contrib import admin
from .models import Assessment,  AssessmentResult, AssessmentLogin, AssessmentToken, Result

# Register your models here.
admin.site.register(Assessment)
admin.site.register(AssessmentResult)
admin.site.register(AssessmentLogin)
admin.site.register(AssessmentToken)
admin.site.register(Result)
