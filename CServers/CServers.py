# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2018-05-06 14:53:59 alex>
#

"""Servers manipulation."""

import random
import string
import logging
import json
import datetime


import slumber

# from main import org


class CServers():
    """Class to manage the servers."""

    def __init__(self, sw):
        """Constructor."""
        logging.debug("init servers")
        self.a_servers = []
        self.sw_api = sw.get_compute_api()

        self.org_id = sw.get_org_id()

        self.last_refresh = 0

        return

    # ----------------------------------------
    def refresh(self):
        """Reload from server the list of servers."""
        if self.last_refresh != 0:
            delta = datetime.datetime.now(datetime.timezone.utc) - self.last_refresh
            if delta.seconds < 60:
                logging.warning("refresh time too low")
                return

        try:
            resp = self.sw_api.query().servers.get()
        except slumber.exceptions.SlumberBaseException as error:
            a_error = json.loads(error.content.decode())
            logging.error("%s: %s", a_error['type'], a_error['message'])
            return False

        self.a_servers = resp['servers']
        self.last_refresh = datetime.datetime.now(datetime.timezone.utc)

    # ----------------------------------------
    def delete(self, srv_id=""):
        """Delete a server."""
        if srv_id == "":
            return False

        try:
            return self.sw_api.query().servers(srv_id).delete()
        except slumber.exceptions.SlumberBaseException as error:
            a_error = json.loads(error.content.decode())
            logging.error("%s: %s", a_error['type'], a_error['message'])
            return False

    # ----------------------------------------
    def __str__(self):
        """Return the list of servers."""
        self.refresh()

        resp = ""
        for serv in sorted(self.a_servers, key=lambda k: k['name']):
            resp = resp + "\n{} {} {} {} {}".format(serv['commercial_type'],
                                                    serv['hostname'],
                                                    serv['arch'],
                                                    serv['state'],
                                                    serv['id'])

            if serv['state'] == "running":
                resp = resp + "\n ip={}/{} {}".format(serv['private_ip'],
                                                      serv['public_ip']['address'],
                                                      serv['ipv6']['address'])

        if resp == "":
            resp = "no server"
        return "servers ---------------\n" + resp

    # ----------------------------------------
    def create_server(self, name="", image="", srv_type="", tags=""):
        """
        Create a server.

        alpine = 24141068-1043-4885-bf2b-8290f617e273
        Ubuntu = 67375eb1-f14d-4f02-bb42-6119cecbde51

        srv_type = START1-XS, START1-S
        """
        if self.org_id == "":
            logging.error("should have an organization id")
            exit(-1)

        if name == "":
            name = ''.join([random.choice(string.ascii_uppercase) for n in range(6)])  # nosec

        if image == "" and srv_type == "":
            image = "67375eb1-f14d-4f02-bb42-6119cecbde51"
            srv_type = "START1-XS"

        if image == "" and srv_type != "":
            logging.error("no image provided with a type server")
            return False

        a_data = {
            "organization": self.org_id,
            "name": name,
            "image": image,
            "commercial_type": srv_type,
            "tags": tags,
            "enable_ipv6": True
        }

        try:
            resp = self.sw_api.query().servers.post(data=a_data)
            return resp
        except slumber.exceptions.SlumberBaseException as error:
            a_error = json.loads(error.content.decode())
            logging.error("%s: %s", a_error['type'], a_error['message'])
            return False
