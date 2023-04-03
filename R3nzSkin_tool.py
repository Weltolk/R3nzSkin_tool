import os
import psutil
from tkinter import *
import tkinter.messagebox
import json
import shutil
import time
import subprocess

text0_0_wait_text = "等待LOL客户端启动..."

mode_button_dark_text = "切换界面\n暗黑模式"

mode_button_white_text = "切换界面\n白昼模式"

config_file = "r3_replace_config.json"

default_game_file_path = "Game\\\\LogitechLed.dll"
default_r3_file_path = "R3nzSkin.dll"

process_name = "LeagueClient.exe"

path_status = False

# 注意: 可迭代对象的遍历
default_config = {
    "game_file_path": default_game_file_path,
    "r3_file_path": default_r3_file_path,
    "exclude_exe_list": [
        "R3nzSkin_tool.exe",
    ],
    "is_dark_mode": 1,
}


def config_checker() -> None:
    global config
    status = False
    for key in default_config:
        if key not in config:
            config[key] = default_config[key]
            status = True

    if status:
        write_config()
        read_config()


def find_procs_by_name(name: str) -> list[psutil.Process]:
    """
    Return a list of processes matching 'name'.
    """
    ls = []
    for p in psutil.process_iter(['name']):
        if p.info['name'] == name:
            ls.append(p)
    return ls


def get_game_path() -> str:
    p_list = find_procs_by_name(process_name)
    if len(p_list) == 0:
        return ""
    else:
        p = psutil.Process(p_list[0].pid)
        client_path = p.exe()
        game_path = os.path.split(os.path.split(client_path)[0])[0]
        return game_path


def write_config() -> None:
    global config
    f = open(config_file, "w", encoding="utf-8")
    f.write(json.dumps(config))
    f.close()


def read_config() -> None:
    global config
    config = json.loads(open(config_file, "r", encoding="utf-8").read())


def r3_replace_game() -> None:
    global path_status, lol_path, config

    if not path_status:
        tkinter.messagebox.showerror(title='Error', message="未获取到lol文件路径")
        return

    if lol_path == "":
        tkinter.messagebox.showerror(title='Error', message="未获取到lol文件路径")
        return

    file_path = os.path.join(lol_path, config["game_file_path"])
    bak_file_path_local = os.path.split(config["game_file_path"])[1] + ".bak"
    bak_file_path_game = os.path.join(os.path.split(file_path)[0], os.path.split(config["game_file_path"])[1] + ".bak")

    if not os.path.isfile(config["r3_file_path"]):
        tkinter.messagebox.showerror(title='Error', message="{}文件不存在".format(config["r3_file_path"]))
        return

    if not os.path.isfile(file_path):
        tkinter.messagebox.showerror(title='Error', message="{}文件不存在".format(file_path))
        return

    if os.path.isfile(bak_file_path_local):
        tkinter.messagebox.showerror(title='Error', message="{}备份文件已存在".format(bak_file_path_local))
        return

    if os.path.isfile(bak_file_path_game):
        tkinter.messagebox.showerror(title='Error', message="{}备份文件已存在".format(bak_file_path_game))
        return

    if text1_0.get("1.0", "end").strip() != config["game_file_path"] \
            or text2_0.get("1.0", "end").strip() != config["r3_file_path"]:
        recovery_file(file_path, bak_file_path_local, bak_file_path_game)
        config["game_file_path"] = text1_0.get("1.0", "end").strip()
        config["r3_file_path"] = text2_0.get("1.0", "end").strip()
        write_config()

    shutil.copyfile(file_path, bak_file_path_local)
    shutil.copyfile(file_path, bak_file_path_game)
    os.remove(file_path)
    shutil.copyfile(config["r3_file_path"], file_path)

    text2_1.delete("1.0", "end")
    text2_1.insert("1.0", "{}替换{}成功\n备份为{},{}".format(config["r3_file_path"], file_path, bak_file_path_local,
                                                             bak_file_path_game))


