# coding: utf-8
"Contact views"
import datetime
from smtplib import SMTPAuthenticationError
from collections import Mapping

from flask import abort, render_template, session, url_for, views, current_app
from flask.ext.babel import lazy_gettext as _, gettext
from flask.ext.mail import Message

from cla_public.apps.base.views import ReasonsForContacting
from cla_public.apps.contact import contact
from cla_public.apps.contact.forms import ContactForm, ConfirmationForm
from cla_public.apps.checker.api import (
    post_to_case_api,
    post_to_eligibility_check_api,
    update_reasons_for_contacting,
    ApiError,
    AlreadySavedApiError,
    get_case_ref_from_api,
)
from cla_public.apps.checker.views import UpdatesMeansTest
from cla_public.libs.views import AjaxOrNormalMixin, AllowSessionOverride, SessionBackedFormView, HasFormMixin


@contact.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, max-age=0"
    response.headers["Pragma"] = "no-cache"
    return response


def create_confirmation_email(data):
    data.update(
        {
            "case_ref": session.stored.get("case_ref"),
            "callback_requested": session.stored.get("callback_requested"),
            "contact_type": session.stored.get("contact_type"),
        }
    )

    if data.get("callback_requested"):
        callback_time = session.stored.get("callback_time")
        end_time = callback_time + datetime.timedelta(minutes=30)
        data.update(
            {"callback_time_string": callback_time.strftime("%A, %d %B at %H:%M - ") + end_time.strftime("%H:%M")}
        )

    recipient = (data["full_name"], data["email"]) if data.get("full_name") else data["email"]

    session["confirmation_email"] = data["email"]

    return Message(
        gettext(u"Your Civil Legal Advice reference number"),
        recipients=[recipient],
        body=render_template("emails/confirmation.txt", data=data),
    )


class Contact(AllowSessionOverride, UpdatesMeansTest, SessionBackedFormView):
    form_class = ContactForm
    template = "contact.html"

    def get(self, *args, **kwargs):
        self.template_context = {"emergency_message": current_app.config["EMERGENCY_MESSAGE_ON"]}
        if ReasonsForContacting.GA_SESSION_KEY in session:
            self.template_context.update({"reasons_for_contacting": session[ReasonsForContacting.GA_SESSION_KEY]})
            del session[ReasonsForContacting.GA_SESSION_KEY]
        return super(Contact, self).get(*args, **kwargs)

    def already_saved(self):
        try:
            get_case_ref_from_api()
            session.store_checker_details()
            return self.redirect(url_for("contact.confirmation"))
        except ApiError:
            error_text = _(u"There was an error submitting your data. " u"Please check and try again.")

            self.form.errors["timeout"] = error_text
            return self.return_form_errors()

    def add_errors(self, el, error_list):
        for error in el:
            if isinstance(error, basestring):
                error_list.append(error)
            elif isinstance(error, Mapping):
                self.add_errors(error.values(), error_list)

    def on_valid_submit(self):
        if self.form.extra_notes.data:
            session.checker.add_note(u"User problem", self.form.extra_notes.data)
        try:
            if not self.form.adaptations.is_other_adaptation.data:
                self.clear_other_adaptation_data()
            post_to_eligibility_check_api(session.checker.notes_object())
            post_to_case_api(self.form)
            if ReasonsForContacting.MODEL_REF_SESSION_KEY in session:
                update_reasons_for_contacting(
                    session[ReasonsForContacting.MODEL_REF_SESSION_KEY], payload={"case": session.checker["case_ref"]}
                )
                del session[ReasonsForContacting.MODEL_REF_SESSION_KEY]
            session.store_checker_details()
            if self.form.email.data and current_app.config["MAIL_SERVER"]:
                current_app.mail.send(create_confirmation_email(self.form.data))
            return self.redirect(url_for("contact.confirmation"))
        except AlreadySavedApiError:
            return self.already_saved()
        except ApiError as e:
            errors = getattr(e, "errors", {})
            error_list = []
            self.add_errors(errors.values(), error_list)
            error_text = _(u"There was an error submitting your data. " u"Please check and try again.")

            if error_list:
                error_text += " - " + ", ".join(error_list)

            self.form.errors["timeout"] = error_text

            return self.return_form_errors()
        except SMTPAuthenticationError:
            self.form._fields["email"].errors.append(
                _(u"There was an error submitting your email. " u"Please check and try again or try without it.")
            )
            return self.return_form_errors()

    def dispatch_request(self, *args, **kwargs):
        if not session:
            session.checker["force_session"] = True
        return super(Contact, self).dispatch_request(*args, **kwargs)

    def clear_other_adaptation_data(self):
        self.form.adaptations.other_adaptation.data = ""
        try:
            session.checker["ContactForm"]["adaptations"]["other_adaptation"] = ""
        except KeyError:
            pass


contact.add_url_rule("/contact", view_func=Contact.as_view("get_in_touch"), methods=("GET", "POST"))


class ContactConfirmation(AjaxOrNormalMixin, HasFormMixin, views.MethodView):

    form_class = ConfirmationForm

    def get(self):
        session.clear_checker()

        confirmation_email = session.get("confirmation_email", None)
        if confirmation_email:
            del session["confirmation_email"]
        if not session.stored.get("case_ref"):
            abort(404)
        return render_template(
            "checker/result/confirmation.html", form=self.form, confirmation_email=confirmation_email
        )

    def post(self):
        is_submitted = getattr(self.form, "is_submitted", lambda: True)
        if is_submitted() and self.form.validate():
            return self.on_valid_submit()
        return self.return_form_errors()

    def on_valid_submit(self):
        if self.form.email.data and current_app.config["MAIL_SERVER"]:
            try:
                current_app.mail.send(create_confirmation_email(self.form.data))
            except SMTPAuthenticationError:
                self.form._fields["email"].errors.append(
                    _(u"There was an error submitting your email. " u"Please check and try again or try without it.")
                )
                return self.return_form_errors()
        return self.redirect(url_for("contact.confirmation"))


contact.add_url_rule(
    "/result/confirmation", view_func=ContactConfirmation.as_view("confirmation"), methods=("GET", "POST")
)
