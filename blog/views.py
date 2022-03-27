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
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, AddTripDetailsForm, AddVehicleDetailsForm
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


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
        
class PostDetailView(DetailView):
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
        form = AddTripDetailsForm(request.POST)
        #formset = TripDetailsFormSet(request.POST)
        if form.is_valid():
            form.save()
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
            return redirect('/')
    context = {'vehicle_details': vehicle_details, 'trip_details':tripdetails, 'loadtypes':loadtypes
                , 'form':form}
    return render(request, 'blog/add_vehicle_details.html', context)


@login_required(login_url='login')
def Dashboard(request):
    
    user = request.user
    categories = user.category_set.all()
    vehicle_details = VehicleDetails.objects.all().order_by('-id')
    tripdetails = TripDetails.objects.all().order_by('-trip_date')
    totaltrips = TripDetails.objects.all().count()
    #totalqty_in_m3 = sum(tripdetails.values_list('qty_m3', flat=True))
    totalqty_in_m3 = "{:.2f}".format(tripdetails.aggregate(Sum('qty_m3'))['qty_m3__sum'])
    #totalqty_in_ton = "{:.2f}".format(sum(tripdetails.values_list('qty_ton', flat=True)))
    totalqty_in_ton = "{:.2f}".format(tripdetails.aggregate(Sum('qty_ton'))['qty_ton__sum'])

    
    trip_details = TripDetails.objects.all()
    trips_count = trip_details.count()
    distinct_dates_m3 = trip_details.values('trip_date','id').annotate(Sum('qty_m3'))
    context = {'vehicle_details': vehicle_details, 'trip_details':tripdetails,
             'totaltrips': totaltrips,
             'totalqty_in_ton':totalqty_in_ton, 'totalqty_in_m3':totalqty_in_m3
             ,'trips_count':trips_count, 'distinct_dates_m3':distinct_dates_m3
             }
    return render(request, 'blog/trip_details.html', context)

from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

def vehicleDetails(request, pk_vehicle):
    vehicle_details = VehicleDetails.objects.get(id=pk_vehicle)
    trip_details = vehicle_details.tripdetails_set.all()
    trips_count = trip_details.count()
    vehicle_payments = vehicle_details.vehiclepayments_set.all()
    #distinct_dates = vehicle_details.tripdetails_set.all().values('trip_date').distinct()
    distinct_dates = vehicle_details.tripdetails_set.values('trip_date').annotate(Sum('qty_m3'))
    #totalqty_in_m3 = "{:.2f}".format(vehicle_details.tripdetails_set.all().aggregate(Sum('qty_m3'))['qty_m3__sum'])
    totalqty_in_m3 = vehicle_details.tripdetails_set.all().aggregate(Sum('qty_m3'))['qty_m3__sum']
    #myFilter = OrderFilter(request.GET, queryset=orders)
    #orders = myFilter.qs 
    #distinct_dates = vehicle_details.tripdetails_set.values('trip_date').annotate(Sum('qty_m3'))
    
    
    context = {'vehicle_details':vehicle_details, 'trip_details':trip_details, 'trips_count':trips_count,
    'vehicle_payments':vehicle_payments, 'totalqty_in_m3':totalqty_in_m3
    ,'distinct_dates':distinct_dates
    }
    return render(request, 'blog/vehicle_details.html',context)




def updateTripDetails(request, pk):
    trip_detail = TripDetails.objects.get(id=pk)
    form = AddTripDetailsForm(instance=trip_detail)
    if request.method == 'POST':
        form = AddTripDetailsForm(request.POST, instance=trip_detail)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'blog/add_trip_details.html', context)

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

def pdf_alldata_view(request):
    tripdetailsnew = TripDetails.objects.all()
    template_path = 'blog/pdf_all_data.html'
    context = {'trip_details':tripdetailsnew}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #if download
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #only view then download
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

