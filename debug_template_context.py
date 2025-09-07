#!/usr/bin/env python
import os
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Voters_system.settings')
django.setup()

from elections.models import Candidate, CustomUser
from django.template import Template, Context
from django.template.loader import get_template
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.test import RequestFactory
from elections.views import candidate_dashboard

# إنشاء طلب وهمي
factory = RequestFactory()
request = factory.get('/candidate/dashboard/')

# محاكاة مستخدم مرشح
candidate_user = CustomUser.objects.filter(user_type='candidate').first()
if candidate_user:
    request.user = candidate_user
    print(f'تسجيل دخول كمرشح: {candidate_user.full_name}')
    print(f'معرف المستخدم: {candidate_user.id}')
    print(f'updated_at: {candidate_user.updated_at}')
    
    # الحصول على بيانات المرشح
    candidate = candidate_user.candidate_profile
    print(f'صورة المرشح: {candidate.profile_image}')
    
    # اختبار القالب مباشرة
    template_code = '''
    {% load static %}
    المرشح: {{ candidate.user.full_name }}
    الصورة: {{ candidate.profile_image }}
    updated_at: {{ candidate.user.updated_at }}
    timestamp: {{ candidate.user.updated_at|date:'U' }}
    
    {% if candidate.profile_image %}
    شرط الصورة: صحيح
    URL: {{ candidate.profile_image.url }}
    URL مع timestamp: {{ candidate.profile_image.url }}?t={{ candidate.user.updated_at|date:'U' }}
    {% else %}
    شرط الصورة: خاطئ - لا توجد صورة
    {% endif %}
    '''
    
    template = Template(template_code)
    context = Context({
        'candidate': candidate,
        'request': request
    })
    
    result = template.render(context)
    print('\nنتيجة القالب:')
    print('=' * 50)
    print(result)
    
else:
    print('لا يوجد مرشحون في النظام')

# فحص جميع المرشحين
print('\nفحص جميع المرشحين:')
print('=' * 50)
for candidate in Candidate.objects.all():
    print(f'المرشح: {candidate.user.full_name}')
    print(f'الصورة: {candidate.profile_image}')
    print(f'نوع الصورة: {type(candidate.profile_image)}')
    print(f'bool(صورة): {bool(candidate.profile_image)}')
    if candidate.profile_image:
        print(f'اسم الملف: {candidate.profile_image.name}')
        print(f'URL: {candidate.profile_image.url}')
    print('-' * 30)