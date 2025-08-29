from django.contrib.auth import authenticate
from rest_framework import status, views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Restaurant, Merchant
from .serializers import (
    UserSerializer, 
    CustomerRegisterSerializer, 
    MerchantRegisterSerializer,
    RestaurantSerializer
)

# --- 註冊視圖 ---
class CustomerRegisterView(views.APIView):
    """
    處理顧客註冊的視圖
    """
    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MerchantRegisterView(views.APIView):
    """
    處理商家註冊的視圖
    """
    def post(self, request):
        serializer = MerchantRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- 其他認證視圖 ---
class UserDetailView(views.APIView):
    """
    獲取當前登入使用者資訊的視圖
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# --- 商家管理餐廳的視圖集 ---
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated]

    # 這個方法會在新增或修改時，將當前登入的商家設定為餐廳的擁有者
    def perform_create(self, serializer):
        serializer.save(merchant=self.request.user.merchant)

    # 確保用戶只能看到和修改自己旗下的餐廳
    def get_queryset(self):
        user = self.request.user
        # 檢查當前登入用戶是否為商家
        if hasattr(user, 'merchant'):
            # 過濾並返回該商家所擁有的所有餐廳
            return Restaurant.objects.filter(merchant=user.merchant)
        
        # 如果不是商家，則返回空查詢集，防止未經授權的訪問
        return Restaurant.objects.none()