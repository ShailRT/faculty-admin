from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.session_list, name="session-list"),
    path('session-student-list/<str:pk>/', views.view_student, name="view-student"),
]