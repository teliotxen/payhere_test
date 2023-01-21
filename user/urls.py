from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView
from . import views

urlpatterns = [
    # 로그인/회원가입
    path('login/', views.JWTLoginView.as_view()),
    path('signup/', views.JWTSignupView.as_view()),
    path('logout/', views.JWTLogOutView.as_view()),

    # 토큰
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]