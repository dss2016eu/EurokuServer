import json

from django.http import JsonResponse, HttpResponse
from django.utils import timezone

from eurokuserver.control.models import Device, ControlPanel
from eurokuserver.game.models import Game

def _json_serializable_datetime(device, date):
    FORMAT_DICT = {'es': '%d-%M-%Y',
                   'eu': '%Y-%M-%d',
                   }
    lang = device and device.language or 'eu'
    return date.strftime(
        FORMAT_DICT.get(
            lang,
            '%Y-%M-%d',
            )
        )
def _cors_response(response=None):
    if response is None:
        response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET,POST'
    response['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

def _error_response(msg):
    return JsonResponse({'error': True, 'message': msg})

def _correct_response(data_dict):
    response = JsonResponse(data_dict, safe=False)
    return _cors_response(response)

def _get_game_from_request(request, device):
    game = None
    msg = ''
    if request.method == 'GET':
        game_id = request.GET.get('game_id')
    if request.method == 'POST':
        data = json.loads(request.body)
        game_id = data.get('game_id')        
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
    elif request.method == 'POST':
        data = json.loads(request.body)
        device_id = data.get('device_id')
    else:
        device_id = None 
    if device_id is None:
        msg = u'No device_id on request'
    else:
        devices = Device.objects.filter(token=device_id)
        if devices.exists():
            device = devices.first()
        else:
            msg = u'No device registered whit this id'
    return (device, msg)

def _create_price_dict(price, device=None):
    return  {'title': price.title,
             'amount': price.available,
             'enddate': _json_serializable_datetime(
                 device,
                 price.valid_until
                 ), 
             }

def _create_userprice_dict(gameprice):
    device = gameprice.device
    data_dict = _create_price_dict(gameprice.price, device)
    data_dict['key'] = gameprice.key
    days_passed = (timezone.now() - gameprice.added).days
    days_to_claim = gameprice.price.must_claim_days_delta
    if days_passed > days_to_claim:
        data_dict['days_left'] =  -1
    else:
        data_dict['days_left'] = days_to_claim - days_passed
    data_dict['claimed'] = gameprice.claimed
    return data_dict

def _create_pricedetail_dict(price):
    pass

