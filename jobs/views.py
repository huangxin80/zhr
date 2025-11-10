from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Job, Application
from .forms import JobForm, ApplicationForm

# Create your views here.

def job_list(request):
    """兼职列表页面"""
    jobs = Job.objects.filter(status='open')

    # 搜索功能
    search_query = request.GET.get('search', '')
    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    # 分类筛选
    category = request.GET.get('category', '')
    if category:
        jobs = jobs.filter(category=category)

    # 薪资类型筛选
    salary_type = request.GET.get('salary_type', '')
    if salary_type:
        jobs = jobs.filter(salary_type=salary_type)

    # 薪资范围筛选
    min_salary = request.GET.get('min_salary', '')
    max_salary = request.GET.get('max_salary', '')
    if min_salary:
        try:
            jobs = jobs.filter(salary__gte=float(min_salary))
        except ValueError:
            pass
    if max_salary:
        try:
            jobs = jobs.filter(salary__lte=float(max_salary))
        except ValueError:
            pass

    # 地点筛选
    location_filter = request.GET.get('location', '')
    if location_filter:
        jobs = jobs.filter(location__icontains=location_filter)

    # 排序功能
    order_by = request.GET.get('order_by', '-created_at')
    valid_orders = {
        'newest': '-created_at',
        'oldest': 'created_at',
        'salary_high': '-salary',
        'salary_low': 'salary',
        'positions_high': '-positions',
        'positions_low': 'positions',
    }
    if order_by in valid_orders:
        jobs = jobs.order_by(valid_orders[order_by])
    else:
        jobs = jobs.order_by('-created_at')

    context = {
        'jobs': jobs,
        'search_query': search_query,
        'category': category,
        'salary_type': salary_type,
        'min_salary': min_salary,
        'max_salary': max_salary,
        'location_filter': location_filter,
        'order_by': order_by,
        'categories': Job.CATEGORY_CHOICES,
        'salary_types': (('hourly', '时薪'), ('daily', '日薪'), ('total', '总计')),
        'total_count': jobs.count(),
    }
    return render(request, 'jobs/job_list.html', context)


def job_detail(request, pk):
    """兼职详情页面"""
    job = get_object_or_404(Job, pk=pk)

    # 检查当前用户是否已申请
    has_applied = False
    user_application = None
    if request.user.is_authenticated:
        try:
            user_application = Application.objects.get(job=job, applicant=request.user)
            has_applied = True
        except Application.DoesNotExist:
            pass

    context = {
        'job': job,
        'has_applied': has_applied,
        'user_application': user_application,
    }
    return render(request, 'jobs/job_detail.html', context)


@login_required
def job_create(request):
    """发布兼职"""
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.publisher = request.user
            job.save()
            messages.success(request, '兼职发布成功！')
            return redirect('jobs:job_detail', pk=job.pk)
        else:
            messages.error(request, '发布失败，请检查输入信息。')
    else:
        form = JobForm()

    return render(request, 'jobs/job_form.html', {'form': form, 'action': '发布兼职'})


@login_required
def job_edit(request, pk):
    """编辑兼职"""
    job = get_object_or_404(Job, pk=pk)

    # 只有发布者才能编辑
    if job.publisher != request.user:
        messages.error(request, '您无权编辑此兼职！')
        return redirect('jobs:job_detail', pk=pk)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, '兼职信息已更新！')
            return redirect('jobs:job_detail', pk=pk)
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/job_form.html', {'form': form, 'action': '编辑兼职', 'job': job})


@login_required
def job_delete(request, pk):
    """删除兼职"""
    job = get_object_or_404(Job, pk=pk)

    # 只有发布者才能删除
    if job.publisher != request.user:
        messages.error(request, '您无权删除此兼职！')
        return redirect('jobs:job_detail', pk=pk)

    if request.method == 'POST':
        job.delete()
        messages.success(request, '兼职已删除！')
        return redirect('jobs:my_published')

    return render(request, 'jobs/job_delete.html', {'job': job})


