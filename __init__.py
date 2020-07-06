from mycroft.skills.core import MycroftSkill, intent_file_handler
from os.path import join, dirname
from os import listdir
from mycroft.skills.core import resting_screen_handler
import random
from mycroft.configuration import LocalConf, USER_CONFIG
from mycroft.messagebus import Message
from monotonic import monotonic


class ParrotSkill(MycroftSkill):
    def __init__(self):
        super(ParrotSkill, self).__init__("ParrotSkill")
        self.parroting = False
        self.heard_utts = []
        self.last_tts = None
        self.last_stt_time = 0

    def initialize(self):
        # events used in intents directly lifted from
        # https://github.com/MatthewScholefield/skill-repeat-recent
        self.add_event('recognizer_loop:utterance', self.on_utterance)
        self.add_event('speak', self.on_speak)

        # check for conflicting skills just in case
        # done after all skills loaded to ensure proper shutdown
        self.add_event("mycroft.skills.initialized", self.deactivate_deprecated)

    def get_intro_message(self):
        # blacklist conflicting skills on install
        self.deactivate_deprecated()

    def deactivate_deprecated(self, message=None):
        # Deactivate official skill
        # TODO depending on https://github.com/MycroftAI/skill-speak/issues/24
        # code bellow can be removed

        skills_config = self.config_core.get("skills", {})
        blacklisted_skills = skills_config.get("blacklisted_skills", [])
        config = LocalConf(USER_CONFIG)
        blacklisted_skills += config.get("skills", {}).get("blacklisted_skills", [])
        store = False
        for skill in ["skill-repeat-recent", "mycroft-speak.mycroftai"]:
            if skill not in blacklisted_skills:
                self.log.info(
                    "Parrot skill blacklisted conflicting skill " + skill)
                self.bus.emit(
                    Message('skillmanager.deactivate', {"skill": skill}))
                blacklisted_skills.append(skill)
                if "skills" not in config:
                    config["skills"] = {}
                if "blacklisted_skills" not in config["skills"]:
                    config["skills"]["blacklisted_skills"] = []
                config["skills"]["blacklisted_skills"] += blacklisted_skills
                store = True
        if store:
            config.store()

    def on_utterance(self, message):
        self.heard_utts += message.data['utterances']
        self.last_stt_time = monotonic()

    def on_speak(self, message):
        self.last_tts = message.data['utterance']

    # Intents
    @intent_file_handler("speak.intent")
    def handle_speak(self, message):
        """
            Repeat the utterance back to the user
        """
        repeat = message.data.get("sentence", "").strip()
        self.update_picture(repeat)
        self.speak(repeat, wait=True)

    @intent_file_handler('repeat.tts.intent')
    def handle_repeat_tts(self):
        self.speak_dialog('repeat.tts',
                          {"tts":self.last_tts})

    @intent_file_handler('repeat.stt.intent')
    def handle_repeat_stt(self):
        if len(self.heard_utts) < 1:
            last_stt = self.translate('nothing')
        else:
            last_stt = self.heard_utts[-2] # last is current utt
        if monotonic() - self.last_stt_time > 120:
            self.speak_dialog('repeat.stt.old', {"stt": last_stt})
        else:
            self.speak_dialog('repeat.stt', {"stt": last_stt})

    @intent_file_handler('did.you.hear.me.intent')
    def handle_did_you_hear_me(self):
        if monotonic() - self.last_stt_time > 60 or len(self.heard_utts) == 0:
            self.speak_dialog('did.not.hear')
            self.speak_dialog('please.repeat', expect_response=True)
        else:
            if len(self.heard_utts) < 1:
                last_stt = self.translate('nothing')
            else:
                last_stt = self.heard_utts[-2] # last is current utt
            self.speak_dialog('did.hear')
            self.speak_dialog('repeat.stt', {"stt": last_stt})

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

    # gui
    def update_picture(self, utterance=None):
        if len(self.heard_utts):
            utterance = utterance or random.choice(self.heard_utts)
        path = join(dirname(__file__), "ui", "parrots")
        pic = join(path, random.choice(listdir(path)))
        self.gui.show_image(pic, caption=utterance,
                            fill='PreserveAspectFit')

    @resting_screen_handler("Parrots")
    def idle(self):
        self.update_picture()

    # continuous conversation
    def converse(self, utterances, lang="en-us"):
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

    def stop(self):
        if self.parroting:
            self.parroting = False
            self.speak_dialog("parrot_stop")
            return True
        return False


def create_skill():
    return ParrotSkill()

