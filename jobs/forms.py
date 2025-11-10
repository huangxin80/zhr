from django import forms
from .models import Job, Application


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'category', 'description', 'requirements', 'salary', 'salary_type',
                  'location', 'duration', 'positions', 'contact']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '请输入职位标题'
            }),
            'category': forms.Select(attrs={
                'class': 'form-input'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': '请详细描述工作内容',
                'rows': 5
            }),
            'requirements': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': '请描述任职要求（可选）',
                'rows': 3
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '请输入薪资',
                'step': '0.01'
            }),
            'salary_type': forms.Select(attrs={
                'class': 'form-input'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '请输入工作地点'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '例如：每天2小时，共5天'
            }),
            'positions': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '请输入招聘人数',
                'min': '1'
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '请输入联系方式（手机或微信）'
            }),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': '请简单介绍自己，说明为什么适合这份工作',
                'rows': 4
            }),
        }
