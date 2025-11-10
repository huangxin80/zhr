from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', '学生'),
        ('employer', '雇主'),
    )

    phone = models.CharField(max_length=11, blank=True, verbose_name='手机号')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student', verbose_name='用户类型')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username
