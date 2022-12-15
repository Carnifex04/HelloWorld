import json
import random
import time

from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
from django.shortcuts import render

from .models import RoomMember
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def lobby(request):
    return render(request, 'base/lobby.html')


def room(request):
    return render(request, 'base/room.html')


def getToken(request):
    appId = 'b6f359a484ac48ba92a17f9a7268abf1'
    appCertificate = 'dbcec7bcbe1141cb8e188e86ad464c8b'
    channelName = request.GET.get('channel')
    uid = random.randint(0, 230)
    role = 1
    currentTimeStamp = time.time()
    expirationInSeconds = 3600*24
    privilegeExpiredTs = currentTimeStamp + expirationInSeconds

    token = RtcTokenBuilder.buildTokenWithUid(
        appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createUser(request):
    data = json.loads(request.body)
    user, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name': data['name']}, safe=False)


def getUser(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')

    user = RoomMember.objects.get(
        uid=uid,
        room_name=room_name
    )

    name = user.name
    return JsonResponse({'name': name}, safe=False)


@csrf_exempt
def deleteUser(request):
    data = json.loads(request.body)
    user = RoomMember.objects.get(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    user.delete()
    return JsonResponse('Member deleted', safe=False)
