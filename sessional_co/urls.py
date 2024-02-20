from django.urls import path
from . import views

urlpatterns = [
    path('', views.sessional_list, name="sessional-list"),
    path('<str:pk>/<str:field>', views.sessional_table_edit, name="sessional-table-edit"),
]
