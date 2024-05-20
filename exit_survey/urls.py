from django.urls import path
from . import views

urlpatterns = [
    path('', views.exit_survey, name="exit-survey"),
    path('survey-student-list/<str:pk>/', views.survey_student_list, name="survey-student-list"),
    path('form/<str:pk>/', views.exit_survey_form, name="exit-survey-form"),
    
]
