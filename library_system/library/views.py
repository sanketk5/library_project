from django.contrib.auth import authenticate, get_user_model, logout
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import action, api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Book, User, Transaction
from .serializers import user_serializer, book_serializer, transaction_serializer, Login_serializer
from .permissions import CheckMember, CheckLibrarian
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny

# Create your views here.

def home(request):
    '''
    Home page
    '''
    return render(request,'index.html')

def usr_logout(request):
    '''
    User logout page
    '''
    logout(request)
    return JsonResponse({"status":"login_sucess"})

def member(request):
    '''
    Redirect to member page
    '''
    return render(request,'member.html')

@action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated,CheckMember])
def librarian(request):
    '''
    Redirect to librarian page
    '''
    print(request.user.is_authenticated)
    context ={}
    if request.user.is_authenticated is False or request.user.role != 'LIBRARIAN':
        context['status']='Error'
    else:
        context['status'] = 'OK'
    return render(request,'librarian.html', context)
class UserViews(viewsets.ModelViewSet):
    '''
    This is for user operation to register new user, login, remove user, update user
    '''
    queryset = User.objects.all()
    serializer_class = user_serializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    @csrf_exempt
    def register(self, request):
        serializer = user_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=request.data['username'],password=request.data['password'], role=request.data['role'], first_name=request.data['first_name'])
            user.save()
            return Response(user_serializer(user).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['post'])
    def login(self,request):
        data = request.data
        serializer = Login_serializer(data=data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(request, username=email, password = password)
            if user is None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            role = user.role
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response(
                {'refresh': str(refresh), 'access': access_token, 'role':role.lower()},
                status=status.HTTP_200_OK
            )

        return Response(status=status.HTTP_400_BAD_REQUEST)

    # @api_view(['PATCH'])
    # @permission_classes([IsAuthenticated]
    @action(detail=False, methods=['PATCH'], permission_classes=[permissions.IsAuthenticated])
    def remove_account(self, request):
        if len(request.data) == 0:
            try:
                user = request.user
                user.is_active = False
                user.save()
                return Response({'message': "Account deleted succesfully."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                user = User.objects.get(id=request.data['user_id'])
                user.is_active = False
                user.save()
                return Response({'message': "Account deleted succesfully."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'], permission_classes=[CheckMember])
    def update_user(self, request):
        user = User.objects.get(id=request.data['user_id'])
        user.first_name = request.data['first_name']
        user.save()
        return Response({'message': "Account updated succesfully."}, status=status.HTTP_200_OK)
class BookView(viewsets.ModelViewSet):
    '''
    This is for add new book, update existing book, remove book
    '''
    queryset = Book.objects.all()
    serializer_class = book_serializer
    permission_classes = [permissions.IsAuthenticated, CheckLibrarian]

    def create_book(self, serializer):
        serializer.save()

    def update_book(self, serializer):
        serializer.save()

    def delete_book(self, instance):
        instance.delete()

class TransactionView(viewsets.ModelViewSet):
    '''
    This is for borrow book, return book, Check history of borrow and return for member and librarian
    '''
    queryset = Transaction.objects.all()
    serializer_class = transaction_serializer
    permission_classes = [permissions.IsAuthenticated, CheckLibrarian]

    @action(detail=False, methods=['post'])
    def borrow_book(self, request):
        book = Book.objects.get(id=request.data['book_id'])
        user = User.objects.get(username=request.user.username)
        if book.status == 'AVAILABLE':
            book.status = 'BORROWED'
            book.save()
            transaction = Transaction.objects.create(user=user, book=book, issue_date=date.today())
            return Response(transaction_serializer(transaction).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def return_book(self, request, pk=None):
        transaction = Transaction.objects.get(id=request.data['transaction_id'])
        if transaction.book.status == 'BORROWED':
            transaction.book.status = 'AVAILABLE'
            transaction.book.save()
            transaction.return_date = date.today()
            transaction.save()
            return Response(transaction_serializer(transaction).data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def history(self,request):
        transactions = Transaction.objects.filter(user=request.user)
        return Response(transaction_serializer(transactions, many=True).data)

    @action(detail=False, methods=['GET'], permission_classes=[CheckLibrarian])
    def all_history(self, request):
        transactions = Transaction.objects.all()
        return Response(transaction_serializer(transactions, many=True).data)


