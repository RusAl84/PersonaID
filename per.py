import math
from tkinter import *;
from tkinter import messagebox;
from tkinter.ttk import Combobox
from tkinter import filedialog as fd
import matplotlib.pyplot as plt;
import numpy as np;
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


class File(object):
    def __init__(self, name, begin, end):
        self.name = name;
        self.begin = begin;
        self.end = end;


def diagram_draw():
    ax.clear();
    text1X = - 0.7;
    text1Y = 1.4
    memory = 0;
    for i in range(0, len(list_memory_cell)):
        if list_memory_cell[i] == "None":
            memory += 1;
    text = "— Занято : " + str(size_memory - memory) + " Кбайт"
    ax.text(text1X, text1Y, text)
    plt.plot(text1X - 0.1, text1Y + 0.05, "o", c=color_insert, ms=8);
    text2X = text1X;
    text2Y = text1Y - 0.2
    text = "— Cвободно : " + str(memory) + " Кбайт"
    ax.text(text2X, text2Y, text)
    plt.plot(text2X - 0.1, text2Y + 0.05, "o", c=color_free_space, ms=8)

    ax.spines['bottom'].set_position(('data', 1000))
    ax.spines['left'].set_position(('data', 1000))
    ax.format_coord = lambda x, y: ""

    for br in range(0, len(list_memory_cell)):
        if list_memory_cell[br] == "None":
            X = [0, R * math.cos(np.pi / 90 * br * 360 / size_memory * 0.5)]
            Y = [0, R * math.sin(np.pi / 90 * br * 360 / size_memory * 0.5)]
            ax.plot(X, Y, color=color_free_space);

    for d in range(0, len(list_memory_cell)):
        if list_memory_cell[d] != "None":
            X = [0, R * math.cos(np.pi / 90 * d * 360 / size_memory * 0.5)]
            Y = [0, R * math.sin(np.pi / 90 * d * 360 / size_memory * 0.5)]
            ax.plot(X, Y, color=color_insert);

    ax.plot(0, 0, "o", c="white", ms=disk_size);

    canvas1.draw()


def window_deleted():
    if messagebox.askokcancel("Выход из приложения", "Хотите выйти из приложения?"):
        window.destroy()


def address(value):
    value = str(hex(value)).upper();
    if value == "0x0":
        return "0x000000"
    elif len(value) == 3:
        temp_value = "0x00000";
    elif len(value) == 4:
        temp_value = "0x0000";
    elif len(value) == 5:
        temp_value = "0x000";
    elif len(value) == 6:
        temp_value = "0x00";

    for i in range(2, len(value)):
        temp_value += value[i];

    return temp_value;


def show_window():
    show_window = Toplevel();
    show_window.resizable(width=False, height=False)
    show_window.title("Explorer.ShowWindow");

    if len(list_files) != 0:
        show_window.wm_geometry("+%d+%d" % (show_window.winfo_screenwidth() / 2 - 1.3 * show_window.winfo_reqwidth(),
                                            show_window.winfo_screenheight() / 2 - 0.9 * show_window.winfo_reqheight()))
        lbl = Label(show_window, text="Название файла и адреса ячеек памяти, в которых они хранятся : ",
                    font='Times 15');
        lbl.pack(side='top', fill=BOTH, anchor=N, ipadx=4, padx=1, ipady=3, pady=3, expand=True);
        for j in range(0, len(list_files)):
            if j == 0:
                temp_text = "'" + list_files[j].name + "' — " + address(list_files[j].begin) + "_" + address(
                    list_files[j].end) + ", размер файла : " + str(list_files[j].end - list_files[j].begin) + " Кбайт";
            else:
                temp_text = "'" + list_files[j].name + "' — " + address(list_files[j].begin) + "_" + address(
                    list_files[j].end) + ", размер файла : " + str(
                    list_files[j].end - list_files[j].begin + 1) + " Кбайт";
            lbl = Label(show_window, text=temp_text, font='Times 13');
            lbl.pack(side='top', fill=BOTH, anchor=N, ipadx=4, padx=1, ipady=3, pady=3, expand=True);
    else:
        show_window.wm_geometry("+%d+%d" % (show_window.winfo_screenwidth() / 2 - 0.8 * show_window.winfo_reqwidth(),
                                            show_window.winfo_screenheight() / 2 - 0.5 * show_window.winfo_reqheight()))
    i = 0;
    lbl = Label(show_window, text="Список свободных адресов памяти : ",
                font='Times 15');
    lbl.pack(side='top', fill=BOTH, anchor=N, ipadx=4, padx=1, ipady=3, pady=3, expand=True);
    while i < len(list_memory_cell):

        if list_memory_cell[i] == "None":

            j = i;
            while j < len(list_memory_cell):
                if list_memory_cell[j] == "None":
                    j = j + 1;

                    if j == len(list_memory_cell):
                        temp_text = address(i) + "_" + address(j)
                        lbl = Label(show_window, text=temp_text, font='Times 13');
                        lbl.pack(side='top', fill=BOTH, anchor=N, ipadx=4, padx=1, ipady=3, pady=3, expand=True);
                        i = j

                        break;

                else:
                    temp_text = address(i) + "_" + address(j - 1);
                    lbl = Label(show_window, text=temp_text, font='Times 13');
                    lbl.pack(side='top', fill=BOTH, anchor=N, ipadx=4, padx=1, ipady=3, pady=3, expand=True);
                    i = j
                    break;
        else:
            i += 1;

    destroy_window_btn = Button(show_window, text="ОК", width=25, command=show_window.destroy, font='Times 13');
    destroy_window_btn.pack(side='top', fill=X, ipadx=6, padx=4, ipady=5, pady=5);
    show_window.focus_set()
    show_window.grab_set()
    show_window.mainloop();


