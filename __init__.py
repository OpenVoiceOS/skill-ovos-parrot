from monotonic import monotonic
from mycroft.skills.core import MycroftSkill, intent_file_handler
from mycroft_bus_client.message import dig_for_message


class ParrotSession:
    def __init__(self, session_id):
        self.session_id = session_id
        self.parroting = False
        self.heard_utts = []
        self.last_tts = []
        self.last_stt_time = []

    @property
    def previous_stt(self):
        # last is current utt
        if len(self.heard_utts) < 2:
            return None
        else:
            return self.heard_utts[-2]


class ParrotSkill(MycroftSkill):
    def __init__(self):
        self.sessions = {"default": ParrotSession("default")}
        super(ParrotSkill, self).__init__("ParrotSkill")

    def initialize(self):
        # events used in intents rom
        # https://github.com/MatthewScholefield/skill-repeat-recent
        self.add_event('recognizer_loop:utterance', self.on_utterance)
        self.add_event('speak', self.on_speak)

    def get_session(self, message=None):
        message = message or dig_for_message()
        
        # use context session id, or fallback to utterance source (client id)
        # utterance source may be a list
        # see https://github.com/OpenVoiceOS/ovos-core/pull/160
        s = message.context.get("session_id") or \
            message.context.get("source")

        # create session objects
        if isinstance(s, list):
            for sess in s:
                if sess not in self.sessions:
                    self.sessions[sess] = ParrotSession(sess)
            # TODO what now? 1st? last?
            # this is a fallback to track different clients
            # cast to default session/treat as broadcast instead?
            return self.sessions["default"]

        elif s not in self.sessions:
            self.sessions[s] = ParrotSession(s)

        return self.sessions[s]

    def on_utterance(self, message):
        ts = monotonic()
        sess = self.get_session(message)
        sess.last_stt_time = ts
        utt = message.data['utterances'][0]
        sess.heard_utts.append(utt)

    def on_speak(self, message):
        sess = self.get_session(message)
        sess.last_tts = message.data['utterance']

    # Intents
    @intent_file_handler("speak.intent")
    def handle_speak(self, message):
        # replaces https://github.com/MycroftAI/skill-speak
        repeat = message.data.get("sentence", "").strip()
        self.speak(repeat, wait=True)

    @intent_file_handler('repeat.tts.intent')
    def handle_repeat_tts(self, message):
        # replaces https://github.com/MatthewScholefield/skill-repeat-recent
        sess = self.get_session(message)
        utt = sess.last_tts or self.translate('nothing')
        self.speak_dialog('repeat.tts', {"tts": utt})

    @intent_file_handler('repeat.stt.intent')
    def handle_repeat_stt(self, message):
        # replaces https://github.com/MatthewScholefield/skill-repeat-recent
        sess = self.get_session(message)
        last_stt = sess.previous_stt or self.translate("nothing")
        if monotonic() - sess.last_stt_time > 120:
            self.speak_dialog('repeat.stt.old', {"stt": last_stt})
        else:
            self.speak_dialog('repeat.stt', {"stt": last_stt})

    @intent_file_handler('did.you.hear.me.intent')
    def handle_did_you_hear_me(self, message):
        # replaces https://github.com/MatthewScholefield/skill-repeat-recent
        sess = self.get_session(message)
        if monotonic() - sess.last_stt_time > 60 or not sess.previous_stt:
            self.speak_dialog('did.not.hear')
            self.speak_dialog('please.repeat', expect_response=True)
        else:
            self.speak_dialog('did.hear')
            self.speak_dialog('repeat.stt', {"stt": sess.previous_stt})

    # continuous conversation
    @intent_file_handler("start_parrot.intent")
    def handle_start_parrot_intent(self, message):
        sess = self.get_session(message)
        sess.parroting = True
        self.speak_dialog("parrot_start", expect_response=True)
        self.gui["running"] = False
        self.gui.show_page("parrot.qml", override_idle=True)

    @intent_file_handler("stop_parrot.intent")
    def handle_stop_parrot_intent(self, message):
        if self.parroting:
            self.stop()
        else:
            self.speak_dialog("not_parroting")

    def converse(self, utterances, lang="en-us", message=None):
        sess = self.get_session(message)
        if sess.parroting:
            # check if stop intent will trigger
            if self.voc_match(utterances[0], "StopKeyword") and \
                    self.voc_match(utterances[0], "ParrotKeyword"):
                return False
            # if not parrot utterance back
            self.speak(utterances[0], expect_response=True)
            return True
        else:
            return False

    def stop(self):
        sess = self.get_session()
        if sess.parroting:
            sess.parroting = False
            self.speak_dialog("parrot_stop")
            self.gui["running"] = False
            self.gui.release()
            return True
        return False


def create_skill():
    return ParrotSkill()
