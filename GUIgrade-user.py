'''
TODO
    altura e distância vertical entre bbox dos dias da semana precisa ser automatizada

BUG
'''

MODE = 'USER'
csv_file = None

import os
import textwrap
import tkinter as tk
from tkinter import ALL
from constantes import *
from dicionario_dados import *


def subs(palavra):
    for k in replace_dic.keys():
        palavra = palavra.replace(k, replace_dic[k])
    return palavra


def check_hand_enter(event):
    curr_canvas[-1].config(cursor="question_arrow")
    show_text(event)


def check_hand_leave(event):
    curr_canvas[-1].config(cursor="arrow")
    show_text(event)


def resetar_grade(event):
    if checkVarAno1.get() == 0:
        checkbutton_ano1.invoke()
    if checkVarAno2.get() == 0:
        checkbutton_ano2.invoke()
    if checkVarAno3.get() == 0:
        checkbutton_ano3.invoke()
    if checkVarAno4.get() == 0:
        checkbutton_ano4.invoke()
    if checkVarSem1.get() == 0:
        checkbutton_semestre1.invoke()
    if checkVarSem2.get() == 0:
        checkbutton_semestre2.invoke()
    if checkVarModalidadeC.get() == 0:
        checkbutton_modalidadeC.invoke()
    if checkVarModalidadeL.get() == 0:
        checkbutton_modalidadeL.invoke()
    if checkVarModalidadeB.get() == 0:
        checkbutton_modalidadeB.invoke()


def anos_selecionados():
    return checkVarAno1.get(), checkVarAno2.get(), checkVarAno3.get(), checkVarAno4.get()


def semestres_selecionados():
    return checkVarSem1.get(), checkVarSem2.get()


def modalidades_selecionados():
    return checkVarModalidadeC.get(), checkVarModalidadeL.get(), checkVarModalidadeB.get()


def toggle_year(ano):
    # Função para alternar a exibição do ano
    semestres_ON = semestres_selecionados()
    modalidades_ON = [modalidades_dict[i]
                      for i, _ in enumerate(modalidades_selecionados()) if _ == 1]

    canvas = curr_canvas[-1]
    for item in canvas.find_all():
        tags = canvas.gettags(item)

        if tags[0] == 'caixa_disc' or tags[0] == 'texto_disc':
            if tags[1] == str(ano) and semestres_ON[int(tags[2])-1] == 1 and tags[3] in modalidades_ON:
                state = canvas.itemcget(item, 'state')
                if state == 'normal':
                    canvas.itemconfig(item, state='hidden')
                else:
                    canvas.itemconfig(item, state='normal')


def toggle_semester(semestre):
    # Função para alternar a exibição do semestre
    anos_ON = anos_selecionados()
    modalidades_ON = [modalidades_dict[i]
                      for i, _ in enumerate(modalidades_selecionados()) if _ == 1]

    canvas = curr_canvas[-1]
    for item in canvas.find_all():
        tags = canvas.gettags(item)

        if tags[0] == 'caixa_disc' or tags[0] == 'texto_disc':
            if tags[2] == str(semestre) and anos_ON[int(tags[1])-1] == 1 and tags[3] in modalidades_ON:
                state = canvas.itemcget(item, 'state')
                if state == 'normal':
                    canvas.itemconfig(item, state='hidden')
                else:
                    canvas.itemconfig(item, state='normal')


def toggle_modalidade(modalidade):
    # Função para alternar a exibição da modalidade
    anos_ON = anos_selecionados()
    semestres_ON = semestres_selecionados()
    
    canvas = curr_canvas[-1]
    for item in canvas.find_all():
        tags = canvas.gettags(item)

        if tags[0] == 'caixa_disc' or tags[0] == 'texto_disc':
            if tags[3] == str(modalidade) and anos_ON[int(tags[1])-1] == 1 and semestres_ON[int(tags[2])-1] == 1:
                state = canvas.itemcget(item, 'state')
                if state == 'normal':
                    canvas.itemconfig(item, state='hidden')
                else:
                    canvas.itemconfig(item, state='normal')


