from tkinter import *
import tkinter as tk
import configparser
import traceback
import psutil
from contextlib import suppress
import re

try:

    window = tk.Tk()
    x = (window.winfo_screenwidth() - 665) / 2
    y = (window.winfo_screenheight() - 510) / 2
    window.geometry("+%d+%d" % (x, y))
    window.title("Settings")

    # Создается новая рамка `frm_form` для ярлыков с текстом и
    # Однострочных полей для ввода информации об адресе.
    frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
    # Помещает рамку на окно приложения.
    frm_form.pack(anchor=W)

    settings_form = tk.Frame()
    settings_form.pack(anchor=W)
    
    resolution_form = tk.Frame(master=settings_form, relief=tk.SUNKEN, borderwidth=3)
    resolution_form.grid(row=0, column=0, sticky='n')
    
    distance_form = tk.Frame(master=settings_form, relief=tk.SUNKEN, borderwidth=3)
    distance_form.grid(row=0, column=1, sticky='n')

    scale_form = tk.Frame(master=settings_form, relief=tk.SUNKEN, borderwidth=3)
    scale_form.grid(row=0, column=2, sticky='n')   
    # Список ярлыков полей.
    labels = [
        "Замер дистанции",
        "Выставка масштаба",
        "Замер дистанции мышь",
        "Выставка масштаба мышь",
    ]

    def read_config(name):
        try:
            config = configparser.ConfigParser()
            config.read(name, encoding='utf-8')
            conf = {}
            conf['distance_measurement'] = config.get("Combinations", "Distance measurement")
            conf['scale_setting'] = config.get("Combinations", "Scale setting")
            conf['distance_measurement_mouse'] = config.get("Combinations", "Distance measurement mouse")
            conf['scale_setting_mouse'] = config.get("Combinations", "Scale setting mouse")
            conf['resolution'] = config.get("Combinations", "Resolution")
            conf['print_x'] = config.get("Combinations", "print_x")
            conf['print_y'] = config.get("Combinations", "print_y")
            conf['print_time'] = config.get("Combinations", "print_time")
            conf['print_distance'] = config.get("Combinations", "print_distance")
            conf['print_azimuth'] = config.get("Combinations", "print_azimuth")
            conf['print_transparent'] = config.get("Combinations", "print_transparent")
            conf['scale_x'] = config.get("Combinations", "scale_x")
            conf['scale_y'] = config.get("Combinations", "scale_y")
            
            return conf
            
        except Exception as e:
            file = open('error.log', 'a')
            file.write('\n\n')
            traceback.print_exc(file=file, chain=True)
            traceback.print_exc()
            file.close()        

    def terminateSignals():
        
        file = open('code/pid.txt', 'a+')
        file.seek(0)
        pid = file.read()
        file.close()  
        
        file = open('code/pid1.txt', 'a+')
        file.seek(0)
        pid1 = file.read()
        file.close() 

        file = open('code/pid3.txt', 'a+')
        file.seek(0)
        pid3 = file.read()
        file.close() 
        
        file = open('code/pid5.txt', 'a+')
        file.seek(0)
        pid5 = file.read()
        file.close()                                           
        
        if pid1 == "":
            pid1 = "0"
        
        if pid3 == "":
            pid3 = "0" 
            
        if pid5 == "":
            pid5 = "0"                       
        
        processes = [int(pid1), int(pid3), int(pid5)]

        for process in processes:
            
            with suppress(psutil.NoSuchProcess, ProcessLookupError):
                
                process = psutil.Process(process)

                if process.name() == 'python.exe':
                    cmdline = process.cmdline()
                    
                    for cmdAttr in cmdline:
                        regexp = r'parent_pid=' + pid + r','
                        result = re.search(regexp, cmdAttr)
                        if result != None:
                            process.terminate()
                            break  
                            
    
    def write_config():
        try:
            config = configparser.ConfigParser()
            config.add_section("Combinations")
            config.set("Combinations", "Distance measurement", frm_form.winfo_children()[1].get())
            config.set("Combinations", "Scale setting", frm_form.winfo_children()[3].get())
            config.set("Combinations", "Distance measurement mouse", frm_form.winfo_children()[5].get())
            config.set("Combinations", "Scale setting mouse", frm_form.winfo_children()[7].get())
            config.set("Combinations", "Resolution", lang.get())
            config.set("Combinations", "print_x", entry_print_x.get())
            config.set("Combinations", "print_y", entry_print_y.get())
            config.set("Combinations", "print_time", entry_print_time.get())
            config.set("Combinations", "print_distance", str(print_distance.get()))
            config.set("Combinations", "print_azimuth", str(print_azimuth.get()))
            config.set("Combinations", "print_transparent", str(print_transparent.get()))
            config.set("Combinations", "scale_x", entry_scale_x.get())
            config.set("Combinations", "scale_y", entry_scale_y.get())            
            
            with open('code/buttons.ini', "w", encoding="utf-8") as file:
                config.write(file)
            
            terminateSignals()
            
            window.destroy()        
                
        except Exception as e:
            file = open('error.log', 'a')
            file.write('\n\n')
            traceback.print_exc(file=file, chain=True)
            traceback.print_exc()
            file.close()
            
    def default():
        try:
            frm_form.winfo_children()[1].delete(0, END)
            frm_form.winfo_children()[1].insert(0, 't')
            
            frm_form.winfo_children()[3].delete(0, END)
            frm_form.winfo_children()[3].insert(0, '<ctrl>+n')
            
            frm_form.winfo_children()[5].delete(0, END)
            frm_form.winfo_children()[5].insert(0, '')
            
            frm_form.winfo_children()[7].delete(0, END)
            frm_form.winfo_children()[7].insert(0, '')
            
            lang.set('3')       
            print_distance.set('1')
            print_azimuth.set('1')
            print_transparent.set('1')
            
            entry_print_x.delete(0, END)
            entry_print_x.insert(0, '15')
            
            entry_print_y.delete(0, END)
            entry_print_y.insert(0, '15')
            
            entry_print_time.delete(0, END)
            entry_print_time.insert(0, '7')            
            
            entry_scale_x.delete(0, END)
            entry_scale_x.insert(0, '15')
            
            entry_scale_y.delete(0, END)
            entry_scale_y.insert(0, '71')            
                
        except Exception as e:
            file = open('error.log', 'a')
            file.write('\n\n')
            traceback.print_exc(file=file, chain=True)
            traceback.print_exc()
            file.close()
            
            
    conf = read_config("code/buttons.ini")

    # Цикл для списка ярлыков полей.
    for idx, text in enumerate(labels):
        # Создает ярлык с текстом из списка ярлыков.
        label = tk.Label(master=frm_form, text=text, font=('Roboto','14'))
        # Создает текстовое поле которая соответствует ярлыку.
        entry = tk.Entry(master=frm_form, width=28, font=('Roboto','14'))
        # Использует менеджер геометрии grid для размещения ярлыков и
        # текстовых полей в строку, чей индекс равен idx.
        label.grid(row=idx, column=0, sticky="e", pady=5)
        entry.grid(row=idx, column=1)

    frm_form.winfo_children()[1].insert(0, conf['distance_measurement'])
    frm_form.winfo_children()[3].insert(0, conf['scale_setting'])
    frm_form.winfo_children()[5].insert(0, conf['distance_measurement_mouse'])
    frm_form.winfo_children()[7].insert(0, conf['scale_setting_mouse'])

    resolution = conf['resolution'] or "3"
    lang = StringVar(value=resolution)

    label_header_resolution = tk.Label(master=resolution_form, text="Разрешение", font=('Roboto','14'))
    label_header_resolution.pack(anchor=W, pady=5)

    a0_btn = tk.Radiobutton(master=resolution_form, text='1366x768', value='0', variable=lang, font=('Roboto','14'))
    a0_btn.pack(anchor=W)
    a1_btn = tk.Radiobutton(master=resolution_form, text='1440x900', value='1', variable=lang, font=('Roboto','14'))
    a1_btn.pack(anchor=W)    
    a2_btn = tk.Radiobutton(master=resolution_form, text='1680x1050', value='2', variable=lang, font=('Roboto','14'))
    a2_btn.pack(anchor=W)    
    a3_btn = tk.Radiobutton(master=resolution_form, text='1920x1080', value='3', variable=lang, font=('Roboto','14'))
    a3_btn.pack(anchor=W)
    a4_btn = tk.Radiobutton(master=resolution_form, text='1920x1200', value='4', variable=lang, font=('Roboto','14'))
    a4_btn.pack(anchor=W)
    #a3_btn = tk.Radiobutton(master=resolution_form, text='2560x1080', value='3', variable=lang, font=('Roboto','14'))
    #a3_btn.pack(anchor=W)     
    a5_btn = tk.Radiobutton(master=resolution_form, text='2560x1440', value='5', variable=lang, font=('Roboto','14'))
    a5_btn.pack(anchor=W)
    a6_btn = tk.Radiobutton(master=resolution_form, text='3440x1440', value='6', variable=lang, font=('Roboto','14'))
    a6_btn.pack(anchor=W)
    a7_btn = tk.Radiobutton(master=resolution_form, text='3840x2160', value='7', variable=lang, font=('Roboto','14'))
    a7_btn.pack(anchor=W)
    a8_btn = tk.Radiobutton(master=resolution_form, text='5120x2280', value='8', variable=lang, font=('Roboto','14'))
    a8_btn.pack(anchor=W)

    distance_form_1 = tk.Frame(master=distance_form)
    distance_form_1.pack(anchor=W)
    distance_form_2 = tk.Frame(master=distance_form)
    distance_form_2.pack(anchor=W)
    distance_form_3 = tk.Frame(master=distance_form)
    distance_form_3.pack(anchor=W)
    distance_form_4 = tk.Frame(master=distance_form)
    distance_form_4.pack(anchor=W) 
    distance_form_5 = tk.Frame(master=distance_form)
    distance_form_5.pack(anchor=W)

    scale_form_1 = tk.Frame(master=scale_form)
    scale_form_1.pack(anchor=W)
    scale_form_2 = tk.Frame(master=scale_form)
    scale_form_2.pack(anchor=W)    
    
    label_header_distance = tk.Label(master=distance_form_1, text="Окно дистанции", font=('Roboto','14'))
    label_header_distance.pack(pady=5)

    label_print_x = tk.Label(master=distance_form_2, text="x", font=('Roboto','14'))
    label_print_x.grid(row=0, column=0, pady=5)
    entry_print_x = tk.Entry(master=distance_form_2, width=7, font=('Roboto','14'))
    entry_print_x.grid(row=0, column=1)
    entry_print_x.insert(0, conf['print_x'])
    
    label_print_y = tk.Label(master=distance_form_2, text="y", font=('Roboto','14'))
    label_print_y.grid(row=0, column=2, pady=5)
    entry_print_y = tk.Entry(master=distance_form_2, width=7, font=('Roboto','14'))
    entry_print_y.grid(row=0, column=3)
    entry_print_y.insert(0, conf['print_y'])

    print_distance = IntVar()
    print_distance.set(int(conf['print_distance']))
    checkbutton_print_distance = tk.Checkbutton(master=distance_form_3, text="Дистанция", font=('Roboto','14'), variable=print_distance)
    checkbutton_print_distance.grid(row=0, column=0)
    
    print_azimuth = IntVar()
    print_azimuth.set(int(conf['print_azimuth']))
    checkbutton_print_azimuth = tk.Checkbutton(master=distance_form_3, text="Азимут", font=('Roboto','14'), variable=print_azimuth)
    checkbutton_print_azimuth.grid(row=0, column=1)

    print_transparent = IntVar()
    print_transparent.set(int(conf['print_transparent']))
    checkbutton_print_transparent = tk.Checkbutton(master=distance_form_4, text="Прозрачный фон", font=('Roboto','14'), variable=print_transparent)
    checkbutton_print_transparent.pack(pady=5)    

    label_print_time = tk.Label(master=distance_form_5, text="Время показа", font=('Roboto','14'))
    label_print_time.grid(row=0, column=0, pady=5)
    entry_print_time = tk.Entry(master=distance_form_5, width=7, font=('Roboto','14'))
    entry_print_time.grid(row=0, column=1)
    entry_print_time.insert(0, conf['print_time'])   


    label_header_scale = tk.Label(master=scale_form_1, text="Окно масштаба", font=('Roboto','14'))
    label_header_scale.pack(pady=5)
    
    label_scale_x = tk.Label(master=scale_form_2, text="x", font=('Roboto','14'))
    label_scale_x.grid(row=0, column=0, pady=5)
    entry_scale_x = tk.Entry(master=scale_form_2, width=7, font=('Roboto','14'))
    entry_scale_x.grid(row=0, column=1) 
    entry_scale_x.insert(0, conf['scale_x'])    
    
    label_scale_y = tk.Label(master=scale_form_2, text="y", font=('Roboto','14'))
    label_scale_y.grid(row=0, column=2, pady=5)
    entry_scale_y = tk.Entry(master=scale_form_2, width=7, font=('Roboto','14'))
    entry_scale_y.grid(row=0, column=3) 
    entry_scale_y.insert(0, conf['scale_y'])     
    
    
    # Создает новую рамку `frm_buttons` для размещения в ней
    # кнопок "Отправить" и "Очистить". Данная рамка заполняет
    # все окно в горизонтальном направлении с
    # отступами в 5 пикселей горизонтально и вертикально.
    frm_buttons = tk.Frame()
    frm_buttons.pack(fill=tk.X, ipadx=5, ipady=5)
     
    # Создает кнопку "Отправить" и размещает ее
    # справа от рамки `frm_buttons`.

    btn_submit = tk.Button(master=frm_buttons, text="Default", command=default, font=('Roboto','12'))
    btn_submit.pack(side=tk.LEFT, padx=10, ipadx=10)

    btn_submit = tk.Button(master=frm_buttons, text="Apply", command=write_config, font=('Roboto','12'))
    btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)
    window.mainloop()
    
except Exception as e:
    file = open('error.log', 'a')
    file.write('\n\n')
    traceback.print_exc(file=file, chain=True)
    traceback.print_exc()
    file.close()    