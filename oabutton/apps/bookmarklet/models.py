from mongoengine import DateTimeField
from mongoengine import DictField
from mongoengine import Document
from mongoengine import EmailField
from mongoengine import StringField
from mongoengine import URLField
from mongoengine import BooleanField
import mongoengine.django.auth


class Event(Document):
    # Note that this has a lowercase 'e' to maintain compatibility
    meta = {'collection': 'events'}
    location = StringField()
    coords = DictField()
    accessed = DateTimeField()
    doi = StringField()
    url = URLField()
    story = StringField()
    description = StringField()
    email = EmailField()

    # This is a lookup to the user object
    user_id = StringField()

    user_name = StringField()
    user_profession = StringField()


class User(mongoengine.django.auth.User):
    """
    This model is modified from mongoengine.django.auth.User
    """
    # This meta blob is hacked from monogoengine.django.auth.User
    meta = {
        'allow_inheritance': True,
        'indexes': [
            {'fields': ['username'], 'unique': True, 'sparse': True},
            {'fields': ['email_verify_slug'], 'unique': True, 'sparse': True},
        ]
    }

    name = StringField()
    profession = StringField()
    mailinglist = BooleanField()

    # We compute SHA(email_address + salt) to get hash that we use to
    # verify the user.
    email_verify_slug = StringField()
    verified_email_expiry = DateTimeField()
    verified_email = BooleanField()
    # Limit this on a per day basis
    mail_sent_today = IntegerField()

    def get_bookmarklet_url(self):
        # generate a boilerplate URL for each user
        from django.conf import settings
        return "%s/api/bookmarklet/%s.js" % (settings.HOSTNAME, self.id)
