#!/usr/bin/env python
import os
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Voters_system.settings')
django.setup()

from elections.models import Candidate, CustomUser
from django.template import Template, Context
from django.template.loader import get_template

# التحقق من بيانات المرشحين
candidates = Candidate.objects.all()
print('تحليل بيانات المرشحين في القوالب:')
print('=' * 60)

for candidate in candidates:
    print(f'\nالمرشح: {candidate.user.full_name}')
    print(f'معرف المستخدم: {candidate.user.id}')
    print(f'نوع المستخدم: {candidate.user.user_type}')
    print(f'الصورة الشخصية: {candidate.profile_image}')
    print(f'updated_at موجود: {hasattr(candidate.user, "updated_at")}')
    
    if hasattr(candidate.user, 'updated_at'):
        print(f'تاريخ التحديث: {candidate.user.updated_at}')
        print(f'timestamp: {candidate.user.updated_at.timestamp() if candidate.user.updated_at else "None"}')
    
    # اختبار شرط القالب
    if candidate.profile_image:
        print('✅ شرط candidate.profile_image صحيح')
        print(f'URL الصورة: {candidate.profile_image.url}')
        
        # محاكاة ما يحدث في القالب
        if hasattr(candidate.user, 'updated_at') and candidate.user.updated_at:
            timestamp = int(candidate.user.updated_at.timestamp())
            full_url = f"{candidate.profile_image.url}?t={timestamp}"
            print(f'URL مع timestamp: {full_url}')
        else:
            print('❌ لا يوجد updated_at أو قيمته None')
    else:
        print('❌ شرط candidate.profile_image فاشل - سيظهر الصورة الافتراضية')
    
    print('-' * 40)

# التحقق من نموذج CustomUser
print('\nفحص نموذج CustomUser:')
user = CustomUser.objects.first()
if user:
    print(f'الحقول المتاحة: {[field.name for field in user._meta.fields]}')
    print(f'updated_at موجود: {"updated_at" in [field.name for field in user._meta.fields]}')
else:
    print('لا يوجد مستخدمون')