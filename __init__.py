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
from mycroft.skills.core import MycroftSkill, intent_handler
from os.path import dirname, join

__author__ = 'jarbas'


class ParrotSkill(MycroftSkill):

    def __init__(self):
        super(ParrotSkill, self).__init__(name="ParrotSkill")
        self.parroting = False
        self.stop_words = []
        # load stop words from .voc file
        # TODO PR for this method
        path = join(dirname(__file__), "dialog", self.lang, "StopKeyword.voc")
        with open(path, 'r') as voc_file:
            for line in voc_file.readlines():
                parts = line.strip().split("|")
                entity = parts[0]
                self.stop_words.append(entity)
                for alias in parts[1:]:
                    self.stop_words.append(alias)

    @intent_handler(
        IntentBuilder("StartParrotIntent").require("StartKeyword").require(
            "ParrotKeyword"))
    def handle_start_parrot_intent(self, message):
        self.parroting = True
        self.speak_dialog("parrot_start", expect_response=True)

    @intent_handler(
        IntentBuilder("StopParrotIntent").require("StopKeyword").require(
            "ParrotKeyword"))
    def handle_stop_parrot_intent(self, message):
        self.parroting = False
        self.speak_dialog("parrot_stop")

    def stop(self):
        if self.parroting:
            self.parroting = False
            self.speak_dialog("parrot_stop")

    def converse(self, utterances, lang="en-us"):
        if self.parroting:
            # check if stop intent will trigger
            for stop in self.stop_words:
                if stop in utterances[0]:
                    return False
            # if not parrot utterance back
            self.speak(utterances[0], expect_response=True)
            return True
        else:
            return False


def create_skill():
    return ParrotSkill()

