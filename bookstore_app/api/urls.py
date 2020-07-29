from django.urls import path, include
from . import views


urlpatterns = [
    path('welcome', views.welcome, name='welcome'),
    path('get-books', views.get_books, name='get_books'),
    path('add-book', views.add_book, name='add_book'),
    path('update-book/<int:book_id>', views.update_book, name='update_book'),
    path('delete-book/<int:book_id>', views.delete_book, name='delete_book')
]
