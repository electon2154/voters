#!/usr/bin/env python
import os
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Voters_system.settings')
django.setup()

from elections.models import Candidate
from django.conf import settings

# التحقق من الوصول للصور
candidates = Candidate.objects.all()
print('اختبار صور المرشحين:')
print('=' * 50)

for candidate in candidates:
    print(f'\nالمرشح: {candidate.user.full_name}')
    if candidate.profile_image:
        image_url = f'http://127.0.0.1:8000{candidate.profile_image.url}'
        print(f'رابط الصورة: {image_url}')
        
        # التحقق من وجود الملف في النظام
        file_path = os.path.join(settings.MEDIA_ROOT, str(candidate.profile_image))
        print(f'مسار الملف: {file_path}')
        print(f'الملف موجود: {os.path.exists(file_path)}')
        
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f'حجم الملف: {file_size} بايت')
            print('✅ الصورة موجودة في النظام')
        else:
            print('❌ الصورة غير موجودة في النظام')
    else:
        print('لا توجد صورة محفوظة')
    print('-' * 30)