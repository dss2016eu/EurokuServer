import json
import datetime

from django.http import JsonResponse, HttpResponse
from django.conf import settings

from eurokuserver.control.models import Device, ControlPanel, INFOPOINT
from eurokuserver.game.models import Game


def _json_serializable_datetime(device, date):
    if date is None:
        return u''
    FORMAT_DICT = {'es': '%d-%m-%Y',
                   'eu': '%Y-%m-%d',
                   }
    lang = device and device.language or 'eu'
    return date.strftime(
        FORMAT_DICT.get(
            lang,
            '%Y-%m-%d',
            )
        )


def _cors_response(response=None):
    if response is None:
        response = HttpResponse()
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


def _error_response(msg):
    response = JsonResponse({'error': True, 'message': msg})
    return _cors_response(response)


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
            game = Game.objects.create(points_to_win=cp.get_difficulty_for_device(device=device),
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
    if device is not None:
        lang = device.language
    else:
        lang = None
    return {'title': price.get_title(lang),
            'url': price.get_url(lang),
            'event': price.event,
            'date': price.valid_until,
            'amount': price.available,
            'enddate': price.valid_until}


def _create_userprice_dict(gameprice):
    device = gameprice.device
    data_dict = _create_price_dict(gameprice.price, device)
    data_dict['key'] = gameprice.key
    data_dict['claimed'] = gameprice.claimed
    lang = device.language
    data_dict['html'] = INFOPOINT[lang]
    data_dict['latlong'] = INFOPOINT['latlong']

    if gameprice.price.event is True:
        data_dict['last_day_to_claim'] = _json_serializable_datetime(
                 device,
                 gameprice.price.get_last_date_to_claim()
                 )
    else:
        max_days_to_claim = getattr(settings, 'EUROKU_MAX_DAYS_TO_CLAIM', 10)
        data_dict['last_day_to_claim'] = _json_serializable_datetime(
            device,
            gameprice.added + datetime.timedelta(days=max_days_to_claim))
        data_dict['enddate'] = data_dict['last_day_to_claim']
    return data_dict
