""" Example setting up a combined Store
"""

from django.contrib.auth.models import User, Group
from modelstore import *

from basic_store import UserStore, GroupStore

class UserGroupStore(Store):

    class Meta(object):
        stores = (UserStore, GroupStore) # Combine the stores into a single store.
                                         # Useful when using ReferenceFields

                                         # This is a store like any other, so you
                                         # Can add fields, objects etc.

        # The other two stores will take on this store's label and identifier settings
        # in which case the defaults will be used -- ie, get_label/get_identifier on THIS store

    def get_label(self, obj):
        if isinstance(obj, User):
            return obj.get_full_name()
        else:
            return obj.name
