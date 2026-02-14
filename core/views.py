import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .ml_utils import FEATURES, ValidationError, validate_and_build_features, predict_diabetes


def home_view(request):
    return render(request, 'core/home.html', {'features': FEATURES})


def predict_view(request):
    if request.method != 'POST':
        return render(request, 'core/home.html', {'features': FEATURES, 'error': 'Use the form to submit values.'})

    payload = {feature: request.POST.get(feature) for feature in FEATURES}
    try:
        feature_array = validate_and_build_features(payload)
        result = predict_diabetes(feature_array)
    except ValidationError as exc:
        return render(request, 'core/home.html', {'features': FEATURES, 'error': str(exc)})
    except FileNotFoundError:
        return render(request, 'core/home.html', {'features': FEATURES, 'error': 'Model file not found. Run train.py first.'})

    return render(request, 'core/result.html', {'result': result})


@csrf_exempt
def predict_api_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST is supported'}, status=405)

    try:
        payload = json.loads(request.body.decode('utf-8'))
        feature_array = validate_and_build_features(payload)
        result = predict_diabetes(feature_array)
        return JsonResponse({'prediction': result['prediction'], 'probability': result['probability']})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
    except ValidationError as exc:
        return JsonResponse({'error': str(exc)}, status=400)
    except FileNotFoundError:
        return JsonResponse({'error': 'Model file not found. Run train.py first.'}, status=500)
