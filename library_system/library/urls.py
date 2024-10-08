from tkinter.font import names

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import BookView, UserViews, TransactionView, home, member, librarian, usr_logout


router = DefaultRouter()
router.register(r'users', UserViews)
router.register(r'book', BookView)
router.register(r'transaction', TransactionView)

urlpatterns=[
    path('', include(router.urls)),
    path('home/', home, name='home'),
    path('usr_logout/', usr_logout, name='usr_logout'),
    path('member/', member, name='member'),
    path('librarian/', librarian, name='librarian'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
