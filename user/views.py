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
            response = {
                         'access': access,
                         'refresh': refresh
                         }
            return JsonResponse(response, status=200)
        else:
            return JsonResponse({'auth':'fail'}, status=400)


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

            return JsonResponse(data,status=200)
        else:
            return JsonResponse({'auth':'fail'}, status=400)



class JWTLogOutView(APIView):
    def post(self, request):
        response = {
            "message": "success"
        }
        return JsonResponse(response, status=203)




