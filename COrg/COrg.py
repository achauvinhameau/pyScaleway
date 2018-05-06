# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2018-05-06 14:39:04 alex>
#

"""Organization manipulation."""


import logging
import json
import slumber


class COrg():
    """Organization."""

    def __init__(self, sw):
        """Constructor."""
        logging.debug("init organization")
        self.sw_api = sw.get_account_api()
        self.a_orgs = []

        # get the first organisation from the account
        try:
            resp = self.sw_api.query().organizations.get()
            self.a_orgs = resp['organizations']
            self.org_id = self.a_orgs[0]['id']
        except slumber.exceptions.SlumberBaseException as error:
            a_error = json.loads(error.content.decode())
            logging.error("%s: %s", a_error['type'], a_error['message'])
            return

        logging.info("using organization id: %s", self.org_id)

        sw.set_org(self.org_id)

        return

    def get_id(self):
        """Return the id of the first organisation."""
        return self.org_id
