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
    path('dashboard/totals/', views.dashboard_totals, name='dashboard-totals'),
    path('dashboard/recent-allocations/', views.show_recent_allocations, name='show-recent-allocations'),

    # ----------------- UPDATE endpoints -----------------
    path('update-student/<int:student_id>/', views.update_student, name='update-student'),
    path('update-sponsor/<int:sponsor_id>/', views.update_sponsor, name='update-sponsor'),
    path('update-program/<int:program_id>/', views.update_scholarship_program, name='update-program'),
    path('update-allocation/<int:allocation_id>/', views.update_allocation, name='update-allocation'),
    path('update-payment/<int:payment_id>/', views.update_payment, name='update-payment'),

    # ----------------- DELETE endpoints -----------------
    path('delete-student/<int:student_id>/', views.delete_student, name='delete-student'),
    path('delete-sponsor/<int:sponsor_id>/', views.delete_sponsor, name='delete-sponsor'),
    path('delete-program/<int:program_id>/', views.delete_scholarship_program, name='delete-program'),
    path('delete-allocation/<int:allocation_id>/', views.delete_allocation, name='delete-allocation'),
    path('delete-payment/<int:payment_id>/', views.delete_payment, name='delete-payment'),
]
