from django.urls import path 
from .views import (LoginPage, LogoutPage, DashboardView, ApplicantDashboard, ApproverDashboard, UserRegisterView,
                    PersonalInfoView, EducationInfoView ,UpdatePersonalInfo, PersonalInfoDetailView, EducationInfoView, 
                    EducationInfoDetailView,UpdateEducationInfo,  VacancyListView, VacancyCreateView, ApplicationsListView,
                    ApplicantDetailView, applicant_dashboard)


urlpatterns = [
    path('', LoginPage.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # path('applicant-dashboard/', ApplicantDashboard.as_view(), name='applicant_dashboard'),
    path('applicant-dashboard/', applicant_dashboard, name='applicant_dashboard'),
    path('personal-info/', PersonalInfoView.as_view(), name='personal_info'),
    path('personalinfo-detail/<int:pk>/', PersonalInfoDetailView.as_view(), name='detail_personalinfo'),
    path('education-info/', EducationInfoView.as_view(), name='education_info'),
    path('educationinfo-detail/<int:pk>/', EducationInfoDetailView.as_view(), name='detail_educationinfo'),
    path('update-personalinfo/<int:pk>/', UpdatePersonalInfo.as_view(), name='update_personalinfo'),
    path('update-educationinfo/<int:pk>/', UpdateEducationInfo.as_view(), name='update_educationinfo'),
    path('vacancy-list/', VacancyListView.as_view(), name='vacancy_list'),
    path('vacancy-create/',VacancyCreateView.as_view(), name='vacancy_create'),
    path('approver-dashboard/', ApproverDashboard.as_view(), name='approver_dashboard'),
    path('applicants-list/', ApplicationsListView.as_view(), name='applications_list'),
    path('applicants-detail/<int:pk>/', ApplicantDetailView.as_view(),name='applicants_detail'),
    path('logout/', LogoutPage.as_view(), name='logout'),
]