import csv
import csv
import glob
import json
import os
import shutil
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

import numpy as np
from pyexcel.cookbook import merge_all_to_a_book
import pandas as pd


def create_bd(name, table_pattern):
    '''
    Создание таблицы в исходном виде
    :param name: название таблицы
    :param table_pattern: метаданные таблицы (названия,
    типы данных столбцов, а так же являются ли признаки
    ключевыми; имя и форма таблицы (записываются в json
    формате в отдельный файл))
    :return: None
    '''

    with open('{}.csv'.format(name), 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(table_pattern[:, 0])

    messagebox.showinfo('Сообщение', 'База данных создана успешно')


def binary_search(feat, val):
    '''
    Бинарный поиск - используется в различных операциях
    при обработке таблиц (например, поиск и удаление строк),
    временная сложность двоичного поиска равна O(log n)
    :param feat: признак, по которому производится поиск
    :param val: значение, по которому производится поиск
    :return: False - если искомых элементов нет, в ином случае - список индексов
    '''

    csv_file = list(filter(lambda x: x.endswith('.csv'), os.listdir(os.getcwd())))[0]
    try:
        col_for_search = sorted(list(enumerate((pd.DataFrame(pd.read_csv(csv_file))[feat]))), key=lambda el: el[1])
        try:
            val = type(col_for_search[0][1])(val)
        except ValueError:
            if val == 'True':
                val = 1
            elif val == 'False':
                val = 0
            else:
                return False

        first = 0
        last = len(col_for_search) - 1
        index = -1
        while (first <= last) and (index == -1):
            mid = (first + last) // 2
            if col_for_search[mid][1] == val:
                index = mid
            else:
                if val < col_for_search[mid][1]:
                    last = mid - 1
                else:
                    first = mid + 1

        if index == -1:
            return False

        i = 1
        result_ind = [col_for_search[index][0], ]
        try:
            while col_for_search[index + i][1] == col_for_search[index][1] or col_for_search[index - i][1] == \
                    col_for_search[index][1]:
                if col_for_search[index + i][1] == col_for_search[index][1]:
                    result_ind.append(col_for_search[index + i][0])
                    i += 1
                else:
                    result_ind.append(col_for_search[index - i][0])
                    i += 1
        except IndexError:
            pass

        return result_ind
    except KeyError:
        return False


def btn_create_bd_1():
    if len(list(filter(lambda x: x.endswith('.csv'), os.listdir(os.getcwd())))) != 0:
        messagebox.showinfo('Предупреждение', 'Таблица уже существует, перед созданием новой удалите предыдущую')
        return

    create_bd_frame_1 = tk.Toplevel(window)
    create_bd_frame_1.title('Выбор кол-ва признаков')
    create_bd_frame_1.geometry('380x100+100+300')
    create_bd_frame_1.resizable(False, False)
    create_bd_frame_1.grab_set()
    create_bd_frame_1.focus_set()

    lbl_1 = tk.Label(create_bd_frame_1, text='Выберите количество признаков объекта таблицы (>=4):')
    lbl_1.pack()
    lbl_1.grid(column=1, row=0)

    spin = tk.Spinbox(create_bd_frame_1, from_=4, to=100)
    spin.grid(column=1, row=1)

    def btn_create_bd_2():
        children = list(scroll_y.children.values()) + list(scroll_y.children.values()) + list(canvas.children.values())
        for child in children:
            child.destroy()

        num_feat = int(spin.get())
        create_bd_frame_1.destroy()

        create_bd_frame_2 = tk.Frame(canvas)

        lbl_2 = tk.Label(create_bd_frame_2, text='Название:')
        lbl_3 = tk.Label(create_bd_frame_2, text='Тип данных:')
        lbl_4 = tk.Label(create_bd_frame_2, text='Является ли ключом:')
        lbl_2.grid(column=0, row=0)
        lbl_3.grid(column=1, row=0)
        lbl_4.grid(column=2, row=0)

        table_params = list()
        for i in range(num_feat):
            txt = tk.Entry(create_bd_frame_2, width=10)
            txt.grid(column=0, row=1 + i)

            combo_1 = ttk.Combobox(create_bd_frame_2, width=5)
            combo_1['values'] = ('str', 'int', 'float', 'bool')
            combo_1.grid(column=1, row=1 + i)

            combo_2 = ttk.Combobox(create_bd_frame_2, width=7)
            combo_2['values'] = ('Key', 'Not key')
            combo_2.grid(column=2, row=1 + i)

            table_params.append([txt, combo_1, combo_2])

        def btn_create_bd_3():
            children = list(scroll_y.children.values()) + list(scroll_x.children.values()) + list(
                canvas.children.values())

            if len(table_params) < 4:
                messagebox.showinfo('Предупреждение', 'Кол-во признаков должно быть >=4')
                for child in children:
                    child.destroy()
                return

            for j in range(num_feat):
                table_params[j] = list(map(lambda el: el.get(), table_params[j]))
                if '' in table_params[j]:
                    for child in children:
                        child.destroy()
                    messagebox.showinfo('Предупреждение', 'Заполните все поля')
                    return

            tp = np.array(table_params)

            if len(np.unique(tp[:, 0])) < len(table_params) or len(np.unique(tp[:, 1])) == 1 or 'Key' not in tp[:, 2]:
                for child in children:
                    child.destroy()
                messagebox.showinfo('Предупреждение',
                                    'Таблица должна содержать признаки с разными типами данных '
                                    'и хотя бы одно ключевое поле, а также имена признаков не должны повторяться')
                return

            for child in children:
                child.destroy()

            name_frame = tk.Toplevel(window)
            name_frame.title('Выбор названия таблицы')
            name_frame.geometry('195x100+100+300')
            name_frame.resizable(False, False)
            name_frame.grab_set()
            name_frame.focus_set()

            table_name = tk.Label(name_frame, text='Введите название таблицы:')
            table_name.grid(column=1, row=0)
            name_txt = tk.Entry(name_frame, width=20)
            name_txt.grid(column=1, row=1)

            def btn_create_bd_4():
                name = name_txt.get()
                name_frame.destroy()

                db_metadata = dict()
                db_metadata['columns'] = list()
                for col in tp:
                    db_metadata['columns'].append({
                        'col_name': col[0],
                        'data_type': col[1],
                        'is_key_feat': col[2]
                    })

                db_metadata['name'], db_metadata['shape'] = name, tp.shape

                with open('{}_info.txt'.format(name), 'w') as outfile:
                    json.dump(db_metadata, outfile)

                create_bd(name, tp)

            btn_set_name = tk.Button(name_frame, text="Создать", command=btn_create_bd_4)
            btn_set_name.grid(column=1, row=2)

        btn_create = tk.Button(create_bd_frame_2, text="Создать", command=btn_create_bd_3)
        btn_create.grid(column=1, row=5 + num_feat)

        canvas.create_window(0, 0, anchor='nw', window=create_bd_frame_2)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'),
                         yscrollcommand=scroll_y.set)

        canvas.pack(fill='both', expand=True, side='left')
        scroll_y.pack(fill='y', side='right')

    btn_accept = tk.Button(create_bd_frame_1, text="Применить", command=btn_create_bd_2)
    btn_accept.grid(column=1, row=3)


