from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now  
from django.forms import ValidationError
from django.db.models import Sum  
from .models import Book, Member, Transaction
from .forms import IssueBookForm, CreateMemberForm, CreateBookForm, BookSearchForm, EditBookForm


from django.forms import ValidationError

def issue_book(request):
    if request.method == 'POST':
        form = IssueBookForm(request.POST)
        if form.is_valid():
            book_id = form.cleaned_data['book_id']
            member_id = form.cleaned_data['member_id']

            book = Book.objects.get(pk=book_id)
            member = Member.objects.get(pk=member_id)

            rent_fee = calculate_rent_fee(book)

            if member.outstanding_debt > 500:
                error_message = 'Outstanding debt exceeds Rs. 500. Cannot issue the book.'
                return render(request, 'library_app/issue_book.html', {'form': form, 'error_message': error_message})


            if member.outstanding_debt + rent_fee > 500:
                error_message = 'Issuing this book would exceed the Rs. 500 outstanding debt limit.'
                return render(request, 'library_app/issue_book.html', {'form': form, 'error_message': error_message})

            if book.available:

                transaction = Transaction.objects.create(
                    book=book,
                    member=member,
                    date_issued=now(),  # Save the current date and time
                    rent_fee=rent_fee  # Save the calculated rent fee
                )

                # Update the member's outstanding debt
                member.outstanding_debt += rent_fee
                member.save()

                book.available = False
                book.save()


                return redirect('transaction_list')
            else:
                error_message = 'Book is not available.'
                return render(request, 'library_app/issue_book.html', {'form': form, 'error_message': error_message})

    else:
        form = IssueBookForm()

    return render(request, 'library_app/issue_book.html', {'form': form})





def check_outstanding_debt(request, member_id):
    try:
        member = Member.objects.get(pk=member_id)
        member_debt = Transaction.objects.filter(member=member, returned=False).aggregate(Sum('rent_fee'))['rent_fee__sum'] or 0.0
        
        if member_debt <= 500:
            return render(request, 'library_app/member_detail.html', {'member': member, 'member_debt': member_debt})
        else:
            return render(request, 'library_app/member_detail.html', {'member': member, 'member_debt': member_debt, 'error_message': 'Outstanding debt exceeds Rs. 500'})
    except Member.DoesNotExist:
        return redirect('member_list')




def member_list(request):
    # Retrieve a list of members from the database
    members = Member.objects.all()

    # Render a template to display the list of members
    return render(request, 'library_app/member_list.html', {'members': members})



def create_book(request):
    if request.method == 'POST':
        form = CreateBookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            authors = form.cleaned_data['authors']
            isbn = form.cleaned_data['isbn']
            publisher = form.cleaned_data['publisher']
            page = form.cleaned_data['page']

            # Create a new book instance
            Book.objects.create(title=title, authors=authors, isbn=isbn, publisher=publisher, page=page)

            # Redirect to a success page or a book list page
            return redirect('book_list')

    else:
        form = CreateBookForm()

    # Retrieve a list of books from the database
    books = Book.objects.all()

    return render(request, 'library_app/create_book.html', {'form': form})



def create_member(request):
    if request.method == 'POST':
        form = CreateMemberForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            # Create a new member instance
            Member.objects.create(name=name)

            # Redirect to a success page or a member list page
            return redirect('member_list')

    else:
        form = CreateMemberForm()

    return render(request, 'library_app/create_member.html', {'form': form})



def calculate_rent_fee(book):
   
    return 50




def return_book(request, book_id):
    try:
        transaction = Transaction.objects.get(book_id=book_id, returned=False)
        transaction.returned = True
        transaction.rent_fee = calculate_rent_fee()
        transaction.member.outstanding_debt += transaction.rent_fee
        transaction.save()
        book = transaction.book
        book.available = True
        book.save()

        # Redirect to a success page or a transaction list page
        return redirect('transaction_list')
    except Transaction.DoesNotExist:
        return redirect('transaction_list')



def book_list(request):
    # Retrieve a list of books from the database
    books = Book.objects.all()

    # Render a template to display the list of books
    return render(request, 'library_app/book_list.html', {'books': books})



def book_search(request):
    if request.method == 'POST':
        form = BookSearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            authors = form.cleaned_data.get('authors')
            
            # Query the database for matching books
            books = Book.objects.filter(title__icontains=title, authors__icontains=authors)
            
            return render(request, 'library_app/book_search_results.html', {'books': books})
    else:
        form = BookSearchForm()
    
    return render(request, 'library_app/book_search.html', {'form': form})



def transaction_list(request):
    # Retrieve a list of transactions from the database
    transactions = Transaction.objects.all()

    # Calculate the outstanding debt for each member
    members = Member.objects.all()
    member_debts = {}

    for member in members:
        member_transactions = transactions.filter(member=member, returned=False)
        total_debt = sum(transaction.rent_fee for transaction in member_transactions)
        member_debts[member] = total_debt

    # Render a template to display the list of transactions with outstanding debts
    return render(request, 'library_app/transaction_list.html', {'transactions': transactions, 'member_debts': member_debts})


def edit_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
        form = EditBookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = EditBookForm(instance=book)

    return render(request, 'library_app/edit_book.html', {'form': form})

def delete_book(request, book_id):
    # Get the book object by its ID or return a 404 page if not found
    book = get_object_or_404(Book, pk=book_id)

    if request.method == 'POST':
        # Delete the book
        book.delete()
        return redirect('book_list')  # Redirect to the book list page after deletion

    return render(request, 'library_app/delete_book.html', {'book': book})


#API

from django.http import JsonResponse
import requests
from django.shortcuts import render
from .forms import ImportBooksForm
def import_book(request):

    frappe_api_url = 'http://127.0.0.1:8000/library/api/import_book'

    # Specify the parameters for the API request
    params = {
        'page': 1,  
        'title': 'Harry Potter',  
                }

    try:
        # Send a GET request to the Frappe API
        response = requests.get(frappe_api_url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response from the API
            data = response.json()

            # Process the book data as needed
            books = data.get('message', [])

            # Return a success message
            response_data = {
                'message': 'Books imported successfully',
            }

            return JsonResponse(response_data)

        else:
            # Handle API request failure
            response_data = {
                'error': 'Failed to fetch books from the Frappe API',
            }
            return JsonResponse(response_data, status=500)

    except Exception as e:
        # Handle any exceptions that may occur during the request
        response_data = {
            'error': f'An error occurred: {str(e)}',
        }
        return JsonResponse(response_data, status=500)






