import speech_recognition as sr
import threading
from mtranslate import translate
from colorama import Fore, init
from indic_transliteration import sanscript

init(autoreset=True)

def Translate_bengali_to_english(text):
    """Translate Bengali text to English"""
    try:
        # Transliterate romanized Bengali to Bengali script
        bengali_script = sanscript.transliterate(text, sanscript.ITRANS, sanscript.BENGALI)
        # Translate from Bengali to English
        english_text = translate(bengali_script, "en", "bn")
        return english_text
    except:
        return text  # Return original text if translation fails

def Speech_to_text_Python():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 300  # Lowered from 34000 to 300 for normal speech detection
    recognizer.dynamic_energy_adjustment_damping = 0.015
    recognizer.dynamic_energy_ratio = 1.5
    recognizer.pause_threshold = 1.0  # Increased to better handle pauses between sentences
    recognizer.operation_timeout = None
    recognizer.non_speaking_duration = 0.2

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            print(Fore.GREEN + "Listening...", end="", flush=True)
            try:
                audio = recognizer.listen(source, timeout=None)
                print("\r" + Fore.LIGHTCYAN_EX + "Recog....", end="", flush=True)

                recognizer_text = ""
                is_bengali = False
                
                # Try to recognize Bengali first
                try:
                    recognizer_text = recognizer.recognize_google(audio, language="bn-IN").lower()
                    is_bengali = True
                except sr.UnknownValueError:
                    # If Bengali fails, try English
                    try:
                        recognizer_text = recognizer.recognize_google(audio, language="en-US").lower()
                        is_bengali = False
                    except sr.UnknownValueError:
                        recognizer_text = ""

                if recognizer_text:
                    if is_bengali:
                        # Only translate if Bengali was recognized
                        translate_text = Translate_bengali_to_english(recognizer_text)
                        print("\r" + Fore.BLUE + "You said (Bengali): " + Fore.CYAN + translate_text)
                    else:
                        # No translation for English
                        print("\r" + Fore.BLUE + "You said: " + Fore.CYAN + recognizer_text)
                else:
                    print("\r" + Fore.YELLOW + "No text recognized", end="", flush=True)
            except sr.UnknownValueError:
                recognizer_text = ""
            finally:
                print("\r", end="", flush=True)

# Run the speech recognition in a separate thread to allow concurrent execution
speech_thread = threading.Thread(target=Speech_to_text_Python)
speech_thread.daemon = True
speech_thread.start()

# Keep the main thread alive
speech_thread.join()
