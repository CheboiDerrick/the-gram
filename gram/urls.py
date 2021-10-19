'''
Module that defines application paths
'''
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.home, name='index'),
    path('profile/', views.profile, name='profile'),


     path('search/', views.search_posts, name='search.images'),

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
