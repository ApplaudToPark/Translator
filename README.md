# NOTICE

- Every file in this repository is in the team <일석육조>'s possessions.
- Participants are 박민석, 임태건, 윤종진, 김영현.
- This project is prepared for the "microprocessor" class at Chung-Ang Univ from May, 2024 to June, 2024.
- It could be used for a qualification for something.
- It is allowed to operate the codes for curiosities, but it cannot be used for any other competitions and beneficial usage.

## Derivation
Using ChatGPT API, it is simple to make a high-quiality translator that requires low specs. ChatGPT API can be used in Python environment to import "openai" modules.
This project is aiming at implementing translators in low-spec devices.

## Dependencies
This codes are operate in python version 3.9.7.
You have to install python modules as shown below :
- gtts
- speech recognition
- pydub
- pyaudio
- wave
- openai

And, if you want to operate codes correctly, you must download all files in "Applaud-To-Park-main-code" section. For convenience, I have uploaded the zip file which contains all the needed files.


## Principles
The algorithms are following steps :
1. Record the sound from monitor or microphone.
2. The recorded signal is transformed to text by STT.
3. Text is sent to ChatGPT with a prompt. The prompt helps to transform to other languages.
4. Operating normally, ChatGPT send us the text which is transformed to what I request.
5. The text is transformed to sound by TTS.
