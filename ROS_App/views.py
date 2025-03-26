from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Review, TBR, SkippedBooks
from .forms import ReviewForm, UpdateAccountForm
from django.db import models 
from django.contrib.auth.models import User  
from django.contrib import messages  
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from .models import Category
from django.http import JsonResponse
import os
import csv
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import Http404


@login_required
def home_view(request):
    trending_books = [
        {'title': 'Dracula', 'author': 'Bram Stoker', 'cover': 'dracula.jpg', 'id': 1},
        {'title': 'The Midnight Library', 'author': 'Matt Haig', 'cover': '49Mid.jpg', 'id': 2},
        {'title': 'Lord of the Rings', 'author': 'J.R.R. Tolkien', 'cover': '58LOTR1.jpg', 'id': 3},
        {'title': 'It Ends With Us', 'author': 'Collen Hoover', 'cover':'11EndsUs.jpg','id': 4},
    ]
    categories = ['Fantasy', 'Classics', 'Thriller', 'Romance']

    context = {
        'trending_books': trending_books,
        'categories': categories,
    }
    return render(request, 'ROS_App/home.html', context)


def categories_view(request):
    categories = Category.objects.all()  
    return render(request, 'ROS_App/categories.html', {'categories': categories})

def book_detail(request, book_id):
    books = [
        {'id': 1, 'title': 'Dracula', 'author': 'Bram Stoker', 'cover': 'dracula.jpg'},
        {'id': 2, 'title': 'The Little Prince', 'author': 'Antoine de Saint-Exupéry', 'cover': 'thelittleprince.jpg'},
        {'id': 3, 'title': 'Lord of the Rings', 'author': 'J.R.R. Tolkien', 'cover': 'lordoftherings.jpg'},
        {'id': 4, 'title': 'Twisted lies', 'author': 'Ali Hazelwood', 'cover': '4TwistedLies.jpg', 'description': 'A romance novel.'},
        {'id': 5, 'title': 'Twisted hate', 'author': 'Ali Hazelwood', 'cover': '5TwistedHate.jpg', 'description': 'A romance novel.'},
        {'id': 6, 'title': 'Twisted games', 'author': 'Ali Hazelwood', 'cover': '6TwistedGames.jpg'},
        {'id': 7, 'title': 'Twisted lies', 'author': 'Ali Hazelwood', 'cover': '7TwistedLove.jpg'},
        {'id': 8, 'title': 'Yours Truly', 'author': 'Abby Jimenez', 'cover': '8YoursTruly.jpg'},
        {'id': 9, 'title': 'Red, White & Royal Blue', 'author': 'Casey McQuinston', 'cover': '9RWRB.jpg'},
        {'id': 10, 'title': 'The Hating game', 'author': 'Sally Thorne', 'cover': '10HatingGame.jpg'},
        {'id': 11, 'title': 'It Ends With Us', 'author': 'Colleen Hoover', 'cover': '11EndsUs.jpg'},
        {'id': 12, 'title': 'It Starts With Us', 'author': 'Colleen Hoover', 'cover': '12StartsUs.jpg'},
        {'id': 13, 'title': 'Ugly Love', 'author': 'Colleen Hoover', 'cover': '13UglyLove.jpg'},
        {'id': 14, 'title': 'Wuthering Heights', 'author': 'Emily Bronte', 'cover': '14WutheringHeight.jpg'},
        {'id': 15, 'title': 'Pride and Prejudice', 'author': 'Jane Austen', 'cover': '15Pride.jpg'},
        {'id': 16, 'title': 'Emma', 'author': 'Jane Austen', 'cover': '16Emma.jpg'},
        {'id': 17, 'title': 'Sense and Sensibility', 'author': 'Jane Austen', 'cover': '17Sence.jpg'},
        {'id': 18, 'title': 'Persuasion', 'author': 'Jane Austen', 'cover': '18Per.jpg'},
        {'id': 19, 'title': '1984', 'author': 'George Orwell', 'cover': '19.1984.jpg'},
        {'id': 20, 'title': 'The Hobbit', 'author': 'J.R.R Tolkien', 'cover': '20Hobbit.jpg'},
        {'id': 21, 'title': 'Romeo and Juliet', 'author': 'William Shakespeare', 'cover': '21Romeo.jpg'},
        {'id': 22, 'title': 'Matilda', 'author': 'Roald Dahl', 'cover': '22Matilda.jpg'},
        {'id': 23, 'title': 'The Shining', 'author': 'Stephan King', 'cover': '23Shining.jpg'},
        {'id': 24, 'title': 'Holes', 'author': 'Louis Sachar', 'cover': '24Holes.jpg'},
        {'id': 25, 'title': 'Life of Pi', 'author': 'Yann Martel', 'cover': '25Pi.jpg'},
        {'id': 26, 'title': 'Gone With the Wind', 'author': 'Margaret Mitchell', 'cover': '26Wind.jpg'},
        {'id': 27, 'title': 'The Lorax', 'author': 'Dr. Seuss', 'cover': '27TheLorax.jpg'},
        {'id': 28, 'title': 'War and Peace', 'author': 'Leo Tolstoy', 'cover': '28War.jpg'},
        {'id': 29, 'title': 'A Streetcar Named Desire', 'author': 'Tennessee Williams', 'cover': '29Street.jpg'},
        {'id': 30, 'title': 'The Silence of the Lambs', 'author': 'Thomas Harris', 'cover': '30Lamb.jpg'},
        {'id': 31, 'title': 'Little House on the Prairie', 'author': 'Laura Ingalls Wilder', 'cover': '31LittleHouse.jpg'},
        {'id': 32, 'title': 'Animal Farm', 'author': 'George Orwell', 'cover': '32AnimalFarm.jpg'},
        {'id': 33, 'title': 'Lord of the Flies', 'author': 'Willian Golding', 'cover': '33LordF.jpg'},
        {'id': 34, 'title': 'Famous Last Words', 'author': 'Gillian McAllister', 'cover': '34FLW.jpg'},
        {'id': 35, 'title': 'The Housemaid', 'author': 'Freida McFadden', 'cover': '35House1.jpg'},
        {'id': 36, 'title': 'The Housemaids secret', 'author': 'Freida McFadden', 'cover': '36House2.jpg'},
        {'id': 37, 'title': 'The Housemaid is Watching', 'author': 'Freida McFadden', 'cover': '37House3.jpg'},
        {'id': 38, 'title': 'The Silent Patient', 'author': 'Alex Michaelides', 'cover': '38Silent.jpg'},
        {'id': 39, 'title': 'Gone Girl', 'author': 'Gillian Flynn', 'cover': '39GoneGirl.jpg'},
        {'id': 40, 'title': 'The Da Vinci Code', 'author': 'Dan Brown', 'cover': '40DaVinci.jpg'},
        {'id': 41, 'title': 'The Girl With The Dragon Tattoo', 'author': 'Stieg Larsson', 'cover': '41Dragon.jpg'},
        {'id': 42, 'title': 'Angels & Demons', 'author': 'Dan Brown', 'cover': '42A&D.jpg'},
        {'id': 43, 'title': 'A Good Girls Guide to Murder', 'author': 'Holly Jackson', 'cover': '43Guide.jpg'},
        {'id': 44, 'title': 'The Woman in the Window', 'author': 'A.J Finn', 'cover': '44WomanInWindow.jpg'},
        {'id': 45, 'title': 'The Guest List', 'author': 'Lucy Foley', 'cover': '45GuestList.jpg'},
        {'id': 46, 'title': 'The Girl Who Played With Fire', 'author': 'Stieg Larsso', 'cover': '46Fire.jpg'},
        {'id': 47, 'title': 'Dark Places', 'author': 'Gillian Flynn', 'cover': '47DarkPlaces.jpg'},
        {'id': 48, 'title': 'None Of This Is True', 'author': 'Lisa Jewell', 'cover': '48NoneTrue.jpg'},
        {'id': 49, 'title': 'The Midnight Library', 'author': 'Matt Haig', 'cover': '49Mid.jpg'},
        {'id': 50, 'title': 'The Balled Of Songbirds And Snakes', 'author': 'Suzanne Collins', 'cover': '50balled.jpg'},
        {'id': 51, 'title': 'A Game of Thrones', 'author': 'George R.R. Martin', 'cover': '51GOT2.jpg'},
        {'id': 52, 'title': 'Harry Potter and the Sorcerers Stone', 'author': 'J.K Rowling', 'cover': '52HP1.jpg'},
        {'id': 53, 'title': 'Harry Potter and the Camber of Secrets', 'author': 'J.K Rowling', 'cover': '53HP2.jpg'},
        {'id': 54, 'title': 'Harry Potter and the Prizoner of Azkaban', 'author': 'J.K Rowling', 'cover': '54HP3.jpg'},
        {'id': 55, 'title': 'Harry Potter and the Goblet of fire', 'author': 'J.K Rowling', 'cover': '55HP4.jpg'},
        {'id': 56, 'title': 'Harry Potter and the Order of the Pheonix', 'author': 'J.K Rowling', 'cover': '56HP5.jpg'},
        {'id': 57, 'title': 'Harry Potter and the Half Blood Prince', 'author': 'J.K Rowling', 'cover': '57HP6.jpg'},
        {'id': 58, 'title': 'The Felloeship of the Ring (LOTR1)', 'author': 'J.R.R. Tolkien', 'cover': '58LOTR1.jpg'},
        {'id': 59, 'title': 'The Two Towers (LOTR2)', 'author': 'J.R.R. Tolkien', 'cover': '59LOTR2.jpg'},
        {'id': 60, 'title': 'The Return of the King (LOTR3)', 'author': 'J.R.R. Tolkien', 'cover': '60LOTR3.jpg'},
        {'id': 61, 'title': 'The Lightning Thief', 'author': 'Rick Riordan', 'cover': '61PJ.jpg'},
        {'id': 62, 'title': 'The Lion, the Witch, and the Wardrobe', 'author': 'C.S. Lewis', 'cover': '62Narnia.jpg'},
        {'id': 63, 'title': 'American Gods', 'author': 'Niel Gailmen', 'cover': '63AG.jpg'}
    ]
    
    # Find the book in hardcoded data
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        raise Http404("Book not found")

    # Set default description if missing
    book_description = book.get('description', 'No description available')

    # Get or create a database Book instance for reviews
    db_book, created = Book.objects.get_or_create(
        id=book['id'],
        defaults={
            'title': book['title'],
            'author': book['author'],
            'description': book_description,
            'cover_image': f"books/covers/{book['cover']}"
        }
    )

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = db_book
            review.save()
            return redirect('book_detail', book_id=book_id)
    else:
        form = ReviewForm()

    reviews = Review.objects.filter(book=db_book)
    average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0

    return render(request, 'books/book_detail.html', {
        'book': {**book, 'id': db_book.id, 'description': book_description},
        'reviews': reviews,
        'form': form,
        'average_rating': average_rating
    })

    
