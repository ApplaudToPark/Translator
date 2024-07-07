from gtts import gTTS
import speech_recognition as sr
import keyboard as kb
# from playsound import playsound
from pydub import AudioSegment
from pydub.playback import play
import pyaudio
import wave
import time
from openai import OpenAI
import os
import platform

######## Information ########
# 이 코드는 마이크로프로세서 프로젝트를 위해 작성되었습니다.
# 이 코드 작성에 참여한 사람은 중앙대학교 전자전기공학부 소속 박민석, 임태건, 윤종진, 김영현입니다.
# OpenAI의 ChatGPT의 API를 이용하여, 저성능 마이크로프로세서 상에서도 동작할 수 있는 번역기 프로그램입니다.
# 이 파일은 중앙대학교 전자전기공학부 박민석의 GITHUB ID : "ApplaudToPark", PATH : /ApplaudToPark/Translator/ai_server_final.py
# 에 위치하고 있습니다.
#############################

######## 함수 정의 ########
def record(filename) : # filename은 ".wav"로 정의되어야 함.
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = filename
    information = """
{0:18}              
{1:18}"""



    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    os.system('clear')

    print(information.format('recording', ''))

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

        # if kb.is_pressed("up") : # 윗키가 눌리면 break
        #     break
        # else :
        #     pass
    os.system('clear')

    print(information.format('finished', ''))
    time.sleep(1)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def translate(r, filename, trs_lang) : # trs_lang : 입력하는 언어 설정. 'en-US'와 같은 형식.
    with sr.AudioFile(filename) as source :
        audio = r.record(source)

    try:
        # 어떤 언어인지를 사전에 설정해야 함. 하루 50회로 제한됨.
        text = r.recognize_google(audio, language=trs_lang)

    except sr.UnknownValueError:
        print('인식 실패')

    except sr.RequestError as e:
        print('요청 실패 : {}'.format(e))  # API key 오류, 또는 네트워크 단절 등


    return text # type : str



######## 실행할 함수 ########

def set_disability() :
    global count
    global cursor
    global disability
    count, cursor, disability = 0, 0, 0
    r = sr.Recognizer()
    information = """
    {0:18}              
    {1:18}"""


    # disable_set_text_en = """
    # Do you have any problem with your sense?
    # If you have, press the arrow or 'ok' button for setting up.
    # The default option is number 0, which means "I have no problem with that."
    # If you press "down" key, that is number 1, which means "I am a hearing-impaired person.
    # If you press "down" key again, that is number 2, which means "I am a visually-impared person."
    # """
    # disable_set_text_ko = """
    # 감각에 어떤 문제가 있나요?
    # 문제가 있다면, 방향키를 누르거나, 오케이 버튼을 눌러 설정해주세요.
    # 초기 설정은 숫자 0, 즉 감각에 아무 문제가 없다는 뜻입니다.
    # 아랫키를 누르면 숫자 1이고, 청각에 문제가 있는 경우를 뜻합니다.
    # 다시 아랫키를 누르면 숫자 2이고, 시각에 문제가 있는 경우를 뜻합니다.
    # """


    # 초기 설정 : 장애 여부
    while True :
        if count == 0 :
            # # with open('disable_set_text_en.txt', 'r', encoding='utf8') as f:
            # #     text = f.read()
            # # tts = gTTS(text=text, lang='en')
            # tts = gTTS(text=disable_set_text_en, lang='en')
            # tts.save('disableen.mp3')
            # tts = gTTS(text=disable_set_text_ko, lang='ko')
            # tts.save('disableko.mp3')
            # print(disable_set_text_en)
            os.system('clear')
            print(information.format("", ""))
            sound = AudioSegment.from_file('disableen.mp3')
            play(sound)

            # print(disable_set_text_ko)
            sound = AudioSegment.from_file('disableko.mp3')
            play(sound)
            # print(information.format("", ""))
            # a는 커서 증가, s는 커서 감소
            count = count + 1
        order = input()

            # wave_obj = sa.WaveObject.from_wave_file("DisableSetText.wav")
            # play_obj = wave_obj.play()
            # play_obj.wait_done()



        if order == "a" :
            if cursor != 2 :
                cursor = cursor + 1
                os.system('clear')
                if cursor == 1 :
                    print(information.format("normal person", "hear-impaired"))
                    sound = AudioSegment.from_file('number1.mp3')
                    play(sound)
                    sound = AudioSegment.from_file('number1ko.mp3')
                    play(sound)




                elif cursor == 2:
                    # print("a visually-impaired person")
                    # print("시각에 문제있는 경우")
                    print(information.format("visual-impaired", ""))
                    sound = AudioSegment.from_file('number2.mp3')
                    play(sound)
                    sound = AudioSegment.from_file('number2ko.mp3')
                    play(sound)




            else : pass

        elif order == 's' :
            if cursor != 0 :
                cursor = cursor - 1
                os.system('clear')

                if cursor == 0 :
                    print(information.format("normal person", "hear-impaired"))
                    # print("No matter with senses")
                    # print("정상인 경우")
                    sound = AudioSegment.from_file('number0.mp3')
                    play(sound)
                    sound = AudioSegment.from_file('number0ko.mp3')
                    play(sound)



                elif cursor == 1:
                    # print('a hearing impaired person')
                    # print("청각에 문제있는 경우")
                    print(information.format("normal person", "hear-impaired"))
                    sound = AudioSegment.from_file('number1.mp3')
                    play(sound)
                    sound = AudioSegment.from_file('number1ko.mp3')
                    play(sound)



            else : pass

        elif order == "1" :
            os.system('clear')
            print(information.format("ok", ""))

            sound = AudioSegment.from_file('ok.mp3')
            play(sound)
            sound = AudioSegment.from_file('okko.mp3')
            play(sound)



            disability = cursor # 장애 여부 설정
            cursor = 0
            count = 0
            break

    return disability


