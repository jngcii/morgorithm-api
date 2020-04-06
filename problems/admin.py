from django.contrib import admin
from .models import Problem, ProblemGroup, OriginProb

admin.site.register(Problem)
admin.site.register(ProblemGroup)
admin.site.register(OriginProb)