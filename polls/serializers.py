from rest_framework import serializers
from .models import Question, Choice, Answered


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ('question_text', 'choice_set')
