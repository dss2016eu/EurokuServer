import csv, codecs
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

def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]

def utf_8_encoder(unicode_csv_data):
    for line in unicode_csv_data:
        yield line.encode('utf-8')

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self
    
class Command(BaseCommand):
    help = " load questions from json file "

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs='?', type=str)
        parser.add_argument('-l','--language', nargs='?', type=str)
        
    def handle(self, *args, **options):
        filename = options.get('csv_file', None)
        language = options.get('language', 'eu')
        with open(filename, 'rb') as f:
            reader = UnicodeReader(f)
            for row in reader:
                mandatory = row[:7]
                optional = row[8:]
                title, correct, incorrect_one, incorrect_two, language, provider, url = mandatory
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
                                               