# 초기 설정 : 언어 설정
def set_lang0() :
    global language0
    global cursor
    global count
    cursor, count, language0 = 0, 0, 0
    information = """
    {0:18}              
    {1:18}"""


    while True :
        if count == 0 :
            count = count + 1
            # print("Set up the language to speak")
            # print("말할 언어를 선택하세요.")
            os.system('clear')
            print(information.format("english", "korean"))
            sound = AudioSegment.from_file('setlangen.mp3')
            play(sound)
            sound = AudioSegment.from_file('setlangko.mp3')
            play(sound)

        order = input()
        if order == "a" :
            if cursor != 4 :
                cursor = cursor + 1
                os.system('clear')

                if cursor == 1 :
                    print(information.format("english", "korean"))
                    sound = AudioSegment.from_file('ko.mp3')
                    play(sound)

                elif cursor == 2 :
                    print(information.format("chinese", "japanese"))
                    sound = AudioSegment.from_file('cn.mp3')
                    play(sound)


                elif cursor == 3 :
                    print(information.format("chinese", "japanese"))
                    sound = AudioSegment.from_file('ja.mp3')
                    play(sound)


                elif cursor == 4 :
                    print(information.format('french', ""))
                    sound = AudioSegment.from_file('fr.mp3')
                    play(sound)



        elif order == 's' :
            if cursor != 0 :
                cursor = cursor - 1
                os.system('clear')

                if cursor == 0 :
                    print(information.format("english", 'korean'))
                    sound = AudioSegment.from_file('en.mp3')
                    play(sound)


                elif cursor == 1:
                    print(information.format("english", 'korean'))
                    sound = AudioSegment.from_file('ko.mp3')
                    play(sound)


                elif cursor == 2:
                    print(information.format("chinese", 'japanese'))
                    sound = AudioSegment.from_file('cn.mp3')
                    play(sound)


                elif cursor == 3:
                    print(information.format("chinese", 'japanese'))
                    sound = AudioSegment.from_file('ja.mp3')
                    play(sound)



        elif order == '1' :
            os.system('clear')
            print(information.format("ok", ""))

            if cursor == 0 :
                sound = AudioSegment.from_file('ok.mp3')
                play(sound)
                language0 = 'en-US', "영어"
            elif cursor == 1 :
                sound = AudioSegment.from_file('okko.mp3')
                play(sound)
                language0 = 'ko', "한국어"
            elif cursor == 2 :
                sound = AudioSegment.from_file('okcn.mp3')
                play(sound)
                language0 = 'zh-CN', "중국어"
            elif cursor == 3 :
                sound = AudioSegment.from_file('okja.mp3')
                play(sound)
                language0 = 'ja', "일본어"
            elif cursor == 4 :
                sound = AudioSegment.from_file('okfr.mp3')
                play(sound)
                language0 = 'fr', "프랑스어"


            cursor = 0
            count = 0

            break
    return language0