def game_replace_r3() -> None:
    global path_status, lol_path, config

    if not path_status:
        tkinter.messagebox.showerror(title='Error', message="未获取到lol文件路径")
        return

    if lol_path == "":
        tkinter.messagebox.showerror(title='Error', message="未获取到lol文件路径")
        return

    file_path = os.path.join(lol_path, config["game_file_path"])
    bak_file_path_local = os.path.split(config["game_file_path"])[1] + ".bak"
    bak_file_path_game = os.path.join(os.path.split(file_path)[0], os.path.split(config["game_file_path"])[1] + ".bak")

    # if not os.path.isfile(config["r3_file_path"]):
    #     tkinter.messagebox.showerror(title='Error', message="{}文件不存在".format(config["r3_file_path"]))
    #     return

    # if not os.path.isfile(file_path):
    #     tkinter.messagebox.showerror(title='Error', message="{}文件不存在".format(file_path))
    #     return

    if not os.path.isfile(bak_file_path_local):
        tkinter.messagebox.showerror(title='Error', message="{}备份文件不存在".format(bak_file_path_local))
        return

    if not os.path.isfile(bak_file_path_game):
        tkinter.messagebox.showerror(title='Error', message="{}备份文件不存在".format(bak_file_path_game))
        return

    if text1_0.get("1.0", "end").strip() != config["game_file_path"] \
            or text2_0.get("1.0", "end").strip() != config["r3_file_path"]:
        recovery_file(file_path, bak_file_path_local, bak_file_path_game)
        config["game_file_path"] = text1_0.get("1.0", "end").strip()
        config["r3_file_path"] = text2_0.get("1.0", "end").strip()
        write_config()

    os.remove(file_path)
    shutil.copyfile(bak_file_path_local, file_path)
    # shutil.copyfile(bak_file_path_game, file_path)
    os.remove(bak_file_path_local)
    os.remove(bak_file_path_game)

    text2_1.delete("1.0", "end")
    text2_1.insert("1.0", "{}替换{}成功\n删除备份{},{}".format(bak_file_path_local, file_path, bak_file_path_local,
                                                               bak_file_path_game))


def recovery_file(file_path: str, bak_file_path_local: str, bak_file_path_game: str) -> None:
    global path_status, lol_path, config

    os.remove(file_path)
    shutil.copyfile(bak_file_path_local, file_path)
    # shutil.copyfile(bak_file_path_game, file_path)
    os.remove(bak_file_path_local)
    os.remove(bak_file_path_game)


def restore() -> None:
    global path_status, lol_path, config

    if not path_status:
        tkinter.messagebox.showerror(title='Error', message="未获取到lol文件路径")
        return

    if lol_path == "":
        tkinter.messagebox.showerror(title='Error', message="未获取到lol文件路径")
        return

    file_path = os.path.join(lol_path, config["game_file_path"])
    bak_file_path_local = os.path.split(config["game_file_path"])[1] + ".bak"
    bak_file_path_game = os.path.join(os.path.split(file_path)[0], os.path.split(config["game_file_path"])[1] + ".bak")

    if text1_0.get("1.0", "end").strip() != default_game_file_path \
            or text2_0.get("1.0", "end").strip() != default_r3_file_path:

        if os.path.isfile(bak_file_path_local) and os.path.isfile(bak_file_path_game):
            recovery_file(file_path, bak_file_path_local, bak_file_path_game)

        config["game_file_path"] = default_game_file_path
        config["r3_file_path"] = default_r3_file_path
        write_config()

    text1_0.delete("1.0", "end")
    text1_0.insert("1.0", default_game_file_path)
    text2_0.delete("1.0", "end")
    text2_0.insert("1.0", default_r3_file_path)

    text2_1.delete("1.0", "end")
    text2_1.insert("1.0", "恢复默认设置成功")


def run_exe() -> None:
    global config

    now_exclude = text2_2.get("1.0", "end").strip()

    if now_exclude != "\n".join(config["exclude_exe_list"]):
        config["exclude_exe_list"] = now_exclude.split("\n")
        write_config()

    file_list = os.listdir("./")
    for file in file_list:
        if len(file) < 4 or file[-4:] != ".exe":
            continue

        if file in config["exclude_exe_list"]:
            continue

        subprocess.Popen([file])
        return

    tkinter.messagebox.showerror(title='Error', message="不存在R3nzSkin程序")
    return


def task() -> None:
    global path_status, lol_path
    lol_path = get_game_path()
    if lol_path != "":
        text0_0.delete("1.0", "end")
        text0_0.insert("1.0", lol_path)
        path_status = True
    else:
        text0_0.delete("1.0", "end")
        text0_0.insert("1.0", text0_0_wait_text)
        path_status = False
    root.after(3000, task)


