from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, Answer, Tag, QuestionLike, AnswerLike
import random
from tqdm import tqdm
from django.db import transaction
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Multiplication factor for data generation')

    def handle(self, *args, **options):
        ratio = options['ratio']
        now = timezone.now()
        min_question_time = now - timedelta(days=30)

        self.stdout.write(f"Generating test data with ratio {ratio}...")
        users = []
        self.stdout.write(f"Creating {ratio} users...")
        with transaction.atomic():
            for i in tqdm(range(ratio)):
                username = f'user_{i}'
                email = f'user_{i}@example.com'
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='testpass123'
                )
                users.append(user)
        tags = []
        self.stdout.write(f"Creating {ratio} tags...")
        for i in tqdm(range(ratio)):
            tag = Tag.objects.create(
                name=f'tag_{i}'
            )
            tags.append(tag)
        questions = []
        self.stdout.write(f"Creating {ratio * 10} questions...")
        for i in tqdm(range(ratio * 10)):
            time_offset = timedelta(
                days=random.randint(1, 30),
                hours=random.randint(1, 23),
                minutes=random.randint(1, 59)
            )
            created_at = now - time_offset

            question = Question.objects.create(
                title=f'Question #{i}',
                text=f'This is the text for question {i}',
                author=random.choice(users),
                rating=random.randint(-10, 10),
                created_at=created_at
            )
            question.tags.set(random.sample(tags, k=random.randint(1, 3)))
            questions.append(question)

        answers = []
        self.stdout.write(f"Creating {ratio * 100} answers...")
        for i in tqdm(range(ratio * 100)):
            question = random.choice(questions)
            min_answer_time = question.created_at + timedelta(minutes=1)
            max_answer_time = min(now, question.created_at + timedelta(days=30))
            time_range = (max_answer_time - min_answer_time).total_seconds()
            if time_range > 0:
                delay_seconds = random.randint(0, int(time_range))
                created_at = min_answer_time + timedelta(seconds=delay_seconds)
            else:
                created_at = min_answer_time

            answer = Answer.objects.create(
                text=f'This is answer #{i} to the question',
                question=question,
                author=random.choice(users),
                is_correct=random.random() < 0.1,
                rating=random.randint(-5, 5),
                created_at=created_at
            )
            answers.append(answer)

        self.stdout.write(f"Creating {ratio * 200} question likes...")
        for _ in tqdm(range(ratio * 200)):
            user = random.choice(users)
            question = random.choice(questions)
            if not QuestionLike.objects.filter(user=user, question=question).exists():
                QuestionLike.objects.create(
                    user=user,
                    question=question,
                    value=random.choice([-1, 1])
                )

        self.stdout.write(f"Creating {ratio * 200} answer likes...")
        for _ in tqdm(range(ratio * 200)):
            user = random.choice(users)
            answer = random.choice(answers)
            if not AnswerLike.objects.filter(user=user, answer=answer).exists():
                AnswerLike.objects.create(
                    user=user,
                    answer=answer,
                    value=random.choice([-1, 1])
                )

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created database:\n'
            f'- Users: {ratio}\n'
            f'- Questions: {ratio * 10}\n'
            f'- Answers: {ratio * 100}\n'
            f'- Tags: {ratio}\n'
            f'- Question likes: {ratio * 200}\n'
            f'- Answer likes: {ratio * 200}'
        ))