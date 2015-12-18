from django.views.decorators.csrf import csrf_exempt

from .apiutils import _error_response, _get_device_from_request, _correct_response, _get_game_from_request
from .apiutils import _create_price_dict, _create_pricedetail_dict
from .game.models import Question, GameQuestionStatus
from .price.models import DevicePrice
from .price.utils import get_price

@csrf_exempt
def question(request):
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
        question_id = request.POST.get('question_id')
        if question_id is None:
            return _error_response(u'No question_id on request')
        answer = request.POST.get('answer')
        if answer is None:
            return _error_response(u'No answer in response')
        gamequestion = GameQuestionStatus.objects.filter(id=question_id)
        if gamequestion.exists():
            gamequestion = gamequestion.first()
            question = gamequestion.question
            correct = question.is_correct_answer(answer)
            return_dict = {'price': False,
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
            if correct:
                game = gamequestion.game
                return_dict['correct'] = True
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
    device, message = _get_device_from_request(request)
    if device is None:
        return _error_response(message)
    prices = DevicePrice.objects.filter(device=device)
    return _correct_response(map(_create_price_dict, prices))

def price(request, price_key):
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
    device, message = _get_device_from_request(request)
    if device is None:
        return _error_response(message)
    response_dict = {}
    if request.method == 'POST':
        #save user lang
        pass
    else:
        #get user lang
        pass
    return _correct_response(response_dict)


def publicprices(request):
    pass
