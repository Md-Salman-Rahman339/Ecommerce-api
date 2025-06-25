
from django.urls import path
from .views import UserRegistrationView,UserLoginView,UserProfileView,UserPasswordChangeView,SendPasswordResetEmailView,UserPasswordResetView
urlpatterns = [
    path('register/', UserRegistrationView.as_view(),name='register'),
    path('login/', UserLoginView.as_view(),name='login'),
    path('profile/', UserProfileView.as_view(),name='profile'),
    path('changepass/', UserPasswordChangeView.as_view(),name='changepass'),
    path('send-email-reset/', SendPasswordResetEmailView.as_view(),name='send-email-reset'),
    path('reset-pass/<uid>/<token>/', UserPasswordResetView.as_view(),name='reset-pass'),

   
]
