    from typing_extensions import ReadOnly
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.utils import QueryDict
from playsound import playsound
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from langdetect import detect
import pycountry
import pyttsx3
import g4f

all_languages = ('afrikaans', 'af', 'albanian', 'sq', 'amharic', 'am', 'arabic', 'ar', 'armenian', 'hy', 'azerbaijani',
                 'az', 'basque', 'eu', 'belarusian', 'be', 'bengali', 'bn', 'bosnian', 'bs', 'bulgarian', 'bg',
                 'catalan', 'ca', 'cebuano', 'ceb', 'chichewa', 'ny', 'chinese (simplified)', 'zh-cn',
                 'chinese (traditional)', 'zh-tw', 'corsican', 'co', 'croatian', 'hr', 'czech', 'cs', 'danish', 'da',
                 'dutch', 'nl', 'english', 'en', 'esperanto', 'eo', 'estonian', 'et', 'filipino', 'tl', 'finnish', 'fi',
                 'french', 'fr', 'frisian', 'fy', 'galician', 'gl', 'georgian', 'ka', 'german', 'de', 'greek', 'el',
                 'gujarati', 'gu', 'haitian creole', 'ht', 'hausa', 'ha', 'hawaiian', 'haw', 'hebrew', 'he', 'hindi',
                 'hi', 'hmong', 'hmn', 'hungarian', 'hu', 'icelandic', 'is', 'igbo', 'ig', 'indonesian', 'id', 'irish',
                 'ga', 'italian', 'it', 'japanese', 'ja', 'javanese', 'jw', 'kannada', 'kn', 'kazakh', 'kk', 'khmer',
                 'km', 'korean', 'ko', 'kurdish (kurmanji)', 'ku', 'kyrgyz', 'ky', 'lao', 'lo', 'latin', 'la', 'latvian',
                 'lv', 'lithuanian', 'lt', 'luxembourgish', 'lb', 'macedonian', 'mk', 'malagasy', 'mg', 'malay', 'ms',
                 'malayalam', 'ml', 'maltese', 'mt', 'maori', 'mi', 'marathi', 'mr', 'mongolian', 'mn', 'myanmar (burmese)',
                 'my', 'nepali', 'ne', 'norwegian', 'no', 'odia', 'or', 'pashto', 'ps', 'persian', 'fa', 'polish', 'pl',
                 'portuguese', 'pt', 'punjabi', 'pa', 'romanian', 'ro', 'russian', 'ru', 'samoan', 'sm', 'scots gaelic',
                 'gd', 'serbian', 'sr', 'sesotho', 'st', 'shona', 'sn', 'sindhi', 'sd', 'sinhala', 'si', 'slovak', 'sk',
                 'slovenian', 'sl', 'somali', 'so', 'spanish', 'es', 'sundanese', 'su', 'swahili', 'sw', 'swedish', 'sv',
                 'tajik', 'tg', 'tamil', 'ta', 'telugu', 'te', 'thai', 'th', 'turkish', 'tr', 'ukrainian', 'uk', 'urdu',
                 'ur', 'uyghur', 'ug', 'uzbek', 'uz', 'vietnamese', 'vi', 'welsh', 'cy', 'xhosa', 'xh', 'yiddish', 'yi',
                 'yoruba', 'yo', 'zulu', 'zu')
focus_languages = ('English', 'Filipino', 'Spanish')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

transmode = False

class Translabuds(App):  
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10,padding=10)
        sizing = BoxLayout(orientation='vertical', spacing=10,padding = 10)

        self.output_text = TextInput(multiline=True, readonly = True)
        layout.add_widget(self.output_text)

        # Dropdown for destination language
        self.spinner = Spinner(text='Select\nLanguage', values=focus_languages, size_hint=(None, None))
        self.spinner.bind(on_text=self.on_spinner_text)
        layout.add_widget(self.spinner)
        chosen = self.spinner.text

        # Toggle button for translation mode
        self.translate_button = ToggleButton(text="Translation Mode", on_press=self.on_toggle)
        layout.add_widget(self.translate_button)

        # Text input for displaying translated words
        self.output_text_translated = TextInput(multiline=True, readonly=True)
        layout.add_widget(self.output_text_translated)

        # Variable to track translation mode state
        self.translation_mode = False

        return layout

    def on_spinner_text(self, spinner, text):
        pass

    def on_toggle(self, instance): 
        # Update the translation mode variable based on the toggle state
        self.translation_mode = instance.state == 'down'
        if instance.state == 'down':
            self.run_translation_mode()

    def destination_language(self):
        print("Enter the language: English, Spanish, Filipino")
        print()
        to_lang = self.spinner.text
        # if statement para sa buttons yan para ready
        if to_lang.lower() == 'spanish':
            to_lang = 'spanish'
        elif to_lang.lower() == 'english':
            to_lang = 'english'
        elif to_lang.lower() == 'filipino':
            to_lang = 'filipino'
        else:
            to_lang = "None"
            while (to_lang == "None"):
                print("Select a Language")
                to_lang = self.spinner.text
        return to_lang

    def take_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            print("Recognizing")
            query = r.recognize_google(audio, language='en-in')
            print(f"The User said {query}\n")
        except Exception as e:
            print("again")
            return "None"
        return query

    def gpt_grammar_filipino(self, text_to_translate):
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "You will be provided with statements, and your task is to convert them to a casual conversation in Filipino."},
                {
                    "role": "user",
                    "content": text_to_translate
                }]
        )
        text_to_translate = response
        return text_to_translate

    def gpt_grammar_spanish(self, text_to_translate):
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "You will be provided with statements, and your task is to convert them to a casual conversation in Spanish."},
                {
                    "role": "user",
                    "content": text_to_translate
                }]
        )
        text_to_translate = response
        return text_to_translate

    def gpt_grammar_english(self, text_to_translate):
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "You will be provided with statements, and your task is to convert them to a casual conversation in English."},
                {
                    "role": "user",
                    "content": text_to_translate
                }]
        )
        text_to_translate = response
        return text_to_translate

    def run_translation_mode(self):
        while self.translation_mode:
            query = self.take_command()
            if query.lower() in ["exit translation mode", "exit", "quit"]:
                self.translate_button.state = 'normal'
                self.translation_mode = False
                break

            while query == "None":
                query = self.take_command()
                from_lang = detect(query)
                
            self.output_text.hint_text = query
            print(query)

            to_lang = self.destination_language()
            to_lang = all_languages[(all_languages.index(to_lang) + 1) % len(all_languages)]
            translator = Translator()
            text_to_translate = translator.translate(query, dest=to_lang)

            if to_lang == "tl":
                self.gpt_grammar_filipino(text_to_translate) 
            elif to_lang == "es":
                self.gpt_grammar_spanish(text_to_translate)
            elif to_lang == "en":
                self.gpt_grammar_english(text_to_translate)

            text = text_to_translate.text
            speak = gTTS(text=text, lang=to_lang, slow=False)
            self.output_text_translated.hint_text = text
            print(text)
            speak.save("audioCap.mp3")
            playsound('audioCap.mp3')
            os.remove('audioCap.mp3')

if __name__ == '__main__':
    Translabuds().run()
