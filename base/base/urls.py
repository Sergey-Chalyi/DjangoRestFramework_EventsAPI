"""
URL configuration for base project.

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
from django.urls import path
from events.views import EventsAPIViews, EventDetailAPIViews, login, logout_view, home
from django.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/events/', EventsAPIViews.as_view()),
    path('api/v1/events/<int:pk>/', EventDetailAPIViews.as_view()),

    path('login/', login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('', home, name='home'),
]
