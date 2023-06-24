from django.shortcuts import render
from django.contrib.auth import login, authenticate

from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated            # 토큰 인증 및 권한 확인을 위한 함수
from rest_framework.authtoken.models import Token                                           # 토큰 기반의 로그인에서 사용, 토큰 검사를 수행한다.
from rest_framework.authentication import SessionAuthentication, BasicAuthentication        # Django에서 기본적으로 사용되는 csrf_token를 BasicAuthentication은 수행하지 않음. CSRF 토큰검사 비활성화
from rest_framework.authentication import TokenAuthentication
from .pagination import SetPagination

from common.models import CustomUser, CustomUserManager
from main.models import Sound_Level, Sound_File, Sound_Level_Verified, CommunityBoard, ComplainBoard
from .serializers import *

# 토큰 인증을 통해 로그인 한 유저의 정보를 가져오는 함수
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user  # 인증된 사용자를 가져옴
        serializer = UserSerializer(user)  # 사용자를 직렬화

        return Response(serializer.data)  # 직렬화된 사용자 데이터를 응답에 포함


# 관리자 유저에 한해, 유저 목록 전체를 불러오는 함수
class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = SetPagination

    def get(self, request, format=None):
        if request.user.is_staff :
            users = CustomUser.objects.all()               # 모든 사용자 데이터를 가져오기
            serializer = UserSerializer(users, many=True)  # 사용자를 직렬화

            return Response(serializer.data)                   # 직렬화된 사용자 데이터를 응답에 포함
        else:  # 슈퍼유저가 아니라면, 접근 거부 메시지를 반환
            return Response({"detail": "관리자 권한이 필요합니다."}, status=403)
    

# API 서버를 통한 회원가입 함수
class UserRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer  # 바로 지정

    def get_serializer_class(self):
        return UserRegisterSerializer
    

class UserLoginView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():                            # 유저 시리얼라이저 확인 후
            user = serializer.validated_data
            token, _ = Token.objects.get_or_create(user=user)          # 로그인 한 유저의 토큰 생성
            response = Response({"token": token.key}, status=200)     # 응답에 토큰 포함
            response.set_cookie('auth-token', token.key)              # 
            return response
        
        return Response(serializer.errors, status=401)
        
    def get(self, request, format=None):
        if request.user.is_staff :
            users = CustomUser.objects.userid()               # 모든 사용자 데이터를 가져오기
            serializer = UserSerializer(users, many=True)     # 사용자를 직렬화

            return Response(serializer.data)                   # 직렬화된 사용자 데이터를 응답에 포함
        else:  # 슈퍼유저가 아니라면, 접근 거부 메시지를 반환
            return Response({"detail": "관리자 권한이 필요합니다."}, status=403)
        

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()        # 로그아웃 사용자 토큰 제거
        return Response(status=204)  # 204 No Content - 성공적으로 처리했지만, 응답할 콘텐츠가 없을 때.
        
        
class SoundLevelViewSet(viewsets.ModelViewSet):
    queryset = Sound_Level.objects.all().order_by('-id')                    # ID 정렬
    serializer_class = SoundLevelSerializer                                 # 데시벨 데이터에 대한 직렬화 처리
    pagination_class = SetPagination

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        queryset = Sound_Level.objects.all().order_by('id')
        if queryset.count() >= 1000:                                        # 데시벨 데이터 생성시, 100개 이상이 되면
            queryset.first().delete()                                       # 가장 먼저 만들어진 데이터부터 삭제
        return response
    


class SoundFileViewSet(viewsets.ModelViewSet):
    queryset = Sound_File.objects.all().order_by('-id')                     # ID 정렬
    serializer_class = SoundFileSerializer                                  # 녹음파일 데이터에 대한 직렬화 처리
    pagination_class = SetPagination

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        queryset = Sound_File.objects.all().order_by('id')
        if queryset.count() >= 1000:                                        # 녹음파일 데이터 생성시, 1000개 이상이 되면
            queryset.first().delete()                                       # 가장 먼저 만들어진 데이터부터 삭제
        return response
    


class SoundLevelVerifiedViewSet(viewsets.ModelViewSet):
    queryset = Sound_Level_Verified.objects.all().order_by('-id')           # ID 정렬
    serializer_class = SoundLevelVerifiedSerializer                         # 녹음파일 데이터에 대한 직렬화 처리
    pagination_class = SetPagination

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        queryset = Sound_Level_Verified.objects.all().order_by('id')
        if queryset.count() >= 1000:                                        # 검증 완료파일 데이터 생성시, 1000개 이상이 되면
            queryset.first().delete()                                       # 가장 먼저 만들어진 데이터부터 삭제
        return response
    

class CommunityBoardViewSet(viewsets.ModelViewSet):
    queryset = CommunityBoard.objects.all().order_by('-created_date')        # 생성일시 기준 정렬
    serializer_class = CommunityBoardSerializer                              # 커뮤니티 게시판 데이터에 대한 직렬화 처리
    pagination_class = SetPagination

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        queryset = CommunityBoard.objects.all().order_by('-created_date')
        if queryset.count() >= 200:                                          # 게시판 데이터 생성시, 200개 이상이 되면
            queryset.first().delete()                                        # 가장 먼저 만들어진 데이터부터 삭제
        return response
    


class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all().order_by('-created_date')        # 생성일시 기준 정렬
    serializer_class = ReplySerializer                              # 커뮤니티 게시판 데이터에 대한 직렬화 처리
    pagination_class = SetPagination

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        queryset = Reply.objects.all().order_by('-created_date')
        if queryset.count() >= 200:                                          # 게시판 데이터 생성시, 200개 이상이 되면
            queryset.first().delete()                                        # 가장 먼저 만들어진 데이터부터 삭제
        return response
    

class ComplainBoardViewSet(viewsets.ModelViewSet):
    queryset = ComplainBoard.objects.all().order_by('-created_date')        # 생성일시 기준 정렬
    serializer_class = ComplainBoardSerializer                              # 민원접수 게시판 데이터에 대한 직렬화 처리
    pagination_class = SetPagination

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        queryset = ComplainBoard.objects.all().order_by('id')
        if queryset.count() >= 200:                                         # 게시판 데이터 생성시, 200개 이상이 되면
            queryset.first().delete()                                       # 가장 먼저 만들어진 데이터부터 삭제
        return response