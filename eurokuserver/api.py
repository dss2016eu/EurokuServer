try:
    import django
    django.setup()
except:
    pass
import json
from django.views.decorators.csrf import csrf_exempt

from .apiutils import _error_response, _get_device_from_request, _correct_response, _get_game_from_request
from .apiutils import _create_userprice_dict, _create_pricedetail_dict, _create_price_dict
from .game.models import Question, GameQuestionStatus
from .price.models import DevicePrice, Price
from .price.utils import get_price

@csrf_exempt
def question(request):
    """
    .. http:get:: /galdera
    
        Galdera berri bat eskatu

        **Erantzuna**:

        .. sourcecode:: http
    
            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: text/javascript

            {
             "photo": "",
             "game_id": 109,
             "id": 101,
             "answers": ["TAKET", "AINGERU", "GOMUTAPEN"],
             "title": "'Aingeru-belarraren lorea' Bizkaian",
             "round": 1,
             "rounds": 16,
             }
                
        :query device_id: Gailuaren tokena
        :query game_id: Partida identifikadorea. Aukerakoa, ez bada bidaltzen partida berri bat hasiko da
        
    .. http:post:: /galdera
    
        Galdera baten erantzuna bidali

        **Erantzuna**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: text/javascript

            {
             "game_id": "",
             "price": "",
             "price_desc": "",
             "price_key": "",
             "correct": true,
             "provider": "twitter.com",
             "url": "https://twitter.com/elonmusk/status/679137936416329728",
             "attribution": "@elonmusk",
            }

        :query game_id: Jokoaren identifikadorea
        :query device_id: Gailuaren identifikadorea
        :query question_id: Galderaren identifikadorea
        :query answer: erantzunaren zenbakia
            
    """
    device, message = _get_device_from_request(request)
    if device is None:
        return _error_response(message)
    if request.method == 'GET':
        game, message = _get_game_from_request(request, device)
        if game is None:
            return _error_response(message)
        else:
            question = Question.objects.get_new(game)
            if question is not None:
                gamequestion = GameQuestionStatus.objects.create(game=game,
                                                                 question=question,
                                                                 correct=False)
                return _correct_response(gamequestion.repr_mobile())
            else:
                return _error_response(u'No question matching criteria')
    if request.method == 'POST':
        data = json.loads(request.body)
        question_id = data.get('question_id')
        if question_id is None:
            return _error_response(u'No question_id on request')
        answer = data.get('answer')
        if answer is None:
            return _error_response(u'No answer in response')
        gamequestion = GameQuestionStatus.objects.filter(id=question_id)
        if gamequestion.exists():
            gamequestion = gamequestion.first()
            question = gamequestion.question
            correct = question.is_correct_answer(answer)
            return_dict = {
                'game_id': '',
                'price': False,
                'price_desc': '',
                'price_key': '',
                'correct': False,
                'provider': question.provider,
                'url': question.url,
                'attribution': question.attribution}
            gamequestion.correct = correct            
            gamequestion.save()
            if gamequestion.game.active is False:
                return _error_response(u'Game is closed')
            game = gamequestion.game
            if correct:
                return_dict['correct'] = True
                return_dict['game_id'] = game.id
                correct_count = game.get_correct_answers_count()
                if correct_count == game.points_to_win:
                    game.active = False
                    game.save()
                    # Get price
                    deviceprice = get_price()
                    return_dict['price'] = True
                    return_dict['price_desc'] = u''
                    return_dict['price_key'] = deviceprice.key
            else:
                game.active = False
                game.save()
            return _correct_response(return_dict)
        else:
            return _error_response(u'No matching question')

def prices(request):
    """
    .. http:get:: /api/1.0/prices

        Gailu batetik eskuratutako sari guztien zerrenda

        **Erantzuna**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: text/javascript

            [{
              "title": "Price title",
              "amount": "Available count",
              "enddate": "Available until",
              "key": "Price key",
              "days_left": "Days to claim the price (-1 for expired prices)",
              "calimed": "true",
            },
            {
             ...
             }] 

        :query device_id: Gailuaren identifikadore tokena
    """
    device, message = _get_device_from_request(request)
    if device is None:
        return _error_response(message)
    prices = DevicePrice.objects.filter(device=device)
    return _correct_response(map(_create_userprice_dict, prices))

def price(request, price_key):
    """
    .. http:get:: /api/1.0/price/(string:price_key)

        Sariaren informazioa

        **Erantzuna**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: text/javascript

            {
            ZEHAZTU BEHAR DA
            }

        :query device_id: Gailuaren identifikadore tokena
        
    """

    device, message = _get_device_from_request(request)
    if device is None:
        return _error_response(message)
    price = DevicePrice.objects.filter(device=device,
                                       key=price_key)
    if not price.exists():
        return _error_response(u'No price with this code for this device')
    else:
        price = price.first()
    return _correct_response(_create_pricedetail_dict(price))

def profile(request):
    """
    .. http:get:: /api/1.0/profile

       Gailuaren hobespenak erakutsi

       **Erantzuna**:

       .. sourcecode:: http
       
            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: text/javascript

            {
             "device_id": "Gailuaren identifikazio tokena",
             "language": "Aukeratutako hizkuntza kodea",
            }

       :query device_id: Gailuaren identifikadore tokena
        
    .. http:post:: /api/1.0/profile

       Gailuaren hobespenak aldatu

       .. sourcecode:: http
       
            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: text/javascript

            {
             "device_id": "Gailuaren identifikazio tokena",
             "language": "Aukeratutako hizkuntza kodea",
            }

       :query device_id: Gailuaren identifikadore tokena.
       :query language: Hizkuntza kode berria.
    """
       
    device, message = _get_device_from_request(request)
    if device is None:
        return _error_response(message)
    response_dict = {'device_id': device.token,
                     'language': device.language}
    if request.method == 'POST':
        data = json.loads(request.body)
        lang = data.get('language')
        if lang is None:
            return _error_response(u'No language on request')
        device.language = lang
        response_dict['language'] = device.language
        device.save()
    return _correct_response(response_dict)


def publicprices(request):
    """
    .. http:get:: /api/1.0/prices/public

       Aukeran dauden sari guztiak zerrendatu

       **Erantzuna**:

       .. sourcecode:: http
       
            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: text/javascript

            [{
             "title": "sariaren izenburua",
             "amount": "sari kopurua",
             "enddate": "noizarte egongo den lortzeko aukera",
            },
            {
             ...
             }]

    """
    prices = Price.objects.get_available()
    
    return _correct_response(map(_create_price_dict, prices))
