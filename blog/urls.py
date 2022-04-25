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
    path('home1/', PostListView.as_view(), name='blog-home'),
    path('houselist/', views.houselist, name='house-list'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('register/', views.register1, name='register'),
    #path('loginnew/', views.loginUser, name='loginnew'),
     
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

    path('addvehiclepayment/', views.addVehiclePaymentDetails, name='add_vehicle_payment'),
    path('addvehiclepayment/<str:amount>', views.payVehiclePaymentDetails, name='pay_vehicle_payment'),
    path('addquarrypayment/', views.addQuarryPaymentDetails, name='add_quarry_payment'),
    path('addcompanypayment/', views.addCompanyPaymentDetails, name='add_company_payment'),
    path('addcompany/', views.addCompanyDetails, name='add_company'),
    path('addmaterial/', views.addLoadtypeDetails, name='add_material'),
    path('addquarry/', views.addQuarryDetails, name='add_quarry'),



    path('pdfroyaltybillimage/<str:pk_pdf>/', views.pdf_royalty_bill_image_view, name='pdf_royalty_bill_image'),
    path('pdfwaybillimage/<str:pk_pdf>/', views.pdf_way_bill_image_view, name='pdf_way_bill_image'),
    #path('pdfday/<str:pk_day>/', views.pdf_day_view, name='pdf_day'),
    path('pdfall/<str:pk_day>/', views.pdf_alldata_view, name='pdf_all'),
    path('pdfday/<str:pk_day>/', views.pdf_day_view, name='pdf_day'),
    path('', views.engineerView, name='engineer_page'),
    path('home/', views.engineerView, name='home_page'),
    path('billsgallery/', views.billsgallery, name='bills_gallery'),
    path('billphoto/<str:pk>/', views.billPhoto, name='gallery_bills_view'),
     

    

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
    path('dailyvehicleownerreport/', views.daily_vehicle_owner_view, name='daily_vehicle_owner_report'),
    path('reports/', views.reports_view, name='reports_all'),
    path('dailygstinvoicereport/', views.daily_gst_invoice_view, name='daily_gst_invoice_report'),
    path('dailymaterialtypereport/', views.daily_material_type_view, name='daily_material_type_report'),
    path('dailymaterialtypereport_old/', views.daily_material_type_view_old, name='daily_material_type_report_old'),
    path('dailyquarryownerreport/', views.daily_quarry_onwer_view, name='daily_quarry_owner_report'),
    path('pdfdaytotal/<str:pk_day>/', views.pdf_day_total_view, name='pdf_day_total'),
    path('pdfdaygst/', views.pdf_day_gst_view, name='pdf_day_gst'),
    path('pdfdayreport/', views.pdf_day_report_view, name='pdf_day_report'),
    
]