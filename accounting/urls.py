from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view()),
    path('login/', views.LoginUser.as_view()),
    # path('testi/ ', views.Testi.as_view()),
    path('get-users/', views.GetUsers.as_view()),
    path('token-validation/', views.ValidateToken.as_view()),
    path('user-profile/', views.YourProfile.as_view()),
    path('profile-update/', views.UpdateProfile.as_view()),
]