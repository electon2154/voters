from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# نموذج المستخدم المخصص
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('admin', 'إدارة'),
        ('entity', 'كيان'),
        ('candidate', 'مرشح'),
        ('pillar', 'ركيزة'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='pillar')
    full_name = models.CharField(max_length=200, verbose_name='الاسم الكامل')
    phone_number = models.CharField(max_length=15, verbose_name='رقم الهاتف', blank=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاريخ الإنشاء')

    class Meta:
        verbose_name = 'مستخدم'
        verbose_name_plural = 'المستخدمون'

# نموذج الكيان
class Entity(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='entity_profile')
    entity_name = models.CharField(max_length=200, verbose_name='اسم الكيان')
    logo = models.ImageField(upload_to='entity_logos/', verbose_name='شعار الكيان', blank=True)
    
    class Meta:
        verbose_name = 'كيان'
        verbose_name_plural = 'الكيانات'
    
    def __str__(self):
        return self.entity_name

# نموذج المرشح
class Candidate(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='candidate_profile')
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='candidates', verbose_name='الكيان')
    profile_image = models.ImageField(upload_to='candidate_images/', verbose_name='الصورة الشخصية', blank=True)
    
    class Meta:
        verbose_name = 'مرشح'
        verbose_name_plural = 'المرشحون'
    
    def __str__(self):
        return self.user.full_name

# نموذج الركيزة
class Pillar(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='pillar_profile')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='pillars', verbose_name='المرشح')
    
    class Meta:
        verbose_name = 'ركيزة'
        verbose_name_plural = 'الركائز'
    
    def __str__(self):
        return self.user.full_name

# نموذج الناخب
class Voter(models.Model):
    CARD_STATUS_CHOICES = (
        ('updated', 'محدث'),
        ('not_updated', 'غير محدث'),
    )
    
    VOTING_STATUS_CHOICES = (
        ('voted', 'صوت'),
        ('not_voted', 'لم يصوت'),
    )
    
    voter_number = models.CharField(max_length=50, unique=True, verbose_name='رقم الناخب')
    name = models.CharField(max_length=200, verbose_name='الاسم')
    governorate = models.CharField(max_length=100, verbose_name='المحافظة')
    district = models.CharField(max_length=100, verbose_name='المنطقة')
    sub_district = models.CharField(max_length=100, verbose_name='الناحية')
    card_status = models.CharField(max_length=20, choices=CARD_STATUS_CHOICES, default='not_updated', verbose_name='حالة البطاقة')
    center_name = models.CharField(max_length=200, verbose_name='اسم المركز')
    center_number = models.CharField(max_length=50, verbose_name='رقم المركز')
    station = models.CharField(max_length=100, verbose_name='المحطة')
    phone_number = models.CharField(max_length=15, verbose_name='رقم الهاتف', blank=True)
    pillar = models.ForeignKey(Pillar, on_delete=models.CASCADE, related_name='voters', verbose_name='الركيزة')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='voters', verbose_name='المرشح')
    voting_status = models.CharField(max_length=20, choices=VOTING_STATUS_CHOICES, default='not_voted', verbose_name='حالة التصويت')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='تاريخ الإضافة')
    
    class Meta:
        verbose_name = 'ناخب'
        verbose_name_plural = 'الناخبون'
    
    def __str__(self):
        return f"{self.name} - {self.voter_number}"
