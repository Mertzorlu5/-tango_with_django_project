from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from rango.models import Page
from django.shortcuts import render
from rango.models import Category  #chp6
from rango.forms import CategoryForm #chp7
from django.shortcuts import redirect #chp7
from rango.forms import PageForm #chp7
from django.urls import reverse #chp7
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login, logout


def index(request):


    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5. # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.
    category_list = Category.objects.order_by('-likes')[:5]  #chp 5 index function is changed!#top 5 categories :5 means and - means descending order.
    page_list = Page.objects.order_by('-views')[:5] #chp6 exercise
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages']=page_list #chp6 exercise


    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    #render sends it back
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict={}#chp8

    return render(request, 'rango/about.html')
def show_category(request, category_name_slug): #chp6! below this line.
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    try:
    # Can we find a category name slug with the given name?
    # If we can't, the .get() method raises a DoesNotExist exception.
    # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
    # Retrieve all of the associated pages. # The filter() will return a list of page objects or an empty list.
        pages = Page.objects.filter(category=category)
    # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)

@login_required #chp 9
def add_category(request): #chp7
    form = CategoryForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
# Have we been provided with a valid form?
        if form.is_valid(): # Save the new category to the database.
            form.save(commit=True) # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect('/rango/')
        else:
            # The supplied form contained errors
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})


@login_required #chp 9exercise
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
# You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect('/rango/')
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
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)
def register(request): #A boolean value for telling the template 3 # whether the registration was successful. 4 # Set to False initially. Code changes value to 5 # True when registration succeeds.
    registered = False  # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':  # Attempt to grab information from the raw form information. 11 # Note that we make use of both UserForm and UserProfileForm. 12 #
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)  # If the two forms are valid... 16 if user_form.is_valid() and profile_form.is_valid(): 17 # Save the user's form data to the database. 18 user = user_form.save() 19 20 # Now we hash the password with the set_password method. 21 # Once hashed, we can update the user object. 22 user.set_password(user.password) 23 user.save() 24 25 # Now sort out the UserProfile instance. 26 # Since we need to set the user attribute ourselves, 27 # we set commit=False. This delays saving the model
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

    return render(request,'rango/register.html',context = {'user_form': user_form,'profile_form': profile_form,'registered': registered})


def user_login(request): #chp 9
    if request.method == 'POST': # Gather the username and password provided by the user. # This information is obtained from the login form. # We use request.POST.get('<variable>') as opposed # to request.POST['<variable>'], because the # request.POST.get('<variable>') returns None if the # value does not exist, while request.POST['<variable>'] # will raise a KeyError exception.
        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:  # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:  # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:  # No context variables to pass to the template system, hence the # blank dictionary object...
        return render(request, 'rango/login.html')
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')
@login_required
def user_logout(request): # Since we know the user is logged in, we can now just log them out.
    logout(request) # Take the user back to the homepage.
    return redirect(reverse('rango:index'))
