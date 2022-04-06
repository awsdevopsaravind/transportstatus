from multiprocessing import context
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import *

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    PersonForm,
    ReportsForm,
    UserRegisterForm, 
    UserUpdateForm, ProfileUpdateForm, AddTripDetailsForm, 
    AddVehicleDetailsForm, 
    AddOwnerDetailsForm,
    InitialTripDetailsForm,
    Layer2TripDetailsForm,
    VehiclePaymentsForm
)
from django.db.models import Avg, Max, Min, Sum
from django.forms import inlineformset_factory

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def register1(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    u_form = UserUpdateForm()
    p_form = ProfileUpdateForm()
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'blog/profile.html', context)

def houselist(request):
    categories = District.objects.get(name='Vizag')
    housecount = categories.housecount
    range1 = range(1,housecount+1)

    context = {'categories': categories, 'housecountvalue': housecount, 'range1':range1}
    return render(request, 'blog/house_list.html', context)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
        
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

from .models import Category, Photo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from .forms import CustomUserCreationForm
# Create your views here.

'''
def loginUser(request):
    page = 'login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('gallery')

    return render(request, 'photos/login_register.html', {'page': page})


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if user is not None:
                login(request, user)
                return redirect('gallery')

    context = {'form': form, 'page': page}
    return render(request, 'photos/login_register.html', context)
'''

@login_required(login_url='login')
def gallery(request):
    user = request.user
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.filter(category__user=user)
    else:
        photos = Photo.objects.filter(
            category__name=category, category__user=user)

    categories = Category.objects.filter(user=user)
    context = {'categories': categories, 'photos': photos}
    return render(request, 'blog/gallery.html', context)


@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'blog/photo.html', {'photo': photo})


@login_required(login_url='login')
def addPhoto(request):
    user = request.user

    categories = user.category_set.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(
                user=user,
                name=data['category_new'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                description=data['description'],
                image=image,
            )

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'blog/add_status.html', context)

@login_required(login_url='login')
def addTripDetailsnew(request):
    
    user = request.user
    categories = user.category_set.all()
    vehicle_details = VehicleDetails.objects.all()
    tripdetails = TripDetails.objects.all()
    loadtypes = LoadType.objects.all()

    if request.method == 'POST':
        data = request.POST
        royalty_image = request.FILES.getlist('royalty_image')
        waybill_image = request.FILES.getlist('waybill_image')

        if data['load_type'] != 'none':
            loadtype = LoadType.objects.get(id=data['load_type'])
        else:
            loadtype = None
        
        if data['vehicle_number'] != 'none':
            vehicle_number = VehicleDetails.objects.get(id=data['vehicle_number'])
        else:
            vehicle_number = None

        tripdetails = TripDetails.objects.create(
                trip_date = data['trip_date'],
                loadtype = loadtype,
                tf_number = data['tf_number'],
                qty_m3 = data['qty_m3'],
                vehicle_number = vehicle_number,
                qty_ton = data['qty_ton'],
                royalty_image = royalty_image,
                waybill_image = waybill_image,
            )
        messages.success(request, f'Your new trip details has been saved!')
        return redirect('dashboard')

    context = {'vehicle_details': vehicle_details, 'trip_details':tripdetails, 'loadtypes':loadtypes
                }
    return render(request, 'blog/add_trip_details_withformsets.html', context)

@login_required(login_url='login')
def addTripDetails(request):
    
    user = request.user
    vehicle_details = VehicleDetails.objects.all()
    tripdetails = TripDetails.objects.all()
    loadtypes = LoadType.objects.all()
    
    form = AddTripDetailsForm()
    #TripDetailsFormSet = inlineformset_factory(LoadType, TripDetails, form=AddTripDetailsForm,extra=5)
    #formsets = TripDetailsFormSet()
    # form = OrderForm(initial={'customer':customer})
    '''def home(request):
    currentdate = datetime.date.today()
    formatDate = currentdate.strftime("%a")'''
    if request.method == 'POST':
        form = AddTripDetailsForm(request.POST, request.FILES)
        #formset = TripDetailsFormSet(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your new trip details has been saved!')
            return redirect('/')
    context = {'vehicle_details': vehicle_details, 'trip_details':tripdetails, 'loadtypes':loadtypes
                , 'form':form}
    return render(request, 'blog/add_trip_details.html', context)

