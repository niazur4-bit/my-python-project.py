import shutil
import tempfile
from datetime import date, time

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from services.models import Service
from .models import Appointment, AppointmentDocument

User = get_user_model()


class AppointmentReplyTests(TestCase):
    def setUp(self):
        self.service = Service.objects.create(title="Income Tax Filing", short_description="x", description="y")
        self.client_user = User.objects.create_user(username="client1", password="pass12345", email="client1@test.com")
        self.staff_user = User.objects.create_user(username="staff1", password="pass12345", is_staff=True)
        self.appointment = Appointment.objects.create(
            user=self.client_user,
            name="Client One",
            email="client1@test.com",
            phone="0300-0000000",
            service=self.service,
            preferred_date=date(2026, 8, 1),
            preferred_time=time(11, 0),
        )

    def test_has_reply_false_by_default(self):
        self.assertFalse(self.appointment.has_reply)

    def test_has_reply_true_after_reply_set(self):
        self.appointment.admin_reply = "We will see you then."
        self.appointment.save()
        self.assertTrue(self.appointment.has_reply)

    def test_non_staff_cannot_access_reply_view(self):
        self.client.login(username="client1", password="pass12345")
        response = self.client.get(reverse("dashboard:appointment_reply", args=[self.appointment.pk]))
        self.assertNotEqual(response.status_code, 200)

    def test_staff_can_submit_reply_and_it_is_saved(self):
        self.client.login(username="staff1", password="pass12345")
        response = self.client.post(
            reverse("dashboard:appointment_reply", args=[self.appointment.pk]),
            {"form_name": "reply", "status": "confirmed", "admin_reply": "Confirmed, see you then."},
        )
        self.assertEqual(response.status_code, 302)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, "confirmed")
        self.assertEqual(self.appointment.admin_reply, "Confirmed, see you then.")
        self.assertIsNotNone(self.appointment.replied_at)

    def test_reply_visible_on_client_my_appointments_page(self):
        self.appointment.admin_reply = "Please bring your CNIC copy."
        self.appointment.save()
        self.client.login(username="client1", password="pass12345")
        response = self.client.get(reverse("appointments:my_appointments"))
        self.assertContains(response, "Please bring your CNIC copy.")


class AppointmentDocumentTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._temp_media = tempfile.mkdtemp()
        cls._override = override_settings(PRIVATE_MEDIA_ROOT=cls._temp_media)
        cls._override.enable()

    @classmethod
    def tearDownClass(cls):
        cls._override.disable()
        shutil.rmtree(cls._temp_media, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.service = Service.objects.create(title="Income Tax Filing", short_description="x", description="y")
        self.client_user = User.objects.create_user(username="client1", password="pass12345", email="client1@test.com")
        self.other_client = User.objects.create_user(username="client2", password="pass12345", email="client2@test.com")
        self.staff_user = User.objects.create_user(username="staff1", password="pass12345", is_staff=True)
        self.appointment = Appointment.objects.create(
            user=self.client_user,
            name="Client One",
            email="client1@test.com",
            phone="0300-0000000",
            service=self.service,
            preferred_date=date(2026, 8, 1),
            preferred_time=time(11, 0),
        )

    def _pdf(self, name="cnic.pdf"):
        return SimpleUploadedFile(name, b"%PDF-1.4 fake content", content_type="application/pdf")

    def test_client_can_upload_document_to_own_appointment(self):
        self.client.login(username="client1", password="pass12345")
        response = self.client.post(
            reverse("appointments:detail", args=[self.appointment.pk]),
            {"file": self._pdf(), "note": "CNIC copy"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.appointment.documents.count(), 1)
        doc = self.appointment.documents.first()
        self.assertEqual(doc.uploaded_by, self.client_user)
        self.assertFalse(doc.uploaded_by_staff)

    def test_client_cannot_view_someone_elses_appointment(self):
        self.client.login(username="client2", password="pass12345")
        response = self.client.get(reverse("appointments:detail", args=[self.appointment.pk]))
        self.assertEqual(response.status_code, 404)

    def test_staff_can_upload_document_via_reply_page(self):
        self.client.login(username="staff1", password="pass12345")
        response = self.client.post(
            reverse("dashboard:appointment_reply", args=[self.appointment.pk]),
            {"form_name": "document", "file": self._pdf("return.pdf"), "note": "Completed tax return"},
        )
        self.assertEqual(response.status_code, 302)
        doc = self.appointment.documents.first()
        self.assertEqual(doc.uploaded_by, self.staff_user)
        self.assertTrue(doc.uploaded_by_staff)

    def test_rejects_disallowed_file_type(self):
        self.client.login(username="client1", password="pass12345")
        bad_file = SimpleUploadedFile("virus.exe", b"MZ fake exe", content_type="application/octet-stream")
        response = self.client.post(
            reverse("appointments:detail", args=[self.appointment.pk]),
            {"file": bad_file, "note": "test"},
        )
        self.assertEqual(response.status_code, 200)  # re-renders with form error
        self.assertEqual(self.appointment.documents.count(), 0)

    def test_owner_can_download_document(self):
        doc = AppointmentDocument.objects.create(
            appointment=self.appointment, uploaded_by=self.client_user, file=self._pdf(), note="CNIC"
        )
        self.client.login(username="client1", password="pass12345")
        response = self.client.get(reverse("appointments:document_download", args=[doc.pk]))
        self.assertEqual(response.status_code, 200)

    def test_staff_can_download_any_document(self):
        doc = AppointmentDocument.objects.create(
            appointment=self.appointment, uploaded_by=self.client_user, file=self._pdf(), note="CNIC"
        )
        self.client.login(username="staff1", password="pass12345")
        response = self.client.get(reverse("appointments:document_download", args=[doc.pk]))
        self.assertEqual(response.status_code, 200)

    def test_other_client_cannot_download_document(self):
        doc = AppointmentDocument.objects.create(
            appointment=self.appointment, uploaded_by=self.client_user, file=self._pdf(), note="CNIC"
        )
        self.client.login(username="client2", password="pass12345")
        response = self.client.get(reverse("appointments:document_download", args=[doc.pk]))
        self.assertEqual(response.status_code, 404)

    def test_anonymous_cannot_download_document(self):
        doc = AppointmentDocument.objects.create(
            appointment=self.appointment, uploaded_by=self.client_user, file=self._pdf(), note="CNIC"
        )
        response = self.client.get(reverse("appointments:document_download", args=[doc.pk]))
        self.assertEqual(response.status_code, 302)  # redirected to login
