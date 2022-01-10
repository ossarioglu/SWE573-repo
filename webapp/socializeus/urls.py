"""socializeUs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# URLs from landing is also added to patterns
# Admin url is triggered from this file
# All other URLs are retrieved from urls.py at landing

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls')),

]

# For pictures at Offering and Profile picture is address Media Urls below
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)