@login_required
def job_close(request, pk):
    """结束招募"""
    job = get_object_or_404(Job, pk=pk)

    # 只有发布者才能结束招募
    if job.publisher != request.user:
        messages.error(request, '您无权操作此兼职！')
        return redirect('jobs:job_detail', pk=pk)

    job.status = 'closed'
    job.save()
    messages.success(request, '招募已结束！')
    return redirect('jobs:job_detail', pk=pk)


@login_required
def apply_job(request, pk):
    """申请兼职"""
    job = get_object_or_404(Job, pk=pk)

    # 不能申请自己发布的兼职
    if job.publisher == request.user:
        messages.error(request, '您不能申请自己发布的兼职！')
        return redirect('jobs:job_detail', pk=pk)

    # 检查是否已申请
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, '您已经申请过此兼职！')
        return redirect('jobs:job_detail', pk=pk)

    # 检查兼职是否还在招募
    if job.status != 'open':
        messages.error(request, '此兼职已结束招募！')
        return redirect('jobs:job_detail', pk=pk)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, '申请提交成功！请等待发布者审核。')
            return redirect('jobs:job_detail', pk=pk)
    else:
        form = ApplicationForm()

    return render(request, 'jobs/apply_form.html', {'form': form, 'job': job})


@login_required
def my_published(request):
    """我发布的兼职"""
    jobs = Job.objects.filter(publisher=request.user)
    return render(request, 'jobs/my_published.html', {'jobs': jobs})


@login_required
def my_applications(request):
    """我的申请"""
    applications = Application.objects.filter(applicant=request.user)
    return render(request, 'jobs/my_applications.html', {'applications': applications})


@login_required
def manage_applications(request, pk):
    """管理兼职申请"""
    job = get_object_or_404(Job, pk=pk)

    # 只有发布者才能管理申请
    if job.publisher != request.user:
        messages.error(request, '您无权查看此页面！')
        return redirect('jobs:job_detail', pk=pk)

    applications = job.applications.all()
    return render(request, 'jobs/manage_applications.html', {'job': job, 'applications': applications})


@login_required
def update_application_status(request, pk, status):
    """更新申请状态"""
    application = get_object_or_404(Application, pk=pk)

    # 只有发布者才能更新申请状态
    if application.job.publisher != request.user:
        messages.error(request, '您无权操作此申请！')
        return redirect('jobs:job_detail', pk=application.job.pk)

    if status in ['accepted', 'rejected']:
        application.status = status
        application.save()
        status_text = '接受' if status == 'accepted' else '拒绝'
        messages.success(request, f'已{status_text}该申请！')

    return redirect('jobs:manage_applications', pk=application.job.pk)


@login_required
def withdraw_application(request, pk):
    """撤回申请"""
    application = get_object_or_404(Application, pk=pk)

    # 只有申请者才能撤回
    if application.applicant != request.user:
        messages.error(request, '您无权操作此申请！')
        return redirect('jobs:my_applications')

    # 只能撤回待审核的申请
    if application.status != 'pending':
        messages.error(request, '只能撤回待审核的申请！')
        return redirect('jobs:my_applications')

    application.status = 'withdrawn'
    application.save()
    messages.success(request, '申请已撤回！')
    return redirect('jobs:my_applications')


@login_required
def complete_application(request, pk):
    """完成兼职"""
    from django.utils import timezone

    application = get_object_or_404(Application, pk=pk)

    # 只有申请者或发布者才能标记完成
    if application.applicant != request.user and application.job.publisher != request.user:
        messages.error(request, '您无权操作此申请！')
        return redirect('jobs:job_detail', pk=application.job.pk)

    # 只能完成已接受的申请
    if application.status != 'accepted':
        messages.error(request, '只能完成已接受的申请！')
        return redirect('jobs:my_applications')

    application.status = 'completed'
    application.completed_at = timezone.now()
    application.save()

    if request.user == application.applicant:
        messages.success(request, '兼职已标记为完成！')
        return redirect('jobs:my_applications')
    else:
        messages.success(request, '已确认该申请者完成兼职！')
        return redirect('jobs:manage_applications', pk=application.job.pk)