@login_required(login_url='login')
def addVehicleDetails(request):
    
    user = request.user
    vehicle_details = VehicleDetails.objects.all()
    tripdetails = TripDetails.objects.all()
    loadtypes = LoadType.objects.all()
    
    form = AddVehicleDetailsForm()
    if request.method == 'POST':
        form = AddVehicleDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your new vehicle details has been saved!')
            return redirect('/')
    context = {'vehicle_details': vehicle_details, 'trip_details':tripdetails, 'loadtypes':loadtypes
                , 'form':form}
    return render(request, 'blog/add_vehicle_details.html', context)

@login_required(login_url='login')
def updateVehicleDetails(request, pk):
    vehicle_detail = VehicleDetails.objects.get(id=pk)
    form = AddVehicleDetailsForm(instance=vehicle_detail)
    if request.method == 'POST':
        form = AddVehicleDetailsForm(request.POST, instance=vehicle_detail)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your vehicle details has been updated!')
            return redirect('/')
    context = {'form':form, 'vehicle_detail':vehicle_detail}
    return render(request, 'blog/add_vehicle_details.html', context)

@login_required(login_url='login')
def deleteVehicleDetails(request, pk):
	delete_vehicle_detail = VehicleDetails.objects.get(id=pk)
	if request.method == "POST":
		delete_vehicle_detail.delete()
		return redirect('/')

	context = {'delete_vehicle_detail':delete_vehicle_detail}
	return render(request, 'blog/delete_vehicle_details.html', context)

@login_required(login_url='login')
def Dashboard(request):
    
    user = request.user
    categories = user.category_set.all()
    vehicle_details = VehicleDetails.objects.all().order_by('-id')
    tripdetails = TripDetails.objects.all().order_by('-trip_date')
    totalqty_in_m3 = "{:.2f}".format(tripdetails.aggregate(Sum('qty_m3'))['qty_m3__sum'])
    totalqty_in_ton = "{:.2f}".format(tripdetails.aggregate(Sum('qty_ton'))['qty_ton__sum'])

    ownernames = TransporterDetails.objects.all().order_by('vehicle_owner_name')
    trip_details = TripDetails.objects.all()
    totaltrips = trip_details.count()
    distinct_dates = trip_details.values('trip_date').annotate(Sum('qty_m3'), Sum('qty_ton'))
    context = {'vehicle_details': vehicle_details, 'trip_details':tripdetails,
             'totaltrips': totaltrips, 'totalqty_in_ton':totalqty_in_ton, 'totalqty_in_m3':totalqty_in_m3
             , 'distinct_dates':distinct_dates
             ,'ownernames':ownernames
             }
    return render(request, 'blog/trip_details.html', context)

from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@login_required(login_url='login')
def vehicleDetails(request, pk_vehicle):
    vehicle_details = VehicleDetails.objects.get(id=pk_vehicle)
    trip_details = vehicle_details.tripdetails_set.all()
    trips_count = trip_details.count()
    vehicle_payments = vehicle_details.vehiclepayments_set.all()
    #distinct_dates = vehicle_details.tripdetails_set.all().values('trip_date').distinct()
    distinct_dates = vehicle_details.tripdetails_set.values('trip_date').annotate(Sum('qty_m3'))
    distinct_dates_ton = vehicle_details.tripdetails_set.values('trip_date').annotate(Sum('qty_ton'))
    new1 = distinct_dates.union(distinct_dates_ton)
    #totalqty_in_m3 = "{:.2f}".format(vehicle_details.tripdetails_set.all().aggregate(Sum('qty_m3'))['qty_m3__sum'])
    totalqty_in_m3 = vehicle_details.tripdetails_set.all().aggregate(Sum('qty_m3'))['qty_m3__sum']
    #myFilter = OrderFilter(request.GET, queryset=orders)
    #orders = myFilter.qs 
    #distinct_dates = vehicle_details.tripdetails_set.values('trip_date').annotate(Sum('qty_m3'))
    
    
    context = {'vehicle_details':vehicle_details, 'trip_details':trip_details, 'trips_count':trips_count,
    'vehicle_payments':vehicle_payments, 'totalqty_in_m3':totalqty_in_m3
    ,'distinct_dates':distinct_dates, 'distinct_dates_ton':distinct_dates_ton
    ,'new1':new1
    }
    return render(request, 'blog/vehicle_details.html',context)

