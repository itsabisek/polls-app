from rest_framework import serializers
from .models import Answered, Question


class QuestionSerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        votes = Answered.objects.filter(question_id=obj.id).count()
        return {
            'question_id': obj.id,
            'question_text': obj.question_text,
            'asked_date': obj.asked_date,
            'votes': votes
        }


class QuestionDetailSerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        choices = obj.choice_set.all()
        return{
            'question_id': obj.id,
            'question_text': obj.question_text,
            'asked_date': obj.asked_date,
            'choices': [
                {
                    'id': choices[0].id,
                    'choice_text':choices[0].choice_text,
                    'choice_votes':choices[0].votes,
                },
                {
                    'id': choices[1].id,
                    'choice_text':choices[1].choice_text,
                    'choice_votes':choices[1].votes,
                }
            ]
        }


class QuestionAnsweredDetailSerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        question = Question.objects.get(pk=obj.question_id)
        choices = question.choice_set.all()
        return {
            'question_id': question.id,
            'question_text': question.question_text,
            'answered_on': obj.answered_on,
            'choices': [
                {
                    'id': choices[0].id,
                    'choice_text':choices[0].choice_text,
                    'choice_votes':choices[0].votes,
                },
                {
                    'id': choices[1].id,
                    'choice_text':choices[1].choice_text,
                    'choice_votes':choices[1].votes,
                }
            ]
        }
