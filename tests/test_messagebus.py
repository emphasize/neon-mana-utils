# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import unittest

from mycroft_bus_client import MessageBusClient
from mycroft_bus_client.client.client import MessageBusClientConf
from ovos_utils.messagebus import FakeBus

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from neon_mana_utils.messagebus import tail_messagebus, send_message_file


class TestMessagebus(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client: MessageBusClient = FakeBus()
        cls.client.config = MessageBusClientConf("fakebus", 0000,
                                                 "/test", False)

    def test_send_message_invalid_file(self):
        invalid_message_file = os.path.join(os.path.dirname(__file__),
                                            "message_files",
                                            "invalid_message.txt")
        with self.assertRaises(ValueError):
            send_message_file(invalid_message_file, self.client)

        with self.assertRaises(FileNotFoundError):
            send_message_file("/test_message", self.client)

    def test_send_message_file_yml(self):
        test_dir = os.path.join(os.path.dirname(__file__), "message_files")
        invalid_message = os.path.join(test_dir, "invalid_message.yml")
        valid_message = os.path.join(test_dir, "valid_message.yml")
        no_ctx_message = os.path.join(test_dir, "valid_message_no_context.yml")

        with self.assertRaises(ValueError):
            send_message_file(invalid_message, self.client)

        self.assertIsNone(send_message_file(valid_message, self.client))
        self.assertIsNone(send_message_file(no_ctx_message, self.client))

    def test_send_message_file_json(self):
        test_dir = os.path.join(os.path.dirname(__file__), "message_files")
        invalid_message = os.path.join(test_dir, "invalid_message.json")
        valid_message = os.path.join(test_dir, "valid_message.json")
        no_ctx_message = os.path.join(test_dir, "valid_message_no_context.json")

        with self.assertRaises(ValueError):
            send_message_file(invalid_message, self.client)

        self.assertIsNone(send_message_file(valid_message, self.client))
        self.assertIsNone(send_message_file(no_ctx_message, self.client))

    def test_tail_messagebus(self):
        tail_messagebus(client=self.client)
        self.assertIsNotNone(self.client.ee.listeners("message"))


if __name__ == '__main__':
    unittest.main()
