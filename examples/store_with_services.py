""" Example setting up a Store with servicemethods
"""

from django.contrib.auth.models import User, Group
from django.db import Model # For trapping Model.DoesNotExist
from modelstore import *
from modestore.utils import get_object_from_identifier

class UserStore(Store):

    username        = StoreField()
    first_name      = StoreField()
    last_name       = StoreField()
    full_name       = StoreField(get_value=ObjectMethod('get_full_name'))
    date_joined     = StoreField(get_value=ValueMethod('strftime', '%Y-%m-%d %H:%M:%S'))
    groups          = ReferenceField()

    class Meta(object):
        objects = User.objects.all()
        label = 'full_name'

    @servicemethod
    def add_to_groups(self, request, user_ident, group_list):
        """ Adds the User identified by user_ident to the Groups
            identified by their identifiers
        """
        try:
            # Get the user object
            user = get_object_from_identifier(user_ident, valid=User)

        # Raised if user_ident is malformed or the model didn't exist or
        # the user_ident didn't resolve to a User model  -- ie they passed auth.group__1
        except StoreException:
            raise Exception('Invalid request') # Report this error to the remote caller

        except Model.DoesNotExist: # Trap the base Model.DoesNotExist
            raise Exception('That User doesn\'t exist')

        groups = []
        for group_ident in group_list:
            try:
                group = get_object_from_identifier(group_ident, valid=Group)
            except StoreException:
                raise Exception('Invalid request')
            except Model.DoesNotExist:
                raise Exception('One or more of the specified Groups don\'t exist')
            groups.append(group)

        user.groups.add(*groups) # Add the user to the groups
        return True # Return some success value        

class GroupStore(Store):

    name        = StoreField()
    users       = ReferenceField(model_field='user_set')

    class Meta(object):
        objects = Group.objects.all()
        label = 'name'