# 초기 설정 1 : 상대방 언어 설정
def set_lang1() :
    global language1
    global cursor
    global count
    cursor, count, language1 = 0, 0, 0
    information = """
    {0:18}              
    {1:18}"""


    while True :
        if count == 0 :
            count = count + 1
            # print("Set up the language to speak")
            # print("말할 언어를 선택하세요.")
            os.system('clear')
            print(information.format("enligsh", "korean"))
            sound = AudioSegment.from_file('setlangen.mp3')
            play(sound)
            sound = AudioSegment.from_file('setlangko.mp3')
            play(sound)


        order = input()
        if order == 'a' :
            if cursor != 4 :
                cursor = cursor + 1
                os.system('clear')

                if cursor == 1 :
                    print(information.format("english", 'korean'))
                    sound = AudioSegment.from_file('ko.mp3')
                    play(sound)


                elif cursor == 2 :
                    print(information.format('chinese', 'japanese'))
                    sound = AudioSegment.from_file('cn.mp3')
                    play(sound)


                elif cursor == 3 :
                    print(information.format('chinese', 'japanese'))
                    sound = AudioSegment.from_file('ja.mp3')
                    play(sound)


                elif cursor == 4 :
                    print(information.format('french', ''))
                    sound = AudioSegment.from_file('fr.mp3')
                    play(sound)


        elif order == 's' :
            if cursor != 0 :
                cursor = cursor - 1
                os.system('clear')

                if cursor == 0 :
                    print(information.format("english", 'korean'))
                    sound = AudioSegment.from_file('en.mp3')
                    play(sound)


                elif cursor == 1:
                    print(information.format("english", 'korean'))
                    sound = AudioSegment.from_file('ko.mp3')
                    play(sound)


                elif cursor == 2:
                    print(information.format("chinese", 'japanese'))
                    sound = AudioSegment.from_file('cn.mp3')
                    play(sound)


                elif cursor == 3:
                    print(information.format("chinese", 'japanese'))
                    sound = AudioSegment.from_file('ja.mp3')
                    play(sound)


        elif order == '1' :
            os.system('clear')
            print(information.format('ok', ""))

            if cursor == 0 :
                sound = AudioSegment.from_file('ok.mp3')
                play(sound)
                language1 = 'en', "영어"
            elif cursor == 1 :
                sound = AudioSegment.from_file('okko.mp3')
                play(sound)
                language1 = 'ko', "한국어"
            elif cursor == 2 :
                sound = AudioSegment.from_file('okcn.mp3')
                play(sound)
                language1 = 'zh-CN', "중국어"
            elif cursor == 3 :
                sound = AudioSegment.from_file('okja.mp3')
                play(sound)
                language1 = 'ja', "일본어"
            elif cursor == 4 :
                sound = AudioSegment.from_file('okfr.mp3')
                play(sound)
                language1 = 'fr', "프랑스어"


            cursor = 0
            count = 0

            break
    return language1



######## 번역기 실행 ########
# 기능1 : 화살표 윗키를 누르면 상대방의 언어(language0)가 녹음됩니다. 같은 키를 한 번 더 누르면 녹음이 종료되고 번역이 시작됩니다.
# 기능2 : 화살표 아랫키를 누르면 내 언어(language1)가 녹음됩니다. 같은 키를 한 번 더 누르면 녹음이 종료되고 번역이 시작됩니다.
# 기능3 : Enter키를 1초간 누르면 기능이 종료됩니다.
# trs_lang에 들어갈 수 있는 변수 : 'en', 'fr', 'ja', 'ko', 'zh-CN'

