# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.




from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.skills.intent_service import IntentParser

__author__ = 'jarbas'

logger = getLogger(__name__)


class ParrotSkill(MycroftSkill):

    def __init__(self):
        super(ParrotSkill, self).__init__(name="ParrotSkill")
        self.parroting = False
        self.parser = None

    def initialize(self):

        start_parrot_intent = IntentBuilder("StartParrotIntent")\
            .require("StartKeyword").require("ParrotKeyword").build()

        self.register_intent(start_parrot_intent,
                             self.handle_start_parrot_intent)

        stop_parrot_intent = IntentBuilder("StopParrotIntent") \
            .require("StopKeyword").require("ParrotKeyword").build()

        self.register_intent(stop_parrot_intent,
                             self.handle_stop_parrot_intent)

        self.parser = IntentParser(self.emitter)

    def handle_start_parrot_intent(self, message):
        self.parroting = True
        self.speak("Parrot Mode Started", expect_response=True)

    def handle_stop_parrot_intent(self, message):
        self.parroting = False
        self.speak("Parrot Mode Stopped")

    def stop(self):
        if self.parroting:
            self.parroting = False
            self.speak("Parrot Mode Stopped")

    def converse(self, utterances, lang="en-us"):
        if self.parroting:
            intent, skill_id = self.parser.determine_intent(utterances[0])
            if skill_id == self.skill_id:
                return False
            else:
                self.speak(utterances[0], expect_response=True)
                return True
        else:
            return False


def create_skill():
    return ParrotSkill()

