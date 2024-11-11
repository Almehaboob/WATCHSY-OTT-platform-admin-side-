from django.urls import path
from apiside import views

urlpatterns = [
    path('api_signup/', views.signup, name='signup'),
    path('api_login/', views.login, name='login'), 
    path('logout/', views.logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
    
    path('api_movies/', views.movie_list, name='movie_list'),  
    path('api_movies/<int:id>/', views.movie_details, name='movie_detail'),
    
    
    
    path('api_plans/', views.plan_list, name='plan_list'),
    path('api_plans/<int:id>/',views.plan_details,name='plandetails'),
    
    path('create-subscription/', views.create_subscription, name='create_subscription'),
    path('subscriptions/<int:user_id>/',views.subscription_history, name='subscription-history'),
    path('rate/', views.create_rating, name='create-rating'),
    
    path('watchlater/', views.watchlater_list, name='watchlater-list'),
    path('watchlater/<int:user_id>/', views.get_watch_later, name='get-watch-later'),
    path('watchlater/delete/<int:movie_id>/', views.delete_watch_later, name='delete-watch-later'),

    path('watch-history/', views.watchHistory_list, name='watch-history'),
    path('watch-history/<int:user_id>/', views.get_watch_history, name='watch-history'),
]
