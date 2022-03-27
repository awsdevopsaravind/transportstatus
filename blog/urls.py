from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('houselist/', views.houselist, name='house-list'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('register/', views.register1, name='register'),
    path('profile/', views.profile, name='profile'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='blog/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='blog/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='blog/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='blog/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    
    path('gallery/', views.gallery, name='gallery'),
    path('photo/<str:pk>/', views.viewPhoto, name='photo'),
    path('add/', views.addPhoto, name='add'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('vehicle_details/<str:pk_vehicle>/', views.vehicleDetails, name="vehicle_details"),

    path('addtrip/', views.addTripDetails, name='addtrip'),
    path('addvehicle/', views.addVehicleDetails, name='addvehicle'),
    path('updatetrip/<str:pk>', views.updateTripDetails, name='updatetrip'),
    path('deletetrip/<str:pk>', views.deleteTripDetails, name='deletetrip'),
    path('pdfroyaltybillimage/<str:pk_pdf>/', views.pdf_royalty_bill_image_view, name='pdf_royalty_bill_image'),
    path('pdfwaybillimage/<str:pk_pdf>/', views.pdf_way_bill_image_view, name='pdf_way_bill_image'),
    #path('pdfday/<str:pk_day>/', views.pdf_day_view, name='pdf_day'),
    path('pdfall/', views.pdf_alldata_view, name='pdf_all'),

]