def clear_before_opening(mes):
    '''
    Функция, осуществляющая чистку холста перед созданием новых виджетов
    :param mes: причина, по которой необходимо иметь созданную таблицу
    :return:
    '''

    if len(list(filter(lambda x: x.endswith('.csv'), os.listdir(os.getcwd())))) == 0:
        messagebox.showinfo('Предупреждение', mes)
        return True

    children = list(scroll_y.children.values()) + list(scroll_x.children.values()) + list(canvas.children.values())
    for child in children:
        child.destroy()


def btn_open_bd():
    if clear_before_opening('Таблица не существует, создайте таблицу, чтбы открыть ее'):
        return

    open_bd_frame_1 = tk.Frame(canvas)

    with open(list(filter(lambda x: x.endswith('.csv'),
                          os.listdir(os.getcwd())))[0], 'r') as f:
        reader = list(csv.reader(f))
        len_row = len(reader[0])

        for col_ind in range(len_row):
            el = tk.Entry(open_bd_frame_1, width=20, fg='blue',
                          font=('Arial', 16, 'bold'))
            el.grid(row=0, column=col_ind)
            el.insert(tk.END, reader[0][col_ind])

        for i in range(1, len(reader)):
            for j in range(len_row):
                el = tk.Entry(open_bd_frame_1)

                el.grid(row=i, column=j)
                el.insert(tk.END, reader[i][j])

    canvas.create_window(0, 0, anchor='nw', window=open_bd_frame_1)
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'),
                     yscrollcommand=scroll_y.set,
                     xscrollcommand=scroll_x.set)

    canvas.pack(fill='both', expand=True)
    scroll_y.pack(fill='y', side='right')
    scroll_x.pack(fill='x', side='bottom')


