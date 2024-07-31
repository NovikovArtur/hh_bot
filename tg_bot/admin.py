from django.contrib import admin
from .models import *

admin.site.register(UserModel)
admin.site.register(CvModel)
admin.site.register(ProjectModel)
admin.site.register(VacancyModel)
