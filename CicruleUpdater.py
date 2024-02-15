#! /usr/bin/env python3
import time
import tkinter as tk
import urllib.request
import shutil
import os
import zipfile
import os.path
from threading import Thread

UPDATER_INTERVAL = 10

top = tk.Tk()

addons = {
    'NSQC': {"link": "https://github.com/Vladgobelen/NSQC/archive/refs/heads/main.zip",
             "описание": "Гильдейский аддон для Ночной стражи", "путь": "Interface/AddOns/NSQC/", "файл": 0,
             "временный путь": "temp/NSQC-main/", "путь к аддону": "Interface/AddOns/NSQC/"},
    'Карты подземелий': {"link": "https://hub.mos.ru/vladgobelen/nsqcmap/-/raw/main/patch-ruRU-M.MPQ",
                         "описание": "Патч для карт подземелий", "путь": "Data/ruRU/patch-ruRU-M.MPQ", "файл": 1,
                         "путь к аддону": "Data/ruRU/patch-ruRU-M.MPQ"},
    'WDM': {"link": "https://github.com/Trimitor/WDM-addons/archive/refs/heads/main.zip",
            "описание": "Аддон для правильного отображения карт подземелий", "путь": "Interface/AddOns/WDM/", "файл": 0,
            "временный путь": "temp/WDM-addons-main/WDM/", "путь к аддону": "Interface/AddOns/WDM/"},
    'Bartender4': {"link": "https://hub.mos.ru/vladgobelen/nsqcmap/-/raw/main/Bartender4.zip",
                   "описание": "Аддон настройки панелей(очень удобный!!!)", "путь": "Interface/AddOns/", "файл": 2,
                   "временный путь": "temp/", "путь к аддону": "Interface/AddOns/Bartender4"},
    'ArkInventory': {"link": "https://hub.mos.ru/vladgobelen/nsqcmap/-/raw/main/ArkInventory.zip",
                     "описание": "Аддон для сумок(объединение сумок в одну, сортировка шмота)",
                     "путь": "Interface/AddOns/", "файл": 2, "временный путь": "temp/",
                     "путь к аддону": "Interface/AddOns/ArkInventory"},
    'Chatter': {"link": "https://hub.mos.ru/vladgobelen/nsqcmap/-/raw/main/Chatter.zip",
                "описание": "Аддон для настройки чата, копирования текста и ссылок", "путь": "Interface/AddOns/",
                "файл": 2, "временный путь": "temp/", "путь к аддону": "Interface/AddOns/Chatter"},
    'Crap Away': {"link": "https://hub.mos.ru/vladgobelen/nsqcmap/-/raw/main/CrapAway.zip",
                  "описание": "Автоматическая продажа серого мусора из сумок", "путь": "Interface/AddOns/", "файл": 2,
                  "временный путь": "temp/", "путь к аддону": "Interface/AddOns/CrapAway"},
    'Gear Score': {"link": "https://hub.mos.ru/vladgobelen/nsqcmap/-/raw/main/GearScore.zip",
                   "описание": "Какой то странный способ оценки крутости шмота", "путь": "Interface/AddOns/", "файл": 2,
                   "временный путь": "temp/", "путь к аддону": "Interface/AddOns/GearScore"},
    'Grid2': {"link": "https://hub.mos.ru/vladgobelen/nsqcmap/-/raw/main/Grid2.zip",
              "описание": "Охренительно удобный аддон для хилов", "путь": "Interface/AddOns/", "файл": 2,
              "временный путь": "temp/", "путь к аддону": "Interface/AddOns/Grid2"},
    'Plate Buffs': {"link": "https://hub.mos.ru/vladgobelen/nsqcmap/-/raw/main/PlateBuffs.zip",
                    "описание": "Отображение бафов и дебафов цели прямо на ней", "путь": "Interface/AddOns/", "файл": 2,
                    "временный путь": "temp/", "путь к аддону": "Interface/AddOns/PlateBuffs"},
    'Range Display': {"link": "https://hub.mos.ru/vladgobelen/nsqcmap/-/raw/main/RangeDisplay.zip",
                      "описание": "Отображение расстояния до цели", "путь": "Interface/AddOns/", "файл": 2,
                      "временный путь": "temp/", "путь к аддону": "Interface/AddOns/RangeDisplay"},
    'Skada': {"link": "https://hub.mos.ru/vladgobelen/nsqcmap/-/raw/main/Skada.zip",
              "описание": "Аддон для вычисления урона, отхила игрока, пати рейда", "путь": "Interface/AddOns/",
              "файл": 2, "временный путь": "temp/", "путь к аддону": "Interface/AddOns/Skada"},
    'Tom Tom': {"link": "https://hub.mos.ru/vladgobelen/nsqcmap/-/raw/main/TomTom.zip",
                "описание": "Добавляет координаты игрока на карту и не только", "путь": "Interface/AddOns/", "файл": 2,
                "временный путь": "temp/", "путь к аддону": "Interface/AddOns/TomTom"},
    'DBM': {"link": "https://hub.mos.ru/vladgobelen/nsqcmap/-/raw/main/dbm.zip",
            "описание": "Обязательный аддон для рейдов", "путь": "Interface/AddOns/", "файл": 2,
            "временный путь": "temp/", "путь к аддону": "Interface/AddOns/DBM-Core"},
    'Gatherer': {"link": "https://hub.mos.ru/vladgobelen/nsqcmap/-/raw/main/Gatherer.zip",
                 "описание": "Аддон для сбора ресурсов: трава, руда", "путь": "Interface/AddOns/", "файл": 2,
                 "временный путь": "temp/", "путь к аддону": "Interface/AddOns/Gatherer"},
    'Auctionator': {"link": "https://hub.mos.ru/vladgobelen/nsqcmap/-/raw/main/Auctionator.zip",
                    "описание": "Аддон для работы с аукционом", "путь": "Interface/AddOns/", "файл": 2,
                    "временный путь": "temp/", "путь к аддону": "Interface/AddOns/Auctionator"},
    'BonusScanner': {"link": "https://hub.mos.ru/vladgobelen/nsqcmap/-/blob/main/BonusScanner.zip",
                     "описание": "Хрень, нужная для аддона Gear Score", "путь": "Interface/AddOns/", "файл": 2,
                     "временный путь": "temp/", "путь к аддону": "Interface/AddOns/BonusScanner"},
}