def on_key_press(event):
    if event.char.lower() == '1':
        toggle_year(1)
        checkbutton_ano1.toggle()
    elif event.char.lower() == '2':
        toggle_year(2)
        checkbutton_ano2.toggle()
    elif event.char.lower() == '3':
        toggle_year(3)
        checkbutton_ano3.toggle()
    elif event.char.lower() == '4':
        toggle_year(4)
        checkbutton_ano4.toggle()
    elif event.char.lower() == 'c':
        toggle_modalidade(event.char.upper())
        checkbutton_modalidadeC.toggle()
    elif event.char.lower() == 'l':
        toggle_modalidade(event.char.upper())
        checkbutton_modalidadeL.toggle()
    elif event.char.lower() == 'b':
        toggle_modalidade(event.char.upper())
        checkbutton_modalidadeB.toggle()
    elif event.char.lower() == 'a':
        toggle_semester(1)
        checkbutton_semestre1.toggle()
    elif event.char.lower() == 'z':
        toggle_semester(2)
        checkbutton_semestre2.toggle()


def toggle_full_screen(dummy=None):
    state = False if root.attributes('-fullscreen') else True
    root.attributes('-fullscreen', state)
    if not state:
        root.geometry('1366x720+0+0')


def do_zoom_in(event):
    global zoom_ctr
    zoom_ctr += 1
    x = curr_canvas[-1].canvasx(event.x)
    y = curr_canvas[-1].canvasy(event.y)
    factor = 1.1
    curr_canvas[-1].fontSize = curr_canvas[-1].fontSize * factor
    for item in curr_canvas[-1].find_all():
        tags = curr_canvas[-1].gettags(item)
        if 'texto' in tags[0]:
            curr_canvas[-1].itemconfigure(item,
                                          font=("Arial", int(curr_canvas[-1].fontSize)))
    curr_canvas[-1].scale(ALL, x, y, factor, factor)


def do_zoom_out(event):
    global zoom_ctr
    zoom_ctr -= 1
    x = curr_canvas[-1].canvasx(event.x)
    y = curr_canvas[-1].canvasy(event.y)
    factor = 0.9
    curr_canvas[-1].fontSize = curr_canvas[-1].fontSize * factor
    for item in curr_canvas[-1].find_all():
        tags = curr_canvas[-1].gettags(item)
        if 'texto' in tags[0]:
            curr_canvas[-1].itemconfigure(item,
                                          font=("Arial", int(curr_canvas[-1].fontSize)))
    curr_canvas[-1].scale(ALL, x, y, factor, factor)


def do_zoom_reset(event):
    if zoom_ctr < 0:
        for _ in range(abs(zoom_ctr)):
            do_zoom_in(event)
    if zoom_ctr > 0:
        for _ in range(abs(zoom_ctr)):
            do_zoom_out(event)


def show_text(event):
    start_drag(event)

    x, y = event.x, event.y
    foo = curr_canvas[-1].find_closest(x, y, halo=10, start=None)
    tags = curr_canvas[-1].gettags(foo)

    if 'texto_disc' in tags:
        txt = curr_canvas[-1].itemcget(foo, 'text')
        ano = int(txt.split('\n')[-1][0])
        txt = txt.replace('\n', ' ')
        csv_labelText.set(f'{txt}')
        csv_Label.config(bg=cores_tkinter[ano])
    elif 'caixa_disc' in tags:
        faa = curr_canvas[-1].find_above(foo)
        txt = curr_canvas[-1].itemcget(faa, 'text')
        ano = int(txt.split('\n')[-1][0])
        txt = txt.replace('\n', ' ')
        csv_labelText.set(f'{txt}')
        csv_Label.config(bg=cores_tkinter[ano])
    else:
        csv_labelText.set(info_message)
        csv_Label.config(bg=root.cget("background"))
        

def start_drag(event):
    # Inicia o arrasto do mouse
    global last_x, last_y
    last_x, last_y = event.x, event.y


def move_canvas(event):
    # Calcula o deslocamento do mouse
    global last_x, last_y
    dx = event.x - last_x
    dy = event.y - last_y

    # Move todos os objetos na canvas
    for item in curr_canvas[-1].find_all():
        curr_canvas[-1].move(item, dx, dy)

    # Atualiza as coordenadas do mouse
    last_x, last_y = event.x, event.y


