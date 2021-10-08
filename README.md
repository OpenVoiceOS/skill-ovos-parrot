# <img src='./icon.png' card_color='#40DBB0' width='50' height='50' style='vertical-align:bottom'/> Parrot

Turn Mycroft into a echoing parrot!

Make Mycroft repeat whatever you want

Repeats recent audio transriptions and text to speech outputs

## About

Turn Mycroft into a parrot. Speak a phrase and listen to it repeated in Mycroft's voice.

    "Hey Mycroft, start parrot"
    "hello"
    hello
    "what"
    what
    "who are you"
    who are you
    "Stop parrot"

Also provides an idle screen with parrot images and a random previous STT
transcription

NOTES:

- This will blacklist and replace the functionality
  of [MycroftAI/skill-speak](https://github.com/MycroftAI/skill-speak),
  see [Issue#24](https://github.com/MycroftAI/skill-speak/issues/24)
- This will blacklist and replace the functionality
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

# Platform support

- :heavy_check_mark: - tested and confirmed working
- :x: - incompatible/non-functional
- :question: - untested
- :construction: - partial support

|     platform    |   status   |  tag  | version | last tested | 
|:---------------:|:----------:|:-----:|:-------:|:-----------:|
|    [Chatterbox](https://hellochatterbox.com)   | :question: |  dev  |         |    never    | 
|     [HolmesV](https://github.com/HelloChatterbox/HolmesV)     | :question: |  dev  |         |    never    | 
|    [LocalHive](https://github.com/JarbasHiveMind/LocalHive)    | :question: |  dev  |         |    never    |  
|  [Mycroft Mark1](https://github.com/MycroftAI/enclosure-mark1)    | :question: |  dev  |         |    never    | 
|  [Mycroft Mark2](https://github.com/MycroftAI/hardware-mycroft-mark-II)    | :question: |  dev  |         |    never    |  
|    [NeonGecko](https://neon.ai)      | :question: |  dev  |         |    never    |   
|       [OVOS](https://github.com/OpenVoiceOS)        | :question: |  dev  |         |    never    |    
|     [Picroft](https://github.com/MycroftAI/enclosure-picroft)       | :question: |  dev  |         |    never    |  
| [Plasma Bigscreen](https://plasma-bigscreen.org/)  | :question: |  dev  |         |    never    |  

- `tag` - link to github release / branch / commit
- `version` - link to release/commit of platform repo where this was tested

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
