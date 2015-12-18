from django.http import JsonResponse

from eurokuserver.control.models import Device, ControlPanel
from eurokuserver.game.models import Game

def _error_response(msg):
    return JsonResponse({'error': True, 'message': msg})

def _correct_response(data_dict):
    return JsonResponse(data_dict)

def _get_game_from_request(request, device):
    game = None
    msg = ''
    if request.method == 'GET':
        game_id = request.GET.get('game_id')
    if request.method == 'POST':
        game_id = request.POST.get('game_id')        
    if game_id is None:
        if request.method == 'GET':
            cp = ControlPanel.objects.all()[0]
            game = Game.objects.create(points_to_win=cp.difficulty,
                                       device=device)
        else:
            msg = u'No game_id on request'
    else:
        game = Game.objects.filter(pk=game_id)
        if game.exists():
            game = game.first()
    if game.active is not True:
        game = None
        msg = u'Closed game'
    return (game, msg)

def _get_device_from_request(request):
    device = None
    msg = ''
    if request.method == 'GET':
        device_id = request.GET.get('device_id')
    if request.method == 'POST':
        device_id = request.POST.get('device_id')
    if device_id is None:
        msg = u'No device_id on request'
    else:
        devices = Device.objects.filter(token=device_id)
        if devices.exists():
            device = devices.first()
        else:
            msg = u'No device registered whit this id'
    return (device, msg)

def _create_price_dict(price):
    pass

def _create_pricedetail_dict(price):
    pass