def btn_delete_bd():
    if clear_before_opening('Таблица не существует, создайте таблицу, чтбы удалить ее'):
        return

    csv_file = list(filter(lambda x: x.endswith('.csv'), os.listdir(os.getcwd())))[0]

    os.remove(csv_file)
    os.remove("{}_info.txt".format(csv_file[:-4]))

    messagebox.showinfo('Сообщение', 'Таблица была успешно удалена')


def btn_clean_bd():
    if clear_before_opening('Таблица не существует, создайте таблицу, чтбы удалить ее'):
        return

    csv_file = list(filter(lambda x: x.endswith('.csv'), os.listdir(os.getcwd())))[0]

    with open(csv_file, 'r') as inp:
        clms = list(csv.reader(inp))
    with open(csv_file, 'w') as out:
        writer = csv.writer(out)
        writer.writerow(clms[0])

    messagebox.showinfo('Сообщение', 'Таблица была успешно очищена')


def btn_add_row_1():
    if clear_before_opening('Таблица не существует, создайте таблицу, чтбы удалить ее'):
        return

    csv_file = list(filter(lambda x: x.endswith('.csv'), os.listdir(os.getcwd())))[0]

    with open('{}_info.txt'.format(csv_file[:-4])) as json_file:
        metadata = json.load(json_file)

    add_row_frame = tk.Frame(canvas)

    value_type_key = list()
    for row_n, col in enumerate(metadata['columns']):
        lbl_name = tk.Label(add_row_frame, text=col['col_name'])
        lbl_name.grid(column=0, row=row_n)

        txt = tk.Entry(add_row_frame, width=10)
        txt.grid(column=1, row=row_n)

        lbl_type = tk.Label(add_row_frame, text='({})'.format(col['data_type']))
        lbl_type.grid(column=2, row=row_n)

        value_type_key.append([txt, col['data_type'], col['is_key_feat'], col['col_name']])

    def btn_add_row_2():
        nonlocal value_type_key
        value_type_key = list(map(lambda el: [el[0].get(), el[1], el[2], el[3]], value_type_key))

        children = list(scroll_y.children.values()) + list(scroll_x.children.values()) + list(
            canvas.children.values())
        for child in children:
            child.destroy()

        row_for_insert = list()

        for col_ind, vtk in enumerate(value_type_key):
            try:
                if dispatcher[vtk[1]] == bool:
                    el = 0 if vtk[0] == 'False' or vtk[0] == '0' else 1

                else:
                    el = dispatcher[vtk[1]](vtk[0])

                with open(csv_file, 'r') as inp:
                    reader = list(csv.reader(inp))
                    if (vtk[2] == 'Key') and (len(reader) > 1) and (
                            el in np.array(reader[1:])[:, col_ind].astype(dispatcher[vtk[1]])):
                        messagebox.showinfo('Предупреждение',
                                            'Такой элемент уже существует ({} - ключевое поле)'.format(vtk[3]))
                        return

                row_for_insert.append(el)

            except ValueError:
                messagebox.showinfo('Предупреждение', 'Неверный тип данных')
                return

        with open(csv_file, 'a+') as out:
            writer = csv.writer(out)
            writer.writerow(row_for_insert)

        messagebox.showinfo('Сообщение', 'Строка добавлена успешно')

    btn_create = tk.Button(add_row_frame, text="Добваить", command=btn_add_row_2)
    btn_create.grid(column=1, row=1 + len(metadata['columns']))

    canvas.create_window(0, 0, anchor='nw', window=add_row_frame)
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'),
                     yscrollcommand=scroll_y.set)

    canvas.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')


