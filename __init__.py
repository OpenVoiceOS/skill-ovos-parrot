from mycroft.skills.core import MycroftSkill, intent_file_handler
from os.path import join, dirname
from os import listdir
from mycroft.skills.core import resting_screen_handler
from lingua_franca.parse import extract_number
import random
from jarbas_utils.configuration import blacklist_skill
from mycroft.messagebus import Message


class ParrotSkill(MycroftSkill):
    def __init__(self):
        super(ParrotSkill, self).__init__("ParrotSkill")
        self.parroting = False
        self.stop_signaled = False
        self.heard_utts = []

    def initialize(self):
        # Deactivate official skill
        self.log.info("Parrot skill is blacklisting official speak skill "
                      "from mycroft")
        self.bus.emit(Message('skillmanager.deactivate',
                              {"skill": "mycroft-speak.mycroftai"}))
        blacklist_skill("mycroft-speak.mycroftai")

    @intent_file_handler("speak.intent")
    def handle_speak(self, message):
        """
            Repeat the utterance back to the user
        """
        repeat = message.data.get("sentence", "").strip()
        self.update_picture(repeat)
        self.speak(repeat, wait=True)

    @intent_file_handler("start_parrot.intent")
    def handle_start_parrot_intent(self, message):
        self.parroting = True
        self.speak_dialog("parrot_start", expect_response=True)

    @intent_file_handler("stop_parrot.intent")
    def handle_stop_parrot_intent(self, message):
        if self.parroting:
            self.parroting = False
            self.speak_dialog("parrot_stop")
        else:
            self.speak_dialog("not_parroting")

    def stop(self):
        self.stop_signaled = True
        if self.parroting:
            self.parroting = False
            self.speak_dialog("parrot_stop")
            return True
        return False

    def update_picture(self, utterance=None):
        if len(self.heard_utts):
            utterance = utterance or random.choice(self.heard_utts)
        path = join(dirname(__file__), "ui", "parrots")
        pic = join(path, random.choice(listdir(path)))
        self.gui.show_image(pic, caption=utterance,
                            fill='PreserveAspectFit')

    # idle screen
    @resting_screen_handler("Parrots")
    def idle(self):
        self.update_picture()

    def converse(self, utterances, lang="en-us"):
        self.heard_utts += utterances
        if self.parroting:
            # check if stop intent will trigger
            if self.voc_match(utterances[0], "StopKeyword") and \
                    self.voc_match(utterances[0], "ParrotKeyword"):
                return False
            # if not parrot utterance back
            self.update_picture(utterances[0])
            self.speak(utterances[0], expect_response=True)
            return True
        else:
            return False


def create_skill():
    return ParrotSkill()

