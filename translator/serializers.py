from rest_framework import serializers
from translator.models import Translation

class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = [
            'source_language',
            'source_text',
            'target_language',
            'target_text'
        ]
    