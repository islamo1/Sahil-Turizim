from django.urls import path  
from django.contrib.auth.views import LoginView, LogoutView
from .views import hotel_list, add_hotel, add_price, create_tour, select_hotels_and_trips, tour_summary, view_tour_detail, delete_tour, edit_tour,my_tours, user_profile, profile_view, favorite_tours, rate_tour, custom_logout_view
from django.shortcuts import render 
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', LoginView.as_view(template_name='hotels/home.html'), name='login'),
    path('logout/', custom_logout_view, name='logout'),  # سمّيته logout عشان القالب يشتغل علطول
    path('hotels/', hotel_list, name='hotel_list'),
    path('hotels/add/', add_hotel, name='add_hotel'),
    path('prices/add/', add_price, name='add_price'),
    path('tours/create/', create_tour, name='create_tour'), 
    path('create-tour/', create_tour, name='create_tour'),
    path('select-plan/', select_hotels_and_trips, name='select_hotels_and_trips'),
    path('tour/summary/', tour_summary, name='tour_summary'),
    path('tour/saved/', lambda r: render(r, 'hotels/tour_saved.html'), name='tour_saved'),
    path('tour/<int:tour_id>/', view_tour_detail, name='view_tour_detail'),
    path('tour/<int:tour_id>/delete/', delete_tour, name='delete_tour'),
    path('tour/<int:tour_id>/edit/', edit_tour, name='edit_tour'),
    path('my-tours/', my_tours, name='my_tours'),
    path('tour/delete/<int:tour_id>/', delete_tour, name='delete_tour'),
    path('users/<str:username>/', user_profile, name='user_profile'),
    path('profile/<str:username>/', profile_view, name='user_profile'),
    path('tour/<int:tour_id>/rate/', views.rate_tour, name='rate_tour'),
    path('tour/<int:tour_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_tours_view, name='favorites'),
    path('favorites/', favorite_tours, name='favorite_tours'),
    path('tour/<int:tour_id>/rate/', rate_tour, name='rate_tour'),
    path('start-tour/', views.start_tour, name='start_tour'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('activity/<str:username>/', views.user_activity_view, name='user_activity'),
    path('journeys/manage/', views.manage_journeys, name='manage_journeys'),






]