@login_required(login_url='login')
def ownerDetails(request, pk_owner):
    owner_details = TransporterDetails.objects.get(id=pk_owner)
    vehicle_details = owner_details.vehicledetails_set.all()
    vehicles_count = vehicle_details.count()
    print(vehicles_count)
    if vehicles_count>0:
        for idx, vehicle_detail in enumerate(vehicle_details):
            if idx == 0:
                trip_details_union= vehicle_detail.tripdetails_set.all()
                trip_details_unions = trip_details_union
            elif idx>=0:
                trip_details = vehicle_detail.tripdetails_set.all()
                trip_details_union =trip_details_union.union(trip_details)
                trip_details_unions = trip_details_union
            trip_details_all = trip_details_unions.order_by('-trip_date') 
        trips_count = trip_details_all.count()   
    else:
        trip_details_all=[]
        trips_count=0
    
    #vehicle_payments = vehicle_details.vehiclepayments_set.all()
    #distinct_dates = vehicle_details.tripdetails_set.all().values('trip_date').distinct()
    #distinct_dates = vehicle_details.tripdetails_set.values('trip_date').annotate(Sum('qty_m3'))
    #distinct_dates_ton = vehicle_details.tripdetails_set.values('trip_date').annotate(Sum('qty_ton'))
    #new1 = distinct_dates.union(distinct_dates_ton)
    #totalqty_in_m3 = "{:.2f}".format(vehicle_details.tripdetails_set.all().aggregate(Sum('qty_m3'))['qty_m3__sum'])
    #totalqty_in_m3 = vehicle_details.tripdetails_set.all().aggregate(Sum('qty_m3'))['qty_m3__sum']
    
    context = {
        'owner_details': owner_details, 'vehicle_details':vehicle_details, 'vehicles_count':vehicles_count
        , 'trip_details_all':trip_details_all, 'trips_count':trips_count 

    }
    return render(request, 'blog/owner_details.html',context)

@login_required(login_url='login')
def addOwnerDetails(request):
    
    user = request.user
    form = AddOwnerDetailsForm()
    if request.method == 'POST':
        form = AddOwnerDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your new owner details has been saved!')
            return redirect('/')
    context = {'form':form}
    return render(request, 'blog/add_owner_details.html', context)

@login_required(login_url='login')
def addPaymentDetails(request):
    user = request.user
    form = VehiclePaymentsForm()
    if request.method == 'POST':
        form = VehiclePaymentsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your new Payment details has been saved!')
            return redirect('/')
    context = {'form':form}
    return render(request, 'blog/add_payment_details.html', context)

@login_required(login_url='login')
def updateTripDetails(request, pk):
    trip_detail = TripDetails.objects.get(id=pk)
    form = AddTripDetailsForm(instance=trip_detail)
    if request.method == 'POST':
        form = AddTripDetailsForm(request.POST, instance=trip_detail)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your trip details has been updated!')
            return redirect('/')
    context = {'form':form}
    return render(request, 'blog/add_trip_details.html', context)

@login_required(login_url='login')
def deleteTripDetails(request, pk):
	delete_trip_detail = TripDetails.objects.get(id=pk)
	if request.method == "POST":
		delete_trip_detail.delete()
		return redirect('/')

	context = {'delete_trip_detail':delete_trip_detail}
	return render(request, 'blog/delete_details.html', context)



from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

