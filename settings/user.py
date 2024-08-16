import json
import os

DEFAULT_PREFERENCES = {
    "colors": {
        "bgc_main": "#1C1E26",
        "bgc_left_panel": "#2E3440",
        "bgc_central_panel": "#3B4252",
        "bgc_rigth_panel": "#434C5E",
        "bgc_btn_crear_humano": "#88C0D0",
        "bgc_btn_eliminar_humano": "#BF616A",
        "bgc_btn_eliminar_vida": "#D08770",
        "bgc_btn_nuevo_dia": "#A3BE8C",
        "bgc_btn_lista_eventos": "#EBCB8B",
        "bgc_btn_tutorial": "#5E81AC",
        "bgc_btn_configuracion": "#4C566A",
        "label_color": "#B0B0B0",
        "indicator_color": "#ECEFF4",
        "divider_color": "#4C566A",
        "bgc_btn_opciones": "#81A1C1",
        "bgc_log": "#2E3440",
        "border_log": "#8FBCBB",
        "bgc_interactuar": "#A3BE8C",
        "bgc_ver_pensamiento": "#B48EAD",
        "bgc_decir": "#D08770",
        "bgc_enfermar": "#BF616A",
        "bgc_curar": "#A3BE8C",
        "bgc_save": "#8FBCBB",
        "bgc_delete": "#BF616A",
        "bgc_btn_talk_someone": "#88C0D0",
        "bgc_btn_flirt": "#EBCB8B",
        "bgc_btn_insult": "#BF616A",
        "bgc_btn_work": "#A3BE8C",
        "bgc_btn_work_cure": "#A3BE8C",
        "bgc_btn_work_arrest": "#D08770",
        "bgc_btn_work_kill": "#BF616A",
        "bgc_btn_select_talk": "#4C566A",
        "bgc_btn_select_flirt": "#88C0D0",
        "bgc_btn_select_insult": "#BF616A",
        "bgc_btn_select_sick": "#5E81AC",
        "bgc_btn_select_sick_cure": "#A3BE8C",
        "bgc_btn_select_event": "#81A1C1",
        "bgc_btn_select_kill": "#000000",
        "fc_btn": "#FFFFFF",
        "text_color": "#FFFFFF",
        "flirt_icon": "#FFFFFF",
        "icon_options": "#FFFFFF",
        "icon_color": "#FFFFFF",
        "icon_events": "#FFFFFF",
        "icon_interact": "#FFFFFF",
        "icon_see_think": "#FFFFFF",
        "icon_say": "#FFFFFF",
        "icon_get_sick": "#FFFFFF",
        "icon_work": "#FFFFFF",
        "icon_delete": "#FFFFFF"
    },
    "language": "ja",
    "music": "off",
    "sfx": "on",
    "full_screen": "on"
}

def load_preferences() -> dict:
    if not os.path.exists("settings/preferences.json"):
        os.makedirs("settings", exist_ok=True)
        with open("settings/preferences.json", "w") as preferences_file:
            json.dump(DEFAULT_PREFERENCES, preferences_file, indent=4)
        return DEFAULT_PREFERENCES
    
    with open("settings/preferences.json", "r") as preferences_file:
        preferences = json.load(preferences_file)
    return preferences

def edit_preferences(new_preferences):
    with open("settings/preferences.json", "w") as preferences_file:
        json.dump(new_preferences, preferences_file, indent=4)

user_data = load_preferences()
COLORS = user_data["colors"]
language = user_data["language"]