def draw_on_canvas(canvas, csv_file, semestre, dia):
    tmp = [p for p in load_dic_grade() if p['dia'] == dia]
    dic_grade = [p for p in tmp if p['semestre'] == semestre]
    if len(tmp) > 0:
        N = max([p['x']+1 for p in tmp])
        largura_dia[dia] = N * largura_caixa + (N - 1) * delta_caixa

    # criar caixas e textos para cada disciplina
    for row in dic_grade:
        ano = int(row['ano'])
        semestre = int(row['semestre'])
        modalidade = str(row['modalidade'])
        dia = str(row['dia'])
        x, y = int(row['x']), int(row['y'])
        cor = cores_tkinter[ano]
        disciplina = subs(str(row['disciplina']))
        hora_begin, hora_end = int(row['hora_begin']), int(row['hora_end'])
        duracao = hora_end - hora_begin
        status = str(row['status'])
    
        if status == 'new':
            border_width = 3
            border_color = 'red'
            border_style = None
        elif status == 'old':
            border_width = 1
            border_color = 'black'
            border_style = (10, 5)
            cor = cores_tkinter['bbox']
        else:
            border_width = 1
            border_color = 'black'
            border_style = None

        idx = week_days.index(dia)
        x = x * (largura_caixa + delta_caixa) + sum([largura_dia[week_days[j]] for j in range(idx)]) + delta_dia * idx
        y = (y-8)*altura_caixa/2 + yoffset_dic[semestre] + y*delta_caixa/2
        #y -= primeira_hora[semestre] * altura_caixa #/ 2 + yoffset_dic[semestre] + y * delta_caixa / 2
        #y *= altura_caixa // 2
        #y -= primeira_hora[semestre] * altura_caixa // 2
        #y += y // 10 + yoffset_dic[semestre]

        # caixas coloridas para as disciplinas
        retangulo = canvas.create_rectangle(
                        x, y, x + largura_caixa, y + altura_caixa * duracao / 2 + (duracao - 2) * delta_caixa / 2, 
                        state='normal', 
                        fill=cor,
                        outline=border_color,
                        width=border_width,
                        dash=border_style,
                        tag=['caixa_disc', f'{ano}', f'{semestre}', f'{modalidade}', f'{dia}', f'{status}'],
                        #cursor='question_arrow',
                        #activefill='gray',
                        )


        canvas.tag_bind('texto_disc', "<Enter>", lambda event: check_hand_enter(event))
        canvas.tag_bind('texto_disc', "<Leave>", lambda event: check_hand_leave(event))
        canvas.tag_bind('caixa_disc', "<Enter>", lambda event: check_hand_enter(event))
        canvas.tag_bind('caixa_disc', "<Leave>", lambda event: check_hand_leave(event))
    
        wrapped = textwrap.fill(disciplina, 25)
        text = f'{wrapped}\n{dia} ({hora_begin}-{hora_end})\n{ano} ano ({modalidade})'
    
        # textos para as disciplinas
        canvas.create_text(
                (x + x + largura_caixa) / 2, 
                (y + y + altura_caixa) / 2, 
                text=f'{text}',
                fill='black', 
                font=('Arial', 10),
                justify='center',
                state='normal',
                tag=['texto_disc', f'{ano}', f'{semestre}', f'{modalidade}', f'{status}'],
                #activefill='red',
                )
 
    # criar bbox cinza para cada dia/sem
    tmp = []
    for item in canvas.find_all():
        tags = canvas.gettags(item)
        if tags[0] == 'caixa_disc' and dia in tags and tags[2] == str(semestre):
            tmp.append(canvas.bbox(item))

    if len(tmp) > 0:
        xmin = min([c[0] for c in tmp]) - bbox_offset
        xmax = max([c[2] for c in tmp]) + bbox_offset
        ymin = min([c[1] for c in tmp]) - bbox_offset
        ymax = max([c[3] for c in tmp]) + bbox_offset
        #ymin = primeira_hora[semestre] - bbox_offset
        #ymin = - bbox_offset
        #ymax = (ultima_hora[semestre] - primeira_hora[semestre]) * altura_caixa // 2 
        #ymax += (ultima_hora[semestre] - primeira_hora[semestre]) * delta_caixa // 2 - bbox_offset
        #ymax *= altura_caixa

        # bbox do dia
        canvas.create_rectangle(
                        xmin, ymin, xmax, ymax, 
                        state='normal', 
                        tag=[f'bb{dia}'],
                        fill=cores_tkinter['bbox'],
                        #activefill='gray',
                        #outline='black',
                        width=0,
                        )

        # faixa acima do bbox do dia
        canvas.create_rectangle(
                        xmin, ymin - 30, xmax , ymin - 5,
                        state='normal', 
                        tag=[f'bb{dia}'],
                        fill='#F0EDDC', 
                        #activefill='gray',
                        outline='#D9CFB9',
                        width=1,
                        )

        # texto da faixa acima do bbox do dia
        canvas.create_text(
                        (xmin + xmax)/2, ymin - 15,
                        text=f'{dia} - sem. {semestre}',
                        font=('Arial', 10, 'bold'),
                        tag=(f'texto',),
                        )

        canvas.tag_lower(f'bb{dia}', 1)




