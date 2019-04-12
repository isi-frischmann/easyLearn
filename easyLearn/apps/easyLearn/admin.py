from django.contrib import admin
# from django.contrib.auth.models import Group
from .models import *


class TrainingSections(admin.ModelAdmin):
     model = Training
     # If you don't specify this, you will get a multiple select widget.
     filter_horizontal = ('trainings',)


# class Activity(admin.ModelAdmin):
#     list_filter = ('name', 'desc')

# Register your models here.
admin.site.site_header = 'Modern Health Admin Panel'
admin.site.register(Training)
admin.site.register(Activity)
admin.site.register(Section, TrainingSections)
admin.site.register(TrainingProgress)
admin.site.register(ActivityProgress)
admin.site.register(SectionProgress)
