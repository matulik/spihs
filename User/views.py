# coding=UTF-8
from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from User.serializers import UserSerializer, TokenSerializer
from User.models import User, Token


@csrf_exempt
def login(request):
    if User.userAuth(request, tokkening=True):
        return redirect('/token/')
    if request.method == 'POST':
        print 'loging..'
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            msg = 'Error. User not found.'
            print msg
            return render_to_response('login.html', {'msg': msg}, context_instance=RequestContext(request))
        except User.MultipleObjectsReturned:
            msg = 'Error. Multiple user. Please contact with administrator.'
            return render_to_response('login.html', {'msg': msg}, context_instance=RequestContext(request))

        if user.passwordCompare(password):
            user.login(request)
            msg = 'Login successfully'
            print msg
            # Return token
            return redirect('/token/')
        else:
            msg = 'Error. Wrong password.'
            return render_to_response('login.html', {'msg': msg}, context_instance=RequestContext(request))
    else:
        return render_to_response('login.html', context_instance=RequestContext(request))


@csrf_exempt
def logout(request):
    if User.userAuth(request, tokkening=True):
        user = User.objects.get(id=request.session['id'])
        user.logout(request)
        return redirect('/')
    else:
        return redirect('/')


@api_view(['GET'])
def token_detail(request, format=None):
    if User.userAuth(request, tokkening=False) == False:
        print u"Access denied"
        return render_to_response('denied.html', context_instance=RequestContext(request))

    if request.method == 'GET':
        try:
            user = User.objects.get(id=request.session['id'])
            token = Token.objects.get(id=user.token_id)
        except Token.DoesNotExist or User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TokenSerializer(token)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def user_list(request, format=None):
    if User.userAuth(request, tokkening=True) == False:
        print u"Access denied"
        return render_to_response('denied.html', context_instance=RequestContext(request))

    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk, format=None):
    if User.userAuth(request, tokkening=True) == False:
        print u"Access denied"
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
