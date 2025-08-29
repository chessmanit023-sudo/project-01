from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'restaurants', views.RestaurantViewSet, basename='restaurant')

urlpatterns = [
    # 新的註冊 API
    path('register/customer/', views.CustomerRegisterView.as_view(), name='customer-register'),
    path('register/merchant/', views.MerchantRegisterView.as_view(), name='merchant-register'),
    
    # 登入和刷新 Token API
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 獲取使用者資訊 API
    path('user/', views.UserDetailView.as_view(), name='user-detail'),


    path('', include(router.urls)),
]