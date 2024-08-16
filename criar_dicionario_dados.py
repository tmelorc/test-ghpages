import csv

# arquivo csv criado pelo programa ./distro.py
csv_file = '/home/thiago/Dropbox/programacao/grade/tkinter_code.csv'

print('** Executando criar_dicionario_dados.py para gerar ./dicionario_dados.py')


with open(csv_file) as f,  open('./dicionario_dados.py', 'w') as foo:
    reader = csv.DictReader(f, delimiter=',')
    foo.write(f'def load_dic_grade():\n')
    foo.write(f'\tdic_grade = [\n')
    for row in reader:
        foo.write(f'\t\t{{\
\'ano\':{row["ano"]},\
\'semestre\':{row["semestre"]},\
\'modalidade\':\'{row["modalidade"]}\',\
\'dia\':\'{row["dia"]}\',\
\'hora_begin\':{row["hora_begin"]},\
\'hora_end\':{row["hora_end"]},\
\'x\':{row["x"]},\
\'y\':{row["y"]},\
\'disciplina\':\'{row["disciplina"]}\',\
\'status\':\'{row["status"]}\'}},\n'\
)
    foo.write(f'\t]\n')
    foo.write(f'\treturn dic_grade')
