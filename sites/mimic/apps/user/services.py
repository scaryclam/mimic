import uuid

from django.template import loader, Context

from apps.user import models


class UserService(object):
    def create_user(self, username, email, first_name="", last_name="", password=None, is_staff=False, is_superuser=False):
        created = False
        try:
            user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            user = models.User.objects.create(username=username,
                                              email=email,
                                              is_staff=is_staff,
                                              is_superuser=is_superuser)
            created = True
        if password:
            user.set_password(password)
        user.save()
        return user, created


class RegistrationService(object):
    def create_password_link(self, user):
        code = str(uuid.uuid4())
        return models.PasswordLink.objects.create(user=user, code=code)

    def send_password_link(self, link, recipient, subject, sender, email_template_html, email_template_text):
        html_template = loader.get_template(email_template_html)
        text_template = loader.get_template(email_template_text)
        context = Context({"link": link})
        rendered_html = html_template.render(context)
        rendered_text = text_template.render(context)

        send_email(subject, sender, [recipient], rendered_html, rendered_text)

    def get_link_by_code(self, code):
        try:
            link = models.PasswordLink.objects.get(code=code)
        except models.PasswordLink.DoesNotExist:
            link = None
        return link

