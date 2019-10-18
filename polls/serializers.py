from rest_framework import serializers
from .models import Question, Choice, Answered


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('question_text', 'asked_date')


class QuestionDetailSerializer(serializers.ModelSerializer):
    choice_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Question
        fields = ('question_text', 'choice_set')


class QuestionResultsSerializer(serializers.ModelSerializer):
    question = serializers.StringRelatedField(many=False)

    class Meta:
        model = Choice
        fields = ('question', 'choice_text', 'votes')
