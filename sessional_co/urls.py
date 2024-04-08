from django.urls import path
from . import views

urlpatterns = [
    path('', views.sessional_list, name="sessional-list"),
    path('<str:pk>/<str:field>', views.sessional_table_edit, name="sessional-table-edit"),
    path('test-pdf/<str:pk>/', views.test_pdf, name="test-pdf"),
    path('sessional-table-edit-request', views.sessional_table_edit_request, name="sessional-table-edit-request")
]