class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip, text=self.text, background="#ffffe0", relief="solid", borderwidth=1)
        label.pack()

    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


def start_guoko():
    os.startfile("Wow.exe")


def dl(count, block_size, total_size):
    progress_size = count * block_size
    percent = progress_size * 100 / total_size
    top.title(str('{0:.2g}'.format(percent)) + "%")


def update_addons(addon_link, addon_tmp_path, addon_final_path):
    urllib.request.urlretrieve(addon_link, "main.zip", reporthook=dl)
    archive = 'main.zip'
    if os.path.isdir('temp'):
        shutil.rmtree('temp/')
    archive = 'main.zip'
    with zipfile.ZipFile(archive, 'r') as zip_file:
        zip_file.extractall("temp")
    file_source = addon_tmp_path
    file_destination = addon_final_path
    if not os.path.exists(file_destination):
        os.mkdir(file_destination)
    get_files = os.listdir(file_source)
    shutil.copytree(file_source, file_destination, dirs_exist_ok=True)
    if os.path.isfile('main.zip'):
        os.remove('main.zip')
    if os.path.isdir('temp'):
        shutil.rmtree('temp/')

def update_dungeons_maps_addon(addon_link, addon_path):
    urllib.request.urlretrieve(addon_link, addon_path, reporthook=dl)


