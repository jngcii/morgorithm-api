from django.contrib import admin
from .models import Solution, Comment, SubComment

admin.site.register(Solution)
admin.site.register(Comment)
admin.site.register(SubComment)