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
    path('home/', PostListView.as_view(), name='blog-home'),
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
    
    path('addtrip/', views.addTripDetails, name='addtrip'),
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('updatetrip/<str:pk>', views.updateTripDetails, name='updatetrip'),
    path('deletetrip/<str:pk>', views.deleteTripDetails, name='deletetrip'),
    path('addvehicle/', views.addVehicleDetails, name='add_vehicle'),
    path('vehicle_details/<str:pk_vehicle>/', views.vehicleDetails, name="vehicle_details"),
    path('updatevehicle/<str:pk>', views.updateVehicleDetails, name='updatevehicle'),
    path('deletevehicle/<str:pk>', views.deleteVehicleDetails, name='deletevehicle'),
    
    path('addowner/', views.addOwnerDetails, name='add_owner'),
    path('owner_details/<str:pk_owner>/', views.ownerDetails, name="owner_details"),

    path('addpayment/', views.addPaymentDetails, name='add_payment'),



    path('pdfroyaltybillimage/<str:pk_pdf>/', views.pdf_royalty_bill_image_view, name='pdf_royalty_bill_image'),
    path('pdfwaybillimage/<str:pk_pdf>/', views.pdf_way_bill_image_view, name='pdf_way_bill_image'),
    #path('pdfday/<str:pk_day>/', views.pdf_day_view, name='pdf_day'),
    path('pdfall/<str:pk_day>/', views.pdf_alldata_view, name='pdf_all'),
    path('pdfday/<str:pk_day>/', views.pdf_day_view, name='pdf_day'),
    path('', views.engineerView, name='engineer_page'),
    path('home/', views.engineerView, name='home_page'),
    

    path('initialadd/', views.layer1TripDetails, name='layer1add'),
    path('getpdfroyaltybillimage/<str:pk_pdf>/', views.get_pdf_royalty_bill_image_view, name='get_pdf_royalty_bill'),
    path('getpdfwaybillimage/<str:pk_pdf>/', views.get_pdf_way_bill_image_view, name='get_pdf_way_bill'),
    path('updatelayer1/<str:pk>', views.updatelayer1TripDetails, name='updatelayer1trip'),
    path('deletelayer1/<str:pk>', views.deletelayer1TripDetails, name='deletelayer1trip'),
    path('layer2add/<str:pk>/', views.layer2TripDetails, name='layer2add'),
    path('layer3add/<str:pk>/', views.layer3TripDetails, name='layer3add'),
    path('layer4add/<str:pk>/', views.layer4TripDetails, name='layer4add'),
    path('ajax/load-vehicles/', views.load_vehicle_numbers, name='ajax_load_vehicle_numbers'),


    path('dashboardnew/', views.dashboard_new, name='dashboard_new'),
    path('reports/', views.reports_all_view, name='reports_all'),
    path('pdfdaytotal/<str:pk_day>/', views.pdf_day_total_view, name='pdf_day_total'),
    path('pdfdayreport/<slug:pk_day>/<slug:pk_load_type/', views.pdf_day_report_view, name='pdf_day_report'),

    
]