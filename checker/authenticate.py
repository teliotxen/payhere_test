import jwt
from rest_framework import status
from payhere_test.settings import SECRET_KEY
import time


def validate_token_detail(request, item):
    try:
        get_header_info = request.META['HTTP_AUTHORIZATION']
        access_token = get_header_info.split('Bearer ')[1]
        output = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')

        if output['user_id'] != item.user:
            # return JsonResponse({'auth':'unauthorized user'}, status=401)
            return 401
        if output['exp'] < time.time():
            # return JsonResponse({'auth':'expired'}, status=402)
            return 402

    except jwt.ExpiredSignatureError:
        return status.HTTP_401_UNAUTHORIZED
    except jwt.InvalidTokenError:
        return status.HTTP_401_UNAUTHORIZED


def validate_token(request):
    try:
        get_header_info = request.META['HTTP_AUTHORIZATION']
        access_token = get_header_info.split('Bearer ')[1]
        output = jwt.decode(access_token, SECRET_KEY, algorithms='HS256')

        if output['exp'] < time.time():
            return 402
        else:
            return output['user_id']

    except jwt.ExpiredSignatureError:
        return status.HTTP_401_UNAUTHORIZED
    except jwt.InvalidTokenError:
        return status.HTTP_401_UNAUTHORIZED

