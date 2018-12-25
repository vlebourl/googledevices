"""Wifi handling on Google Home units."""
from googledevices.helpers import gdh_request
from googledevices.utils.const import CAST_HEADERS, CASTPORT
import googledevices.utils.log as log


class Wifi(object):
    """A class for Wifi."""

    def __init__(self, host, loop, session, test):
        """Initialize the class."""
        self.loop = loop
        self.host = host
        self.session = session
        self.port = None if test else CASTPORT
        self._configured_networks = None
        self._nearby_networks = None

    async def get_configured_networks(self):
        """Get the configured networks of the device."""
        endpoint = 'setup/configured_networks'
        response = await gdh_request(host=self.host, port=self.port,
                                     loop=self.loop, session=self.session,
                                     endpoint=endpoint, headers=CAST_HEADERS)
        self._configured_networks = response
        log.debug(self._configured_networks)
        return self._configured_networks

    async def get_wifi_scan_result(self):
        """Get the result of a wifi scan."""
        endpoint = 'setup/configured_networks'
        response = await gdh_request(host=self.host, port=self.port,
                                     loop=self.loop, session=self.session,
                                     endpoint=endpoint, headers=CAST_HEADERS)
        self._configured_networks = response
        log.debug(self._configured_networks)
        return self._configured_networks

    async def scan_for_wifi(self):
        """Scan for nearby wifi networks."""
        endpoint = 'setup/scan_wifi'
        returnvalue = False
        result = await gdh_request(host=self.host, port=self.port,
                                   endpoint=endpoint, method='post',
                                   loop=self.loop, session=self.session,
                                   headers=CAST_HEADERS, json=False)
        try:
            if result.status == 200:
                returnvalue = True
        except AttributeError:
            msg = "Error connecting to - {}".format(self.host)
            log.error(msg)
        return returnvalue

    async def forget_network(self, wpa_id):
        """Forget a network."""
        endpoint = 'setup/forget_wifi'
        returnvalue = False
        data = {"wpa_id": int(wpa_id)}
        returnvalue = False
        result = await gdh_request(host=self.host, port=self.port,
                                   endpoint=endpoint, method='post',
                                   loop=self.loop, session=self.session,
                                   json_data=data, headers=CAST_HEADERS,
                                   json=False)
        try:
            if result.status == 200:
                returnvalue = True
        except AttributeError:
            msg = "Error connecting to - {}".format(self.host)
            log.error(msg)
        return returnvalue

    @property
    def configured_networks(self):
        """Return the configured networks of the device."""
        return self._configured_networks

    @property
    def nearby_networks(self):
        """Return the nearby networks of the device."""
        return self._nearby_networks