def info_window(temp_text):
    info_window = Toplevel();
    info_window.resizable(width=False, height=False)
    info_window.wm_geometry("+%d+%d" % (info_window.winfo_screenwidth() / 2 - 1.1 * info_window.winfo_reqwidth(),
                                        info_window.winfo_screenheight() / 2 - 0.5 * info_window.winfo_reqheight()))
    info_window.title("Explorer.Dialog");
    lbl = Label(info_window, text=temp_text, font='Times 13');
    lbl.pack(side='top', anchor=N, ipadx=4, padx=1, ipady=3, pady=3);
    destroy_window_btn = Button(info_window, text="ОК", command=info_window.destroy, font='Times 13');
    destroy_window_btn.pack(side='top', fill=BOTH, ipadx=6, padx=4, ipady=5, pady=5, expand=True);
    info_window.focus_set()
    info_window.grab_set()
    info_window.mainloop();


def delete_file():
    if len(list_files) == 0:
        info_window("На диске нет ни одного файла!")
    elif txt2.get() == "":
        info_window("Ввведите названия файла, который хотите удалить!")
    else:
        for i in range(0, len(list_files)):
            if list_files[i].name == txt2.get():
                temp_text = "Файл '" + list_files[i].name + "' размером '" + str(
                    list_files[i].end - list_files[i].begin + 1) + " Кбайт' был успешно удален!";

                txt2.delete(0, END);

                for j in range(list_files[i].begin, list_files[i].end + 1):
                    list_memory_cell[j] = "None";

                diagram_draw();
                list_files.pop(i);

                info_window(temp_text);
                break;
        else:
            temp_text = "Файл c названием'" + list_files[i].name + "' не существует, поэтому не был удалён!";
            txt.delete(0, END);
            info_window(temp_text);


def load():
    n = 0;
    try:
        file_name = fd.askopenfilename();
        with open(file_name, 'r') as file:

            list_files.clear();
            list_memory_cell.clear();

            str2 = file.readlines();

            for i in range(0, len(str2)):

                str = str2[i];
                name = "";
                begin = "";
                end = "";
                flag = 0;
                flag2 = 0;

                for i in range(0, len(str)):
                    if str[i] == " ":
                        break;
                    name += str[i];
                    flag = i + 2;
                for i in range(flag, len(str)):
                    if str[i] == " ":
                        break;
                    begin += str[i];
                    flag2 = i + 2;
                for i in range(flag2, len(str)):
                    if str[i] == " ":
                        break;
                    end += str[i];

                temp_file = File(name, int(begin), int(end));
                list_files.append(temp_file);

    except:
        n = 1;
        info_window('Файл не был выбран!')

    if n == 0:
        for i in range(0, size_memory):
            list_memory_cell.append("None");
        for i in range(0, len(list_files)):
            for j in range(list_files[i].begin, list_files[i].end):
                list_memory_cell[j] = "No none"
            diagram_draw()
        info_window('Данные успешно загружены из файла!');


def save():
    file_name = fd.asksaveasfilename(
        filetypes=(("TXT files", "*.txt"), ("HTML files", "*.html;*.htm"), ("All files", "*.*")))
    with open(file_name, 'w') as file:
        for i in range(0, len(list_files)):
            file.write(list_files[i].name + " " + str(list_files[i].begin) + " " + str(list_files[i].end) + "\n");

    file_name = "Данные сохранены в файл '" + file_name + "'!"
    info_window(file_name);


