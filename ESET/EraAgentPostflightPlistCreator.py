#!/usr/bin/python
#
# Copyright 2015 Tyler Riti
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""See docstring for EraAgentPostflightPlistCreator class."""

from __future__ import absolute_import
from autopkglib import Processor, ProcessorError
import FoundationPlist


__all__ = ["EraAgentPostflightPlistCreator"]


class EraAgentPostflightPlistCreator(Processor):
    """Create postflight plist for the ESET Remote Administrator Agent package."""
    description = __doc__
    input_variables = {
        "input_plist_path": {
            "required": False,
            "description":
                ("File path to a plist; empty or undefined to start with "
                 "an empty plist."),
        },
        "output_plist_path": {
            "required": True,
            "description":
                "File path to a plist. Can be the same path as input_plist.",
        },
        "eraa_server_hostname": {
            "required": True,
            "description":
                "Hostname of the ESET Remote Administrator server.",
        },
        "eraa_server_port": {
            "required": True,
            "description":
                "The ESET Remote Administrator server port.",
        },
        "eraa_peer_cert_pwd": {
            "required": False,
            "description":
                ("Client certificate password; empty or undefined if cert is "
                 "unencrypted."),
        },
        "eraa_peer_cert_b64": {
            "required": True,
            "description":
                "Base64 encoded client certificate.",
        },
        "eraa_ca_cert_b64": {
            "required": False,
            "description":
                "Base64 encoded CA certificate.",
        },
        "eraa_product_uuid": {
            "required": False,
            "description":
                "Product UUID.",
        },
        "eraa_initial_sg_token": {
            "required": False,
            "description":
                "Initial static group token.",
        },
    }
    output_variables = {
    }

    __doc__ = description

    def read_plist(self, pathname):
        """Read a plist from pathname."""
        # pylint: disable=no-self-use
        if not pathname:
            return {}
        try:
            return FoundationPlist.readPlist(pathname)
        except BaseException as err:
            raise ProcessorError(
                'Could not read %s: %s' % (pathname, err))

    def write_plist(self, data, pathname):
        """Write a plist to pathname."""
        # pylint: disable=no-self-use
        try:
            FoundationPlist.writePlist(data, pathname)
        except BaseException as err:
            raise ProcessorError(
                'Could not write %s: %s' % (pathname, err))

    def main(self):
        # read original plist (or empty plist)
        working_plist = self.read_plist(self.env.get("input_plist_path"))

        # insert new data
        working_plist["Hostname"] = self.env["eraa_server_hostname"]

        working_plist["Port"] = self.env["eraa_server_port"]

        if "eraa_peer_cert_pwd" in self.env:
            working_plist["PeerCertPassword"] = self.env["eraa_peer_cert_pwd"]

        working_plist["PeerCertContent"] = self.env["eraa_peer_cert_b64"]

        if "eraa_ca_cert_b64" in self.env:
            working_plist["CertAuthContent"] = self.env["eraa_ca_cert_b64"]

        if "eraa_product_uuid" in self.env:
            working_plist["ProductGuid"] = self.env["eraa_product_uuid"]

        if "eraa_initial_sg_token" in self.env:
            working_plist["InitialStaticGroup"] = self.env["eraa_initial_sg_token"]

        # write changed plist
        self.write_plist(working_plist, self.env["output_plist_path"])
        self.output("Updated plist at %s" % self.env["output_plist_path"])


if __name__ == '__main__':
    PROCESSOR = EraAgentPostflightPlistCreator()
    PROCESSOR.execute_shell()
