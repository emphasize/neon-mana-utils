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

from mycroft_bus_client import Message, MessageBusClient


def get_skills_list(bus: MessageBusClient) -> dict:
    """
    Get a list of skills from the SkillManager
    :param bus: Connected MessageBusClient to query
    :returns: dict of loaded skills
    """
    resp = bus.wait_for_response(
            Message("skillmanager.list",
                    context={"source": ["mana"],
                             "destination": ["skills"]}), "mycroft.skills.list")
    skills = resp.data if resp else None
    return skills


def deactivate_skill(bus: MessageBusClient, skill: str):
    """
    Request deactivation of a skill
    :param bus: Connected MessageBusClient to query
    :param skill: skill ID to deactivate
    """
    bus.emit(Message("intent.service.skills.deactivate", {'skill_id': skill},
                     context={"source": ["mana"],
                              "destination": ["skills"]}))


def activate_skill(bus: MessageBusClient, skill: str):
    """
    Request activation of a skill
    :param bus: Connected MessageBusClient to query
    :param skill: skill ID to activate
    """
    bus.emit(Message("intent.service.skills.activate", {'skill_id': skill},
                     context={"source": ["mana"],
                              "destination": ["skills"]}))


def get_active_skills(bus: MessageBusClient) -> dict:
    """
    Get a list of skills from the intent service
    """
    msg = Message("intent.service.active_skills.get",
                  context={"destination": ["intent_service"],
                           "source": ["mana"]})
    resp = bus.wait_for_response(msg, 'intent.service.active_skills.reply')
    data = resp.data["skills"] if resp else dict()
    return data


def get_adapt_manifest(bus: MessageBusClient) -> dict:
    """
    Get a dict of all Adapt intents
    """
    msg = Message("intent.service.adapt.manifest.get",
                  context={"destination": ["intent_service"],
                           "source": ["mana"]})
    resp = bus.wait_for_response(msg, 'intent.service.adapt.manifest')
    data = resp.data["intents"] if resp else dict()
    return data


def get_padatious_manifest(bus: MessageBusClient) -> dict:
    """
    Get a dict of all Padatious intents
    """
    msg = Message("intent.service.padatious.manifest.get",
                  context={"destination": ["intent_service"],
                           "source": ["mana"]})
    resp = bus.wait_for_response(msg, 'intent.service.padatious.manifest')
    data = resp.data["intents"] if resp is not None else dict()
    return data
