# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2018-05-06 14:56:00 alex>
#

"""Volumes manipulation."""


import logging
import json
import datetime
import re
import slumber


class CVolumes():
    """Volumes."""

    def __init__(self, sw):
        """Constructor."""
        logging.debug("init volumes")
        self.a_volumes = []
        self.sw_api = sw.get_compute_api()

        self.last_refresh = 0

    # ----------------------------------------
    def refresh(self):
        """Reload from server the list of volumes."""
        if self.last_refresh != 0:
            delta = datetime.datetime.now(datetime.timezone.utc) - self.last_refresh
            if delta.seconds < 60:
                logging.warning("refresh time too low")
                return False

        try:
            resp = self.sw_api.query().volumes.get()
        except slumber.exceptions.SlumberBaseException as error:
            a_error = json.loads(error.content.decode())
            logging.error("%s: %s", a_error['type'], a_error['message'])
            return False

        self.a_volumes = resp['volumes']
        self.last_refresh = datetime.datetime.now(datetime.timezone.utc)

    # ----------------------------------------
    def __str__(self):
        """Return a string with volumes information."""
        self.refresh()

        if not self.a_volumes:
            return "volumes ---------------\n" + " no volume found"

        resp = ""

        for volume in self.a_volumes:
            changed, subs = re.subn(r'\+00:00',
                                    "+0000",
                                    volume['modification_date'])
            if subs > 0:
                s_last_used = changed
            else:
                s_last_used = volume['modification_date']

            date_mod = datetime.datetime.strptime(s_last_used,
                                                  "%Y-%m-%dT%H:%M:%S.%f%z")
            delta = str(datetime.datetime.now(datetime.timezone.utc) - date_mod)

            resp = resp + "\n{} {:.1f}G".format(volume['volume_type'],
                                                volume['size'] / 1e9)

            if volume['server'] is not None:
                resp = resp + "\n server={}, last used={}".format(volume['server']['name'],
                                                                  delta)
            else:
                resp = resp + "\n not attached, last used={:s}".format(delta)

            resp = resp + "\n id={}".format(volume['id'])

        return "volumes ---------------\n" + resp

    # ----------------------------------------
    def delete(self, volume_id=""):
        """Delete the specified volume."""
        if volume_id == "":
            logging.error("should specify a volume to delete")
            return False

        try:
            return self.sw_api.query().volumes(volume_id).delete()
        except slumber.exceptions.SlumberBaseException as error:
            a_error = json.loads(error.content.decode())
            logging.error("%s: %s", a_error['type'], a_error['message'])
            return False
