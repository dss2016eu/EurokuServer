import json
import requests
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
    
    try:
        photo = load_photo_from_raw_data(title[:100], tags, slug, format, image)
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
        photo. slug=slug
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
        print 'Errorea irudi honekin', title, e
    return photo

class Command(BaseCommand):
    help = " load questions from json file "

    def add_arguments(self, parser):
        parser.add_argument('json_file', nargs='?', type=str)
        parser.add_argument('-l','--language', nargs='?', type=str)
        
    def handle(self, *args, **options):
        filename = options.get('json_file', None)
        language = options.get('language', 'eu')
        with open(filename) as f:
            data = json.loads(f.read())
            for question in data:
                q = Question.objects.create(title=question.get('title'),
                                            correct_answer=question.get('correct')
                                            incorrect_answer_one=question.get('incorrect_answer_one'),
                                            incorrect_answer_two=question.get('incorrect_answer_two'),
                                            lang=language,
                                            provider=question.get('provider'),
                                            url=question.get('url'),
                                            attribution=question.get('attribution'),
                                            public=True,
                                            reviewed=True,)            
                if question.get('photo_url', None) is not None:
                    photo = get_photo_from_url(question.get(question.get('photo_url')))
                    if photo is not None:
                        q.photo = photo
                
                                               
                    
