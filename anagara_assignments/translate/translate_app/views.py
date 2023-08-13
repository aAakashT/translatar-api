from .utils import translator_function
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from googletrans import Translator
from .utils import TranslationCache
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging
from .models import TranslationLog
# Create your views here.

class TranslationAPI(APIView):
    # define permission and authentication classes
    permission_classes = [IsAuthenticated,]
    authentication_classes = [JWTAuthentication,]

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    
    def get(self, request):
        # Get source, target, and text from query parameters
        source_lang = request.query_params.get('source')
        target = request.query_params.get('target')
        target_lang = target.split()
        source_text = request.query_params.get('text')
        user = request.user if request.user.is_authenticated else None
        
        # validate input parameters
        if not source_text:
            source_text = request.data
            if not request.data:
                 # Log unsuccessful translation
                error = "Translation failed: text not provided"
                self.logger.error(error)
                if user:
                    TranslationLog.objects.create(user=user,source_text=source_text, source_language=source_lang, target_language=target_lang, translated_text=error)
                return Response({'error': 'Translation failed please provide text for translation'}, status=status.HTTP_400_BAD_REQUEST)
        if not source_lang:
             # Log unsuccessful translation
            error = "Translation failed: source language not provided"
            self.logger.error(error)
            if user:
                TranslationLog.objects.create(user=user,source_text=source_text, source_language=source_lang, target_language=target_lang, translated_text=error)
            return Response({'error': '2Translation failed please provide source language'}, status=status.HTTP_400_BAD_REQUEST)
        if not target_lang:
             # Log unsuccessful translation
            error = "Translation failed: target language not provided"
            self.logger.error(error)
        # Save the translation log in the database
            if user:
                TranslationLog.objects.create(user=user,source_text=source_text, source_language=source_lang, target_language=target_lang, translated_text=error)
            return Response({'error': 'Translation failed please provide taget language'}, status=status.HTTP_400_BAD_REQUEST)

        
        # check if translation is already cached
        cached_translation = TranslationCache.get_translation(source_text, source_lang, target_lang)


        if cached_translation:
            # return cashed translation
            response_data = {
                'source_text': source_text,
                'translated_text': cached_translation,
                'source_language': source_lang,
                'target_language': target_lang,
                'from cache': "true"
            }
             # Log successful translation
            self.logger.info(f"Translation successful: Source: {source_text}, Source Language: {source_lang}, Target Language: {target_lang}")
            if user:
                TranslationLog.objects.create(user=user,source_text=source_text, source_language=source_lang, target_language=target_lang, translated_text=cached_translation, is_success=True)

            return Response(response_data, status=status.HTTP_200_OK)

        # translate using translator founction
        translated_data = translator_function(source_lang=source_lang, source_text=source_text, target_lang=target_lang)
        # cache the translated data
        TranslationCache.set_translation(source_text, source_lang, target_lang, translated_data)
        response_data = {
                'source_text': source_text,
                'translated_text': translated_data,
                'source_language': source_lang,
                'target_language': target_lang,
                'from cache': "false"
            }    
        if user:
            TranslationLog.objects.create(user=user,source_text=source_text, source_language=source_lang, target_language=target_lang, translated_text=translated_data, is_success = True)
        
        # return response with from cache = false
        return Response(response_data, status=status.HTTP_200_OK)

