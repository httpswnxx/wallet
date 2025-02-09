from django.contrib import admin
from django.urls import path,include
from dj_test.settings import BASE_DIR, MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static


urlpatterns = ([
    path('admin/', admin.site.urls),
    path("",include("apps.urls"))])+static(MEDIA_URL, document_root=MEDIA_ROOT)