def generate_checkbox_processors(name, addon):
    def on_call():
        if addon['check_var'].get() == 0:
            if addon['файл'] == 0:
                if os.path.isdir(addon['путь']):
                    shutil.rmtree(addon['путь'])
            if addon['файл'] == 1:
                if os.path.isfile(addon['путь']):
                    os.remove(addon['путь'])
            if addon['файл'] == 2:
                if os.path.isdir(addon['путь к аддону']):
                    shutil.rmtree(addon['путь к аддону'])
        else:
            if addon['файл'] == 0 or addon['файл'] == 2:
                main_addons_updater_thread = Thread(target=update_addons, args=(addon['link'],
                                                                                addon['временный путь'],
                                                                                addon['путь']))
                main_addons_updater_thread.daemon = True
                main_addons_updater_thread.start()
            if addon['файл'] == 1:
                dmaps_addon_updater_thread = Thread(target=update_dungeons_maps_addon, args=(addon['link'],
                                                                                             addon['путь']))
                dmaps_addon_updater_thread.daemon = True
                dmaps_addon_updater_thread.start()
    return on_call


def update_guild_addon():
    is_nsqc_installed = os.path.isfile('Interface/AddOns/NSQC/vers')
    if is_nsqc_installed:
        f = urllib.request.urlopen('https://raw.githubusercontent.com/Vladgobelen/NSQC/main/vers').read().decode(
            'utf-8').strip()
        with open('Interface/AddOns/NSQC/vers', 'r') as file:
            vers_file_content = file.readline().strip()
    if not os.path.exists('Data/ruRU/patch-ruRU-M.MPQ'):
        urllib.request.urlretrieve("https://hub.mos.ru/vladgobelen/nsqcmap/-/raw/main/patch-ruRU-M.MPQ",
                                   "patch-ruRU-M.MPQ")
        os.replace("patch-ruRU-M.MPQ", "Data/ruRU/patch-ruRU-M.MPQ")
        urllib.request.urlretrieve("https://github.com/Trimitor/WDM-addons/archive/refs/heads/main.zip", "main.zip")
        if os.path.isdir('temp'):
            shutil.rmtree('temp/')
        archive = 'main.zip'
        with zipfile.ZipFile(archive, 'r') as zip_file:
            zip_file.extractall("temp")
        file_source = 'temp/WDM-addons-main/WDM/'
        file_destination = 'Interface/AddOns/WDM/'
        if not os.path.exists(file_destination):
            os.mkdir(file_destination)
        get_files = os.listdir(file_source)
        shutil.copytree(file_source, file_destination, dirs_exist_ok=True)
        if os.path.isfile('main.zip'):
            os.remove('main.zip')
        if os.path.isdir('temp'):
            shutil.rmtree('temp/')

    if not is_nsqc_installed or vers_file_content not in f:
        if os.path.isdir('temp'):
            shutil.rmtree('temp/')
        urllib.request.urlretrieve("https://github.com/Vladgobelen/NSQC/archive/refs/heads/main.zip", "main.zip")
        archive = 'main.zip'
        with zipfile.ZipFile(archive, 'r') as zip_file:
            zip_file.extractall("temp")
        file_source = 'temp/NSQC-main/'
        file_destination = 'Interface/AddOns/NSQC/'
        if not os.path.exists(file_destination):
            os.mkdir(file_destination)
        get_files = os.listdir(file_source)
        shutil.copytree(file_source, file_destination, dirs_exist_ok=True)
        if os.path.isfile('main.zip'):
            os.remove('main.zip')
        if os.path.isdir('temp'):
            shutil.rmtree('temp/')

def guild_addon_update_timer():
    while True:
        time.sleep(UPDATER_INTERVAL)
        update_guild_addon()


if __name__ == "__main__":
    gamestart_btn = tk.Button(text="Запустить игру", command=start_guoko)
    gamestart_btn.pack()
    for name, value in addons.items():
        var = tk.IntVar()
        btn = tk.Checkbutton(top,
                             text=name,
                             variable=var,
                             onvalue=1,
                             offvalue=0,
                             command=generate_checkbox_processors(name, value))
        if os.path.isdir(value['путь к аддону']) or os.path.isfile(value['путь к аддону']):
            var.set(1)
        else:
            var.set(0)
        btnT = Tooltip(btn, value['описание'])
        btn.pack()
        addons[name]['button'] = btn
        addons[name]['check_var'] = var
    top.title("Апдейтер от Ночной стражи")
    top.geometry("300x530")
    updater_timer_thread = Thread(target=guild_addon_update_timer)
    updater_timer_thread.daemon = True
    updater_timer_thread.start()
    top.mainloop()