def btn_del_row_1():
    if clear_before_opening('Таблица не существует, создайте таблицу, чтбы удалить из нее элемент'):
        return

    csv_file = list(filter(lambda x: x.endswith('.csv'), os.listdir(os.getcwd())))[0]

    del_row_frame_1 = tk.Toplevel(window)
    del_row_frame_1.title('Удаление элемента из таблицы')
    del_row_frame_1.geometry('700x100+100+300')
    del_row_frame_1.resizable(False, False)
    del_row_frame_1.grab_set()
    del_row_frame_1.focus_set()

    lbl_1 = tk.Label(del_row_frame_1, text='Выберите признак, по которому будет произведено удаление:')
    lbl_1.grid(column=0, row=0)

    with open('{}_info.txt'.format(csv_file[:-4])) as json_file:
        metadata = json.load(json_file)
        combo_val = [col['col_name'] for col in metadata['columns']]
        combo = ttk.Combobox(del_row_frame_1)
        combo['values'] = combo_val
        combo.grid(column=1, row=0)

    lbl_2 = tk.Label(del_row_frame_1, text='Введите значние признака для поиска:')
    lbl_2.grid(column=0, row=1)

    val = tk.Entry(del_row_frame_1)
    val.grid(column=1, row=1)

    def btn_del_row_2():
        children = list(scroll_y.children.values()) + list(scroll_y.children.values()) + list(canvas.children.values())
        for child in children:
            child.destroy()

        name_col = combo.get()
        value = val.get()
        del_row_frame_1.destroy()

        suitable_ind = binary_search(name_col, value)

        if not suitable_ind:
            messagebox.showinfo('Сообщение', 'Элемент не найден')
            return

        pd.DataFrame(pd.read_csv(csv_file)).drop(suitable_ind).to_csv(csv_file, index=False)

    btn_accept = tk.Button(del_row_frame_1, text="Удалить", command=btn_del_row_2)
    btn_accept.grid(column=0, row=2)


def btn_search_row_1():
    if clear_before_opening('Таблица не существует, создайте таблицу, чтбы найти в ней элементы'):
        return

    csv_file = list(filter(lambda x: x.endswith('.csv'), os.listdir(os.getcwd())))[0]

    search_row_frame_1 = tk.Toplevel(window)
    search_row_frame_1.title('Поиск элемента в таблице')
    search_row_frame_1.geometry('700x100+100+300')
    search_row_frame_1.resizable(False, False)
    search_row_frame_1.grab_set()
    search_row_frame_1.focus_set()

    lbl_1 = tk.Label(search_row_frame_1, text='Выберите признак, по которому будет произведен поиск:')
    lbl_1.grid(column=0, row=0)

    with open('{}_info.txt'.format(csv_file[:-4])) as json_file:
        metadata = json.load(json_file)
        combo_val = [col['col_name'] for col in metadata['columns']]
        combo = ttk.Combobox(search_row_frame_1)
        combo['values'] = combo_val
        combo.grid(column=1, row=0)

    lbl_2 = tk.Label(search_row_frame_1, text='Введите значние признака для поиска:')
    lbl_2.grid(column=0, row=1)

    val = tk.Entry(search_row_frame_1)
    val.grid(column=1, row=1)

    def btn_search_row_2():
        children = list(scroll_y.children.values()) + list(scroll_y.children.values()) + list(canvas.children.values())
        for child in children:
            child.destroy()

        name_col = combo.get()
        value = val.get()
        search_row_frame_1.destroy()

        suitable_ind = binary_search(name_col, value)

        if not suitable_ind:
            messagebox.showinfo('Сообщение', 'Элемент не найден')
            return

        search_row_frame_2 = tk.Frame(canvas)

        with open(list(filter(lambda x: x.endswith('.csv'),
                              os.listdir(os.getcwd())))[0], 'r') as f:
            reader = list(csv.reader(f))
            len_row = len(reader[0])

            for col_ind in range(len_row):
                el = tk.Entry(search_row_frame_2, width=20, fg='blue',
                              font=('Arial', 16, 'bold'))
                el.grid(row=0, column=col_ind)
                el.insert(tk.END, reader[0][col_ind])

            for i in suitable_ind:
                for j in range(len_row):
                    el = tk.Entry(search_row_frame_2)

                    el.grid(row=i + 1, column=j)
                    el.insert(tk.END, reader[i + 1][j])

        canvas.create_window(0, 0, anchor='nw', window=search_row_frame_2)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'),
                         yscrollcommand=scroll_y.set,
                         xscrollcommand=scroll_x.set)

        canvas.pack(fill='both', expand=True)
        scroll_y.pack(fill='y', side='right')
        scroll_x.pack(fill='x', side='bottom')

    btn_accept = tk.Button(search_row_frame_1, text="Найти", command=btn_search_row_2)
    btn_accept.grid(column=0, row=2)


