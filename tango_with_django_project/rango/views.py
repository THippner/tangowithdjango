from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
from rango.bing_search import run_query


@login_required
def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})


@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    page_list = Page.objects.order_by('-views')[:5]
    context_dict['pages'] = page_list

    # visits counter
    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')

    if last_visit:
        # if last visit exist

        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 5:  # .days > 0:
            # if more than 24h passed
            visits += 1
            reset_last_visit_time = True
    else:
        # no last visit in cookie
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    context_dict['visits'] = visits
    response = render(request, 'rango/index.html', context_dict)

    return response


def about(request):
    visits = request.session.get('visits')
    if not visits:
        visits = 1

    return render(request, 'rango/about.html', {'visits': visits})


def category(request, category_name_slug):

    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['category_name_slug'] = category_name_slug

    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)


@login_required
def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # print new category in terminal
            # print "New Category added: \"" + str(cat) + "\", slug: \"" + str(cat.slug)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})


@login_required
def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':

        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()

                # print newly added page in terminal
                print "New Page added: \"" + str(page.title) + "\", url: \"" + str(page.url)
                print "Under Category: \"" + str(cat) + "\", slug: \"" + str(cat.slug)

                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat, 'category_name_slug': category_name_slug}

    return render(request, 'rango/add_page.html', context_dict)


# def register(request):
#
#     registered = False
#
#     # if request is a http POST
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)
#
#         # if forms are valid
#         if user_form.is_valid() and profile_form.is_valid():
#
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             # was picture supplied
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#
#             profile.save()
#
#             registered = True
#
#         # errors in forms
#         else:
#             print user_form.errors, profile_form.errors
#
#     # not a http POST
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#     # render response
#     return render(request,
#                   'rango/register.html',
#                   {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

#@login_required
# def user_logout(request):
#     logout(request)
#
#     return HttpResponseRedirect('/rango/')


# def user_login(request):
#
#     context_dict = {'login_failed': False, 'user_is_active': True}
#
#     # request is http post
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#
#         # returns user object if combination matches
#         user = authenticate(username=username, password=password)
#
#         # user exists
#         if user:
#             # user is active
#             if user.is_active:
#
#                 login(request, user)
#                 return HttpResponseRedirect('/rango/')
#
#             # account is not active
#             else:
#                 context_dict['user_is_active'] = False
#
#                 return render(request, 'rango/login.html', context_dict)
#
#         # invalid details
#         else:
#             print "Invalid login details: {0}, {1}" .format(username, password)
#             context_dict['login_failed'] = True
#
#             return render(request, 'rango/login.html', context_dict)
#
#     # not http post
#     else:
#         return render(request, 'rango/login.html', context_dict)
























