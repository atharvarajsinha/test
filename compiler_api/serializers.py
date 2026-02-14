from rest_framework import serializers
from .models import CompilationRecord


class CompileRequestSerializer(serializers.Serializer):
    source_language = serializers.ChoiceField(choices=['python', 'java', 'cpp'])
    target_language = serializers.ChoiceField(choices=['python', 'java', 'cpp'])
    code = serializers.CharField()


class RunRequestSerializer(serializers.Serializer):
    language = serializers.ChoiceField(choices=['python', 'java', 'cpp'])
    code = serializers.CharField()


class CompilationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompilationRecord
        fields = '__all__'
