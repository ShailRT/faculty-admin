from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('login/' , auth_views.LoginView.as_view(), name='login'),
    path('login/' , views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('register/', views.registration, name='register'),

    path('', views.index, name='dashboard'),
    path('add-subject/', views.add_subject, name='add-subject'),
    path('remove-subject/<str:pk>/', views.remove_subject, name='remove-subject'),
    path('co-po-table/', views.co_po_table, name="co-po-table"),
    path('co-po-table/download-table/<str:pk>/', views.download_table, name="download-table"),
    path('add-co/', views.add_co, name='add-co'),
    path('delete-co/<str:pk>/', views.delete_co, name='delete-co'),

    path('add-po/', views.add_po, name='add-po'),
    path('table-edit-request/', views.table_edit_request, name="table-edit-request")
]