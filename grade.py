'''
BUGS 
    disciplinas de 1 hora de duração: não cabe conteúdo na caixa do node;
'''

'''
TODO
'''

import numpy as np
import pandas as pd
import subprocess
from constantes import cores_tkinter

def atualizarMapa(horaInicial, duracao, vagas):
    horaFinal = horaInicial + duracao
    tmp = sum(vagas[horaInicial:horaFinal,:]) == False
    idx = np.argmax(tmp)
    vagas[horaInicial:horaFinal, idx] = True
    return (int(idx), int(horaInicial))

# diretórios
csv_dir='csv/'
tex_dir='tex/'
pdf_dir='pdf/'

# arquivo de input
csv_file = csv_dir + 'grade-old-new.csv'

modalidades_desejadas = ['L', 'B']
anos_desejadas = [1, 2, 3, 4]
semestres_desejados = [1, 2]
ano = 2025
show_old = True

cores = {
    1:'corI',
    2:'corII',
    3:'corIII',
    4:'corIV'
}

ccores_tkinter = {
    1:'#80F479',
    2:'#FFF92C',
    3:'#97C6F8',
    4:'#FF941E'
}


# colunas a serem usadas do csv
clf = ['disciplina','ano','semestre','modalidade','dia','hora','Carga Horária','status']

df = pd.read_csv(csv_file, comment='#').sort_values(['ano', 'semestre', 'disciplina'])[clf]
df = df[df['ano'].isin(anos_desejadas)][clf]
df['semestre'] = df['semestre'].fillna(value=0).astype(int)
df['dia'] = df['dia'].fillna(value='')
df['hora'] = df['hora'].fillna(value='')

#foo = df[df['ano'].isin(anos_desejadas)][['dia', 'hora', 'disciplina', 'ano']]
#df.to_csv('foo.csv', index=False)

tkinter_list_code = ['ano,semestre,modalidade,dia,hora_begin,hora_end,x,y,disciplina,status']

def grade_diaria(modalidade, semestre, dia):
    print(f'Filtrando dados para {dia} do {semestre} semestre da modalidade {modalidade}')
    tmp = df[df['semestre'] == semestre]
    tmp = tmp[(tmp['modalidade'].isin(modalidade)) | (tmp['modalidade'] == 'C')]
    tmp = tmp[tmp['dia'].str.contains(dia, na=False)].to_numpy() #.sort_values('credito', ascending=False)
    
    tex_file = tex_dir + f'sem{semestre}-{dia}.tex'
    vagas = np.full((24, 20), False)

    with open(tex_file, 'w') as f:
        f.write('%% Criado por grade.py\n%% Autor: Thiago de Melo\n% !TeX root = ../main.tex\n')
        f.write(r"\node[semestre] {\ano\ (%s\textsuperscript{o} sem.)  %s.};" % (semestre, dia.replace('sab', 'sáb')) + "\n")
        for i, linha in enumerate(tmp):
            # 'disciplina','ano','semestre','modalidade','dia','hora','status'
            #print(linha)
            
            disciplina = linha[0].replace('Geometria','Geom.').replace('Cálculo Diferencial','Cálc. Dif.').replace('Teoria','Teo.')
            ano = linha[1]
            semestre = linha[2]
            modalidade = linha[3]
            cor = cores[ano]
            status = linha[7]
            
            indices = [i for i, x in enumerate(linha[4].split(';')) if x == dia]
            
            for idx in indices:
                hora_begin = int(linha[5].split(';')[idx].split('-')[0])
                hora_end = int(linha[5].split(';')[idx].split('-')[1])
                duracao = hora_end - hora_begin
                credito_disciplina = linha[6] // 15
                position = atualizarMapa(hora_begin, duracao, vagas)
                horario = f"{hora_begin}--{hora_end}" + f" ({int(credito_disciplina)}) - {ano}\\textsuperscript o ano"

                icon_modalidade = r"\node[modalidade] at (hora-%02d.south east) {\aviso{%s}};" % (hora_begin, modalidade)

                code = r"\node[disciplina={%d}{%s}] (hora-%02d) at %s {\dados{%s}{}{%s}{%s}};" % (duracao, cor, hora_begin, position, disciplina, horario, modalidade)
                code += icon_modalidade

                if status == 'new':
                    icon_status = r"\node[sem docente] at (hora-%02d.south west) {\aviso{\faWarning}};" % (hora_begin)
                    code += icon_status

                if status == 'old' and show_old:
                    code = r"\node[disciplina={%d}{%s},old] (hora-%02d) at %s {\dados{%s}{}{%s}{%s}};" % (duracao, cor, hora_begin, position, disciplina, horario, modalidade)
                    icon_modalidade = r"\node[modalidade,old] at (hora-%02d.south east) {\aviso{%s}};" % (hora_begin, modalidade)
                    code += icon_modalidade

                f.write(code + "\n")
                
                if status == 'old':
                    tkinter_cor = 'white'
                else:
                    tkinter_cor = cores_tkinter[ano]

                tkinter_code = f"{ano},{semestre},{modalidade},{dia},{hora_begin},{hora_end},{position[0]},{position[1]},\"{disciplina}\",{status}"
                tkinter_list_code.append(tkinter_code)
                '''
                for i in range(1, duracao):
                    j = int(hora_begin) + i
                    poscode = r"\node[vazio] (hora-%02d) at (hora-%02d.north east){};" % (j, j) + "\n"
                    f.write(poscode)
                '''
    
    #with open(tex_dir + 'horas.tex', 'a') as f:
        #num_cols = len(np.nonzero(sum(vagas))[0])
        #f.write(r"\draw[help lines] (0,8) grid (%d, 24);" % num_cols)
        f.close()

