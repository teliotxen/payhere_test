import json
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import JWTSignupSerializer, JWTLoginSerializer


class JWTSignupView(APIView):
    serializer_class = JWTSignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            user = serializer.save(request)
            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)

            return JsonResponse({'user': user,
                                 'access': access,
                                 'refresh': refresh

                                 })


class JWTLoginView(APIView):
    serializer_class = JWTLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=False):
            access = serializer.validated_data['access']
            refresh = serializer.validated_data['refresh']
            data = {
                'access': access,
                'refresh': refresh
            }
            response = JsonResponse(data,status=200)
            #쿠키 설정
            cookie = json.dumps(data)
            response.set_cookie(key='jwt', value=cookie, httponly=False, samesite='None')
            return response



class JWTLogOutView(APIView):
    def post(self, request):
        response = JsonResponse({
            "message": "success"
        })
        response.delete_cookie('jwt')
        return response
