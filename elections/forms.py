from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Voter, Pillar, Candidate, Entity

# نموذج تسجيل الدخول
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'اسم المستخدم',
            'dir': 'rtl'
        }),
        label='اسم المستخدم'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'كلمة المرور',
            'dir': 'rtl'
        }),
        label='كلمة المرور'
    )

# نموذج إضافة ناخب
class VoterForm(forms.ModelForm):
    class Meta:
        model = Voter
        fields = [
            'voter_number', 'name', 'governorate', 'district', 'sub_district',
            'card_status', 'center_name', 'center_number', 'station',
            'phone_number'
        ]
        widgets = {
            'voter_number': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl', 'required': True}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl', 'required': True}),
            'governorate': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl', 'required': True}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl', 'required': True}),
            'sub_district': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
            'card_status': forms.Select(attrs={'class': 'form-select', 'dir': 'rtl', 'required': True}, choices=[
                ('updated', 'محدث'),
                ('not_updated', 'غير محدث')
            ]),
            'center_name': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl', 'required': True}),
            'center_number': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl', 'required': True}),
            'station': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl', 'required': True}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl', 'required': True}),
        }
        labels = {
            'voter_number': 'رقم الناخب *',
            'name': 'الاسم *',
            'governorate': 'المحافظة *',
            'district': 'المنطقة *',
            'sub_district': 'الناحية',
            'card_status': 'حالة البطاقة *',
            'center_name': 'اسم المركز *',
            'center_number': 'رقم المركز *',
            'station': 'المحطة *',
            'phone_number': 'رقم الهاتف *',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # جعل جميع الحقول مطلوبة باستثناء الناحية
        for field_name, field in self.fields.items():
            if field_name != 'sub_district':
                field.required = True
        
        # تحديد خيارات حالة البطاقة
        self.fields['card_status'].choices = [
             ('', 'اختر حالة البطاقة'),
             ('updated', 'محدث'),
             ('not_updated', 'غير محدث')
         ]

# نموذج إضافة ناخب للمرشح
class VoterCandidateForm(forms.ModelForm):
    pillar = forms.ModelChoiceField(
        queryset=None,
        required=True,
        empty_label="اختر الركيزة",
        widget=forms.Select(attrs={'class': 'form-select', 'dir': 'rtl'}),
        label='الركيزة *'
    )
    
    class Meta:
        model = Voter
        fields = [
            'voter_number', 'name', 'governorate', 'district', 'sub_district',
            'card_status', 'center_name', 'center_number', 'station',
            'phone_number', 'pillar'
        ]
        widgets = {
            'voter_number': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl', 'required': True}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl', 'required': True}),
            'governorate': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl', 'required': True}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl', 'required': True}),
            'sub_district': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
            'card_status': forms.Select(attrs={'class': 'form-select', 'dir': 'rtl', 'required': True}),
            'center_name': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl', 'required': True}),
            'center_number': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl', 'required': True}),
            'station': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl', 'required': True}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl', 'required': True}),
        }
        labels = {
            'voter_number': 'رقم الناخب *',
            'name': 'الاسم *',
            'governorate': 'المحافظة *',
            'district': 'المنطقة *',
            'sub_district': 'الناحية',
            'card_status': 'حالة البطاقة *',
            'center_name': 'اسم المركز *',
            'center_number': 'رقم المركز *',
            'station': 'المحطة *',
            'phone_number': 'رقم الهاتف *',
        }
    
    def __init__(self, *args, **kwargs):
        candidate = kwargs.pop('candidate', None)
        super().__init__(*args, **kwargs)
        
        # جعل جميع الحقول مطلوبة باستثناء الناحية
        for field_name, field in self.fields.items():
            if field_name not in ['sub_district']:
                field.required = True
        
        # تحديد خيارات حالة البطاقة
        self.fields['card_status'].choices = [
            ('', 'اختر حالة البطاقة'),
            ('updated', 'محدث'),
            ('not_updated', 'غير محدث')
        ]
        
        # تحديد queryset للركائز
        if candidate:
            self.fields['pillar'].queryset = Pillar.objects.filter(candidate=candidate)
        else:
            self.fields['pillar'].queryset = Pillar.objects.none()

# نموذج إضافة ركيزة
class PillarForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        label='اسم المستخدم'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        label='كلمة المرور'
    )
    full_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        label='الاسم الكامل'
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        label='رقم الهاتف'
    )
    
    class Meta:
        model = Pillar
        fields = []
    
    def save(self, candidate, commit=True):
        # إنشاء المستخدم أولاً
        user = CustomUser.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            full_name=self.cleaned_data['full_name'],
            phone_number=self.cleaned_data['phone_number'],
            user_type='pillar'
        )
        
        # إنشاء الركيزة
        pillar = Pillar.objects.create(
            user=user,
            candidate=candidate
        )
        
        return pillar

# نموذج إضافة مرشح
class CandidateForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        label='اسم المستخدم'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        label='كلمة المرور'
    )
    full_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        label='الاسم الكامل'
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'dir': 'rtl'}),
        label='رقم الهاتف'
    )
    
    class Meta:
        model = Candidate
        fields = ['profile_image']
        widgets = {
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def save(self, entity, commit=True):
        # إنشاء المستخدم أولاً
        user = CustomUser.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            full_name=self.cleaned_data['full_name'],
            phone_number=self.cleaned_data['phone_number'],
            user_type='candidate'
        )
        
        # إنشاء المرشح
        candidate = Candidate.objects.create(
            user=user,
            entity=entity,
            profile_image=self.cleaned_data.get('profile_image')
        )
        
        return candidate

# نموذج إنشاء الكيان
class EntityForm(forms.Form):
    entity_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'اسم الكيان',
            'dir': 'rtl'
        }),
        label='اسم الكيان'
    )
    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'اسم المسؤول',
            'dir': 'rtl'
        }),
        label='اسم المسؤول'
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'اسم المستخدم',
            'dir': 'rtl'
        }),
        label='اسم المستخدم'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'كلمة المرور',
            'dir': 'rtl'
        }),
        label='كلمة المرور'
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'رقم الهاتف',
            'dir': 'rtl'
        }),
        label='رقم الهاتف'
    )
    logo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        label='شعار الكيان'
    )
    
    def save(self, commit=True):
        # إنشاء المستخدم أولاً
        user = CustomUser.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            full_name=self.cleaned_data['full_name'],
            phone_number=self.cleaned_data['phone_number'],
            user_type='entity'
        )
        
        # إنشاء الكيان
        entity = Entity.objects.create(
            user=user,
            entity_name=self.cleaned_data['entity_name'],
            logo=self.cleaned_data.get('logo')
        )
        
        return entity

# نموذج رفع ملف Excel
class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls'
        }),
        label='ملف Excel'
    )
    pillar = forms.ModelChoiceField(
        queryset=Pillar.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select', 'dir': 'rtl'}),
        label='الركيزة المسؤولة',
        required=False
    )
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user.user_type == 'candidate':
            candidate = Candidate.objects.get(user=user)
            self.fields['pillar'].queryset = candidate.pillars.all()
        elif user.user_type == 'entity':
            entity = Entity.objects.get(user=user)
            self.fields['pillar'].queryset = Pillar.objects.filter(candidate__entity=entity)