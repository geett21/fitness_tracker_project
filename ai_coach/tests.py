import json
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse


class AiCoachTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        user = user_model.objects.create_user(
            username="coach-test-user",
            email="coach-test@example.com",
            phone="1234567890",
            password="TestPassword!42",
        )
        self.client.force_login(user)

    def test_ai_coach_page_loads(self):
        response = self.client.get(reverse('ai_coach'))
        self.assertEqual(response.status_code, 200)

    def test_ai_coach_reply_returns_json(self):
        url = reverse('ai_coach_reply') + '?q=What should I eat after training?'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertIn('reply', response.json())

    def test_chat_page_uses_api_endpoint(self):
        response = self.client.get(reverse('ai_coach:chat'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/ai-coach/api/chat/')

    @patch('ai_coach.views._generate_coach_reply', return_value='Hydrate and keep protein balanced.')
    def test_chat_api_returns_json_response(self, mock_generate):
        url = reverse('ai_coach:api_chat')
        response = self.client.post(url, {'question': 'What should I eat after a workout?'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.json())
        self.assertEqual(response.json()['response'], 'Hydrate and keep protein balanced.')
        mock_generate.assert_called_once_with('What should I eat after a workout?')

    @patch('ai_coach.views._generate_coach_reply', return_value='Hydrate and keep protein balanced.')
    def test_chat_route_accepts_ajax_json_post(self, mock_generate):
        url = reverse('ai_coach:chat')
        response = self.client.post(
            url,
            data=json.dumps({'message': 'What should I eat after a workout?'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['response'], 'Hydrate and keep protein balanced.')
        mock_generate.assert_called_once_with('What should I eat after a workout?')

    @override_settings(OPENAI_API_KEY='')
    def test_chat_falls_back_when_api_key_is_missing(self):
        url = reverse('ai_coach:api_chat')
        response = self.client.post(
            url,
            data=json.dumps({'question': 'What should I eat after a workout?'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.json())
        response_text = response.json()['response'].lower()
        self.assertIn('protein', response_text)
        self.assertIn('carbohydrates', response_text)
        self.assertIn('water', response_text)

    @override_settings(OPENAI_API_KEY='')
    def test_chat_greeting_returns_helpful_response(self):
        url = reverse('ai_coach:api_chat')
        response = self.client.post(
            url,
            data=json.dumps({'question': 'hi'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        response_text = response.json()['response'].lower()
        self.assertIn('hi', response_text)
        self.assertIn('workouts', response_text)
