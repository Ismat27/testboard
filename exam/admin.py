from django.contrib import admin
from .models import Assessment,  AssessmentResult

# Register your models here.
admin.site.register(Assessment)
admin.site.register(AssessmentResult)
