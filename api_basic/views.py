from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from .models import Article
from rest_framework.decorators import api_view
# Create your views here.
from rest_framework.response import Response
from .serializers import ArticleSerializer
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView





class ArticleAPIView (APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many =True)
        return Response(serializer.data)

    def post(seld,request):
        serializer = ArticleSerializer(data = request.data)
        if serializer.is_valid():
            #if serializer is valid then only save
            serializer.save()
            #create status
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



@api_view(['GET' , 'POST'])
def article_list(request):
    if request.method =='GET':
        #get data from database
        articles = Article.objects.all()
        #serialize the articles
        serializer = ArticleSerializer(articles, many =True)
        return Response(serializer.data)
    elif request.method =='POST':
        
        serializer = ArticleSerializer(data = request.data)
        if serializer.is_valid():
            #if serializer is valid then only save
            serializer.save()
            #create status
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
#class based Views
class ArticleDetails(APIView):
    def get_object(self,id):
        try:
            return Article.objects.get(id = id)
        except Article.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

    def get(self , request , id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self , request , id):
        article = self.get_object(id)
        serializer = ArticleSerializer(article, data = request.data)
        if serializer.is_valid():
            #if serializer is valid then only save
            serializer.save()
            #create status
            return Response(serializer.data) 
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request , id):
        article = self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#function based API view
# @csrf_exempt
# def article_detail(request,pk):
#     try:
#         article = Article.objects.get(pk = pk)
#     except Article.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method =='GET':
         
#         #serialize the articles
#         serializer = ArticleSerializer(article)
#         return JsonResponse(serializer.data)
#     elif request.method =='PUT':
#         data = JSONParser().parse(request)
#         serializer = ArticleSerializer(article, data = data)
#         if serializer.is_valid():
#             #if serializer is valid then only save
#             serializer.save()
#             #create status
#             return JsonResponse(serializer.data) 
#         else:
#             return JsonResponse(serializer.errors, status=400)
#     elif  request.method == 'DELETE':
#         article.delete()
#         return HttpResponse(status=204)


@api_view(['GET' ,'PUT' , 'DELETE'])
def article_detail(request,pk):
    try:
        article = Article.objects.get(pk = pk)
    except Article.DoesNotExist:
        return HttpResponse(status = status.HTTP_404_NOT_FOUND)

    if request.method =='GET':
         
        #serialize the articles
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    elif request.method =='PUT':
        
        serializer = ArticleSerializer(article, data = request.data)
        if serializer.is_valid():
            #if serializer is valid then only save
            serializer.save()
            #create status
            return Response(serializer.data) 
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif  request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)