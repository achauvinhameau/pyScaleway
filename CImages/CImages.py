# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2018-05-06 15:33:22 alex>
#

"""Image manipulation."""

import logging
import json
import datetime
import slumber


class CImages():
    """Image of the installation templates."""

    # ----------------------------------------
    def __init__(self, sw):
        """Constructor."""
        logging.debug("init images")
        self.a_images = []
        self.sw_api = sw.get_compute_api()

        self.last_refresh = 0

        return

    # ----------------------------------------
    def refresh(self):
        """Reload from server the list of volumes."""
        if self.last_refresh != 0:
            delta = datetime.datetime.now(datetime.timezone.utc) - self.last_refresh
            if delta.seconds < 60:
                logging.warning("refresh time too low")
                return False

        try:
            resp = self.sw_api.query().images.get()
        except slumber.exceptions.SlumberBaseException as error:
            a_error = json.loads(error.content.decode())
            logging.error("%s: %s", a_error['type'], a_error['message'])
            return False

        self.a_images = resp['images']
        self.last_refresh = datetime.datetime.now(datetime.timezone.utc)

        return True

    # ----------------------------------------
    def __str__(self):
        """Return string representation of this object."""
        self.refresh()
        resp = ""
        for i in sorted(self.a_images, key=lambda k: k['arch']):
            template = "\n{} {}\n last mod: {}\n vol:{} {:.1f}G\n id: {}"
            resp = resp + template.format(i['arch'],
                                          i['name'],
                                          i['modification_date'],
                                          i['root_volume']['volume_type'],
                                          i['root_volume']['size'] / 1e9,
                                          i['id']
                                          )

        if resp == "":
            resp = "no images"

        return "images ----------------\n" + resp
