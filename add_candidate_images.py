import os
import django
from django.core.files import File
from django.core.files.storage import default_storage

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Voters_system.settings')
django.setup()

from elections.models import Entity, Candidate

# Get the test entity
try:
    entity = Entity.objects.get(entity_name="الكيان التجريبي")
    print(f"تم العثور على الكيان: {entity.entity_name}")
    
    # Get all candidates for this entity
    candidates = Candidate.objects.filter(entity=entity)
    print(f"عدد المرشحين: {candidates.count()}")
    
    # Image files to assign
    image_files = [
        'elections/images/candidate1.svg',
        'elections/images/candidate2.svg', 
        'elections/images/candidate3.svg'
    ]
    
    # Assign images to candidates
    for i, candidate in enumerate(candidates[:3]):
        if i < len(image_files):
            # Copy the static file to media directory
            static_path = f'/Users/mymac/TraeProjects/Voters/Voters_system/elections/static/{image_files[i]}'
            if os.path.exists(static_path):
                with open(static_path, 'rb') as f:
                    file_name = f'candidate_{candidate.id}.svg'
                    candidate.profile_image.save(file_name, File(f), save=True)
                    print(f"تم تعيين صورة للمرشح: {candidate.user.full_name}")
            else:
                print(f"لم يتم العثور على الملف: {static_path}")
        
    print("تم الانتهاء من تعيين الصور")
    
except Entity.DoesNotExist:
    print("لم يتم العثور على الكيان التجريبي")
except Exception as e:
    print(f"حدث خطأ: {e}")