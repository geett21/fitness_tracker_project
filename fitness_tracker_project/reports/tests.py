from django.test import SimpleTestCase


class ReportsSmokeTests(SimpleTestCase):
    def test_reports_dashboard_url_is_available(self):
        response = self.client.get("/reports/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response["Location"])