@login_required(login_url='login')
def pdf_royalty_bill_image_view(request, pk_pdf):
    tripdetailsnew = get_object_or_404(TripDetails, pk=pk_pdf)
    template_path = 'blog/pdf_royalty_bill_image.html'
    context = {'trip_detail':tripdetailsnew}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #if download
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #only view then download
    print(tripdetailsnew)
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html.encode("UTF-8"), dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required(login_url='login')
def pdf_way_bill_image_view(request, pk_pdf):
    tripdetailsnew = get_object_or_404(TripDetails, pk=pk_pdf)
    template_path = 'blog/pdf_way_bill_image.html'
    context = {'trip_detail':tripdetailsnew}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #if download
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #only view then download
    print(tripdetailsnew)
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required(login_url='login')
def pdf_alldata_view(request, pk_day):
    tripdetailsnew = TripDetails.objects.filter(trip_date=pk_day)
    distinct_dates = tripdetailsnew.values('trip_date','load_type').annotate(Sum('qty_m3'), Sum('qty_ton'))
    loadtyperate = LoadType.objects.all()

    template_path = 'blog/pdf_all_data.html'
    context = {'trip_details':tripdetailsnew ,'distinct_dates':distinct_dates
    , 'loadtyperate':loadtyperate
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

from datetime import datetime
@login_required(login_url='login')
def pdf_day_view(request, pk_day):
    tripdetailsnew = TripDetails.objects.filter(trip_date=pk_day)
    distinct_dates = tripdetailsnew.values('trip_date','load_type').annotate(Sum('qty_m3'), Sum('qty_ton'))
    trip_details_count = tripdetailsnew.count()
    g1 = 0
    g=0
    for a in tripdetailsnew:

        d = a.load_type.load_type_rate_per_tonne * a.qty_ton
        f = d+g1
        g += f
    totalamount = g
    template_path = 'blog/pdf_day_data.html'
    context = {'trip_details':tripdetailsnew ,'distinct_dates':distinct_dates
    ,'pk_day':pk_day, 'totalamount':totalamount
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
@login_required(login_url='login')
def engineerView(request):
    layer1details = LayerWiseTripDetails.objects.filter(Q(verifiedbyengineer='No')).order_by('-id')
    layer1detailscount = layer1details.count()
    if layer1detailscount >0:
        layer1totalqty_in_m3 = "{:.2f}".format(layer1details.aggregate(Sum('qty_m3'))['qty_m3__sum'])
    else:
        layer1totalqty_in_m3 = 0
    paginator = Paginator(layer1details, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    #layer2tripdetails = LayerWiseTripDetails.objects.filter((Q(sendtomalli=1) & Q(verifiedbymalli=0)) | (Q(verifiedbysuresh=2) & Q(verifiedbymalli=1)))
    layer2tripdetails = LayerWiseTripDetails.objects.filter((Q(verifiedbymalli='No') & Q(verifiedbyengineer='Yes'))).order_by('-id')
    layer2tripdetailscount = layer2tripdetails.count()
    if layer2tripdetailscount >0:
        layer2totalqty_in_m3 = "{:.2f}".format(layer2tripdetails.aggregate(Sum('qty_m3'))['qty_m3__sum'])
        layer2totalqty_in_ton = "{:.2f}".format(layer2tripdetails.aggregate(Sum('qty_ton'))['qty_ton__sum'])
        layer2pending_m3 = "{:.2f}".format(float(layer2totalqty_in_m3) - (float(layer2totalqty_in_ton)/1.5))
    else:
        layer2totalqty_in_m3 = 0
        layer2totalqty_in_ton = 0
        layer2pending_m3 = 0
    layer2paginator = Paginator(layer2tripdetails, 3)
    page = request.GET.get('page')
    try:
        layer2posts = layer2paginator.page(page)
    except PageNotAnInteger:
        layer2posts = layer2paginator.page(1)
    except EmptyPage:
        layer2posts = layer2paginator.page(layer2paginator.num_pages)

    #layer3tripdetails = LayerWiseTripDetails.objects.filter(Q(verifiedbymalli=1) & Q(verifiedbysuresh=0))
    layer3tripdetails = LayerWiseTripDetails.objects.filter(Q(verifiedbysuresh='No') & Q(verifiedbymalli='Yes') ).order_by('-id')
    layer3tripdetailscount = layer3tripdetails.count()
    if layer3tripdetailscount >0:
        layer3totalqty_in_m3 = "{:.2f}".format(layer3tripdetails.aggregate(Sum('qty_m3'))['qty_m3__sum'])
        layer3totalqty_in_ton = "{:.2f}".format(layer3tripdetails.aggregate(Sum('qty_ton'))['qty_ton__sum'])
        layer3pending_m3 = "{:.2f}".format(float(layer3totalqty_in_m3)-(float(layer3totalqty_in_ton)/1.5))
    else:
        layer3totalqty_in_m3 = 0
        layer3totalqty_in_ton = 0
        layer3pending_m3 = 0
    layer3paginator = Paginator(layer3tripdetails, 3)
    page = request.GET.get('page')
    try:
        layer3posts = layer3paginator.page(page)
    except PageNotAnInteger:
        layer3posts = layer3paginator.page(1)
    except EmptyPage:
        layer3posts = layer3paginator.page(layer3paginator.num_pages)

    layer4tripdetails = LayerWiseTripDetails.objects.filter(Q(verifiedbymalli='Yes') & Q(verifiedbysuresh='Yes') ).order_by('-id')[:2]
    layer4tripdetailscount = layer4tripdetails.count()
    if layer4tripdetailscount >0:
        layer4totalqty_in_m3 = "{:.2f}".format(layer4tripdetails.aggregate(Sum('qty_m3'))['qty_m3__sum'])
        layer4totalqty_in_ton = "{:.2f}".format(layer4tripdetails.aggregate(Sum('qty_ton'))['qty_ton__sum'])
        layer4pending_m3 = "{:.2f}".format(float(layer4totalqty_in_m3)-(float(layer4totalqty_in_ton)/1.5))
    else:
        layer4totalqty_in_m3 = 0
        layer4totalqty_in_ton = 0
        layer4pending_m3 = 0
    layer4paginator = Paginator(layer4tripdetails, 3)
    page = request.GET.get('page')
    try:
        layer4posts = layer4paginator.page(page)
    except PageNotAnInteger:
        layer4posts = layer4paginator.page(1)
    except EmptyPage:
        layer4posts = layer4paginator.page(layer4paginator.num_pages)
    
    trip_details = LayerWiseTripDetails.objects.all()
    distinct_dates = trip_details.values('trip_date','load_type').annotate(Sum('qty_m3'), Sum('qty_ton'))

    context = { 'page':page, 'posts':posts, 'initialdetails':layer1details, 'layer1detailscount':layer1detailscount,'layer1totalqty_in_m3':layer1totalqty_in_m3
                ,'layer2posts':layer2posts,'layer2tripdetailscount':layer2tripdetailscount, 'layer2tripdetails':layer2tripdetails, 'layer2totalqty_in_m3':layer2totalqty_in_m3, 'layer2totalqty_in_ton':layer2totalqty_in_ton, 'layer2pending_m3':layer2pending_m3
                ,'layer3posts':layer3posts,'layer3tripdetailscount':layer3tripdetailscount, 'layer3tripdetails':layer3tripdetails, 'layer3totalqty_in_m3':layer3totalqty_in_m3, 'layer3totalqty_in_ton':layer3totalqty_in_ton, 'layer3pending_m3':layer3pending_m3
                ,'layer4posts':layer4posts,'layer4tripdetailscount':layer4tripdetailscount, 'layer4tripdetails':layer4tripdetails, 'layer4totalqty_in_m3':layer4totalqty_in_m3, 'layer4totalqty_in_ton':layer4totalqty_in_ton, 'layer4pending_m3':layer4pending_m3
                , 'distinct_dates': distinct_dates
                }
    return render(request, 'blog/engineer_page.html', context)

@login_required(login_url='login')
def layer1TripDetails(request):
    form = Layerwise1TripDetailsForm()
    if request.method == 'POST':
        form = Layerwise1TripDetailsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your new initial trip details has been saved!')
            return redirect('/')
    context = {'form':form}
    return render(request, 'blog/initial_add_trip_details.html', context)

@login_required(login_url='login')
def updatelayer1TripDetails(request, pk):
    trip_detail = LayerWiseTripDetails.objects.get(id=pk)
    form = Layerwise1TripDetailsForm(instance=trip_detail)
    if request.method == 'POST':
        form = Layerwise1TripDetailsForm(request.POST,  instance=trip_detail)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your trip details has been updated!')
            return redirect('/')
    context = {'form':form}
    return render(request, 'blog/initial_add_trip_details.html', context)

@login_required(login_url='login')
def deletelayer1TripDetails(request, pk):
	delete_trip_detail = LayerWiseTripDetails.objects.get(id=pk)
	if request.method == "POST":
		delete_trip_detail.delete()
		return redirect('/')

	context = {'delete_trip_detail':delete_trip_detail}
	return render(request, 'blog/delete_layer_trip_details.html', context)


from .forms import Layerwise2TripDetailsForm
@login_required(login_url='login')
def layer2TripDetails(request, pk):
    layer1trip_detail = LayerWiseTripDetails.objects.get(id=pk)
    form = Layerwise2TripDetailsForm(instance=layer1trip_detail)
    if request.method == 'POST':
        form = Layerwise2TripDetailsForm(request.POST, request.FILES, instance=layer1trip_detail)
        if form.is_valid():
            if form.cleaned_data['qty_ton'] >= (form.cleaned_data['qty_m3'] * 1.5 ):
                form.save()
                messages.success(request, f'Your trip details has been updated!')
                return redirect('/')
            else:
                messages.warning(request, f'Please Enter quantity higher than zero !')
            
    context = {'form':form}
    return render(request, 'blog/layer2_add_trip_details.html', context)

from .forms import Layerwise3TripDetailsForm
@login_required(login_url='login')
def layer3TripDetails(request, pk):
    layer3trip_detail = LayerWiseTripDetails.objects.get(id=pk)
    form = Layerwise3TripDetailsForm(instance=layer3trip_detail)
    if request.method == 'POST':
        form = Layerwise3TripDetailsForm(request.POST, request.FILES, instance=layer3trip_detail)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your trip details has been updated!')
            return redirect('/')
    context = {'form':form}
    return render(request, 'blog/layer3_add_trip_details.html', context)

from .forms import Layerwise4TripDetailsForm
@login_required(login_url='login')
def layer4TripDetails(request, pk):
    layer4trip_detail = LayerWiseTripDetails.objects.get(id=pk)
    form = Layerwise4TripDetailsForm(instance=layer4trip_detail)
    if request.method == 'POST':
        form = Layerwise4TripDetailsForm(request.POST, request.FILES, instance=layer4trip_detail)
        if form.is_valid():
            form.save()
            messages.success(request, f'Trip details has been verified successfully!')
            return redirect('/')
    context = {'form':form}
    return render(request, 'blog/layer4_add_trip_details.html', context)

from .forms import Layerwise1TripDetailsForm
@login_required(login_url='login')
def get_pdf_royalty_bill_image_view(request, pk_pdf):
    tripdetailsnew = get_object_or_404(LayerWiseTripDetails, pk=pk_pdf)
    template_path = 'blog/get_pdf_royalty_bill.html'
    context = {'trip_detail':tripdetailsnew}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
       html.encode("UTF-8"), dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required(login_url='login')
def get_pdf_way_bill_image_view(request, pk_pdf):
    tripdetailsnew = get_object_or_404(LayerWiseTripDetails, pk=pk_pdf)
    template_path = 'blog/get_pdf_way_bill.html'
    context = {'trip_detail':tripdetailsnew}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
       html.encode("UTF-8"), dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required(login_url='login')
def dashboard_new(request):
    user = request.user
    categories = user.category_set.all()
    vehicle_details = VehicleDetails.objects.all().order_by('-id')
    trip_details = LayerWiseTripDetails.objects.all().order_by('-trip_date')
    totaltrips = trip_details.count()
    if totaltrips >0:
        totalqty_in_m3 = "{:.2f}".format(trip_details.aggregate(Sum('qty_m3'))['qty_m3__sum'])
        totalqty_in_ton = "{:.2f}".format(trip_details.aggregate(Sum('qty_ton'))['qty_ton__sum'])
        totalpending_m3 = "{:.2f}".format(float(totalqty_in_m3)-(float(totalqty_in_ton)/1.5))
    else:
        totalqty_in_m3 = 0
        totalqty_in_ton = 0
        totalpending_m3 = 0
    

    ownernames = TransporterDetails.objects.all().order_by('vehicle_owner_name')
    distinct_dates = trip_details.values('trip_date','load_type').annotate(Sum('qty_m3'), Sum('qty_ton'))
    for i in distinct_dates:
        print(i)
        for key in i:
            print(key)
            print(i[key])
            j = i[key]
            print(i[key])
    
    context = {'vehicle_details': vehicle_details, 'trip_details':trip_details,
             'totaltrips': totaltrips, 'totalqty_in_ton':totalqty_in_ton, 'totalqty_in_m3':totalqty_in_m3,'totalpending_m3':totalpending_m3
             , 'distinct_dates':distinct_dates
             ,'ownernames':ownernames
             }
    return render(request, 'blog/dashboard_details.html', context)


from datetime import datetime
@login_required(login_url='login')
def pdf_day_total_view(request, pk_day):
    tripdetailsnew = LayerWiseTripDetails.objects.filter(trip_date=pk_day)
    distinct_dates = tripdetailsnew.values('trip_date','load_type').annotate(Sum('qty_m3'), Sum('qty_ton'))
    trip_details_count = tripdetailsnew.count()
    g1 = 0
    g=0
    for a in tripdetailsnew:

        d = a.load_type.load_type_rate_per_tonne * a.qty_ton
        f = d+g1
        g += f
    totalamount = g
    template_path = 'blog/pdf_day_data.html'
    context = {'trip_details':tripdetailsnew ,'distinct_dates':distinct_dates
    ,'pk_day':pk_day, 'totalamount':totalamount
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def pdf_day_report_view(request,pk_day, pk_load_type):
    a = request.GET.get('description')
    print(a)
    selected_Material=request.GET.get('selected_material')
    print(selected_Material)
    print(pk_load_type)
    print(pk_day)
    selected_Date=request.GET.get('selected_date')
    print(selected_Date)
    trip_details = LayerWiseTripDetails.objects.filter(Q(trip_date=selected_Date) & Q(load_type=selected_Material))
    print(trip_details)
    if selected_Material == 'None' or selected_Date == "None":
        messages.warning(request, f'Please Enter quantity higher than zero !')
    else:
        distinct_dates = trip_details.values('trip_date','load_type').annotate(Sum('qty_m3'), Sum('qty_ton'))
        trip_details_count = trip_details.count()
        g1 = 0
        g=0
        for a in trip_details:

            d = a.load_type.load_type_rate_per_tonne * a.qty_ton
            f = d+g1
            g += f
            print(g)
        totalamount = g
        template_path = 'blog/pdf_day_data.html'
        context = {'trip_details':trip_details ,'distinct_dates':distinct_dates
        ,'pk_day':selected_Date, 'totalamount':totalamount
        }
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="report.pdf"'
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
        html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

def reports_all_view(request):
    form = ReportsForm()
    #distinct_dates1 = LayerWiseTripDetails.objects.all().order_by('datevalue')
    trip_details = LayerWiseTripDetails.objects.all()
    distinct_load_types = trip_details.values('load_type').annotate(Sum('qty_m3'))
    distinct_dates = trip_details.values('trip_date').annotate(Sum('qty_m3'))
    context = { 'trip_details':trip_details
                ,'distinct_load_types':distinct_load_types, 'distinct_dates':distinct_dates
                ,'form':form}
    return render(request, 'blog/reports.html', context)

def load_vehicle_numbers(request):
    owner_id = request.GET.get('country_Id')
    vehicle_numbers = VehicleDetails.objects.filter(owner_name_id=owner_id).order_by('id')
    return render(request, 'blog/vehicle_dropdown_list_options.html', {'vehicle_numbers': vehicle_numbers})

