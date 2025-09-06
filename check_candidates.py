from elections.models import *

# البحث عن الكيان التجريبي
try:
    entity = Entity.objects.get(entity_name='الكيان التجريبي')
    print(f'تم العثور على الكيان: {entity.entity_name}')
    
    # عدد المرشحين في الكيان
    candidates = Candidate.objects.filter(entity=entity)
    print(f'عدد المرشحين في الكيان: {candidates.count()}')
    
    # تفاصيل كل مرشح
    for candidate in candidates:
        has_image = bool(candidate.profile_image)
        print(f'- {candidate.user.full_name} - صورة: {has_image}')
        if candidate.profile_image:
            print(f'  مسار الصورة: {candidate.profile_image.url}')
            
except Entity.DoesNotExist:
    print('لم يتم العثور على الكيان التجريبي')
    # عرض جميع الكيانات المتاحة
    entities = Entity.objects.all()
    print('الكيانات المتاحة:')
    for entity in entities:
        print(f'- {entity.entity_name}')