from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.session_list, name="session-list"),
    path('student-list/<str:pk>/', views.view_student, name="view-student"),
    path('final-marks/<str:pk>/', views.final_subjects, name="final-subjects"),
    path('final-marks/<str:pk>/<str:sub>/', views.final_marks, name="final-marks"),
]