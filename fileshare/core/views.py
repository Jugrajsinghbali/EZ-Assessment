from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, FileUploadSerializer
from .models import User, FileUpload
from .tasks import send_verification_email
from cryptography.fernet import Fernet
from django.conf import settings
import base64
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from rest_framework.generics import ListAPIView


fernet = Fernet(settings.FERNET_KEY.encode())

def generate_verification_token(email):
    return fernet.encrypt(email.encode()).decode()

def decode_verification_token(token):
    return fernet.decrypt(token.encode()).decode()

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # generate verification token
            token = generate_verification_token(user.email)
            verification_link = f"http://localhost:8000/api/verify-email/{token}/"
            # send email using celery
            send_verification_email.delay(user.email, verification_link)
            return Response({'message': 'User registered, please verify your email'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def get(self, request, token):
        try:
            email = decode_verification_token(token)
            user = User.objects.get(email=email)
            user.email_verified = True
            user.save()
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid or expired verification link'}, status=status.HTTP_400_BAD_REQUEST)

class FileUploadView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != 'ops':
            raise PermissionDenied("Only Ops users can upload files.")
        serializer.save(uploaded_by=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_download_link(request, file_id):
    if request.user.role != 'client':
        return JsonResponse({'error': 'Only clients can access download link.'}, status=403)
    
    token = fernet.encrypt(str(file_id).encode()).decode()
    download_link = f"http://localhost:8000/api/download-file/{token}/"
    
    return JsonResponse({'download-link': download_link, 'message': 'success'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_file(request, token):
    if request.user.role != 'client':
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        file_id = fernet.decrypt(token.encode()).decode()
        file_obj = FileUpload.objects.get(pk=file_id)
        return FileResponse(file_obj.file.open(), as_attachment=True)
    except:
        raise Http404("Invalid or expired link")
    
class FileListView(ListAPIView):
    queryset = FileUpload.objects.all()
    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != 'client':
            raise PermissionDenied("Only client users can view file list.")
        return super().get_queryset()