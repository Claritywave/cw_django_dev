from django.test import TestCase
from .models import Question, Answer, QuestionLike
from django.contrib.auth import get_user_model
import datetime
# Create your tests here.


class ModelTest(TestCase):
    @classmethod
    def setUpClass(self):
        super(ModelTest, self).setUpClass()
        User = get_user_model()

        self.author = User.objects.create(
            first_name="test1", username="test2", email="test1@test.com"
        )
        #Create Question today
        question = Question(author=self.author, title="Test1", description="test1",)
        question.save()
        question = Question(author=self.author, title="Test2", description="test2",)
        question.save()

    def test_ranking_by_creted_on(self):
        question = Question.objects.last()
        self.assertEqual(question.ranking, 10)

        question = Question.objects.last()
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        question.created_on = yesterday
        question.save(update_fields=['created_on'])
        self.assertEqual(question.ranking, 0)

    def test_ranking_by_answers(self):
        question = Question.objects.last()
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        question.created_on = yesterday
        question.save(update_fields=['created_on'])

        question.question_answers.create(comment="test", author=self.author, value=2)
        self.assertEqual(question.ranking, 10)
        question.question_answers.create(comment="test2", author=self.author, value=3)
        self.assertEqual(question.ranking, 20)

    def test_ranking_by_answers(self):
        question = Question.objects.last()
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        question.created_on = yesterday
        question.save(update_fields=['created_on'])

        question.question_answers.create(comment="test", author=self.author, value=2)
        self.assertEqual(question.ranking, 10)
        question.question_answers.create(comment="test2", author=self.author, value=3)
        self.assertEqual(question.ranking, 20)

    def test_ranking_by_likes(self):
        question = Question.objects.last()
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        question.created_on = yesterday
        question.save(update_fields=['created_on'])
        question.question_like.create(
            author=self.author,
            like=True
        )
        self.assertEqual(question.ranking, 5)

    def test_ranking_by_dislikes(self):
        question = Question.objects.first()
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        question.created_on = yesterday
        question.save(update_fields=['created_on'])
        question.question_like.create(
            author=self.author,
            like=False
        )
        self.assertEqual(question.ranking, -3)