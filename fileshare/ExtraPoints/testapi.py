from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.models import User, FileUpload
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.files.uploadedfile import SimpleUploadedFile
from cryptography.fernet import Fernet
from django.conf import settings


class FileShareTestCase(APITestCase):
    def setUp(self):
        self.client_user = User.objects.create_user(
            username="client1",
            email="client@email.com",
            password="client@123",
            role="client",
            email_verified=True
        )
        self.ops_user = User.objects.create_user(
            username="ops",
            email="ops@email.com",
            password="opspass123",
            role="ops"
        )

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_signup_client(self):
        url = reverse('signup')
        data = {
            "username": "client1",
            "email": "client1@email.com",
            "password": "client@1234",
            "role": "client"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        url = reverse('token_obtain_pair')
        data = {
            "username": "client1",
            "password": "client@1234"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_email_verification(self):
        from core.views import generate_verification_token, decode_verification_token

        token = generate_verification_token("client@example.com")
        url = reverse('verify-email', args=[token])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = User.objects.get(email="client@example.com")
        self.assertTrue(user.email_verified)

    def test_signup_missing_field(self):
        url = reverse('signup')
        data = {
            "username": "incomplete",
            "password": "test123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ops_upload_valid_file(self):
        url = reverse('upload-file')
        token = self.get_token(self.ops_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        doc_file = SimpleUploadedFile("test.docx", b"dummy content", content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response = self.client.post(url, {'file': doc_file})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_upload_denied(self):
        url = reverse('upload-file')
        token = self.get_token(self.client_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        doc_file = SimpleUploadedFile("test.docx", b"dummy content", content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        response = self.client.post(url, {'file': doc_file})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_file_type(self):
        url = reverse('upload-file')
        token = self.get_token(self.ops_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        exe_file = SimpleUploadedFile("test.exe", b"malicious content", content_type="application/octet-stream")
        response = self.client.post(url, {'file': exe_file})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_generate_download_link_by_client(self):
        # Upload file by ops
        file = FileUpload.objects.create(
            uploaded_by=self.ops_user,
            file=SimpleUploadedFile("test.docx", b"content")
        )

        url = reverse('generate-download-link', args=[file.id])
        token = self.get_token(self.client_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("download-link", response.data)

    def test_download_by_client(self):
        # Upload file
        file = FileUpload.objects.create(
            uploaded_by=self.ops_user,
            file=SimpleUploadedFile("test.docx", b"content")
        )
        from cryptography.fernet import Fernet
        fernet = Fernet(settings.FERNET_KEY)
        token = fernet.encrypt(str(file.id).encode()).decode()

        url = reverse('download-file', args=[token])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_token(self.client_user))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_download_by_ops(self):
        # Upload file
        file = FileUpload.objects.create(
            uploaded_by=self.ops_user,
            file=SimpleUploadedFile("test.docx", b"content")
        )
        from cryptography.fernet import Fernet
        fernet = Fernet(settings.FERNET_KEY)
        token = fernet.encrypt(str(file.id).encode()).decode()

        url = reverse('download-file', args=[token])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.get_token(self.ops_user))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