def tbr_list(request):
    if request.user.is_authenticated:
        # Fetch all books in the user's TBR list
        tbr_books = TBR.objects.filter(user=request.user)  # Fetch TBR entries for the logged-in user
        books_in_tbr = [entry.book for entry in tbr_books]  # Get the actual Book instances from TBR

        return render(request, 'ROS_App/tbr_list.html', {'books': books_in_tbr})  # Render the TBR list page
    else:
        return redirect('login') 

@login_required
def add_to_tbr(request, book_id):
    # Ensure the request is POST and the user is authenticated
    if request.method == 'POST' and request.user.is_authenticated:
        book = get_object_or_404(Book, id=book_id)

        # Check if the book is already in the TBR list
        if not TBR.objects.filter(user=request.user, book=book).exists():
            # Add the book to the TBR list if it's not already there
            TBR.objects.create(user=request.user, book=book)
            return JsonResponse({'success': True})  # Respond with success
        
        # If the book is already in the TBR list, return failure
        return JsonResponse({'success': False, 'message': 'This book is already in your TBR list.'})

    # If the user is not authenticated, return failure
    return JsonResponse({'success': False, 'message': 'You need to be logged in to add a book to TBR.'})


def delete_from_tbr(request, book_id):
    # Get the book object by its ID
    book = get_object_or_404(Book, id=book_id)
    
    # Check if the user is authenticated before removing the book from TBR
    if request.user.is_authenticated:
        # Get the TBR entry for the logged-in user and the selected book
        tbr_entry = TBR.objects.filter(user=request.user, book=book).first()
        
        if tbr_entry:
            tbr_entry.delete()  # Delete the TBR entry
        
        # Redirect to the user's TBR list after deletion
        return redirect('tbr_list')
    
    # Redirect to the login page if the user is not logged in
    return redirect('login')

