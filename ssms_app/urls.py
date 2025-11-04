from django.urls import path
from . import views

urlpatterns = [
    # ----------------- ADD endpoints -----------------
    path('add-student/', views.add_student, name='add-student'),
    path('add-sponsor/', views.add_sponsor, name='add-sponsor'),
    path('add-scholarship-program/', views.add_scholarship_program, name='add-scholarship-program'),
    path('add-allocation/', views.add_sponsorship_allocation, name='add-allocation'),
    path('add-payment/', views.add_payment, name='add-payment'),

    # ----------------- GET endpoints -----------------
    path('show-students/', views.show_students, name='show-students'),
    path('show-sponsors/', views.show_sponsors, name='show-sponsors'),
    path('show-programs/', views.show_scholarship_programs, name='show-programs'),
    path('show-allocations/', views.show_sponsorship_allocations, name='show-allocations'),
    path('show-payments/', views.show_payments, name='show-payments'),

    # Dashboard analytics
    path('dashboard/totals/', views.dashboard_totals, name='dashboard-totals'),
    path('dashboard/recent-allocations/', views.show_recent_allocations, name='show-recent-allocations'),
    path('dashboard/sponsorship-trends/', views.sponsorship_trends, name='sponsorship-trends'),
    path('dashboard/students-by-university/', views.students_by_university, name='students-by-university'),
    path('dashboard/sponsorship-status-distribution/', views.sponsorship_status_distribution, name='sponsorship-status-distribution'),
    path('dashboard/payments-per-semester/', views.payments_per_semester, name='payments-per-semester'),
    path('dashboard/sponsor-contributions/', views.sponsor_contributions, name='sponsor-contributions'),
    path('dashboard/students-by-year/', views.students_by_year, name='students-by-year'),
    path('dashboard/gender-distribution/', views.gender_distribution, name='gender-distribution'),
    path('dashboard/upcoming-end-dates/', views.upcoming_end_dates, name='upcoming-end-dates'),
    path('dashboard/average-scholarship-amount/', views.average_scholarship_amount, name='average-scholarship-amount'),
    path('dashboard/top-programs-by-funding/', views.top_programs_by_funding, name='top-programs-by-funding'),

    # ----------------- REPORT FORM endpoints -----------------
    path('report/student-sponsorship/', views.student_sponsorship_report, name='student-sponsorship-report'),
    path('report/payment-summary/', views.payment_summary_report, name='payment-summary-report'),
    path('report/sponsor-contribution/', views.sponsor_contribution_report, name='sponsor-contribution-report'),
    path('report/scholarship-program-summary/', views.scholarship_program_summary, name='scholarship-program-summary'),
    path('report/active-completed-sponsorships/', views.active_completed_sponsorships, name='active-completed-sponsorships'),
    path('report/students-per-university/', views.students_per_university_report, name='students-per-university-report'),

    # ----------------- UPDATE endpoints -----------------
    path('update-student/<int:student_id>/', views.update_student, name='update-student'),
    path('update-sponsor/<int:sponsor_id>/', views.update_sponsor, name='update-sponsor'),
    path('update-program/<int:program_id>/', views.update_scholarship_program, name='update-program'),
    path('update-allocation/<int:allocation_id>/', views.update_sponsorship_allocation, name='update-allocation'),
    path('update-payment/<int:payment_id>/', views.update_payment, name='update-payment'),

    # ----------------- DELETE endpoints -----------------
    path('delete-student/<int:student_id>/', views.delete_student, name='delete-student'),
    path('delete-sponsor/<int:sponsor_id>/', views.delete_sponsor, name='delete-sponsor'),
    path('delete-program/<int:program_id>/', views.delete_scholarship_program, name='delete-program'),
    path('delete-allocation/<int:allocation_id>/', views.delete_sponsorship_allocation, name='delete-allocation'),
    path('delete-payment/<int:payment_id>/', views.delete_payment, name='delete-payment'),
]