def enable_dark_mode() -> None:
    dark_root_bg = "#1F1F1F"
    dark_lb_bg = "#1F1F1F"
    dark_text_bg = "#1F1F1F"
    dark_btn_bg = "#333333"
    dark_fg = "#FFFFFF"
    dark_insert_background = "#FFFFFF"
    root.config(bg=dark_root_bg)
    mode_button.config(bg=dark_btn_bg, fg=dark_fg)
    lb0_0.config(bg=dark_lb_bg, fg=dark_fg)
    text0_0.config(bg=dark_text_bg, fg=dark_fg, insertbackground=dark_insert_background)
    btn0_0.config(bg=dark_btn_bg, fg=dark_fg)
    btn0_1.config(bg=dark_btn_bg, fg=dark_fg)
    lb1_0.config(bg=dark_lb_bg, fg=dark_fg)
    text1_0.config(bg=dark_text_bg, fg=dark_fg, insertbackground=dark_insert_background)
    lb2_0.config(bg=dark_lb_bg, fg=dark_fg)
    text2_0.config(bg=dark_text_bg, fg=dark_fg, insertbackground=dark_insert_background)
    btn2_0.config(bg=dark_btn_bg, fg=dark_fg)
    btn2_1.config(bg=dark_btn_bg, fg=dark_fg)
    lb2_1.config(bg=dark_lb_bg, fg=dark_fg)
    text2_1.config(bg=dark_text_bg, fg=dark_fg, insertbackground=dark_insert_background)
    lb2_2.config(bg=dark_lb_bg, fg=dark_fg)
    text2_2.config(bg=dark_text_bg, fg=dark_fg, insertbackground=dark_insert_background)
    lb2_3.config(bg=dark_lb_bg, fg=dark_fg)

    mode_button.config(text=mode_button_white_text)


def disable_dark_mode() -> None:
    white_root_bg = "#FFFFFF"
    white_lb_bg = "#FFFFFF"
    white_text_bg = "#FFFFFF"
    white_btn_bg = "#F0F0F0"
    white_fg = "#000000"
    white_insert_background = "#000000"
    root.config(bg=white_root_bg)
    mode_button.config(bg=white_btn_bg, fg=white_fg)
    lb0_0.config(bg=white_lb_bg, fg=white_fg)
    text0_0.config(bg=white_text_bg, fg=white_fg, insertbackground=white_insert_background)
    btn0_0.config(bg=white_btn_bg, fg=white_fg)
    btn0_1.config(bg=white_btn_bg, fg=white_fg)
    lb1_0.config(bg=white_lb_bg, fg=white_fg)
    text1_0.config(bg=white_text_bg, fg=white_fg, insertbackground=white_insert_background)
    lb2_0.config(bg=white_lb_bg, fg=white_fg)
    text2_0.config(bg=white_text_bg, fg=white_fg, insertbackground=white_insert_background)
    btn2_0.config(bg=white_btn_bg, fg=white_fg)
    btn2_1.config(bg=white_btn_bg, fg=white_fg)
    lb2_1.config(bg=white_lb_bg, fg=white_fg)
    text2_1.config(bg=white_text_bg, fg=white_fg, insertbackground=white_insert_background)
    lb2_2.config(bg=white_lb_bg, fg=white_fg)
    text2_2.config(bg=white_text_bg, fg=white_fg, insertbackground=white_insert_background)
    lb2_3.config(bg=white_lb_bg, fg=white_fg)

    mode_button.config(text=mode_button_dark_text)


def toggle_dark_mode() -> None:
    global config
    if config["is_dark_mode"]:
        disable_dark_mode()
        config["is_dark_mode"] = 0
        write_config()
    else:
        enable_dark_mode()
        config["is_dark_mode"] = 1
        write_config()


def set_theme() -> None:
    global config
    if config["is_dark_mode"]:
        enable_dark_mode()
    else:
        disable_dark_mode()


