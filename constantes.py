DATA = '29/07/2024'
# {datetime.today().strftime("%d/%m/%Y")}

LINUX = False
WINDOWS = False

# diretórios
csv_dir = './csv/'
#tex_dir = 'tex/'
#pdf_dir = 'pdf/'

# dias da semana
week_days = ['seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom']

# semestres
semestres = [1, 2]

#clf = ['disciplina', 'ano', 'semestre', 'modalidade',       'dia', 'hora', 'Carga Horária', 'status']

# dimensões/espaçamento das caixas
largura_caixa = 170
altura_caixa = 80
delta_caixa = 10
delta_dia = 30

zoom_ctr = 0
bbox_offset = 5

largura_dia = {d: 0 for d in week_days}
altura_semestre = {1: 0, 2: 0}
primeira_hora = {1: 24, 2: 24}
ultima_hora = {1: 0, 2: 0}


#yoffset = 600
yoffset_dic = {
    1: 0,
    2: 600 #-(ultima_hora[2] - primeira_hora[2]) * altura_caixa / 2
}


# dicionários
cores_tkinter = {
    1: '#80F479',
    2: '#FFF92C',
    3: '#97C6F8',
    4: '#FF941E',
    'bbox': '#D9CFB9'
}

modalidades_dict = {
    0: 'C',
    1: 'L',
    2: 'B'
}

replace_dic = {
    'Educação':'Ed.', 
    'Matemática':'Mat.', 
    'Equações':'Eq.', 
    'Funções':'Fçs.', 
    'Euclidiana':'Eucl.', 
    'Variável':'Var.', 
    'Supervisionado':'Superv.',
    'Métodos':'Mét.',
    #'Diferencial':'Dif.',
}

# Listas
curr_canvas = []

# Strings
#info_message = 'Clique em uma caixa para exibir as informações da disciplina. Mouse Scroll para zoom.'
info_message = ''

if __name__ == '__main__':
    print('teste')
