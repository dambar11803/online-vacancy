from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

def validate_file_extension(value):
    if not value.name.endswith(('.pdf', '.jpg', '.jpeg')):
        raise ValidationError("Only PDF and JPG files are allowed.")

def user_directory_path(instance, filename):
    return f'uploads/{instance.user.username}/{filename}'

class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userstatus')
    is_applicant = models.BooleanField(default=False)
    is_approver = models.BooleanField(default=False)
    user_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class ApplicantInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=50)
    dob = models.DateField(null=True, blank=True)
    father_name = models.CharField(max_length=100)
    citizenship = models.CharField(max_length=50)
    issued_date = models.DateField(blank=True, null=True)
    issued_district = models.CharField(max_length=50, blank=True)
    mobile = models.CharField(max_length=15, unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    upload_citizenship = models.FileField(
        upload_to=user_directory_path,
        validators=[validate_file_extension],
        help_text="(pdf or jpg)"
    )

    def __str__(self):
        return f"{self.user.username} Personal Info"


def education_document_path(instance, filename):
    return f'uploads/{instance.applicant.user.username}/{filename}'

class EducationInfo(models.Model):
    LEVEL_CHOICES = [
        ('Plus2', 'Plus2'),
        ('Bachelor', 'Bachelor'),
        ('Master', 'Master')
    ]

    FACULTY_CHOICES = [
        ('IT', 'IT'),
        ('Commerce', 'Commerce')
    ]

    UNIVERSITY_CHOICES = [
        ('Pokhara University', 'Pokhara University'),
        ('Purbanchal University', 'Purbanchal University'),
        ('Tribhuwan University', 'Tribhuwan University')
    ]

    applicant = models.ForeignKey(ApplicantInfo, on_delete=models.CASCADE, related_name='education_infos')
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default='Plus2')
    faculty = models.CharField(max_length=50, choices=FACULTY_CHOICES, default='Commerce')
    course_name = models.CharField(max_length=50)
    university_name = models.CharField(max_length=100, choices=UNIVERSITY_CHOICES, default='Tribhuwan University')
    college_name = models.CharField(max_length=100)
    passed_year = models.IntegerField()
    grade_percent = models.FloatField()
    upload_transcript1 = models.FileField(upload_to=education_document_path, validators=[validate_file_extension], help_text="(pdf or jpg)")
    upload_transcript2 = models.FileField(upload_to=education_document_path, validators=[validate_file_extension], help_text="(pdf or jpg)")
    upload_character = models.FileField(upload_to=education_document_path, validators=[validate_file_extension], help_text="(pdf or jpg)")
    upload_license = models.FileField(upload_to=education_document_path, validators=[validate_file_extension], help_text="(pdf or jpg)", blank=True)
    upload_other = models.FileField(upload_to=education_document_path, validators=[validate_file_extension], help_text="(pdf or jpg)", blank=True)
    upload_other1 = models.FileField(upload_to=education_document_path, validators=[validate_file_extension], help_text="(pdf or jpg)", blank=True)

    def __str__(self):
        return f"{self.applicant.user.username} Educational Detail"

class VacancyInfo(models.Model):
    POSITION_CHOICES = [('Assistant(Level 4)','Assistant(Level 4)'),('Senior Assistant(Level 5)','Senior Assistant(Level 5)'),('Officer(Level 6)','Officer(Level 6)')]

    GROUP_CHOICES = [
        ('Administration', 'Administration'),
        ('IT', 'IT'),
       
    ]

    applicant = models.ForeignKey(ApplicantInfo, on_delete=models.CASCADE, related_name='vacancy_infos')
    vacancy_position = models.CharField(max_length=50, choices=POSITION_CHOICES, default='Assistant')
    vacancy_level = models.CharField(max_length=8, null=True, blank= True)
    vacancy_group = models.CharField(choices = GROUP_CHOICES, max_length=50, default='Administration')
    vacancy_created_at = models.DateField(null=True, blank= True)
    # vacancy_status = models.CharField(max_length=9, default = 'Pending')
    vacancy_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    is_approved = models.BooleanField(default=False)
    approved_at = models.DateTimeField(null=True, blank=True)
    payment_amount = models.PositiveIntegerField(default=0)
    is_payment_made = models.BooleanField(default=False)

    class Meta:
        unique_together = ('applicant', 'vacancy_position','vacancy_group')  # ✅ Prevents duplicate applications

    def __str__(self):
        return f"{self.applicant.user.username} - {self.vacancy_position}"

    