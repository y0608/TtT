#import argostranslate

from argostranslate import package, translate
package.install_from_path('en_es.argosmodel')
installed_languages = translate.get_installed_languages()
translation_en_es = installed_languages[0].get_translation(installed_languages[1])
with open('input.txt', encoding='utf8') as f:
    with open('output.txt', "w") as file:
        for line in f:
            file.write(translation_en_es.translate(line.strip()) + "\n")
with open('output.txt', "r") as f:
    for line in f:
        print(translation_en_es.translate(line.strip()))
