from django import forms
from .models import Book  

class IssueBookForm(forms.Form):
    book_id = forms.IntegerField()
    member_id = forms.IntegerField()

class CreateMemberForm(forms.Form):
    name = forms.CharField(max_length=255)

class CreateBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'authors', 'isbn', 'publisher', 'page']

class BookSearchForm(forms.Form):
    title = forms.CharField(required=False, label='Book Title')
    authors = forms.CharField(required=False, label='Author')


class EditBookForm(forms.ModelForm):
    class Meta:
        model = Book  
        fields = ['title', 'authors', 'isbn', 'publisher','page']


#API 

from django import forms

class ImportBooksForm(forms.Form):
    number_of_books = forms.IntegerField(label='Number of Books to Import', min_value=1)
    title = forms.CharField(required=False, label='Title')
    authors = forms.CharField(required=False, label='Authors')
    isbn = forms.CharField(required=False, label='ISBN')
    publisher = forms.CharField(required=False, label='Publisher')
    pages = forms.IntegerField(required=False, label='Pages')



