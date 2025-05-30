Online Vacancy System - README
Overview
The Online Vacancy System is a Django-based web application that streamlines the job application process for government or organizational vacancies. It features role-based access control, allowing applicants to submit applications and approvers to review and manage them.
Key Features
1. Role-Based User System
•	Applicants: Can create profiles, submit applications, and track status
•	Approvers: Can review, approve, or reject applications
•	User Status Management: Each user is assigned a role (applicant/approver) upon registration
2. Application Management
•	Multi-step Application Process:
1.	Personal Information
2.	Educational Qualifications
3.	Vacancy Selection
•	Document Upload: Supports PDF and JPG files for certificates and identification
•	Application Tracking: View status (Pending/Approved/Rejected)
3. Vacancy System
•	Multiple Position Support: Different levels (Assistant, Senior Assistant, Officer)
•	Group Selection: Administrative or IT positions
•	Payment Calculation: Automatic fee calculation based on position level
4. Approval Workflow
•	Bulk Actions: Approve or reject all applications for a candidate
•	Status Tracking: Timestamped approval records
•	Dashboard Views: Separate interfaces for applicants and approvers
Technical Implementation
Models
•	UserStatus: Manages user roles (applicant/approver)
•	ApplicantInfo: Stores personal details and documents
•	EducationInfo: Manages educational qualifications with document uploads
•	VacancyInfo: Tracks vacancy applications and status
Views
•	Authentication: Registration, login, logout
•	Applicant Flow: Dashboard, profile creation, application submission
•	Approver Flow: Application review, approval/rejection
•	Detail Views: Comprehensive application information
Security Features
•	Login-required access for sensitive operations
•	User-specific data access restrictions
•	File type validation for uploads
Installation
1.	Clone the repository
2.	Create and activate virtual environment
3.	Install requirements: pip install -r requirements.txt
4.	Run migrations: python manage.py migrate
5.	Create superuser: python manage.py createsuperuser
6.	Run development server: python manage.py runserver
Usage
1.	Register as either an applicant or approver
2.	Applicants complete their profile and submit applications
3.	Approvers review submissions and update statuses
4.	Applicants track their application status through the dashboard
File Structure
•	models.py: Database schema definitions
•	views.py: Application logic and routing
•	templates/: HTML templates organized by user role
•	static/: CSS, JavaScript, and uploaded files
This system provides a complete solution for managing vacancy applications with proper access control and workflow management.