def btn_edit_row_1():
    if clear_before_opening('Таблица не существует, создайте таблицу, чтбы изменить в ней элементы'):
        return

    csv_file = list(filter(lambda x: x.endswith('.csv'), os.listdir(os.getcwd())))[0]

    table_len = pd.DataFrame(pd.read_csv(csv_file)).shape[0]

    edit_row_frame_1 = tk.Toplevel(window)
    edit_row_frame_1.title('Изменение элемента в таблице')
    edit_row_frame_1.geometry('500x100+100+300')
    edit_row_frame_1.resizable(False, False)
    edit_row_frame_1.grab_set()
    edit_row_frame_1.focus_set()

    lbl_2 = tk.Label(edit_row_frame_1, text='Введите индекс строки для редактирования:')
    lbl_2.grid(column=0, row=0)

    val = tk.Entry(edit_row_frame_1)
    val.grid(column=1, row=0)

    def btn_edit_row_2():
        children = list(scroll_y.children.values()) + list(scroll_y.children.values()) + list(canvas.children.values())
        for child in children:
            child.destroy()

        try:
            ind = int(val.get())
            if ind not in range(table_len):
                edit_row_frame_1.destroy()
                messagebox.showinfo('Предупреждение', 'Некорректный номер строки')
                return
        except ValueError:
            edit_row_frame_1.destroy()
            messagebox.showinfo('Предупреждение', 'Некорректный номер строки')
            return

        edit_row_frame_1.destroy()
        edit_row_frame_2 = tk.Frame(canvas)

        with open('{}_info.txt'.format(csv_file[:-4])) as json_file:
            metadata = json.load(json_file)

        value_type_key = list()
        for row_n, col in enumerate(metadata['columns']):
            lbl_name = tk.Label(edit_row_frame_2, text=col['col_name'])
            lbl_name.grid(column=0, row=row_n)

            txt = tk.Entry(edit_row_frame_2, width=10)
            txt.grid(column=1, row=row_n)

            lbl_type = tk.Label(edit_row_frame_2, text='({})'.format(col['data_type']))
            lbl_type.grid(column=2, row=row_n)

            value_type_key.append([txt, col['data_type'], col['is_key_feat'], col['col_name']])

        def btn_edit_row_3():
            nonlocal value_type_key
            value_type_key = list(map(lambda el: [el[0].get(), el[1], el[2], el[3]], value_type_key))

            children = list(scroll_y.children.values()) + list(scroll_x.children.values()) + list(
                canvas.children.values())
            for child in children:
                child.destroy()

            row_for_edit = list()

            for col_ind, vtk in enumerate(value_type_key):
                try:
                    if dispatcher[vtk[1]] == bool:
                        el = 0 if vtk[0] == 'False' or vtk[0] == '0' else 1

                    else:
                        el = dispatcher[vtk[1]](vtk[0])
                    with open(csv_file, 'r') as inp:
                        reader = list(csv.reader(inp))
                        if (vtk[2] == 'Key') and (len(reader) > 1) and (
                                el in np.array(reader[1:])[:, col_ind].astype(dispatcher[vtk[1]])):
                            messagebox.showinfo('Предупреждение',
                                                'Такой элемент уже существует ({} - ключевое поле)'.format(vtk[3]))
                            return
                    row_for_edit.append(el)
                except ValueError:
                    messagebox.showinfo('Предупреждение', 'Неверный тип данных')
                    return

            tmp = pd.DataFrame(pd.read_csv(csv_file))
            tmp.iloc[ind] = row_for_edit
            tmp.to_csv(csv_file, index=False)

            messagebox.showinfo('Сообщение', 'Элемент был успешно изменен')

        btn_edit = tk.Button(edit_row_frame_2, text="Изменить", command=btn_edit_row_3)
        btn_edit.grid(column=1, row=1 + len(metadata['columns']))

        canvas.create_window(0, 0, anchor='nw', window=edit_row_frame_2)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'),
                         yscrollcommand=scroll_y.set)

        canvas.pack(fill='both', expand=True)
        scroll_y.pack(fill='y', side='right')

    btn_accept = tk.Button(edit_row_frame_1, text="Изменить", command=btn_edit_row_2)
    btn_accept.grid(column=0, row=1)


def btn_create_backup():
    if clear_before_opening('Таблица не существует, создайте таблицу, чтбы создать backup-файл'):
        return

    csv_file = list(filter(lambda x: x.endswith('.csv'), os.listdir(os.getcwd())))[0]

    try:
        os.mkdir('Backups')
    except OSError:
        pass

    shutil.copy(csv_file, 'Backups')
    shutil.copy('{}_info.txt'.format(csv_file[:-4]), 'Backups')

    messagebox.showinfo('Сообщение', 'Backup-файл был успешно создан')


