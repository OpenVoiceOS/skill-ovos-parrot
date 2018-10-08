from mycroft.skills.core import MycroftSkill, intent_file_handler

__author__ = 'jarbas'


class ParrotSkill(MycroftSkill):
    parroting = False

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
        if self.parroting:
            self.parroting = False
            self.speak_dialog("parrot_stop")

    def converse(self, utterances, lang="en-us"):
        if self.parroting:
            # check if stop intent will trigger
            if self.voc_match(utterances[0], "StopKeyword") and self.voc_match(utterances[0], "ParrotKeyword"):
                return False
            # if not parrot utterance back
            self.speak(utterances[0], expect_response=True)
            return True
        else:
            return False


def create_skill():
    return ParrotSkill()

