from django.shortcuts import render,redirect,get_object_or_404
from .models import Movie,Theater,Seat,Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from movies.models import Movie
from django.http import HttpResponse
from django.db.models import Count
from django.core.paginator import Paginator
import PIL
def home(request):
    movies=Movie.objects.all()
    #return HttpResponse('Welcome to BookMySeat!')
    return render(request,'movies/home.html',{'movies':movies})

def movie_list(request):
    movies = Movie.objects.all()
    print(request.GET)

    # Search
    search = request.GET.get('search')
    if search:
        movies = movies.filter(name__icontains=search)

    # Genre filter
    genres = request.GET.getlist('genre')
    print("Genres:", genres) 
    if genres:
        movies = movies.filter(genre__in=genres)

    # Language filter
    languages = request.GET.getlist('language')
    print("Languages:", languages) 
    if languages:
        movies = movies.filter(language__in=languages)

    # Sorting
    sort = request.GET.get('sort')
    if sort == "rating":
        movies = movies.order_by('-rating')
    elif sort == "name":
        movies = movies.order_by('name')
    print(movies.query) 
    print("Filtered Movies:")          # <-- ADD
    for movie in movies:
        print(movie.name, movie.genre)

    # Dynamic filter counts
    genre_qs = Movie.objects.all()

    if languages:
        genre_qs = genre_qs.filter(language__in=languages)

    if search:
        genre_qs = genre_qs.filter(name__icontains=search)

    genre_counts = genre_qs.values("genre").annotate(
        total=Count("id")
    )
    # -------- Dynamic Language Counts --------
    language_qs = Movie.objects.all()

    if genres:
        language_qs = language_qs.filter(genre__in=genres)

    if search:
        language_qs = language_qs.filter(name__icontains=search)

    language_counts = language_qs.values("language").annotate(
        total=Count("id")
    )

    # Pagination
    paginator = Paginator(movies, 6)
    page_number = request.GET.get('page')
    movies = paginator.get_page(page_number)

    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'genre_counts': genre_counts,
        'language_counts': language_counts,
    })

def theater_list(request,movie_id):
    movie=get_object_or_404(Movie,id=movie_id)
    theaters=Theater.objects.filter(movie=movie)
    return render(request,'movies/theater_list.html',{'movie':movie,'theaters':theaters})

@login_required(login_url='/login/')
def book_Seats(request,theater_id):
    theaters=get_object_or_404(Theater,id=theater_id)
    seats=Seat.objects.filter(theater=theaters)
    if request.method=='POST':
        selected_Seats=request.POST.getlist('seats')
        error_seats=[]
        if not selected_Seats:
            return render(request,"movies/seat_selection.html",{'theater':theaters,"seats":seats,'error':"No seat selected"})
        for seat_id in selected_Seats:
            seat=get_object_or_404(Seat,id=seat_id,theater=theaters)
            if seat.is_booked:
                error_seats.append(seat.seat_number)
                continue
            try:
                Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theaters.movie,
                    theater=theaters
                )
                seat.is_booked=True
                seat.save()
            except IntegrityError:
                error_seats.append(seat.seat_number)
        if error_seats:
            error_message=f"The following seats are already booked:{','.join(error_seats)}"
            return render(request,'movies/seat_selection.html',{'theater':theaters,"seats":seats,'error':"No seat selected"})
        return redirect('profile')

        
    return render(request,'movies/seat_selection.html',{'theaters':theaters,'seats':seats})



def test_pillow(request):
    return HttpResponse("Pillow Version: " + PIL.__version__)