def btn_rest_backup_1():
    children = list(scroll_y.children.values()) + list(scroll_x.children.values()) + list(canvas.children.values())
    for child in children:
        child.destroy()

    rest_backup_frame_1 = tk.Toplevel(window)
    rest_backup_frame_1.title("Восстановление таблицы из backup'a")
    rest_backup_frame_1.geometry('500x100+100+300')
    rest_backup_frame_1.resizable(False, False)
    rest_backup_frame_1.grab_set()
    rest_backup_frame_1.focus_set()

    lbl_1 = tk.Label(rest_backup_frame_1, text='Выберите backup-файл:')
    lbl_1.grid(column=0, row=0)

    try:
        combo_val = list(filter(lambda x: x.endswith('.csv'), os.listdir(os.getcwd() + '/Backups')))
    except FileNotFoundError:
        messagebox.showinfo('Предупреждение', 'Backup-файлов нет')
        rest_backup_frame_1.destroy()
        return

    combo = ttk.Combobox(rest_backup_frame_1)
    combo['values'] = combo_val
    combo.grid(column=1, row=0)

    def btn_rest_backup_2():
        rest_file_name = combo.get()
        rest_backup_frame_1.destroy()

        try:
            csv_file = list(filter(lambda x: x.endswith('.csv'), os.listdir(os.getcwd())))[0]
            os.remove(csv_file)
            os.remove('{}_info.txt'.format(csv_file[:-4]))
        except IndexError:
            pass

        shutil.copy(os.getcwd() + '/Backups/' + rest_file_name, os.getcwd())
        shutil.copy(os.getcwd() + '/Backups/{}_info.txt'.format(rest_file_name[:-4]), os.getcwd())

        messagebox.showinfo('Сообщение', 'Бд успешно восстановлена из backup-файла')

    btn_rest = tk.Button(rest_backup_frame_1, text="Восстановить", command=btn_rest_backup_2)
    btn_rest.grid(column=0, row=1)


def btn_import_xlsx():
    if clear_before_opening('Таблица не существует, создайте таблицу, чтбы импортировать ее в .xlsx файл'):
        return

    csv_file = list(filter(lambda x: x.endswith('.csv'), os.listdir(os.getcwd())))[0]

    try:
        os.mkdir('Xlsx')
    except OSError:
        pass

    merge_all_to_a_book(glob.glob(csv_file), 'Xlsx/{}.xlsx'.format(csv_file[:-4]))
    messagebox.showinfo('Сообщение', 'Бд успешно импортирована в .xlsx')


if __name__ == '__main__':
    '''
    Для создания графического интерфейса
    использовался встроенный модуль tkinter
    '''

    dispatcher = {'int': int, 'float': float, 'str': str, 'bool': bool}

    window = tk.Tk()
    window.title("My Data Base")
    window.geometry('1190x500')

    toolbar = tk.Frame(bg='#d7d8e0', bd=2)
    toolbar.pack(side=tk.TOP, fill=tk.X)

    canvas = tk.Canvas(window)
    scroll_y = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scroll_x = tk.Scrollbar(window, orient="horizontal", command=canvas.xview)

    btn = tk.Button(toolbar, text="Создать бд", command=btn_create_bd_1)
    btn.grid(row=0, column=0)

    btn = tk.Button(toolbar, text="Открыть бд", command=btn_open_bd)
    btn.grid(row=0, column=1)

    btn = tk.Button(toolbar, text="Удалить бд", command=btn_delete_bd)
    btn.grid(row=0, column=2)

    btn = tk.Button(toolbar, text="Очистить бд", command=btn_clean_bd)
    btn.grid(row=0, column=3)

    btn = tk.Button(toolbar, text="Добавить запись", command=btn_add_row_1)
    btn.grid(row=0, column=4)

    btn = tk.Button(toolbar, text="Удалить запись", command=btn_del_row_1)
    btn.grid(row=0, column=5)

    btn = tk.Button(toolbar, text="Поиск записей", command=btn_search_row_1)
    btn.grid(row=0, column=6)

    btn = tk.Button(toolbar, text="Изменение записи", command=btn_edit_row_1)
    btn.grid(row=0, column=7)

    btn = tk.Button(toolbar, text="Создать backup-файл бд", command=btn_create_backup)
    btn.grid(row=0, column=8)

    btn = tk.Button(toolbar, text="Восстановить бд", command=btn_rest_backup_1)
    btn.grid(row=0, column=9)

    btn = tk.Button(toolbar, text="Импорт бд в .xlsx", command=btn_import_xlsx)
    btn.grid(row=0, column=10)

    window.mainloop()
