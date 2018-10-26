from django.contrib import admin
from .models import Problems,Submissions,TestCase,ProblemSubmission

# Register your models here.
admin.site.register(Problems)
admin.site.register(Submissions)
admin.site.register(TestCase)
admin.site.register(ProblemSubmission)
