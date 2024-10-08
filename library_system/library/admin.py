from django.contrib import admin
from .models import Book, User, Transaction
# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'issue_date', 'return_date')

admin.site.register(Book)
admin.site.register(User)
admin.site.register(Transaction, TransactionAdmin)
