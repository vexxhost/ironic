# vim: tabstop=4 shiftwidth=4 softtabstop=4

# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import wsme
from wsme import types as wtypes


class APIBase(wtypes.Base):

    def as_dict(self):
        """Render this object as a dict of its fields."""
        return dict((k, getattr(self, k))
                    for k in self.fields
                    if hasattr(self, k) and
                    getattr(self, k) != wsme.Unset)

    # TODO(lucasagomes): Deprecated. Remove it after updating the chassis
    #                    and nodes elements
    @classmethod
    def from_rpc_object(cls, m, fields=None):
        """Convert a RPC object to an API object."""
        obj_dict = m.as_dict()
        # Unset non-required fields so they do not appear
        # in the message body
        obj_dict.update(dict((k, wsme.Unset)
                        for k in obj_dict.keys()
                        if fields and k not in fields))
        return cls(**obj_dict)

    def unset_fields_except(self, except_list=None):
        """Unset fields so they don't appear in the message body.

        :param except_list: A list of fields that won't be touched.

        """
        if except_list is None:
            except_list = []

        for k in self.as_dict():
            if k not in except_list:
                setattr(self, k, wsme.Unset)
