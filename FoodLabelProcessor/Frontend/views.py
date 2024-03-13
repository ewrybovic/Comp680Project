import os
import cv2

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render

# To import local scripts in seperate folders
import sys
sys.path.append("..")

from LabelDetectionModel import LabelDetection
from LabelReader import LabelReader

label_detection = LabelDetection()
label_reader = LabelReader()

def home(request):
    return render(request, 'Frontend/home.html')

def results(request):
    uploaded_image_path = request.session.get('uploaded_image_path')
    return render(request, 'Frontend/results.html', {'uploaded_image_path': uploaded_image_path,
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
        print(label_reader.read_label(cropped_image))

        # Store the image path in the session
        request.session['uploaded_image_path'] = os.path.join('uploads', image.name)
        
        # Redirect to the results page
        return JsonResponse({'redirectURL': '/results/'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)