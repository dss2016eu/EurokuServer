from random import shuffle

from django.db import models
from django.conf import settings
from django.utils import timezone

from photologue.models import Photo

from eurokuserver.control.models import Device, LANGUAGES

MAX_RESPONSE_TIME = getattr(settings, 'EUROKU_MAX_RESPONSE_TIME_SECONDS', 30)

# Create your models here.

class Game(models.Model):
    device = models.ForeignKey(Device)
    points_to_win = models.SmallIntegerField(default=16)
    active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)

    def get_correct_answers_count(self):
        return GameQuestionStatus.objects.filter(correct=True, game=self).count()
    
class QuestionManager(models.Manager):
    def get_new(self, game):
        q = self.filter(public=True, lang=game.device.language).order_by('?')
        if q.exists():
            return q.first()
    
class Question(models.Model):
    title = models.CharField(max_length=250)
    correct_answer = models.CharField(max_length=100)        
    incorrect_answer_one = models.CharField(max_length=100)
    incorrect_answer_two = models.CharField(max_length=100)
    photo = models.ForeignKey(Photo, blank=True, null=True)
    order = models.CharField(max_length=3, blank=True, null=True)
    lang = models.CharField(max_length=5,choices=LANGUAGES)
    provider = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    attribution = models.CharField(max_length=255, blank=True, null=True)
    added = models.DateField(auto_now_add=True)
    reviewed = models.BooleanField()
    public = models.BooleanField()

    objects = QuestionManager()
    
    def order_to_attr(self, index):
        _map = {'1': 'correct_answer',
                '2': 'incorrect_answer_one',
                '3': 'incorrect_answer_two'}
        return _map[index]
        
    def repr_mobile(self):
        photo = ''
        if self.photo is not None:
            photo = self.photo.get_display_url()
        return {'title': self.title,
                'answers': [getattr(self, self.order_to_attr(self.order[0])),
                            getattr(self, self.order_to_attr(self.order[1])),
                            getattr(self, self.order_to_attr(self.order[2]))],
                'photo': photo,
                }
    
    def is_correct_answer(self, order_index):
        return order_index != '-1' and self.order[int(order_index)-1] == '1'

    def save(self, *args, **kwargs):
        if self.order is None:
            a = ['1','2','3']
            shuffle(a)
            self.order = ''.join(a)
        super(Question, self).save(*args, **kwargs)
    
class GameQuestionStatus(models.Model):
    game = models.ForeignKey(Game)
    question = models.ForeignKey(Question)
    correct = models.BooleanField(default=False)
    added = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(blank=True, null=True)

    def repr_mobile(self):
        data_dict = self.question.repr_mobile()
        data_dict['id'] = self.pk
        data_dict['game_id'] = self.game.pk
        data_dict['round'] = self.game.get_correct_answers_count() + 1
        data_dict['rounds'] = self.game.points_to_win
        return data_dict

    def save(self, *args, **kwargs):
        # testatu behar da self.added None datorrela lehen gordetzean.
        if self.added is not None:
            self.answered = timezone.now()
            delta = self.answered - self.added
            if delta.seconds > MAX_RESPONSE_TIME:
                self.game.active = False
                self.game.save()
        super(GameQuestionStatus, self).save(*args, **kwargs)
