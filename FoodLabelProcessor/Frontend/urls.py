from django.urls import path
from .views import home, analyze_image, results
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('analyze-image/', analyze_image, name='analyze_image'),
    path('results/', results, name='results'),
]

# Existing urlpatterns list...
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)