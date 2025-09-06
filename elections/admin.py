from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Entity, Candidate, Pillar, Voter

# تخصيص إدارة المستخدم
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'full_name', 'user_type', 'phone_number', 'is_active', 'created_at')
    list_filter = ('user_type', 'is_active', 'created_at')
    search_fields = ('username', 'full_name', 'phone_number')
    
    fieldsets = UserAdmin.fieldsets + (
        ('معلومات إضافية', {'fields': ('user_type', 'full_name', 'phone_number')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('معلومات إضافية', {'fields': ('user_type', 'full_name', 'phone_number')}),
    )

# إدارة الكيان
class EntityAdmin(admin.ModelAdmin):
    list_display = ('entity_name', 'user', 'get_candidates_count')
    search_fields = ('entity_name', 'user__full_name')
    
    def get_candidates_count(self, obj):
        return obj.candidates.count()
    get_candidates_count.short_description = 'عدد المرشحين'

# إدارة المرشح
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'entity', 'get_pillars_count', 'get_voters_count')
    list_filter = ('entity',)
    search_fields = ('user__full_name', 'entity__entity_name')
    
    def get_full_name(self, obj):
        return obj.user.full_name
    get_full_name.short_description = 'الاسم الكامل'
    
    def get_pillars_count(self, obj):
        return obj.pillars.count()
    get_pillars_count.short_description = 'عدد الركائز'
    
    def get_voters_count(self, obj):
        return obj.voters.count()
    get_voters_count.short_description = 'عدد الناخبين'

# إدارة الركيزة
class PillarAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'candidate', 'get_voters_count')
    list_filter = ('candidate',)
    search_fields = ('user__full_name', 'candidate__user__full_name')
    
    def get_full_name(self, obj):
        return obj.user.full_name
    get_full_name.short_description = 'الاسم الكامل'
    
    def get_voters_count(self, obj):
        return obj.voters.count()
    get_voters_count.short_description = 'عدد الناخبين'

# إدارة الناخب
class VoterAdmin(admin.ModelAdmin):
    list_display = ('name', 'voter_number', 'governorate', 'district', 'card_status', 'voting_status', 'pillar', 'candidate')
    list_filter = ('governorate', 'district', 'card_status', 'voting_status', 'candidate', 'pillar')
    search_fields = ('name', 'voter_number', 'phone_number', 'center_name')
    list_editable = ('card_status', 'voting_status')
    
    fieldsets = (
        ('معلومات الناخب', {
            'fields': ('voter_number', 'name', 'phone_number')
        }),
        ('الموقع الجغرافي', {
            'fields': ('governorate', 'district', 'sub_district')
        }),
        ('معلومات المركز', {
            'fields': ('center_name', 'center_number', 'station')
        }),
        ('الحالة والانتماء', {
            'fields': ('card_status', 'voting_status', 'pillar', 'candidate')
        }),
    )

# تسجيل النماذج
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Pillar, PillarAdmin)
admin.site.register(Voter, VoterAdmin)

# تخصيص عناوين لوحة الإدارة
admin.site.site_header = 'نظام مراقبة الانتخابات'
admin.site.site_title = 'إدارة النظام'
admin.site.index_title = 'لوحة التحكم الرئيسية'
