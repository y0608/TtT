from argostranslate import package, translate



def translate(message, from_language, to_language):
    first = from_language.upper()
    second = to_language.upper()
    output = ""
    temp = ""

    languages = {"EN" : 0, "AR" : 1, "ZH" : 2, "FR" : 3, "DE" : 4, "IT" : 5, "JA": 6, "PR" : 7, "RU" : 8, "ES" : 9}
    language_installers = {
                        languages["EN"] * 10 + languages["AR"] : 'models/en_ar.argosmodel',
                        languages["EN"] * 10 + languages["ZH"] : 'models/en_zh.argosmodel',
                        languages["EN"] * 10 + languages["FR"] : 'models/en_fr.argosmodel',
                        languages["EN"] * 10 + languages["DE"] : 'models/en_de.argosmodel',
                        languages["EN"] * 10 + languages["IT"] : 'models/en_it.argosmodel',
                        languages["EN"] * 10 + languages["PR"] : 'models/en_pr.argosmodel',
                        languages["EN"] * 10 + languages["RU"] : 'models/en_ru.argosmodel',
                        languages["EN"] * 10 + languages["ES"] : 'models/en_es.argosmodel',
                        languages["EN"] * 10 + languages["JA"] : 'models/en_ja.argosmodel',
                        languages["AR"] * 10 + languages["EN"] : 'models/ar_en.argosmodel',
                        languages["ZH"] * 10 + languages["EN"] : 'models/zh_en.argosmodel',
                        languages["FR"] * 10 + languages["EN"] : 'models/fr_en.argosmodel',
                        languages["DE"] * 10 + languages["EN"] : 'models/de_en.argosmodel',
                        languages["IT"] * 10 + languages["EN"] : 'models/it_en.argosmodel',
                        languages["PR"] * 10 + languages["EN"] : 'models/pr_en.argosmodel',
                        languages["RU"] * 10 + languages["EN"] : 'models/ru_en.argosmodel',
                        languages["ES"] * 10 + languages["EN"] : 'models/es_en.argosmodel',
                        languages["JA"] * 10 + languages["EN"] : 'models/ja_en.argosmodel'
}
    if first not in ["EN", "AR", "ZH", "FR", "DE", "IT", "PR", "RU", "ES", "JA"] or second not in ["EN", "AR", "ZH", "FR", "DE", "IT", "PR", "RU", "ES", "JA"] or  first == second:
        print("oopsie")
    elif first != "EN" and second != "EN":
        package.install_from_path(language_installers[languages[first] * 10])
        package.install_from_path(language_installers[languages[second]])
        installed_languages = translate.get_installed_languages()
        translation = installed_languages[languages[first]].get_translation(installed_languages[languages["EN"]])
        translation2 = installed_languages[languages["EN"]].get_translation(installed_languages[languages[second]])

        
        for line in message:
            temp += translation.translate(line.strip()) + "\n")
        for line in temp:
            output += translation2.translate(line.strip()) + "\n")

    else:
        package.install_from_path(language_installers[languages[first] * 10 + languages[second]])
        installed_languages = translate.get_installed_languages()
        translation = installed_languages[languages[first]].get_translation(installed_languages[languages[second]])

        for line in message:
            output += translation.translate(line.strip()) + "\n")
    
    return output 
