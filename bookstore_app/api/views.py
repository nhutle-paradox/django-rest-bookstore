from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .serializers import AuthorSerializer, BookSerializer
from .models import Author, Book
from rest_framework import status
import json

@api_view(['GET'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def welcome(request):
    content = {'message': 'Welcome to the BookStore!'}
    return JsonResponse(content)


@api_view(['GET'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_books(request):
    user_id = request.user.id
    books = Book.objects.filter(added_by=user_id)
    serializer = BookSerializer(books, many=True)
    return JsonResponse({'books': serializer.data}, safe=False, status=status.HTTP_200_OK)


@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_book(request):
    payload = json.loads(request.body)
    user = request.user
    try:
        author = Author.objects.get(id=payload['author'])
        book = Book.objects.create(
            title=payload['title'],
            description=payload['description'],
            added_by=user,
            author=author
        )
        serializer = BookSerializer(book)
        return JsonResponse({'book': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
    except Author.DoesNotExistn:
        return JsonResponse({'error: Author does not exist'}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_book(request, book_id):
    user_id = request.user.id
    payload = json.loads(request.body)
    try:
        book_item = Book.objects.filter(added_by=user_id, id=book_id)
        book_item.update(**payload)
        book = Book.objects.get(id=book_id)
        serializer = BookSerializer(book)
        return JsonResponse({'book': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except Book.DoesNotExist:
        return JsonResponse({'error: Book does not exist'}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@csrf_exempt
@permission_classes([IsAuthenticated])
def delete_book(request, book_id):
    user_id = request.user.id
    try:
        book = Book.objects.get(added_by=user_id, id=book_id)
        book.delete()
        return JsonResponse(status=status.HTTP_204_NO_CONTENT)
    except Book.DoesNotExist:
        return JsonResponse({'error: Book does not exist'}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