def SkippedBooks_list(request):
    if request.user.is_authenticated:
        Skipped_books = SkippedBooks.objects.filter(user=request.user)  
        books_in_Skipped = [entry.book for entry in Skipped_books]  
        return render(request, 'ROS_App/skipped_books_list.html', {'books': books_in_Skipped})  
    else:
        return redirect('login') 
    
@login_required
def add_to_Skipped(request, book_id):
    # Ensure the request is POST and the user is authenticated
    if request.method == 'POST' and request.user.is_authenticated:
        book = get_object_or_404(Book, id=book_id)

        # Check if the book is already in the skipped list
        if not SkippedBooks.objects.filter(user=request.user, book=book).exists():
            # Add the book to the skipped list if it's not already there
            SkippedBooks.objects.create(user=request.user, book=book)
            return JsonResponse({'success': True})  # Respond with success
        
        # If the book is already in the skipped list, return failure
        return JsonResponse({'success': False, 'message': 'This book is already in your skipped list.'})

    # If the user is not authenticated, return failure
    return JsonResponse({'success': False, 'message': 'You need to be logged in to add a book to Skipped books.'})


def delete_from_Skipped(request, book_id):
    # Get the book object by its ID
    book = get_object_or_404(Book, id=book_id)
    
    # Check if the user is authenticated before removing the book from skipped book list
    if request.user.is_authenticated:
        # Get the TBR entry for the logged-in user and the selected book
        skippedBook_entry = SkippedBooks.objects.filter(user=request.user, book=book).first()
        
        if skippedBook_entry:
            skippedBook_entry.delete()  # Delete the skipped book entry
        
        # Redirect to the user's skipped book list after deletion
        return redirect('skipped_book_list')
    
    # Redirect to the login page if the user is not logged in
    return redirect('login')

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Ensure that the logged-in user is the author of the review
    if review.user == request.user:
        review.delete()  # Delete the review

    return redirect('book_detail', book_id=review.book.id)  

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    
    # Ensure that the logged-in user is the author of the review
    if review.user != request.user:
        return redirect('book_detail', book_id=review.book.id)  # Redirect if not the author

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)  # Bind the form to the existing review
        if form.is_valid():
            form.save()  # Save the updated review
            return redirect('book_detail', book_id=review.book.id)  # Redirect to book detail page
    else:
        form = ReviewForm(instance=review)  # Pre-fill the form with existing review data

    return render(request, 'ROS_App/edit_review.html', {'form': form, 'review': review})

