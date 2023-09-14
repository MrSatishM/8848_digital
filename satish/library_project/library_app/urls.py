from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_book, name='create_book'),
    path('create_member/', views.create_member, name='create_member'),
    path('issue_book/', views.issue_book, name='issue_book'),
    path('return_book/<int:book_id>/', views.return_book, name='return_book'),
    path('member_list/', views.member_list, name='member_list'),
    path('check_outstanding_debt/<int:member_id>/', views.check_outstanding_debt, name='check_outstanding_debt'),
    path('book_list/', views.book_list, name='book_list'),  
    path('transaction_list/', views.transaction_list, name='transaction_list'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('api/import_book/', views.import_book, name='import_book'),
]
