#!/usr/bin/env python
import os
import django

# إعداد Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Voters_system.settings')
django.setup()

from elections.models import Candidate

# التحقق من المرشحين
candidates = Candidate.objects.all()
print(f'عدد المرشحين: {candidates.count()}')
print('\nتفاصيل المرشحين:')
for candidate in candidates:
    print(f'- المرشح: {candidate.user.full_name}')
    print(f'  الصورة: {candidate.profile_image}')
    if candidate.profile_image:
        print(f'  مسار الصورة: {candidate.profile_image.url}')
    else:
        print('  لا توجد صورة')
    print('---')