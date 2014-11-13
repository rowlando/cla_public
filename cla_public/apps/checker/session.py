from flask.sessions import SecureCookieSession, SecureCookieSessionInterface

from cla_public.apps.checker.constants import F2F_CATEGORIES, NO, \
    PASSPORTED_BENEFITS, YES


class CheckerSession(SecureCookieSession):
    "Provides some convenience properties for inter-page logic"

    @property
    def needs_face_to_face(self):
        return self.get('ProblemForm_categories') in F2F_CATEGORIES

    @property
    def has_savings(self):
        return self.get('AboutYouForm_have_savings', NO) == YES

    @property
    def owns_property(self):
        return self.get('AboutYouForm_own_property', NO) == YES

    @property
    def is_on_benefits(self):
        return self.get('AboutYouForm_on_benefits', NO) == YES

    @property
    def is_on_passported_benefits(self):
        benefits = set(self.get('YourBenefitsForm_benefits', []))
        return bool(benefits.intersection(PASSPORTED_BENEFITS))

    @property
    def has_tax_credits(self):
        has_children = self.get('AboutYouForm_have_children', NO) == YES
        is_carer = self.get('AboutYouForm_have_dependants', NO) == YES
        benefits = set(self.get('YourBenefitsForm_benefits', []))
        other_benefits = bool(benefits.difference(PASSPORTED_BENEFITS))
        return has_children or is_carer or other_benefits

    @property
    def has_children(self):
        return self.get('AboutYouForm_have_children', NO) == YES

    @property
    def has_partner(self):
        partner = self.get('AboutYouForm_have_partner', NO) == YES
        in_dispute = self.get('AboutYouForm_in_dispute', NO) == YES
        return partner and not in_dispute

    @property
    def is_employed(self):
        return self.get('AboutYouForm_is_employed', NO) == YES

    @property
    def is_self_employed(self):
        return self.get('AboutYouForm_is_self_employed', NO) == YES


class CheckerSessionInterface(SecureCookieSessionInterface):
    session_class = CheckerSession