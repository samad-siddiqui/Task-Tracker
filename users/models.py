from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):

    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('QA', 'QA'),
        ('developer', 'Developer'),
        ('engineer', 'Engineer'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    image = models.ImageField(
        default='default.jpg', blank=True,
        upload_to='profile_pics/')

    contact = models.IntegerField(blank=True, null=True)

    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='developer')

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Project(models.Model):

    title = models.CharField(max_length=20, blank=False)
    description = models.TextField(max_length=500, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    team_member = models.ManyToManyField(User, related_name="projects")

    def __str__(self):
        return self.title


class Task(models.Model):

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('review', 'Review'),
        ('working', 'Working'),
        ('awaiting_release', 'Awaiting Release'),
        ('waiting_qa', 'Waiting QA')
    ]
    title = models.CharField(max_length=20, blank=False)
    description = models.TextField(max_length=500, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open'
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="tasks")
    assignee = models.ForeignKey(
        Profile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="tasks")

    def __str__(self):
        return self.title

    @property
    def get_comments(self):
        return self.comments.all()


class Document(models.Model):
    name = models.CharField(max_length=10, blank=False)
    description = models.TextField(max_length=500, blank=True)
    file = models.FileField(upload_to='documents/')
    version = models.FloatField(default=1.0)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="documents")

    def __str__(self):
        return f"{self.name} (v{self.version})"


class Comment(models.Model):
    text = models.TextField(max_length=500, blank=False, null=True)
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.task.title}"
