# <img src='./icon.png' card_color='#40DBB0' width='50' height='50' style='vertical-align:bottom'/> Parrot

Make Mycroft repeat whatever you want

## About

Repeats recent audio transriptions and text to speech outputs

Turn Mycroft into a echoing parrot! Speak a phrase and listen to it repeated in Mycroft's voice.

    "Hey Mycroft, start parrot"
    "hello"
    hello
    "what"
    what
    "who are you"
    who are you
    "Stop parrot"

NOTES:

- This replaces the functionality
  of [MycroftAI/skill-speak](https://github.com/MycroftAI/skill-speak),
  see [Issue#24](https://github.com/MycroftAI/skill-speak/issues/24)
- This replaces the functionality
  of [MatthewScholefield/skill-repeat-recent](https://github.com/MatthewScholefield/skill-repeat-recent)
- When asking to repeat what was previously said source is taken into
  consideration, if you ask in cli, gui, hivemind or STT response will vary
  accordingly, ie. using voice satellite wont respond with STT from device,
  only same source is taken into consideration
- Previous transcriptions are not persisted to disk

## Examples

* "say Goodnight, Gracie"
* "repeat Once upon a midnight dreary, while I pondered, weak and weary, Over
  many a quaint and curious volume of forgotten lore"
* "speak I can say anything you'd like!"
* "Repeat what you just said"
* "Repeat that"
* "Can you repeat that?"
* "What did I just say?"
* "Tell me what I just said."
* "start parrot"
* "stop parrot"

## Credits

- JarbasAl
- [MatthewScholefield/skill-repeat-recent](https://github.com/MatthewScholefield/skill-repeat-recent)

## Category

**Entertainment**

## Tags

# parrot

# converse

# echo

# Template

# Tutorial

# Debug
