""" Examples setting up a basic Store
"""

from django.contrib.auth.models import User, Group
from modelstore import *

class UserStore(Store):

    username        = StoreField()
    first_name      = StoreField()
    last_name       = StoreField()
    full_name       = StoreField(get_value=ObjectMethod('get_full_name'))
    date_joined     = StoreField(get_value=ValueMethod('strftime', '%Y-%m-%d %H:%M:%S'))
    groups          = ReferenceField()

    class Meta(object):
        objects = User.objects.all()
        identifier = 'id' # Defaults to __id__ if not set

        label = 'full_name' # Defaults to __label__
                            # or not set in store at all if label = None

        # You can also specify custom get_label(obj) and get_identifier(obj) methods
        # in the store:
        #
        # class Meta(object):
        #     label = 'custom_label_field'
        #     identifier = 'custom_identifier_field'
        #
        # def get_label(self, obj):
        #     return 'custom label for obj'
        #
        # def get_identifier(self, obj):
        #     """ Just keeps a running count of objects
        #     """
        #     try:
        #         self.cur_id += 1
        #     except AttributeError:
        #         self.cur_id = 1
        #     return self.cur_id

class GroupStore(Store):

    name        = StoreField()
    users       = ReferenceField(model_field='user_set')

    class Meta(object):
        objects = Group.objects.all()
        label = 'name'
