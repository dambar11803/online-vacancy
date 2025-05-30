from django.shortcuts import render, redirect, HttpResponseRedirect  
from .forms import UserRegisterationForm, ApplicantInfoForm, EducationInfoForm, VacancyInfoForm, VacancyApplicationFormSet
from .models import UserStatus, ApplicantInfo, VacancyInfo, EducationInfo 
from django.urls import reverse_lazy 
from django.views.generic import CreateView, TemplateView, UpdateView, DetailView, ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.views import View
from django.contrib.auth.models import User 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from django.shortcuts import get_object_or_404 
from django.contrib import messages
from django.views.generic import FormView
from django.forms import modelformset_factory 
from django.utils import timezone  # Import timezone for current date 
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ApplicantInfo, VacancyInfo
from .forms import VacancyApplicationFormSet 
from django.urls import reverse 
from django.contrib.auth.decorators import login_required

# User Registration View
class UserRegisterView(CreateView):
    model = User 
    form_class = UserRegisterationForm 
    template_name = 'registeration/register.html' 
    success_url  = reverse_lazy('login')  # Redirect to login after registration

    def form_valid(self, form):
        response = super().form_valid(form)
        user_status = UserStatus.objects.create(user=self.object)  # Create a UserStatus for the new user
        
        # Set the user as an applicant
        user_status.is_applicant = True
        user_status.is_approver = False
        user_status.save()  # Save the updated status
        return response

# Login Page
class LoginPage(LoginView):
    template_name = 'registeration/login.html'
    
    
    def get_success_url(self):
        return reverse_lazy('dashboard')

# Dashboard Redirect View
class DashboardView(View):
    def get(self, request, *args, **kwargs):
        user_status = getattr(request.user, 'userstatus', None)
        if user_status:
            if user_status.is_applicant:
                return redirect('applicant_dashboard')
            elif user_status.is_approver:
                return redirect('approver_dashboard')
        return redirect('login')  # Redirect to login if user has no status

# Applicant Dashboard
class ApplicantDashboard(TemplateView):
    template_name = 'applicant/applicant_dashboard.html'

# Approver Dashboard
class ApproverDashboard(TemplateView):
    template_name = 'approver/approver_dashboard.html'


class PersonalInfoView(LoginRequiredMixin,CreateView):
    model = ApplicantInfo 
    form_class = ApplicantInfoForm
    #fields = ['first_name','last_name','dob','father_name','citizenship','issued_date','issued_district','mobile']
    template_name = 'applicant/personalinfo.html'
    success_url = reverse_lazy('education_info')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            application = ApplicantInfo.objects.filter(user=request.user).first()
            if application:
                return redirect('detail_personalinfo', pk=application.pk)
        return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        form.instance.user = self.request.user  #link application to logged-in user
        return super().form_valid(form)
    
    