def main_function() :
    api_key = "put your api key"
    client = OpenAI(api_key=api_key)
    r = sr.Recognizer()
    cursor = 0
    global language0
    global language1
    information = """
    {0:18}              
    {1:18}"""

    while True :
        order = input()

        if order == '1' : # 기능1 실행
            filename = "theirs.wave" # record(filename)
            record(filename)
            text1 = translate(r, filename, trs_lang=language0[0])
            prompt = text1 + "를 {0}로 번역하고, 오직 {0}문장만 표시해줘.".format(language1[1])
            response = client.chat.completions.create(
                model = 'gpt-3.5-turbo',
                messages = [
                    {"role" : "system", "content" : prompt}
                ]
            )
            # response = openai.ChatCompletion.create(
            #     engine = "text-davinci-002",
            #     prompt = text + "를 {0}로 번역하고, 오직 {0}문장만 표시해줘.".format(language1[1])
            # )
            response = str(response.choices[0].message.content)
            tts = gTTS(text=response, lang=language1[0])
            tts.save('theirs.mp3')
            sound = AudioSegment.from_file('theirs.mp3')
            play(sound)

            if len(response) > 100 :
                response = response[0:100]
            else :
                response = response.ljust(100)
            os.system('clear')
            print(information.format(response[:16], response[16:32]))

            while True :

                order = input()
                if order == 'a' :
                    cursor = cursor + 1
                    os.system('clear')

                    if cursor == 0 :
                        print(information.format(response[:16], response[16:32]))
                    elif cursor == 1 :
                        print(information.format(response[32:48], response[48:64]))
                    elif cursor == 2 :
                        print(information.format(response[64:80], response[80:96]))
                    elif cursor == 3 :
                        print(information.format(response[96:100], ""))

                elif order == 's' :
                    cursor = cursor - 1
                    os.system('clear')
                    if cursor == 0 :
                        print(information.format(response[:16], response[16:32]))
                    elif cursor == 1 :
                        print(information.format(response[32:48]), response[48:64])
                    elif cursor == 2 :
                        print(information.format(response[64:80]), response[80:96])
                    elif cursor == 3 :
                        print(information.format(response[96:100]), "")

                elif order == '1' :
                    break





        elif order == '2' :
            filename = "mine.wave" # record(filename)
            record(filename)
            text1 = translate(r, filename, trs_lang=language1[0])
            prompt = text1 + "를 {0}로 번역하고, 오직 {0}문장만 표시해줘.".format(language0[1])
            response = client.chat.completions.create(
                model = 'gpt-3.5-turbo',
                messages = [
                    {"role" : "system", "content" : prompt}
                ]
            )
            # response = openai.ChatCompletion.create(
            #     engine = "text-davinci-002",
            #     prompt = text + "를 {0}로 번역하고, 오직 {0}문장만 표시해줘.".format(language1[1])
            # )
            response = str(response.choices[0].message.content)
            tts = gTTS(text=response, lang=language0[0])
            tts.save('mine.mp3')
            sound = AudioSegment.from_file('mine.mp3')
            play(sound)

            if len(response) > 100 :
                response = response[0:100]
            else :
                response = response.ljust(100)
            os.system('clear')
            print(information.format(response[:16], response[16:32]))
            while True :
                order = input()
                if order == 'a' :
                    cursor = cursor + 1
                    os.system('clear')

                    if cursor == 0 :
                        print(information.format(response[:16], response[16:32]))
                    elif cursor == 1 :
                        print(information.format(response[32:48]), response[48:64])
                    elif cursor == 2 :
                        print(information.format(response[64:80]), response[80:96])
                    elif cursor == 3 :
                        print(information.format(response[96:100]), "")

                elif order == 's' :
                    cursor = cursor - 1
                    os.system('clear')
                    if cursor == 0 :
                        print(information.format(response[:16], response[16:32]))
                    elif cursor == 1 :
                        print(information.format(response[32:48]), response[48:64])
                    elif cursor == 2 :
                        print(information.format(response[64:80]), response[80:96])
                    elif cursor == 3 :
                        print(information.format(response[96:100]), "")

                elif order == '1' :
                    break


if __name__ == "__main__" :
    set_disability()
    set_lang0()
    set_lang1()
    main_function()
