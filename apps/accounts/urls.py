from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView 
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterView, ActivateAccountView, UserProfileView,LogoutView

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<str:uidb64>/<str:token>/', ActivateAccountView.as_view(), name='activate'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
]