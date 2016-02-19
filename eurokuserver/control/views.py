from django.shortcuts import render
from django.contrib.auth import login as d_login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from .unicodecsvreader import UnicodeReader
from eurokuserver.game.models import Question
from eurokuserver.game.management.commands.load_csv_questions import get_photo_from_url

# Create your views here.
def login(request, template_name='accounts/login.html'):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        redirect = request.POST.get('next', '/')
        user = authenticate(username=username, password=password)
        if user is not None:
            d_login(request, user)
            return HttpResponseRedirect(redirect)
    else:
        next = request.GET.get('next')
    return render(request, template_name, locals())

@staff_member_required
def add_questions(request):
    if request.method == 'POST':
        csvfile = request.FILES.get('file')
        try:
            reader = UnicodeReader(csvfile)
        except:
            alert_message = u'Erroreren bat dago fitxategian. Ezin automatikoki kargatu'
            return render(request, 'admin/load_csv_questions.html', locals())
        kont = 0
        for row in reader:    
            if kont != 0:
                mandatory = row[:7]
                optional = row[7:]
                try:
                    title, correct, incorrect_one, incorrect_two, language, provider, url = mandatory
                except:
                    alert_message = u'Fitxategiaren zutabe kopurua ez da zuzena'
                    return render(request, 'admin/load_csv_questions.html', locals())
                q = Question.objects.create(title=title,
                                            correct_answer=correct,
                                            incorrect_answer_one=incorrect_one,
                                            incorrect_answer_two=incorrect_two,
                                            lang=language,
                                            provider=provider,
                                            url=url,
                                            public=True,
                                            reviewed=True,)
                for extra_data in optional:
                    if extra_data.startswith('http'):
                        photo = get_photo_from_url(url=extra_data)
                        if photo is not None:
                            q.photo = photo
                    else:
                        q.attribution = extra_data
                    q.save()
                view_message = u'Karga bukatu da. {0} galdera gehitu dira'.format(kont)
            kont += 1
    return render(request, 'admin/load_csv_questions.html', locals())
        
