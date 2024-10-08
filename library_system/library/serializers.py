from rest_framework import serializers
from .models import Book, User, Transaction

class user_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class book_serializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class transaction_serializer(serializers.ModelSerializer):
    book = book_serializer()
    user = user_serializer()
    class Meta:
        model = Transaction
        fields = '__all__'

class Login_serializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()