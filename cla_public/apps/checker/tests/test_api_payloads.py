from mock import Mock
import unittest

import flask
from werkzeug.datastructures import MultiDict

from cla_public import app
from cla_public.apps.checker.forms import YourBenefitsForm


class TestApiPayloads(unittest.TestCase):

    def setUp(self):
        self.app = app.create_app('config/testing.py')
        self.app = self.app.test_client()

    def payload(self, form_class, form_data):
        form_class._get_translations = lambda args: None
        form = form_class(MultiDict(form_data), csrf_enabled=False)
        return form.api_payload()

    def test_your_benefits_form_passported(self):
        form_data = {'benefits': ['income_support']}
        payload = self.payload(YourBenefitsForm, form_data)
        self.assertTrue(payload['specific_benefits']['income_support'])
        self.assertTrue(payload['on_passported_benefits'])

    def test_your_benefits_form_multiple_passported(self):
        form_data = {'benefits': ['income_support', 'pension_credit']}
        payload = self.payload(YourBenefitsForm, form_data)
        self.assertTrue(payload['specific_benefits']['income_support'])
        self.assertTrue(payload['specific_benefits']['pension_credit'])
        self.assertTrue(payload['on_passported_benefits'])

    def test_your_benefits_form_no_passported(self):
        form_data = {'benefits': ['other-benefit']}
        payload = self.payload(YourBenefitsForm, form_data)
        are_false = lambda (benefit, selected): not selected
        self.assertTrue(
            all(map(are_false, payload['specific_benefits'].items())))
        self.assertFalse(payload['on_passported_benefits'])