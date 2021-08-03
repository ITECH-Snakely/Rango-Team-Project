from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rango.models import Category, Page, Video, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm, VideoForm
from datetime import datetime
import json

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    context_dict['extra'] = 'From the model solution on GitHub'
    
    visitor_cookie_handler(request)

    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    # Spoiler: now you DO need a context dictionary!
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        videos = Video.objects.filter(category=category) #added

        context_dict['pages'] = pages
        context_dict['videos'] = videos #added
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['videos'] = None
        context_dict['category'] = None
    
    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None
    
    # You cannot add a page to a Category that does not exist... DM
    if category is None:
        return redirect(reverse('rango:index'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)  # This could be better done; for the purposes of TwD, this is fine. DM.
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

@login_required
def add_video(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None
    
    # You cannot add a page to a Category that does not exist... DM
    if category is None:
        return redirect(reverse('rango:index'))

    form = VideoForm()

    if request.method == 'POST':
        form = VideoForm(request.POST)

        if form.is_valid():
            if category:
                video = form.save(commit=False)
                video.category = category
                video.views = 0
                video.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)  # This could be better done; for the purposes of TwD, this is fine. DM.
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_video.html', context=context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'rango/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')

@login_required
def profile(request):
    return render(request, 'rango/profile.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    
    request.session['visits'] = visits

class LikeCategoryView(View):
    def get(self, request):
        category_id = request.GET['category_id']

        try:
            category = Category.objects.get(id=int(category_id))
        except Category.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        
        
        user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
        allCategories = user_profile.cats.all()

        dislikeFlag = 0
        likeFlag = 0
        for cat in allCategories.iterator():
            if cat.name == category.name and cat.likeDislikeDefault == 1:
                likeFlag = 1
                break
            elif cat.name == category.name and cat.likeDislikeDefault == -1:
                dislikeFlag = 1
                break     


        if dislikeFlag: 
            category.dislikes = category.dislikes - 1
            category.save()
            
        if not likeFlag:
            category.likeDislikeDefault = 1
            category.likes = category.likes + 1
            category.save()
            user_profile.cats.add(category)

        data_details = {'likeData' : category.likes, 'dislikeData' : category.dislikes}

        return HttpResponse(json.dumps(data_details)) 

class DislikeCategoryView(View):
    def get(self, request):
        category_id = request.GET['category_id']

        try:
            category = Category.objects.get(id=int(category_id))
        except Category.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        
        user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
        allCategories = user_profile.cats.all()

        dislikeFlag = 0
        likeFlag = 0
        for cat in allCategories.iterator():
            if cat.name == category.name and cat.likeDislikeDefault == -1:
                dislikeFlag = 1
                break
            elif cat.name == category.name and cat.likeDislikeDefault == 1:
                likeFlag = 1
                break

        if likeFlag:
            category.likes = category.likes - 1
            category.save()

        if not dislikeFlag:
            category.likeDislikeDefault = -1
            category.dislikes = category.dislikes + 1
            category.save()
            user_profile.cats.add(category)

        data_details = {'likeData' : category.likes, 'dislikeData' : category.dislikes}

        return HttpResponse(json.dumps(data_details)) 

def profile(request):
    current_user = request.user
    number_user = current_user.id-1
    email_user = current_user.email

    obj = UserProfile.objects.get(id=number_user)
    context = {
    'name': obj.user,
    'id': obj.id,
    'email': obj.email,
    'website': obj.website,
    'picture': obj.picture,
    }

    return render(request, 'rango/profile.html', context= context)


@login_required
def settings(request):
    return render(request, 'rango/settings.html')
