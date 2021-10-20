'''
Module that defines application paths
'''
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('upload/add/', views.new_post, name='save.image'),


    path('profile/update/', views.update_profile, name='update.profile'),
    path('like/<int:id>/', views.like_image, name='like.image'),
    path('picture/<int:id>/', views.view_post, name='single.image'),
    path('comment/add', views.add_comment, name='comment.add'),

    path('user/<int:id>/', views.user_profile, name='user.profile'),
    path('search/', views.search_posts, name='search.images'),

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
