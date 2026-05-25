import locale
import os
import gettext

from src.utils.file_functions.get_root_path import get_root_path


class TranslationManager:

    def __init__(self, domain = "sleep_analysis", locale_dir=None):
        self.translator = None

        if locale_dir is None:
            locale_dir = os.path.join(get_root_path(), "translations")

        self.domain = domain
        self.locale_dir = locale_dir

        self.curr_lang = None

        if os.path.exists(locale_dir) is False:
            os.mkdir(locale_dir)


    def detect_system_language(self):


        lang = os.environ.get('LANG', 'en_US').split('.')[0] # Strip encoding like '.UTF-8'

        return lang

    def load_translation(self, lang_code = None):
        if lang_code is None:
            lang_code = self.detect_system_language()

        try:
            self.translator = gettext.translation(
                self.domain,
                localedir=self.locale_dir,
                languages=[lang_code],
                fallback=True
            )
            self.translator.install()
            self.curr_lang = lang_code

        except FileNotFoundError:
            print(f"No translation found for {lang_code}, using default language.")
            self.curr_lang = lang_code

    def gettext(self, text):
        if self.translator is not None and self.translator:
            return self.translator.gettext(text)
        else:
            return text

# Global mappings
i18n = TranslationManager()
_ = i18n.gettext

