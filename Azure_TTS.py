import os
import random

import azure.cognitiveservices.speech as speechsdk
import pygame


def GetVoicePath():
    with open('VoicePath.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def GetAzureKeyPath():
    with open('Azure_Key.txt', 'r', encoding='utf-8') as file:
        content = file.read().splitlines()
    return content

# 連結Azure_API (免費每月約50萬字)
def Azure_TTS(path, voice_name='en-US-SaraNeural', text='Test Test Connent to Azure API', GetFile=False, FileName=None):
    # path = GetVoicePath()

    AzureKey = GetAzureKeyPath()
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=AzureKey[0],
                                           region=AzureKey[1])
    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name = voice_name

    # Connect API
    if GetFile == False:
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    else:
        if FileName == None:
            audio_config = speechsdk.audio.AudioOutputConfig(
                filename=f"{path}/{text}.wav")  # filename="{name}.wav".format(name=text)
        else:
            audio_config = speechsdk.audio.AudioOutputConfig(filename=f"{path}/{FileName}.wav")
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    # # for Debug
    # if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    #     print("Speech synthesized for text [{}]".format(text))
    # elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
    #     cancellation_details = speech_synthesis_result.cancellation_details
    #     print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
    #         if cancellation_details.error_details:
    #             print("Error details: {}".format(cancellation_details.error_details))
    #             print("Did you set the speech resource key and region values?")

# 音色庫
def Azure_VoiceName(DeleteList=[]):
    VoiceList = [
        'en-US-JennyNeural',
        'en-US-SaraNeural',
        'en-US-AmberNeural',
        'en-US-EmmaNeural',
        'en-GB-OliviaNeural',
        'en-GB-SoniaNeural',
        'en-AU-TinaNeural',
        'en-AU-AnnetteNeural',
        'en-US-BrianNeural',
        'en-US-GuyNeural',
        'en-US-DavisNeural',
        'en-US-JasonNeural',
        'en-GB-NoahNeural',
        'en-GB-OliverNeural',
        'en-AU-TimNeural',
        'en-AU-DarrenNeural',
    ]
    result_list = [item for item in VoiceList if item not in DeleteList]
    random_element = random.choice(result_list)
    return random_element


# 播放已經存在的檔案
def Play_wav(file_path):
    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        # 等待音樂播放結束
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.mixer.quit()
        pygame.quit()


def Check_wav(file_path):
    return os.path.isfile(file_path) and file_path.lower().endswith('.wav')


# def Check_wav(file_path):
#     pygame.init()
#     pygame.mixer.init()
#
#     try:
#         pygame.mixer.music.load(file_path)
#         pygame.mixer.quit()
#         pygame.quit()
#         return True
#     except Exception as e:
#         return False

if __name__ == '__main__':
    pass
    path = GetVoicePath()
    voice_name = Azure_VoiceName(DeleteList=[])
    Azure_TTS(path, voice_name=voice_name, text='Test completed', GetFile=False, FileName='Test_Over')

    # # 路徑替換成你的 wav 檔案
    # path = GetVoicePath()
    # path = f'{path}/20_voice.wav'
    # print(Check_wav(path))
