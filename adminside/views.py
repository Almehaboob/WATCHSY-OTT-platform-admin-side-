from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import MovieForm,PlanForm
from apiside.models import Movie,Plan,User_table,watch_history_table
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if the user is a staff member (admin)
            if user.is_staff:
                auth_login(request, user)  # Log in the user
                return redirect('movies')  # Redirect to movies page
            else:
                messages.error(request, 'You do not have permission to access this site.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'adminlogin.html')


def admin_logout(request):
    auth_logout(request)
    return redirect('adminlogin') 


@login_required
def toggle_block_user(request, user_id):
    user = get_object_or_404(User_table, id=user_id)
    user.is_blocked = not user.is_blocked
    user.save()
    return JsonResponse({'status': 'success', 'is_blocked': user.is_blocked})


def forgotpass(request):
    return render(request,'admnforgotpass.html')

def updatepass(request):
    return render(request,'adminUpdatepass.html')



@login_required
def movies(request):
    # Get search query from GET parameters
    query = request.GET.get('q', '')
    movie_list = Movie.objects.filter(title__icontains=query) if query else Movie.objects.all()
    
    # Paginate the filtered movie list
    paginator = Paginator(movie_list, 5)  # Show 5 movies per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Check if the request is AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Render only the movie list portion as HTML
        html = render_to_string('partials_movielist.html', {'movies': page_obj})
        return JsonResponse({'html': html})
    
    # For non-AJAX requests, render the entire page
    return render(request, 'movies.html', {'page_obj': page_obj})
@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movies')  # Redirect to the movies page after saving
        else:
            print(form.errors)  # Debug: print form errors in the console
    else:
        form = MovieForm()
    return render(request, 'addmovie.html', {'form': form})

@login_required
def ViewMovie(request, id):
    movie = get_object_or_404(Movie, id=id)  # Fetch the movie by ID or return 404 if not found
    return render(request, 'viewmovie.html', {'movie': movie})

@login_required
def editMovie(request, id):
    movie = get_object_or_404(Movie, id=id)

    if request.method == 'POST':
        # Update movie details based on form data
        movie.title = request.POST.get('title')
        movie.video = request.POST.get('video')
        movie.description = request.POST.get('description')
        
        # Update thumbnail based on the URL provided in the form
        movie.thumbnail = request.POST.get('thumbnail')  # Use POST data for URL, not FILES
        movie.save()
        
        return redirect('viewmovie', id=movie.id)  # Redirect to the movie detail page

    return render(request, 'editmovie.html', {'movie': movie})
@login_required
def deleteMovie(request, id):
    if request.method == "POST":
        movie = get_object_or_404(Movie, id=id)
        movie.delete()
        return redirect('movies')  # Redirect to the movies list page after deletion
    else:
        movie = get_object_or_404(Movie, id=id)
        return render(request, 'deletemovie.html', {'movie': movie})




@login_required
def users(request):
    user_list = User_table.objects.exclude(is_staff=True)
    paginator = Paginator(user_list, 3)  # Show 5 users per page
    page_number = request.GET.get('page')  # Get the current page number from the request
    page_obj = paginator.get_page(page_number)  # Get the users for the current page
    return render(request, 'users.html', {"page_obj": page_obj})
@login_required


def activity(request, user_id):
    # Get the user based on the provided user ID
    user = get_object_or_404(User_table, id=user_id)

    # Get the watch history for the specific user
    watch_history = watch_history_table.objects.filter(user=user).select_related('movie')

    # Render the activity page with the user’s watch history
    return render(request, 'activity.html', {'watch_history': watch_history, 'user': user})





@login_required
def Plans(request):
    plan_list = Plan.objects.all()
    paginator = Paginator(plan_list, 3)  # Show 3 plans per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, 'plans.html', context)
@login_required
def Viewplan(request, id):
    plan = get_object_or_404(Plan, id=id)  # Fetch the movie by ID or return 404 if not found
    return render(request, 'planview.html', {'plan': plan})

@login_required
def add_plan(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)  
        if form.is_valid():
            form.save()
            return redirect('plans')
        else:
            print(form.errors)
    else:
        form = PlanForm()
    
    return render(request, 'addplan.html', {'form': form})



@login_required
def report(request):
    return render(request,'report.html')

@login_required
def revenue(request):
    return render(request,'revenue.html')

@login_required
def viewcount(request):
    return render(request,'totalview.html')

@login_required
def totalsubs(request):
    return render(request,'totalsubs.html')

@login_required
def rating(request):
    return render(request,'rating.html')





