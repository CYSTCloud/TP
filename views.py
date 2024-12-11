from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from translator.models import Translation
from translator.serializers import TranslationSerializer
import requests
from django.conf import settings

try:
    from drf_yasg.utils import swagger_auto_schema
    DRF_YASG_INSTALLED = True
except ImportError:
    DRF_YASG_INSTALLED = False


class TranslationAPI(APIView):
    """
    API endpoint to handle translations between languages.
    """

    @swagger_auto_schema(
        operation_summary="Retrieve all translations",
        responses={200: TranslationSerializer(many=True)}
    ) if DRF_YASG_INSTALLED else None
    def get(self, request):
        """
        Handle GET request: retrieve all translations from the database.
        """
        translations = Translation.objects.all()
        serializer = TranslationSerializer(translations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new translation",
        request_body=TranslationSerializer,
        responses={
            201: TranslationSerializer,
            400: "Invalid request. Missing required fields.",
        }
    ) if DRF_YASG_INSTALLED else None
    def post(self, request):
        
        """
        Handle POST request: create a new translation using the Gemini API.
        """
        # 1. Récupérer les données de la requête
        print("Requête reçue :", request.data)  # Debugging
        source_language = request.data.get("source_language")
        target_language = request.data.get("target_language")
        source_text = request.data.get("source_text")

        # 2. Vérifier que toutes les données sont présentes
        if not (source_language and target_language and source_text):
            return Response(
                {"error": "source_language, target_language, and source_text are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Appeler l'API Gemini pour effectuer la traduction
        gemini_url = "https://ai.google.dev/gemini-api/translate"
        headers = {"Authorization": f"Bearer {settings.GEMINI_API_KEY}"}
        payload = {
            "source_language": source_language,
            "target_language": target_language,
            "text": source_text
        }

        try:
            gemini_response = requests.post(gemini_url, headers=headers, json=payload)
            gemini_data = gemini_response.json()

            if gemini_response.status_code == 200:
                # 4. Récupérer le texte traduit
                translated_text = gemini_data.get("translated_text")
                # 5. Sauvegarder la traduction dans la base de données
                translation = Translation.objects.create(
                    source_language=source_language,
                    target_language=target_language,
                    source_text=source_text,
                    target_text=translated_text
                )
                serializer = TranslationSerializer(translation)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"error": gemini_data.get("error", "Translation failed")},
                    status=gemini_response.status_code
                )

        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def index(request):
    """
    A simple index view for rendering the home page.
    """
    return render(request, 'index.html', context={})