def gerar_grade():
    for semestre in range(1, 3):
        for dia in ['seg', 'ter', 'qua', 'qui', 'sex', 'sab']:
            #continue
            grade_diaria(modalidades_desejadas, semestre, dia)
    np.savetxt('tkinter_code.csv', tkinter_list_code, delimiter=",", fmt="%s")
    subprocess.run(["python3", "criar_dicionario_dados.py"]) 


''' FUNÇÕES PRINCIPAIS '''
gerar_grade()

quit()




#print(docentes[docentes != ''])
#print(df[df['docente'] != ''][['docente', 'curso', 'disciplina']])
#print(df[df['docente'] == ''][['curso', 'disciplina', 'credito']])

disciplinas_com_docente = df[df['docente'] != sem_docente].shape[0]
disciplinas_sem_docente = df[df['docente'] == sem_docente].shape[0]
num_disciplinas = disciplinas_com_docente + disciplinas_sem_docente




## bug: não dá pra usar str na coluna de créditos se ela é int.
tmpa = df[df['docente'] != sem_docente]['credito'].str.split(';', expand=True)[0].to_numpy()
tmpb = df[df['docente'] != sem_docente]['credito'].str.split(';', expand=True)[1].to_numpy()

creditos_com_docente = sum(int(x) for x in tmpb[tmpb != None]) + sum(int(x) for x in tmpa)
creditos_sem_docente = df[df['docente'] == sem_docente]['credito'].astype(int).sum()
num_creditos = creditos_com_docente + creditos_sem_docente

with open('tex/old-rodape.tex', 'w') as f:
    f.write(r"Disciplinas com docente: \textbf{%d/%d} (%.0f\%%) (\textbf{%d/%d} créditos). " % (disciplinas_com_docente, num_disciplinas, disciplinas_com_docente/num_disciplinas*100, creditos_com_docente, num_creditos))
    f.write(r"Disciplinas sem docente: \textbf{%d/%d} (%.0f\%%) (\textbf{%d/%d} créditos). " % (disciplinas_sem_docente, num_disciplinas, disciplinas_sem_docente/num_disciplinas*100, creditos_sem_docente, num_creditos))
    f.write(r"Cursos atendidos: ")
    for curso in df['curso'].unique():
        tmp = df[df['curso'] == curso]['credito'].str.split(';').sum()
        num_cred = sum([int(s) for s in tmp])
        num_disc = df[df['curso'] == curso].shape[0]
        tmp = df[(df['curso'] == curso) & (df['docente'] != sem_docente)]['credito'].str.split(';').sum()
        num_cred_coberto = 0
        if tmp != 0:
            num_cred_coberto += sum([int(s) for s in tmp])
        f.write(r"%s (\textbf{%d} disc.; \textbf{%d/%d} (%.0f\%%) créd.). " % (curso, num_disc, num_cred_coberto, num_cred, num_cred_coberto/num_cred*100))
    #print(disciplinas_com_docente, creditos_com_docente, disciplinas_sem_docente, creditos_sem_docente)
    f.close()


#print(df.sort_values(by=['hora'], inplace=False)[['dia', 'hora']])


