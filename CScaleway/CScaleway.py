# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2018-05-06 14:49:24 alex>
#

"""Scaleway access to the API."""

import logging


from scaleway.apis import AccountAPI, ComputeAPI


class CScaleway():
    """Scaleway."""

    def __init__(self, auth_token="", region='par1'):
        """Constructor."""
        if auth_token == "":
            logging.error("no auth token provided, exiting")
            exit(-1)

        # --------------------------------
        self.auth_token = auth_token
        self.region = region
        self.org_id = None
        # --------------------------------

        logging.debug("init scaleway")
        self.api_compute = ComputeAPI(region=self.region,
                                      auth_token=self.auth_token)
        self.api_account = AccountAPI(auth_token=self.auth_token)

    def get_account_api(self):
        """Return the API descriptor for accounts manipulation."""
        return self.api_account

    def get_compute_api(self):
        """Return the API descriptor for computing manipulation."""
        return self.api_compute

    def set_org(self, org):
        """Set the organization that should be used in the calls."""
        self.org_id = org

    def get_org_id(self):
        """Return the organization that should be used in the calls."""
        return self.org_id