if __name__ == "__main__":
    lol_path = ""
    config = dict()
    if os.path.isfile(config_file):
        read_config()
        config_checker()
    else:
        config = default_config
        write_config()

    root = Tk()
    root.title("R3nzSkin tool")
    root.geometry("850x650")
    # root.iconphoto(True, PhotoImage(file="./icon.png"))

    root.after(3000, task)

    # 暗黑模式部分
    mode_button = Button(root, text=mode_button_dark_text, command=toggle_dark_mode)
    mode_button.place(relwidth=0.075, relheight=0.095, relx=0.9125, rely=0.025)

    # LOL路径部分
    lb0_0 = Label(root, text="LOL路径(自动获取) 启动LOL客户端后会自动获取到", anchor=NW)
    lb0_0.place(relwidth=0.6, relheight=0.03, relx=0.05, rely=0.025)

    text0_0 = Text(root, relief=GROOVE, bg="#FFFFFF")
    text0_0.place(relwidth=0.6, relheight=0.065, relx=0.05, rely=0.06)
    text0_0.insert("1.0", text0_0_wait_text)

    btn0_0 = Button(root, text="替换并备份", command=r3_replace_game)
    btn0_0.place(relwidth=0.2, relheight=0.0425, relx=0.70, rely=0.025)

    btn0_1 = Button(root, text="恢复并删除备份", command=game_replace_r3)
    btn0_1.place(relwidth=0.2, relheight=0.0425, relx=0.70, rely=0.0775)

    # 游戏文件部分
    lb1_0 = Label(root, text="要替换的LOL文件(路径+文件名,以LOL文件夹为根目录)", anchor=NW)
    lb1_0.place(relwidth=0.45, relheight=0.03, relx=0.05, rely=0.15)

    text1_0 = Text(root, relief=GROOVE, bg="#FFFFFF")
    text1_0.place(relwidth=0.45, relheight=0.03, relx=0.05, rely=0.185)
    text1_0.insert("1.0", config["game_file_path"])

    # r3文件部分
    lb2_0 = Label(root, text="要替换的r3 file(当前目录)", anchor=NW)
    lb2_0.place(relwidth=0.45, relheight=0.03, relx=0.05, rely=0.24)

    text2_0 = Text(root, relief=GROOVE, bg="#FFFFFF")
    text2_0.place(relwidth=0.45, relheight=0.03, relx=0.05, rely=0.275)
    text2_0.insert("1.0", config["r3_file_path"])

    # 执行按钮部分
    btn2_0 = Button(root, text="运行R3nzSkin", command=run_exe, bg="#70F3FF")
    btn2_0.place(relwidth=0.15, relheight=0.1225, relx=0.525, rely=0.15)

    # 恢复默认按钮部分
    btn2_1 = Button(root, text="恢复默认设置", command=restore)
    btn2_1.place(relwidth=0.2, relheight=0.1225, relx=0.7, rely=0.15)

    # 消息框部分
    lb2_1 = Label(root, text="消息框", anchor=NW)
    lb2_1.place(relwidth=0.375, relheight=0.03, relx=0.1, rely=0.33)

    text2_1 = Text(root, relief=GROOVE, bg="#FFFFFF")
    text2_1.place(relwidth=0.375, relheight=0.275, relx=0.1, rely=0.365)
    text2_1.insert("1.0", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    # 排除框部分
    lb2_2 = Label(root, text="排除框", anchor=NW)
    lb2_2.place(relwidth=0.375, relheight=0.03, relx=0.525, rely=0.33)

    text2_2 = Text(root, relief=GROOVE, bg="#FFFFFF")
    text2_2.place(relwidth=0.375, relheight=0.275, relx=0.525, rely=0.365)
    text2_2.insert("1.0", "\n".join(config["exclude_exe_list"]) + "\n")

    # 提示框部分
    lb2_3 = Label(root, text="""'
    帮助信息:
    
    1.将本软件放在R3nzSkin文件夹下,也就是R3nzSkin.dll同目录下
    2.替换的时候软件会自动在LOL的文件夹和R3nzSkin的文件夹放置一个备份文件
    3.软件同目录下的r3_replace_config.json是本软件的配置文件,请勿删除,会影响文件的恢复
    4.当已经替换了一个文件时,修改要替换的文件,软件会自动恢复上一个文件,无需手动恢复
    """.strip(), relief=GROOVE, bg="#FFFFFF")
    lb2_3.place(relwidth=0.8, relheight=0.31, relx=0.1, rely=0.665)

    set_theme()  # 初始化主题

    root.mainloop()
