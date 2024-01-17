from django.contrib import admin
from .models import (College, CustomUser, Subject, 
CourseOutcome, ProgramOutcome, ProgramEducationalObjective, 
ProgramSpecificOutcome, FacultyInfo, AccessRequest)

admin.site.register(College)
admin.site.register(CustomUser)
admin.site.register(Subject)
admin.site.register(CourseOutcome)
admin.site.register(ProgramOutcome)
admin.site.register(ProgramEducationalObjective)
admin.site.register(ProgramSpecificOutcome)
admin.site.register(FacultyInfo)
admin.site.register(AccessRequest)
