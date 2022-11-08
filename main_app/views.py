from curses.ascii import HT
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Art, Profile, PhotoArt, PhotoProfile

import uuid
import boto3

S3_BASE_URL = 'https://s3.amazonaws.com/'
BUCKET = 'compartment-photos'
# Create your views here.

def home(request):
    return render(request, 'home.html')

@login_required
def profile(request):
    profile = Profile.objects.filter(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

def global_art(request):
    art = Art.objects.all()
    return render(request, 'global_art/index.html',
    {'art': art})

def global_art_detail(request, art_id):
    art = Art.objects.get(id=art_id)
    return render(request, 'global_art/detail.html', {'art': art})

@login_required
def art_gallery(request):
    art = Art.objects.filter(user=request.user).order_by('-id')
    return render(request, 'art/index.html',
    {'art': art})

@login_required
def art_detail(request, art_id):
    art = Art.objects.get(id=art_id)
    return render(request, 'art/detail.html', {'art': art})

# ______PHOTO LOGIC________

@login_required
def add_art_photo(request, art_id):
    photo_file = request.FILES.get('art_photo_file', None)
    if photo_file:
        s3 = boto3.client('s3') 
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}" 
            photo = PhotoArt(url=url, art_id=art_id)
            photo.save()
        except Exception as error:
            print("Error uploading photo:", error)
            return redirect('detail', art_id=art_id)
    return redirect('detail', art_id=art_id)
    
@login_required
def add_profile_photo(request, profile_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3') 
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}" 
            photo = PhotoProfile(url=url, profile_id=profile_id)
            photo.save()
        except Exception as error: 
            print("Error uploading photo:", error)
            return redirect('profile', profile_id=profile_id)
    return redirect('profile')



# ______PHOTO LOGIC________

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

# class views
class ArtCreate(LoginRequiredMixin, CreateView):
    model = Art
    fields = ['name', 'date', 'mediums', 'description']
    success_url = '/art_gallery/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    # def get_form(self, form_class):
    #     form = super(ArtCreate, self).get_form(form_class)
    #     form.fields['date_field'].eidget.attrs.update({'class': 'datepicker'})
    #     return form
class ArtUpdate(LoginRequiredMixin, UpdateView):
    model = Art
    fields = ['name', 'date', 'mediums', 'description']
class ArtDelete(LoginRequiredMixin, DeleteView):
    model = Art
    success_url = '/art_gallery/'

class ProfileCreate(LoginRequiredMixin, CreateView):
    model = Profile
    fields = ['artist_name', 'statement', 'about']
    success_url = '/profile/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['artist_name', 'statement', 'about']
    success_url = '/profile/'