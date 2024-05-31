from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import pickle


@api_view(['POST'])
@csrf_exempt
def classifytext(request):
    data = request.data
    text = data['data']
    # loading the model
    model_file_path = 'Businessclassifier_model.pkl'
    with open(model_file_path, 'rb') as file:
         classifier1 = pickle.load(file)
    with open('BusinessClassifier_model_vectorizer.pkl', 'rb') as file:
        vectorizer = pickle.load(file)
    new_text = [text]
    new_text_vect = vectorizer.transform(new_text)  # Vectorize the new text using the same vectorizer
    predicted_category = classifier1.predict(new_text_vect)
    print("Predicted category:", predicted_category)
    return JsonResponse({'prediction':predicted_category[0]}, status=status.HTTP_200_OK)