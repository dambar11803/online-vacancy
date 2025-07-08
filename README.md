Online Vacancy System - README
==============================

Overview
--------
The **Online Vacancy System** is a Django-based web application designed to simplify and automate the job application process for governmental or organizational vacancies. It features role-based access control, allowing **Applicants** to submit and track their applications and **Approvers** to review, approve, or reject them efficiently.

Key Features
------------
1. **Role-Based User Management**
   - **Applicants**: Can register, create profiles, upload documents, and apply for vacancies.
   - **Approvers**: Can review submitted applications and take actions (approve/reject).
   - **User Status Assignment**: Each user is assigned a role during or after registration.

2. **Application Management Workflow**
   - Multi-step application process:
     1. Personal Information Entry
     2. Educational Qualification Submission
     3. Vacancy Selection
   - Document Upload: Supports PDF and JPG formats for certificates and IDs.
   - Application Tracking: Applicants can track their application status (Pending / Approved / Rejected).

3. **Vacancy System Features**
   - Support for multiple positions (e.g., Assistant, Senior Assistant, Officer).
   - Group Selection (e.g., Administrative, IT).
   - Automatic Payment Calculation based on the applied position level.

4. **Approval Workflow**
   - Bulk Actions: Approvers can take batch actions (approve/reject all).
   - Timestamped Status Updates: Records who approved/rejected and when.
   - Dedicated Dashboards: Different views/interfaces for applicants and approvers.

Technical Implementation
------------------------
### Models:
- **UserStatus**: Stores user roles (applicant/approver).
- **ApplicantInfo**: Manages personal details and uploaded documents.
- **EducationInfo**: Handles academic qualifications with associated document uploads.
- **VacancyInfo**: Tracks applications, applied posts, and status.

### Views:
- **Authentication**: Login, logout, registration.
- **Applicant Views**: Dashboard, profile, and application workflow.
- **Approver Views**: Application list, detail view, approval/rejection.
- **Detail Views**: Full details of an application for review.

Security Features
-----------------
- Login-required for all restricted operations.
- Role-based access: applicants and approvers see only their relevant data.
- File upload validation: only specific formats allowed (PDF, JPG).


