from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import CompilationRecord
from .pipeline import compile_code, run_code
from .serializers import (
    CompileRequestSerializer,
    CompilationRecordSerializer,
    RunRequestSerializer,
)


class CompileView(APIView):
    def post(self, request):
        serializer = CompileRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if data['source_language'] == data['target_language']:
            return Response({'detail': 'Source and target language must differ.'}, status=status.HTTP_400_BAD_REQUEST)

        result = compile_code(data['source_language'], data['target_language'], data['code'])
        CompilationRecord.objects.create(
            source_code=data['code'],
            source_language=data['source_language'],
            target_language=data['target_language'],
            tokens_file_path=result['tokens_file'],
            ast_file_path=result['ast_file'],
            ir_file_path=result['ir_file'],
            converted_code=result['converted_code'],
            original_output=result['original_output'],
            converted_output=result['converted_output'],
        )
        return Response(result, status=status.HTTP_200_OK)


class RunCodeView(APIView):
    def post(self, request):
        serializer = RunRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        output = run_code(serializer.validated_data['language'], serializer.validated_data['code'])
        return Response({'output': output}, status=status.HTTP_200_OK)


class HistoryView(APIView):
    def get(self, request):
        rows = CompilationRecord.objects.order_by('-timestamp')[:100]
        return Response(CompilationRecordSerializer(rows, many=True).data, status=status.HTTP_200_OK)
