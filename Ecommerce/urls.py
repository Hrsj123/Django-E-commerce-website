"""Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
# my imports to set media-url to render image via the website
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls'))
]

# using static to add in our MEDIA_URL as a file path
# add it after urlpatterns list only!
# Basically: converts '<list_path>/images.xyz.jpg' to '<list_path>/static/images/xyz.jpg'       <turns it into path format>
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
