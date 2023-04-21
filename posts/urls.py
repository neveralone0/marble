from django.urls import path
from . import views

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'uploadd', views.MyModelViewSet)

app_name = 'posts'
urlpatterns = [
    path('upload/', views.PostAPI.as_view()),
    path('retrieve/', views.PostResponceAPI.as_view()),
    path('like/<int:id>/', views.PostLike.as_view(), name='like'),
]

urlpatterns += router.urls
