
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('exit-survey/', include('exit_survey.urls')),
    path('session/', include('exit_survey.student_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
