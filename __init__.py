from monotonic import monotonic
from mycroft.skills.core import MycroftSkill, intent_file_handler


class ParrotSkill(MycroftSkill):
    def __init__(self):
        super(ParrotSkill, self).__init__("ParrotSkill")
        self.parroting = False
        self.heard_utts = {"_all": []}
        self.last_tts = {"_all": []}
        self.last_stt_time = {"_all": 0}

    def initialize(self):
        # events used in intents rom
        # https://github.com/MatthewScholefield/skill-repeat-recent
        self.add_event('recognizer_loop:utterance', self.on_utterance)
        self.add_event('speak', self.on_speak)

    def on_utterance(self, message):
        ts = monotonic()
        sources = message.context.get("source", "broadcast")
        if isinstance(sources, str):
            sources = [sources]

        for source in sources:
            if source not in self.heard_utts:
                self.heard_utts[source] = []
            self.heard_utts[source] += message.data['utterances']
            self.heard_utts["_all"] += message.data['utterances']
            self.last_stt_time[source] = self.last_stt_time["_all"] = ts
            #self.log.info(f"{source} utterance: {message.data['utterances']}")
            if source == "broadcast":
                for s in self.heard_utts:
                    if s == source:
                        continue
                    self.heard_utts[s] += message.data['utterances']
                for s in self.last_stt_time:
                    if s == source:
                        continue
                    self.last_stt_time[s] = ts

    def on_speak(self, message):
        sources = message.context.get("destination", "broadcast")
        if isinstance(sources, str):
            sources = [sources]
        for source in sources:
            if source not in self.last_tts:
                self.last_tts[source] = ""
            self.last_tts[source] = self.last_tts["_all"] = message.data['utterance']
            #self.log.info(f"{source} speak: {message.data['utterance']}")
            if source == "broadcast":
                for s in self.last_tts:
                    if s == source:
                        continue
                    self.last_tts[s] = message.data['utterance']

    # Intents
    @intent_file_handler("speak.intent")
    def handle_speak(self, message):
        # replaces https://github.com/MycroftAI/skill-speak
        repeat = message.data.get("sentence", "").strip()
        self.speak(repeat, wait=True)

    @intent_file_handler('repeat.tts.intent')
    def handle_repeat_tts(self, message):
        # replaces https://github.com/MatthewScholefield/skill-repeat-recent
        sources = message.context.get("destination", ["broadcast"])
        if isinstance(sources, str):
            sources = [sources]
        utts = []
        for source in sources:
            utt = self.last_tts.get(source)
            if utt:
                utts.append(utt)
        if len(utts) < 1:
            last_tts = self.translate('nothing')
        else:
            last_tts = utts[-1]  # last is current utt
        self.speak_dialog('repeat.tts',
                          {"tts": last_tts})

    @intent_file_handler('repeat.stt.intent')
    def handle_repeat_stt(self, message):
        # replaces https://github.com/MatthewScholefield/skill-repeat-recent
        sources = message.context.get("destination", ["broadcast"])
        if isinstance(sources, str):
            sources = [sources]
        utts = []
        for source in sources:
            utts += self.heard_utts.get(source, [])
        ts = max([self.last_stt_time.get(source) or 0 for source in sources])
        if len(utts) < 2:
            last_stt = self.translate('nothing')
        else:
            last_stt = utts[-2]  # last is current utt
        if monotonic() - ts > 120:
            self.speak_dialog('repeat.stt.old', {"stt": last_stt})
        else:
            self.speak_dialog('repeat.stt', {"stt": last_stt})

    @intent_file_handler('did.you.hear.me.intent')
    def handle_did_you_hear_me(self, message):
        # replaces https://github.com/MatthewScholefield/skill-repeat-recent
        sources = message.context.get("destination", ["broadcast"])
        if isinstance(sources, str):
            sources = [sources]
        ts = max([self.last_stt_time.get(source, 0) for source in sources])

        if monotonic() - ts > 60 or len(self.heard_utts) == 0:
            self.speak_dialog('did.not.hear')
            self.speak_dialog('please.repeat', expect_response=True)
        else:
            utts = []
            for source in sources:
                utts += self.heard_utts.get(source, [])

            if len(utts) < 2:
                last_stt = self.translate('nothing')
            else:
                last_stt = utts[-2]  # last is current utt

            self.speak_dialog('did.hear')
            self.speak_dialog('repeat.stt', {"stt": last_stt})

    # continuous conversation
    @intent_file_handler("start_parrot.intent")
    def handle_start_parrot_intent(self, message):
        self.parroting = True
        self.speak_dialog("parrot_start", expect_response=True)
        self.gui["running"] = False
        self.gui.show_page("parrot.qml", override_idle=True)

    @intent_file_handler("stop_parrot.intent")
    def handle_stop_parrot_intent(self, message):
        if self.parroting:
            self.stop()
        else:
            self.speak_dialog("not_parroting")

    def converse(self, utterances, lang="en-us"):
        if self.parroting:
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
        if self.parroting:
            self.parroting = False
            self.speak_dialog("parrot_stop")
            self.gui["running"] = False
            self.gui.release()
            return True
        return False


def create_skill():
    return ParrotSkill()
