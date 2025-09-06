from .models import AppearanceSettings

def appearance_settings(request):
    """
    Context processor لإضافة إعدادات المظهر إلى جميع القوالب
    """
    settings = AppearanceSettings.get_active_settings()
    
    if settings:
        return {
            'appearance_settings': {
                'primary_color': settings.primary_color,
                'secondary_color': settings.secondary_color,
                'button_text_color': settings.button_text_color,
                'card_title_color': settings.card_title_color,
            }
        }
    else:
        # القيم الافتراضية في حالة عدم وجود إعدادات
        return {
            'appearance_settings': {
                'primary_color': '#007bff',
                'secondary_color': '#6c757d',
                'button_text_color': '#ffffff',
                'card_title_color': '#212529',
            }
        }