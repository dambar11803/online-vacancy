from django.contrib import admin 
from .models import UserStatus, ApplicantInfo, VacancyInfo, EducationInfo

class UserStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_approver', 'is_applicant')  # Show these fields
    search_fields = ('user__username',)  # Enable search by username
    list_filter = ('is_applicant', 'is_approver')  # Add filters

admin.site.register(UserStatus, UserStatusAdmin)  


class ApplicantInfoAdmin(admin.ModelAdmin):
    list_display = ('first_name','citizenship','mobile')

admin.site.register(ApplicantInfo, ApplicantInfoAdmin)    

class VacancyInfoAdmin(admin.ModelAdmin):
    list_display = ('vacancy_position', 'vacancy_level', 'applicant_name')  # Added applicant_name

    def applicant_name(self, obj):
        return f"{obj.applicant.first_name} {obj.applicant.last_name}" if obj.applicant else "No Name"

    applicant_name.short_description = "Applicant Name"  # Admin column name

admin.site.register(VacancyInfo, VacancyInfoAdmin)

class EducationInfoAdmin(admin.ModelAdmin):
    list_display = ('level','faculty','course_name','university_name','passed_year','grade_percent')
admin.site.register(EducationInfo, EducationInfoAdmin)        
    