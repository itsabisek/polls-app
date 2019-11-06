"""

    serializers.py: Contains all the serailzer classes that serializes the model 
    querysets into readable json format that can be sent as a reponse

"""


from rest_framework import serializers
from .models import Answered, Question


class QuestionSerializer(serializers.BaseSerializer):
    """
        Serializer class for serializing all the questions for the index page. 
        Does not serialize data that require login like choices in each question 
        and number of votes per choice

    """

    def to_representation(self, obj):
        votes = Answered.objects.filter(question_id=obj.id).count()
        return {
            'question_id': obj.id,
            'question_text': obj.question_text,
            'asked_date': obj.asked_date,
            'votes': votes
        }


class QuestionDetailSerializer(serializers.BaseSerializer):
    """
        Serializer class for serializing a single instance of a question. 
        Serializes all the information about a poll like choices, votes per choice and
        id of each choice, asked date, question text and question id

    """

    def to_representation(self, obj):
        choices = obj.choice_set.all()
        total_votes = choices[0].votes + choices[1].votes
        return{
            'question_id': obj.id,
            'question_text': obj.question_text,
            'asked_date': obj.asked_date,
            'votes': total_votes,
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


class QuestionDetailNoVotesSerializer(serializers.BaseSerializer):
    """
        Serializes all information about a particular poll like the QuestionDetailSerializer 
        above but does not include the votes_per_choice. 

        Can be used when the user is logged in but did not vote for the poll asked for.

    """

    def to_representation(self, obj):
        choices = obj.choice_set.all()
        total_votes = Answered.objects.filter(question_id=obj.id).count()
        return{
            'question_id': obj.id,
            'question_text': obj.question_text,
            'asked_date': obj.asked_date,
            'votes': total_votes,
            'choices': [
                {
                    'id': choices[0].id,
                    'choice_text':choices[0].choice_text,
                },
                {
                    'id': choices[1].id,
                    'choice_text':choices[1].choice_text,
                }
            ]
        }


class QuestionAnsweredDetailSerializer(serializers.BaseSerializer):
    """
        Serializes every information about all questions that a user has answered. 
        Same as QuestionSerializer but with a change. 

        Includes answered on field instead of asked on.

    """

    def to_representation(self, obj):
        question = Question.objects.get(pk=obj.question_id)
        choices = question.choice_set.all()
        total_votes = Answered.objects.filter(
            question_id=obj.question_id).count()
        return {
            'question_id': question.id,
            'question_text': question.question_text,
            'answered_on': obj.answered_on,
            'votes': total_votes,
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
