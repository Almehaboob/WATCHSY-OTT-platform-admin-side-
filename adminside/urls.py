from django.contrib import admin
from django.urls import path
from adminside import views

urlpatterns = [
    path('', views.login, name='adminlogin'),
    path('adminforgot/', views.forgotpass, name='adminforogotpass'),
    path('adminupdate/', views.updatepass, name='adminupdatepass'),
    path('adminlogout/', views.admin_logout, name='adminlogout'),
    path('movies/', views.movies, name='movies'),
    path('users/', views.users, name='users'),
    path('users/toggle_block/<int:user_id>/', views.toggle_block_user, name='toggle_block_user'),
    path('plans/', views.Plans, name='plans'),
    path('report/', views.report, name='report'),
    path('movies/addmovies/', views.add_movie, name='addmovies'),
    path('movies/view/<int:id>/', views.ViewMovie, name='viewmovie'),  # Added ID parameter
    path('movies/edit/<int:id>/', views.editMovie, name='editmovie'),  # Added ID parameter
    path('movies/delete/<int:id>/', views.deleteMovie, name='deletemovie'),  # Added ID parameter
    path('users/activity/<int:user_id>/', views.activity, name='activity'),
    path('plans/view/<int:id>/', views.Viewplan, name='planview'),
    path('plans/add/', views.add_plan, name='addplan'),
    path('report/revenue', views.revenue, name='revenue'),
    path('report/totalview', views.viewcount, name='viewcount'),
    path('report/totalsubs', views.totalsubs, name='totalsubs'),
    path('report/ratings', views.rating, name='rating'),
]
