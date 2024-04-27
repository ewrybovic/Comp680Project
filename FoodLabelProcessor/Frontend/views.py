import os
import cv2

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render
from pathlib import Path

# To import local scripts in seperate folders
import sys
sys.path.append("..")

from LabelDetectionModel import LabelDetection
from LabelReader import LabelReader
import NutritionEvaluator

CFG = Path(Path.cwd().parent, "LabelDetectionModel","pipeline.config")
CKPT = Path(Path.cwd().parent, "LabelDetectionModel","checkpoint", "ckpt-3")
LABELS = Path(Path.cwd().parent, "LabelDetectionModel", "label_map.pbtxt")

label_detection = LabelDetection(CFG, CKPT, LABELS)
label_reader = LabelReader(path_to_superres_model=r"../LabelReader/ESPCN_x3.pb", is_Windows=True)

def home(request):
    return render(request, 'Frontend/home.html')

def results(request):
    found_label_data = request.session.get('found_label_data')
    uploaded_image_path = request.session.get('uploaded_image_path')
    nutrition_eval_score = request.session.get('nutrition_eval_score')
    nutrition_eval_reason = request.session['nutrition_eval_reason']
    return render(request, 'Frontend/results.html', {'uploaded_image_path': uploaded_image_path,
                                                     'found_label_data' : found_label_data,
                                                     'nutrition_eval_score' : nutrition_eval_score,
                                                     'nutrition_eval_reason' : nutrition_eval_reason,
                                                     'MEDIA_URL': settings.MEDIA_URL,})

@csrf_exempt
def analyze_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        
        # Save the image to the uploads directory
        save_path = os.path.join(settings.MEDIA_ROOT, 'uploads', image.name)
        with open(save_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        cv2_image = cv2.imread(save_path)
        cropped_image = label_detection.detect_label(cv2_image, debug=True)
        
        # Check that LabelDetectionModel found a label
        if len(cropped_image) > 0:
            label_data = label_reader.read_label(cropped_image, threshold=False, debug=True)

            # Check that LabelReader red the label properly
            if len(label_data) > 0:
                score, reason = NutritionEvaluator.ScoreNutirion(label_data)

                # Store the found label data to session
                request.session['found_label_data'] = label_data
                request.session['nutrition_eval_score'] = str(score.name)
                request.session['nutrition_eval_reason'] = reason
            else:
                print("No label data")

            # override the uploaded image with the cropped image
            cv2.imwrite(save_path, cropped_image)

            print(label_data)
        else:
            print("No label found")

        # Store the image path in the session
        request.session['uploaded_image_path'] = os.path.join('uploads', image.name)
        
        # Redirect to the results page
        return JsonResponse({'redirectURL': '/results/'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)