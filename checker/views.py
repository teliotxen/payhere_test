from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Item
from .serializers import ItemSerializer
from django.shortcuts import get_object_or_404
from .authenticate import validate_token_detail, validate_token
import string
import random
from django.core.cache import cache


class ItemListAPIView(APIView):
    def get(self, request):
        val = validate_token(request)
        if val == 402:
            return JsonResponse({'auth': 'expired'}, status=402)
        elif val == 401:
            return JsonResponse({'auth': 'unauthorized'}, status=401)
        else:
            serializer = ItemSerializer(Item.objects.filter(user=val), many=True)
            return Response(serializer.data)

    def post(self, request):
        val = validate_token(request)
        if val == 402:
            return JsonResponse({'auth': 'expired'}, status=402)
        elif val == 401:
            return JsonResponse({'auth': 'unauthorized'}, status=401)
        else:
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)


class ItemDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Item,pk=pk)


    def get(self, request, pk):
        item = self.get_object(pk)
        val = validate_token_detail(request,item)
        if val == 401:
            return JsonResponse({'auth': 'unauthorized user'}, status=401)
        elif val == 402:
            return JsonResponse({'auth': 'expired'}, status=402)
        else:
            serializer = ItemSerializer(item)
            return Response(serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk)
        val = validate_token_detail(request,item)
        if val == 401:
            return JsonResponse({'auth': 'unauthorized user'}, status=401)
        elif val == 402:
            return JsonResponse({'auth': 'expired'}, status=402)
        else:
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShortenUrlGenerator(APIView):
    def get(self, request, pk):
        val = validate_token(request)
        if val == 402:
            return JsonResponse({'auth': 'expired'}, status=402)
        elif val == 401:
            return JsonResponse({'auth': 'unauthorized'}, status=401)
        else:
            letters_set = string.ascii_letters
            random_list = random.sample(letters_set, 10)
            result = ''.join(random_list)

            if not cache.get(result):
                _key = result

            _value = pk
            cache.set(_key,_value, timeout=30*30)
            return JsonResponse({'shortenUrl':_key},status=200)


class ShortenUrl(APIView):
    def get(self, request, key):
        val = validate_token(request)
        if val == 402:
            return JsonResponse({'auth': 'expired'}, status=402)
        else:
            _value = cache.get(key)
            if _value is None:
                return JsonResponse({'shortenUrl':_value},status=422)
            else:
                item = Item.objects.get(pk=_value)
                serializer = ItemSerializer(item)
                return Response(serializer.data)