class UpdatePersonalInfo(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ApplicantInfo 
    form_class = ApplicantInfoForm 
    template_name = 'applicant/update_personalinfo.html'

    def get_success_url(self):
        return reverse_lazy('applicant_dashboard')
    
     #Ensure the logged-in user can only edit their own application.
    def test_func(self):
        application = self.get_object()
        return self.request.user == application.user 

class PersonalInfoDetailView(LoginRequiredMixin, DetailView):
    model = ApplicantInfo
    template_name = 'applicant/personalinfo_detail.html'  # Create this template
    context_object_name = 'applicant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #check if user has an existing application
        application = ApplicantInfo.objects.filter(user = self.request.user).first()

        if application:
            #Get all vacancy_infos related to this applicant
            vacancy_infos = (
                application.vacancy_infos.all()
                if hasattr(application, 'vacancy_infos')
                else application.vacancy_info_set.all()
            )

            #check if any vacancy is approved
            context['is_approved'] = vacancy_infos.filter(is_approved=True).exists()
        else:
            context['is_approved'] = False 
        return context    



class EducationInfoView(LoginRequiredMixin, CreateView):
    model = EducationInfo
    form_class = EducationInfoForm
    template_name = 'applicant/educationinfo.html'
    success_url = reverse_lazy('vacancy_create')

    def dispatch(self, request, *args, **kwargs):
        # Ensure the user has an associated ApplicantInfo object
        if not hasattr(self.request.user, 'applicantinfo'):
            return redirect('personal_info')  # Redirect to create ApplicantInfo
        # Check if EducationInfo already exists for the user
        education_data = EducationInfo.objects.filter(applicant__user=self.request.user).first()
        if education_data:
            return redirect('detail_educationinfo', pk=education_data.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Set the applicant field to the logged-in user's ApplicantInfo
        form.instance.applicant = self.request.user.applicantinfo
        return super().form_valid(form)
    
    
class EducationInfoDetailView(LoginRequiredMixin, DetailView):
    model = EducationInfo
    template_name = 'applicant/educationinfo_detail.html'  # Create this template
    context_object_name = 'applicant'  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #check if user has an existing application
        application = ApplicantInfo.objects.filter(user = self.request.user).first()

        if application:
            #Get all vacancy_infos related to this applicant
            vacancy_infos = (
                application.vacancy_infos.all()
                if hasattr(application, 'vacancy_infos')
                else application.vacancy_info_set.all()
            )

            #check if any vacancy is approved
            context['is_approved'] = vacancy_infos.filter(is_approved=True).exists()
        else:
            context['is_approved'] = False 
        return context    



class UpdateEducationInfo(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EducationInfo 
    form_class = EducationInfoForm 
    template_name = 'applicant/update_educationinfo.html'




    def get_success_url(self):
        return reverse_lazy('education_info')
    
     #Ensure the logged-in user can only edit their own application.
    def test_func(self):
        update_edu = self.get_object()
        return self.request.user == update_edu.applicant.user  


class VacancyCreateView(LoginRequiredMixin, View):
    template_name = 'applicant/vacancy_create.html'
    success_url = reverse_lazy('vacancy_list')

    def get(self, request, *args, **kwargs):
        applicant = ApplicantInfo.objects.filter(user=request.user).first()

        if not applicant:
            messages.error(request, "Please complete your Education profile before applying.")
            return redirect('vacancy_list')

        # Check if the applicant already has a vacancy application
        has_applied = VacancyInfo.objects.filter(applicant=applicant).exists()
        if has_applied:
            messages.info(request, "You have already submitted a vacancy application.")
            return redirect(self.success_url)

        formset = VacancyApplicationFormSet(queryset=VacancyInfo.objects.none())  
        return render(request, self.template_name, {'formset': formset, 'has_applied': has_applied, 'total_amount': 0})

    def post(self, request, *args, **kwargs):
        formset = VacancyApplicationFormSet(request.POST)
        applicant = ApplicantInfo.objects.filter(user=request.user).first()

        if not applicant:
            messages.error(request, "Please complete your Education profile before applying.")
            return redirect('applicant_dashboard')

        total_amount = 0  # ✅ Initialize total_amount inside the method

        if formset.is_valid():
            vacancies_to_save = []
            
            for form in formset:
                if form.cleaned_data.get('vacancy_position') and form.cleaned_data.get('vacancy_group'):
                    vacancy = form.save(commit=False)
                    vacancy.applicant = applicant  

                    vacancy.vacancy_level = vacancy.vacancy_position.split("(")[-1].strip(")")
                    vacancy.vacancy_created_at = timezone.now().date()

                    if vacancy.vacancy_position == 'Assistant(Level 4)':
                        vacancy.payment_amount = 500
                    elif vacancy.vacancy_position == 'Senior Assistant(Level 5)':
                        vacancy.payment_amount = 700
                    else:
                        vacancy.payment_amount = 900
                    
                    total_amount += vacancy.payment_amount  # ✅ Update instance variable
                    vacancies_to_save.append(vacancy)

            if vacancies_to_save:
                VacancyInfo.objects.bulk_create(vacancies_to_save)

            messages.success(request, f"Vacancy applications submitted successfully! Total payment: Rs. {total_amount}")
            return redirect(self.success_url)

        # ✅ Ensure total_amount is passed even if the form is invalid
        return render(request, self.template_name, {'formset': formset, 'has_applied': False, 'total_amount': total_amount})



class VacancyListView(LoginRequiredMixin, ListView):
    model = VacancyInfo
    template_name = 'applicant/vacancy_list.html'
    context_object_name = 'vacancies'

    def get_queryset(self):
        try:
            return VacancyInfo.objects.filter(applicant= self.request.user.applicantinfo)
        except ApplicantInfo.DoesNotExist:
            return VacancyInfo.objects.none()

#Applications_List_Display
class ApplicationsListView(ListView):
    model = ApplicantInfo
    template_name = 'approver/applicants_list.html'
    context_object_name = 'applicants'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch related vacancy_status for each applicant
        applicants = self.get_queryset().prefetch_related('vacancy_infos')

        for applicant in applicants:
            latest_vacancy = applicant.vacancy_infos.order_by('-vacancy_created_at').first()  # Get the latest vacancy
            applicant.vacancy_status = latest_vacancy.vacancy_status if latest_vacancy else "Pending"

        context['applicants'] = applicants  # ✅ Moved outside the loop
        return context  # ✅ Moved outside the loop


#Applicants Detail
class ApplicantDetailView(DetailView):
    model = ApplicantInfo 
    template_name = 'approver/applicants_detail.html'
    context_object_name = 'applicant'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        applicant = self.get_object()

        # Fetch related data
        context['education_infos'] = EducationInfo.objects.filter(applicant=applicant)
        context['vacancy_infos'] = VacancyInfo.objects.filter(applicant=applicant)

        # Ensure vacancy_info relation exists
        latest_vacancy = applicant.vacancy_infos.order_by('-vacancy_created_at').first()

        if latest_vacancy:
            context['vacancy_status'] = latest_vacancy.vacancy_status
            context['vacancy'] = latest_vacancy
        else:
            context['vacancy_status'] = "Pending"
            context['vacancy'] = None  # Avoids errors if accessed in template

        return context
    
    def post(self, request, *args, **kwargs):
        applicant = self.get_object()
        
        # Get ALL vacancy_infos (not just the latest)
        vacancy_infos = (
            applicant.vacancy_infos.all() 
            if hasattr(applicant, 'vacancy_infos') 
            else applicant.vacancy_info_set.all()
        )

        if not vacancy_infos.exists():  # Check if there are any records
            messages.error(request, "No vacancy records found for this applicant.")
            return redirect('applicants_detail', pk=applicant.pk)

        action = request.POST.get('action')

        if action == 'approve':
            # Update ALL related vacancy_infos
            vacancy_infos.update(
                vacancy_status='Approved',
                is_approved=True,
                approved_at=timezone.now()
            )
            messages.success(request, "All applications Approved")

        elif action == 'reject':
            # Update ALL related vacancy_infos
            vacancy_infos.update(
                vacancy_status='Rejected',
                is_approved=False,
                approved_at=timezone.now()
            )
            messages.warning(request, "All applications Rejected")

        else:
            messages.error(request, "Invalid action")
            return redirect('applicants_detail', pk=applicant.pk)

        return redirect('applications_list')

    
        # return HttpResponseRedirect(reverse('applicants_detail', kwargs={'pk': applicant.pk}))
       
##Applicant's Information in Dashboard

@login_required
def applicant_dashboard(request):
    try:
        # Get applicant's basic info
        applicant = ApplicantInfo.objects.get(user=request.user)
        
        # Get all education info for this applicant
        education_infos = EducationInfo.objects.filter(applicant=applicant)
        
        # Get all vacancy applications
        vacancy_infos = VacancyInfo.objects.filter(applicant=applicant)
        
        context = {
            'applicant': applicant,
            'education_infos': education_infos,
            'vacancy_infos': vacancy_infos,
        }
        
    except ApplicantInfo.DoesNotExist:
        # Handle case where applicant info doesn't exist
        context = {
            'message': 'Please complete your applicant profile',
            'applicant': None,
            'education_infos': [],
            'vacancy_infos': [],
        }
    
    return render(request, 'applicant/applicant_dashboard.html', context)
    
    




# Logout Page (POST request for security)
class LogoutPage(View):
    def get(self, request):
        logout(request)
        return redirect('login')
