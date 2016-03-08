import json
import requests
import random
import string
from cStringIO import StringIO
try:
    from PIL import Image
except ImportError:
    import Image

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

from photologue.models import Photo

from eurokuserver.game.models import Question

def get_photo_from_url(url='', title='', tags='', format='jpg', slug=''):
    """ """
    if not url:
        return None
    
    try:
        response = requests.get(url)
    except:
        return None
    if not response.status_code == 200:
        return None
    image = response.content
    N=10
    title = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    slug = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
                   
    try:
        photo = load_photo_from_raw_data(title, tags, slug, format, image)
    except Exception, e:
        print 'Errorea irudi honekin RGB', title, e
        return None
    return photo

def load_photo_from_raw_data(title, tags, slug, image_format, image):
    photo = Photo.objects.filter(title=title)
    if not photo.exists():
        photo = Photo()
        photo.title = title
        photo.tags=tags
        photo.slug=slug
    else:
        photo = photo[0]
    image_t = Image.open(ContentFile(image))
    image_t = image_t.convert("RGB")
    f=StringIO()
    image_t.save(f,"JPEG")
    f.seek(0)

    
    photo.image.save('%s.%s' % (slug,image_format), ContentFile(f.read()))
    try:
        photo.save()
    except Exception, e:
        import pdb;pdb.set_trace()
        print 'Errorea irudi honekin', title, e
    return photo

class Command(BaseCommand):
    help = " load questions from json file "

    def add_arguments(self, parser):
        parser.add_argument('json_file', nargs='?', type=str)
        parser.add_argument('-l','--language', dest='language', default='eu', nargs='?', type=str)
        parser.add_argument('-t','--title', dest='title', default=None, nargs='?', type=str)
        parser.add_argument('-p','--provider', dest='provider', default=None, nargs='?', type=str)
        parser.add_argument('-u','--url', dest='url', default=None, nargs='?', type=str)
        
    def handle(self, *args, **options):
        filename = options.get('json_file', None)
        language = options.get('language', 'eu')
        title = options.get('title', None)
        provider = options.get('provider', None)
        url = options.get('url', None)
        
        with open(filename) as f:
            data = json.loads(f.read())
            for question in data:
                title = title or question.get('title')
                provider = provider or question.get('provider')
                url = url or question.get('url')
                q = Question.objects.create(title=title,
                                            correct_answer=question.get('correct'),
                                            incorrect_answer_one=question.get('incorrect_answer_one'),
                                            incorrect_answer_two=question.get('incorrect_answer_two'),
                                            lang=language,
                                            provider=provider,
                                            url=url,
                                            attribution=question.get('attribution'),
                                            public=True,
                                            reviewed=True,)                  
                if question.get('photo_url', None) is not None:
                    photo = get_photo_from_url(url=question.get('photo_url'))
                    if photo is not None:
                        q.photo = photo
                        q.save()
                                               
                    