def book_review(request, review_id):
    book = get_object_or_404(Book, id=review_id)  # Fetch the book being reviewed
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Assign the logged-in user to the review
            review.book = book  
            review.save()
            return redirect('book_detail', book_id=review.book.id) 
    else:
        form = ReviewForm()

    reviews = Review.objects.filter(book=book).order_by('-created_at')
    return render(request, 'ROS_App/book_review.html', {'form': form, 'reviews': reviews, 'book': book})

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register') 

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        messages.success(request, "Registration successful! Please log in.")
        return redirect('login') 
    return render(request, 'ROS_App/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in successfully.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'ROS_App/login.html') 

def aboutUs_view(request):
    return render(request, 'ROS_App/about_us.html') 

def faq_view(request):
    return render(request, 'ROS_App/faq.html')  

def contactUs_view(request):
    return render(request, 'ROS_App/contact_us.html')

@login_required
def myAccount_view(request):
    return render(request, 'ROS_App/my_account.html')

@login_required
def update_account_view(request):
    if request.method == "POST":
        form = UpdateAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()

          
            old_password = form.cleaned_data.get("old_password")
            new_password1 = form.cleaned_data.get("new_password1")
            if old_password and new_password1:
                user.set_password(new_password1)
                user.save()
                update_session_auth_hash(request, user)  

            messages.success(request, "Your account details have been updated successfully!")
            return redirect("myAccount")  
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UpdateAccountForm(instance=request.user)
    return render(request, "ROS_App/update_account.html", {"form": form})

@login_required
def confirm_delete_account(request):
    """GET request shows confirmation form"""
    return render(request, 'ROS_App/delete_account.html')

@login_required
def delete_account(request):
    """POST request processes deletion after password check"""
    if request.method == 'POST':
        password = request.POST.get('password', '')
        
        if not request.user.check_password(password):
            messages.error(request, "Incorrect password. Account not deleted.")
            return redirect('confirm_delete')
            
        request.user.delete()
        logout(request)
        messages.success(request, "Your account has been permanently deleted.")
        return redirect('home')
    

    return redirect('confirm_delete')


def load_books_from_csv():
    books = {
        'Fantasy': [],
        'Thriller': [],
        'Romance': [],
        'Classics': [],
    }

    csv_file_path = os.path.join(settings.MEDIA_ROOT, 'books.csv')

    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            book_data = {
                'id': row['id'],
                'title': row['title'],
                'author': row['author'],
                'cover': row['cover'],
            }
            category = row['category']
            if category in books:
                books[category].append(book_data)
    
    return books


def fantasy_view(request):
    books = load_books_from_csv() 
    fantasy_books = books.get('Fantasy', []) 
    return render(request, 'ROS_App/fantasy.html', {'fantasy_books': fantasy_books})

def thriller_view(request):
    books = load_books_from_csv()  
    thriller_books = books.get('Thriller', [])  
    return render(request, 'ROS_App/thriller.html', {'thriller_books': thriller_books})


def romance_view(request):
    books = load_books_from_csv() 
    romance_books = books.get('Romance', [])  
    return render(request, 'ROS_App/romance.html', {'romance_books': romance_books})

def classics_view(request):
    books = load_books_from_csv()
    classics_books = books.get('Classics', [])  
    return render(request, 'ROS_App/classics.html', {'classics_books': classics_books})


def logout_view(request):
    logout(request)
    return render(request, 'ROS_App/logout.html')

def user_register(request):
    return render(request, 'ROS_App/register.html')

def user_login(request):
    return render(request, "ROS_App/login.html")

def user_logout(request):
    return render(request, "ROS_App/logout.html")
