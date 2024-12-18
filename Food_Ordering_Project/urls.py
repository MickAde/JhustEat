"""
URL configuration for Food_Ordering_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Food_Ordering_App.urls')),
]

from Food_Ordering_App import views
from django.conf.urls import handler400, handler403, handler404, handler500


handler400 = views.custom_400_view
handler403 = views.custom_403_view
handler404 = views.custom_404_view
handler500 = views.custom_500_view
# handler503 = views.custom_503_view
