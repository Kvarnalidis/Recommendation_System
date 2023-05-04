"""RecSys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from Pages.views import home_view
from RecSys import settings
from django.conf.urls.static import static
from account.views import login_view,register_view,logout_view
from FoodChoice.views import food_choice_view
from MuseumChoice.views import museum_choice_view
from SightChoice.views import sight_choice_view
from Resaults.views import resault_view,again_view
urlpatterns = [
	path('',home_view,name='home'),
    path('admin/', admin.site.urls),
    path('account/login/',login_view),
    path('account/register/',register_view),
    path('account/logout/',logout_view),
    path('food/',food_choice_view),
    path('museum/',museum_choice_view),
    path('sight/',sight_choice_view),
    path('resaults/',resault_view),
    path('again/',again_view),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)