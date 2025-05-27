from django.db import models
from django.contrib.auth.models import User, UserManager as DjangoUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Count, Q


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class TagManager(models.Manager):
    def get_popular_tags(self, count=6):
        return self.annotate(num_questions=Count('question')).order_by('-num_questions')[:count]


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    objects = TagManager()

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def get_new_questions(self):
        return self.annotate(
            num_likes=Count('questionlike', filter=Q(questionlike__value=1))
        ).order_by('-created_at')

    def get_hot_questions(self):
        return self.annotate(
            num_likes=Count('questionlike', filter=Q(questionlike__value=1))
        ).order_by('-rating', '-created_at')


class Question(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def get_answers_count(self):
        return self.answers.count()

    class Meta:
        ordering = ['-created_at']


class Answer(models.Model):
    text = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"Answer to {self.question.title}"


class UserManager(DjangoUserManager):
    def get_best_members(self, count=4):
        return self.annotate(num_answers=Count('answer')).order_by('-num_answers')[:count]



User.add_to_class('best_members', UserManager())


class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(validators=[MinValueValidator(-1), MaxValueValidator(1)])

    class Meta:
        unique_together = ('question', 'user')


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(validators=[MinValueValidator(-1), MaxValueValidator(1)])

    class Meta:
        unique_together = ('answer', 'user')
