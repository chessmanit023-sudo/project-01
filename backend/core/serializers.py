from rest_framework import serializers
from django.db import transaction
from .models import User, Customer, Merchant, MembershipLevel, Restaurant, Comment

# --- 基礎序列化器 ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

# --- 註冊序列化器 ---

class CustomerRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label='Confirm password')

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    @transaction.atomic # 確保 User 和 Customer 一起成功或一起失敗
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        # 建立對應的 Customer profile
        Customer.objects.create(user=user)
        return user

class MerchantRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label='Confirm password')
    # 商家註冊時，必須提供會員等級 ID
    membership_level_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'membership_level_id')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        # 檢查提供的 membership_level_id 是否存在
        if not MembershipLevel.objects.filter(pk=attrs['membership_level_id']).exists():
            raise serializers.ValidationError({"membership_level_id": "Invalid Membership Level ID."})
        return attrs

    @transaction.atomic # 確保 User 和 Merchant 一起成功或一起失敗
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        # 建立對應的 Merchant profile
        Merchant.objects.create(
            user=user,
            membership_level_id=validated_data['membership_level_id']
        )
        return user

class MembershipLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipLevel
        fields = ['id', 'get_id_display', 'description']
        
class MerchantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    membership_level = MembershipLevelSerializer(read_only=True)

    class Meta:
        model = Merchant
        fields = ['user', 'membership_level']

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'introduction', 'created_at', 'merchant']
        read_only_fields = ['created_at', 'merchant']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'user', 'restaurant', 'created_at']