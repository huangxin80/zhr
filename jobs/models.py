from django.db import models
from django.conf import settings

# Create your models here.

class Job(models.Model):
    STATUS_CHOICES = (
        ('open', '招募中'),
        ('closed', '已结束'),
    )

    CATEGORY_CHOICES = (
        ('tutoring', '家教辅导'),
        ('service', '服务类'),
        ('promotion', '推广宣传'),
        ('event', '活动助理'),
        ('tech', '技术类'),
        ('other', '其他'),
    )

    title = models.CharField(max_length=200, verbose_name='职位标题')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name='职位类别')
    description = models.TextField(verbose_name='职位描述')
    requirements = models.TextField(blank=True, verbose_name='任职要求')
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='薪资')
    salary_type = models.CharField(
        max_length=10,
        choices=(('hourly', '时薪'), ('daily', '日薪'), ('total', '总计')),
        default='hourly',
        verbose_name='薪资类型'
    )
    location = models.CharField(max_length=200, verbose_name='工作地点')
    duration = models.CharField(max_length=100, verbose_name='工作时长', help_text='例如：每天2小时，共5天')
    positions = models.IntegerField(default=1, verbose_name='招聘人数')
    contact = models.CharField(max_length=100, verbose_name='联系方式')

    publisher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='published_jobs',
        verbose_name='发布者'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open', verbose_name='状态')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '兼职任务'
        verbose_name_plural = '兼职任务'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_applied_count(self):
        """获取申请人数"""
        return self.applications.count()

    def get_accepted_count(self):
        """获取已接受的申请人数"""
        return self.applications.filter(status='accepted').count()


class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('accepted', '已接受'),
        ('rejected', '已拒绝'),
        ('withdrawn', '已撤回'),
        ('completed', '已完成'),
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='兼职任务'
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='申请者'
    )
    message = models.TextField(verbose_name='申请留言')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='状态')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='申请时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')

    class Meta:
        verbose_name = '申请记录'
        verbose_name_plural = '申请记录'
        ordering = ['-created_at']
        unique_together = ['job', 'applicant']  # 防止重复申请

    def __str__(self):
        return f'{self.applicant.username} 申请 {self.job.title}'