def insert_file():
    flag_save = 0;
    flag_break = 0;
    if txt.get() == "" or combo.get() == "None":
        info_window("Ввведите названия файла и его размер!")
    else:
        for i in range(0, len(list_files)):
            if list_files[i].name == txt.get():
                flag_break = 1;
                break;
        if flag_break == 1:
            temp_text = "Файл с названием '" + txt.get() + "' уже существует!";
            txt.delete(0, END);
            info_window(temp_text);

        else:

            length = int(combo.get());

            for i in range(0, len(list_memory_cell)):
                j = i;
                if list_memory_cell[i] == "None":

                    size_of_memory = 0;

                    while j < len(list_memory_cell):
                        if list_memory_cell[j] == "None":

                            size_of_memory += 1;
                            if size_of_memory == length:

                                for k in range(i, j + 1):
                                    list_memory_cell[k] = "No none";

                                file = File(txt.get(), i, j);
                                list_files.append(file);
                                diagram_draw();
                                flag_save = 1;

                                break;
                        else:
                            break;
                        j += 1;

                if flag_save == 1:
                    temp_text = "Файл '" + txt.get() + "' размером '" + combo.get() + " Кбайт' был успешно сохранен!";

                    txt.delete(0, END);
                    combo.current(0);
                    info_window(temp_text);
                    break;

            if flag_save == 0:
                temp_text = "Файл '" + txt.get() + "' размером '" + combo.get() + " Кбайт' не был сохранен!";
                txt.delete(0, END);
                combo.current(0);
                info_window(temp_text);


list_memory_cell = [];
size_memory = 320;
for i in range(0, size_memory):
    list_memory_cell.append("None");

R = 1;
list_files = [];

window = Tk()
color_insert = "#21a1db"
color_free_space = "#adaeae"
disk_size = 65;

fig = plt.figure(figsize=(2.5, 3))
border_width = 0.05
ax_size = [0 + border_width, 0 + border_width, 1 - 2 * border_width, 1 - 2 * border_width]
ax = fig.add_axes(ax_size)

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.spines['bottom'].set_position(('data', 1000))
ax.spines['left'].set_position(('data', 1000))
text1X = - 0.7;
text1Y = 1.4
ax.text(text1X, text1Y, "— Занято : 0 Кбайт")
plt.plot(text1X - 0.1, text1Y + 0.05, "o", c=color_insert, ms=8);
text2X = text1X;
text2Y = text1Y - 0.2
text = "— Свободно : " + str(size_memory) + " Кбайт"
ax.text(text2X, text2Y, text)
plt.plot(text2X - 0.1, text2Y + 0.05, "o", c=color_free_space, ms=8);
for br in range(0, len(list_memory_cell)):
    if list_memory_cell[br] == "None":
        X2 = [0, R * math.cos(np.pi / 90 * br * 360 / size_memory * 0.5)]
        Y = [0, R * math.sin(np.pi / 90 * br * 360 / size_memory * 0.5)]
        ax.plot(X2, Y, color=color_free_space);

ax.plot(0, 0, "o", c="white", ms=disk_size);
ax.format_coord = lambda x, y: ""

canvas1 = FigureCanvasTkAgg(fig, master=window)
canvas1.draw()
canvas1.get_tk_widget().pack(side=RIGHT, fill=NONE, expand=0)

window.title("Explorer");
window.geometry('800x280');
window.resizable(width=False, height=False)
menu = Menu(window);
new_item = Menu(menu, tearoff=0)
new_item.add_command(label='Загрузить данные из резервной копии гибкого магнитного диска!', command=load);
new_item.add_separator();
new_item.add_command(label='Cохранить резервную копию гибкого магнитного диска!', command=save);
menu.add_cascade(label='Меню', menu=new_item);
window.config(menu=menu);

lbl = Label(window, text="Введите название файла и выберите его размер в Кбайтах :", font='Times 14');
lbl.pack(side='top', anchor=W, ipadx=4, padx=1, ipady=3, pady=3);
f = Frame()
f.pack(side=TOP);
txt = Entry(f, width=40, font='Times 14');
txt.pack(side=LEFT, anchor=N, fill='x', ipadx=7, padx=5, ipady=7, pady=1);
combo = Combobox(f, state="readonly")
combo['values'] = ("None", 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32);
combo.current(0)
combo.pack(side=LEFT, ipadx=7, padx=5, ipady=7, pady=1);
insert_btn = Button(window, text="Записать файл на диск", width=25, command=insert_file, font='Times 13');
insert_btn.pack(side='top', fill=X, ipadx=6, padx=4, ipady=7, pady=5);
lbl.pack(side='top', anchor=W, ipadx=4, padx=1, ipady=3, pady=3);
txt2 = Entry(window, font='Times 14');
txt2.pack(side=TOP, anchor=N, fill='x', ipadx=7, padx=5, ipady=7, pady=1);
veiw_btn = Button(window, text="Удалить", width=25, command=delete_file, font='Times 13');
veiw_btn.pack(side='top', fill=X, ipadx=6, padx=4, ipady=7, pady=5);
txt2.pack(side=TOP, anchor=N, fill='x', ipadx=7, padx=5, ipady=7, pady=1);
veiw_btn = Button(window, text="Показать подробную информацию", width=25, command=show_window, font='Times 13');
veiw_btn.pack(side='top', fill=X, ipadx=6, padx=4, ipady=4, pady=0);
window.focus_force()
window.wm_geometry("+%d+%d" % (window.winfo_screenwidth() / 2 - 2 * window.winfo_reqwidth(),
                               window.winfo_screenheight() / 2 - window.winfo_reqheight()))
window.mainloop();