def create_canvas(csv_file):

    canvas = tk.Canvas(root, bg='white', width=screen_width,
                       height=int(0.8*screen_height))
    canvas.grid(row=1, sticky='nswe')
    curr_canvas.append(canvas)
    curr_canvas[-1].fontSize = 10
    canvas.focus_set()

    canvas.bind("<Left>", lambda event: canvas.xview_scroll(-1, "units"))
    canvas.bind("<Right>", lambda event: canvas.xview_scroll(1, "units"))
    canvas.bind("<Up>", lambda event: canvas.yview_scroll(-1, "units"))
    canvas.bind("<Down>", lambda event: canvas.yview_scroll(1, "units"))
    canvas.bind('<Button-1>', start_drag)
    canvas.bind('<Button-1>', show_text)
    canvas.bind('<B1-Motion>', move_canvas)
    canvas.bind('<4>', do_zoom_in)
    canvas.bind('<5>', do_zoom_out)

    for dia in week_days:
        for semestre in [1, 2]:
            draw_on_canvas(canvas, csv_file, semestre, dia)

    return canvas


if __name__ == '__main__':
    
    basedir = os.path.dirname(__file__)
    icon_file = 'icone-m.png'
    icon_file = 'hopf.png'
    icon_file = 'icone.png'

    # main window
    root = tk.Tk()
    root.title('Grade Curricular Matematica - IGCE Unesp')
    root.attributes('-fullscreen', False)
    root.attributes('-zoomed', True)

    icon = tk.PhotoImage(file=os.path.join(basedir, icon_file)) #/home/thiago/Dropbox/programacao/grade/icone-m.png
    root.iconphoto(False, icon)

    # layout all of the main containers
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # barra de botões
    header_frame = tk.Frame(root, height=20)
    header_frame.grid(row=0, sticky='we')

    # canvas da grade
    canvas = create_canvas(None)
    curr_canvas[-1].fontSize = 10

    # barra de rodapé
    footer_frame = tk.Frame(root, height=12)
    footer_frame.grid(row=2, columnspan=True, sticky='we')
    author_Label = tk.Label(footer_frame, text='Criado por Thiago de Melo', font=(
        'Arial', 10))
    author_Label.pack(side='left', expand=False, padx=0, pady=5)

    csv_labelText = tk.StringVar()
    csv_labelText.set(info_message)
    csv_Label = tk.Label(
        footer_frame,
        text=f'{csv_file}',
        textvariable=csv_labelText,
        font=('Arial', 12),
        #fg='blue',
    )
    csv_Label.pack(side='left', expand=True, pady=5)

    date_Label = tk.Label(footer_frame, text=f'Mode: {MODE}   Compilado em {DATA}', font=(
        'Arial', 10))
    date_Label.pack(side='right', expand=False, pady=5)

    #button = tk.Button(footer_frame, text='change csv', command=open_csv)
    #button.pack(side='left')

    # iniciar variaveis
    checkVarAno1 = tk.IntVar()
    checkVarAno2 = tk.IntVar()
    checkVarAno3 = tk.IntVar()
    checkVarAno4 = tk.IntVar()
    checkVarSem1 = tk.IntVar()
    checkVarSem2 = tk.IntVar()
    checkVarModalidadeC = tk.IntVar()
    checkVarModalidadeL = tk.IntVar()
    checkVarModalidadeB = tk.IntVar()

    # checkbuttons para os anos
    checkbutton_ano1 = tk.Checkbutton(header_frame, text=f'1 ano', underline=0, font=(
        'Arial', 12), bg=cores_tkinter[1], variable=checkVarAno1, onvalue=1, offvalue=0, command=lambda: toggle_year(1))
    checkbutton_ano1.pack(side='left', padx=3, pady=3)
    checkbutton_ano1.select()
    checkbutton_ano2 = tk.Checkbutton(header_frame, text=f'2 ano', underline=0, font=(
        'Arial', 12), bg=cores_tkinter[2], variable=checkVarAno2, onvalue=1, offvalue=0, command=lambda: toggle_year(2))
    checkbutton_ano2.pack(side='left', padx=3, pady=3)
    checkbutton_ano2.select()
    checkbutton_ano3 = tk.Checkbutton(header_frame, text=f'3 ano', underline=0, font=(
        'Arial', 12), bg=cores_tkinter[3], variable=checkVarAno3, onvalue=1, offvalue=0, command=lambda: toggle_year(3))
    checkbutton_ano3.pack(side='left', padx=3, pady=3)
    checkbutton_ano3.select()
    checkbutton_ano4 = tk.Checkbutton(header_frame, text=f'4 ano', underline=0, font=(
        'Arial', 12), bg=cores_tkinter[4], variable=checkVarAno4, onvalue=1, offvalue=0, command=lambda: toggle_year(4))
    checkbutton_ano4.pack(side='left', padx=3, pady=3)
    checkbutton_ano4.select()

    # checkbuttons para os semestres
    checkbutton_semestre1 = tk.Checkbutton(header_frame, text=f'1 sem (A)', underline=7, font=(
        'Arial', 12), variable=checkVarSem1, onvalue=1, offvalue=0, command=lambda: toggle_semester(1))
    checkbutton_semestre1.pack(side='left', padx=3, pady=3)
    checkbutton_semestre1.select()
    checkbutton_semestre2 = tk.Checkbutton(header_frame, text=f'2 sem (Z)', underline=7, font=(
        'Arial', 12), variable=checkVarSem2, onvalue=1, offvalue=0, command=lambda: toggle_semester(2))
    checkbutton_semestre2.pack(side='left', padx=3, pady=3)
    checkbutton_semestre2.select()

    # checkbuttons para as modalidades
    checkbutton_modalidadeC = tk.Checkbutton(header_frame, text=f'Comum', fg='darkblue', underline=0, font=(
        'Arial', 12), variable=checkVarModalidadeC, onvalue=1, offvalue=0, command=lambda: toggle_modalidade('C'))
    checkbutton_modalidadeC.pack(side='left', padx=3, pady=3)
    checkbutton_modalidadeC.select()
    checkbutton_modalidadeL = tk.Checkbutton(header_frame, text=f'Lic', fg='darkblue', underline=0, font=(
        'Arial', 12), variable=checkVarModalidadeL, onvalue=1, offvalue=0, command=lambda: toggle_modalidade('L'))
    checkbutton_modalidadeL.pack(side='left', padx=3, pady=3)
    checkbutton_modalidadeL.select()
    checkbutton_modalidadeB = tk.Checkbutton(header_frame, text=f'Bach', fg='darkblue', underline=0, font=(
        'Arial', 12), variable=checkVarModalidadeB, onvalue=1, offvalue=0, command=lambda: toggle_modalidade('B'))
    checkbutton_modalidadeB.pack(side='left', padx=3, pady=3)
    checkbutton_modalidadeB.select()

    # labels para teclas de atalho
    label_Reset = tk.Label(header_frame, text='Reset (F5)',
                           font=('Arial', 12), fg='red')
    label_Reset.pack(side='left', padx=3, pady=3)
    label_F11 = tk.Label(header_frame, text='Tela Cheia (F11)',
                         font=('Arial', 12), fg='blue')
    label_F11.pack(side='left', padx=3, pady=3)
    label_ESC = tk.Label(header_frame, text='Sair (ESC)',
                         font=('Arial', 12), fg='brown')
    label_ESC.pack(side='left', padx=3, pady=3)

    # eventos da main window
    root.bind('-', do_zoom_out)
    root.bind('=', do_zoom_in)
    root.bind('0', do_zoom_reset)
    root.bind('<KeyPress>', on_key_press)
    root.bind('<F11>', toggle_full_screen)
    root.bind('<F5>', resetar_grade)
    root.bind('<Escape>', lambda x: root.destroy())

    #canvas.create_rectangle(0, 0, 200, altura_semestre[1] * altura_caixa + (altura_semestre[1] - 1 ) * delta_caixa )
    #draw_grid()
    
    # main loop
    root.mainloop()
