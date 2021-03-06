from django.urls import path, include
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('category/<slug:category_name_slug>/add_video/', views.add_video, name='add_video'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('like_category/', views.LikeCategoryView.as_view(), name='like_category'),
    path('dislike_category/', views.DislikeCategoryView.as_view(), name='dislike_category'),
    path('generate_quote/', views.GenerateQuoteView.as_view(), name='generate_quote/'),
    path('profile/', views.profile, name='profile'),
    path('profile/settings/', views.settings, name='settings'),
    #path('accounts/', include('allauth.urls')),
    ]