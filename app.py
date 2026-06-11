# ------------------------------------------------
# IMPORTAÇÃO DE BIBLIOTECAS
# ------------------------------------------------

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# ------------------------------------------------
# CONFIGURAÇÃO DA API XANO
# ------------------------------------------------

# Substitua pela SUA URL real do grupo de API no Xano
BASE_URL = 'https://x8ki-letl-twmt.n7.xano.io/api:brtRNGSH'

# ------------------------------------------------
# FUNÇÕES DE CONEXÃO E UTILITÁRIOS
# ------------------------------------------------

def get_headers():
    '''
    Gera o cabeçalho com o JSON Web Token (JWT) para autenticação segura.
    '''
    headers = {'Content-Type': 'application/json'}
    if 'auth_token' in st.session_state:
        headers['Authorization'] = f'Bearer {st.session_state.auth_token}'
    return headers

def api_get(endpoint):
    '''
    Lê dados do Xano (filtra automaticamente pelo usuário no servidor).
    '''
    resposta = requests.get(f'{BASE_URL}/{endpoint}', headers=get_headers())
    return resposta.json() if resposta.status_code == 200 else []

def api_post(endpoint, dados):
    '''
    Cria um novo registro vinculado ao aluno logado.
    '''
    return requests.post(f'{BASE_URL}/{endpoint}', json=dados, headers=get_headers())

def api_patch(endpoint, id, dados):
    '''
    Atualiza um registro existente.
    '''
    return requests.patch(f'{BASE_URL}/{endpoint}/{id}', json=dados, headers=get_headers())

def api_delete(endpoint, id):
    '''
    Remove um registro do banco de dados.
    '''
    return requests.delete(f'{BASE_URL}/{endpoint}/{id}', headers=get_headers())

# ------------------------------------------------
# SISTEMA DE AUTENTICAÇÃO
# ------------------------------------------------

def tela_acesso():
    st.title('Portal Acadêmico Personalizado')
    
    if st.session_state.page == 'forgot':
        st.header('Recuperar Senha')
        email_recuperado = st.text_input('Digite o e-mail cadastrado', key='email_rec')
        if st.button('Enviar instruções'):
            emails_existentes = api_get('user')  # Qual é o endpoint?
            email_usado = [u['email'] for u in emails_existentes]

            st.success('Se o e-mail estiver cadastrado, você receberá instruções em breve.')
        if st.button('Voltar ao Login'):
            st.session_state.page = 'login'
            st.rerun()
        return

    tab_login, tab_cadastro = st.tabs(['Entrar', 'Criar Minha Conta'])
    st.markdown("""
<style>  
/* Fundo dos inputs (email e senha) */
input, .stTextInput input {
    background-color: #1E1E1E !important;  /* cinza bem mais escuro */
    color: white !important;
    border: 1px solid #444 !important;
    border-radius: 8px;
}

/* Quando clica no input */
input:focus {
    background-color: #151515 !important;
    border: 1px solid #2563EB !important;
}

/* Label (E-mail / Senha) */
label {
    color: #E0E0E0 !important;
}

</style>
""", unsafe_allow_html=True)

    with tab_login:
        with st.form('login_form'):
            email = st.text_input('E-mail')
            senha = st.text_input('Senha', type='password')
            if st.form_submit_button('Acessar Meu Painel'):
                res = requests.post(f'{BASE_URL}/auth/login', json={'email': email, 'password': senha})
                if res.status_code == 200:
                    st.session_state.auth_token = res.json().get('authToken')
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error('Credenciais inválidas.')
            
            if st.form_submit_button('Esqueci a Senha'):
                st.session_state.page = 'forgot'
                st.rerun()

    with tab_cadastro:
        with st.form('cadastro_form'):
            nome = st.text_input('Nome')
            email_c = st.text_input('E-mail')
            pass_c = st.text_input('Senha', type='password')
            pass_c2 = st.text_input('Confirmar Senha')

            if st.form_submit_button('Cadastrar'):
                if not nome or not email_c or not pass_c or not pass_c2:
                    st.error('Preencha todos os campos.')
                elif pass_c != pass_c2:
                    st.error('As senhas não coincidem.')
                else:
                    # Verificar se nome já existe
                    usuarios_existentes = api_get('user')  # Qual é o endpoint?
                    nomes_usados = [u['name'] for u in usuarios_existentes]
                
                    if nome in nomes_usados:
                        st.error('Este nome de usuário já está em uso.')
                    else:
                        res = requests.post(f'{BASE_URL}/auth/signup', json={'name': nome, 'email': email_c, 'password': pass_c})
                        if res.status_code == 200:
                            st.success('Conta criada! Agora faça o login.')
                        elif res.status_code == 409:  # Conflito (já existe)
                            st.error('Nome ou e-mail já cadastrado.')
                        else:
                            st.error(f'Erro ao cadastrar usuário (Código {res.status_code}).')
                

# ------------------------------------------------
# MÓDULOS CRUD PARA PROFESSORES, DISCIPLINAS
# E TAREFAS
# ------------------------------------------------

# GESTÃO DE PROFESSORES

def modulo_professores():
    st.header('‍Meus Professores')
    # [C]REATE
    with st.expander('➕ Adicionar Professor'):
        nome = st.text_input('Nome do Professor')
        email = st.text_input('E-mail de Contato')
        if st.button('Cadastrar Professor'):
            api_post('professores', {'nome': nome, 'email': email})
            st.rerun()

    # [R]EAD & [U]PDATE & [D]ELETE
    dados = api_get('professores')
    if dados:
        df = pd.DataFrame(dados)
        st.subheader('Seus Professores Cadastrados')
        # Editor de dados para facilitar a vida do aluno
        df_display = df.reindex(columns=['id', 'nome', 'email'])
        df_editado = st.data_editor(df_display, use_container_width=True, hide_index=True, num_rows='dynamic')

        if st.button('Salvar Alterações/Exclusões em Professores'):
            # Para simplificar, atualizamos o que foi alterado
            for _, row in df_editado.iterrows():
                api_patch('professores', row['id'], {'nome': row['nome'], 'email': row['email']})
            st.success('Dados sincronizados!')
            st.rerun()
    else:
        st.info('Nenhum professor cadastrado ainda.')

# GESTÃO DE DISCIPLINAS

def modulo_disciplinas():
    st.header('Minhas Disciplinas')
    profs = api_get('professores')
    
    if not profs:
        st.warning('Cadastre um professor antes de criar disciplinas.')
        return

    # [C]REATE
    with st.expander('➕ Nova Disciplina'):
        nome_d = st.text_input('Nome da Matéria')
        hours = st.text_input('Carga Horária')
        course = st.text_input('Curso')
        credits = st.text_input('Créditos')
        opcoes_p = {p['nome']: p['id'] for p in profs}
        p_escolhido = st.selectbox('Professor Responsável', options=list(opcoes_p.keys()))
        if st.button('Salvar Disciplina'):
            api_post('disciplinas', {
                'nome': nome_d, 
                'prof_id': opcoes_p[p_escolhido],
                'hours': hours, 'course': course, 'credits': credits})
            st.rerun()

    # [R]EAD
    # GET request to fetch subjects connected to the authenticated user_id
    discs = api_get('disciplinas')
    
    if discs:
        st.subheader('Disciplinas Cadastradas')
        df_d = pd.DataFrame(discs)
        df_p = pd.DataFrame(profs)

        # Prepara o DataFrame de professores renomeando colunas para evitar conflitos de nomes no merge
        df_p_sub = df_p.reindex(columns=['id', 'nome']).rename(columns={'id': 'p_id', 'nome': 'nome_prof'})

        # Garante que as colunas necessárias existam em df_d para evitar erro no merge e inclui as novas colunas
        df_d = df_d.reindex(columns=['nome', 'prof_id', 'hours', 'course', 'credits'])

        # Join names to display subjects and their respective teachers
        df_view = df_d.merge(df_p_sub, left_on='prof_id', right_on='p_id', how='left')
        
        # Renomeia o nome original da disciplina e exibe a tabela
        df_view = df_view.rename(columns={'nome': 'nome_disc'})
        cols_to_show = ['nome_disc', 'hours', 'course', 'credits', 'nome_prof']
        st.dataframe(df_view.reindex(columns=cols_to_show), use_container_width=True, hide_index=True)      

        # [D]ELETE
        id_del = st.number_input('ID para remover', min_value=1, step=1)
        if st.button('Remover Disciplina', type='primary'):
            api_delete('disciplinas', id_del)
            st.rerun()

# GESTÃO DE TAREFAS ---

def modulo_tarefas():
    st.header('Minhas Tarefas e Notas')
    discs = api_get('disciplinas')

    if not discs:
        st.warning('Cadastre uma disciplina primeiro.')
        return

    # [C]REATE
    with st.expander('➕ Lançar Atividade/Nota'):
        nome_t = st.text_input('Nome da Atividade')
        opcoes_d = {d['nome']: d['id'] for d in discs}
        d_escolhida = st.selectbox('Selecione a Disciplina', options=list(opcoes_d.keys()))
        nota = st.number_input('Nota Obtida', 0.0, 10.0, 0.0)
        if st.button('Registrar Nota'):
            api_post('tarefas', {'nome': nome_t, 'disc_id': opcoes_d[d_escolhida], 'nota': nota})
            st.rerun()
            
    # [R]EAD
    tarefas = api_get('tarefas')
    if tarefas:
        df_t = pd.DataFrame(tarefas)
        df_d = pd.DataFrame(discs)

        # Prepara o DataFrame de disciplinas para evitar conflitos de nomes no merge
        df_d_sub = df_d.reindex(columns=['id', 'nome']).rename(columns={'id': 'd_id', 'nome': 'nome_disc'})
        
        # Garante que disc_id existe e faz o merge para obter o nome da disciplina
        df_t = df_t.reindex(columns=['id', 'nome', 'nota', 'disc_id'])
        df_merged = df_t.merge(df_d_sub, left_on='disc_id', right_on='d_id', how='left')

        st.subheader('Quadro de Notas')
        # Seleciona colunas e renomeia para melhor legibilidade
        df_display = df_merged.reindex(columns=['id', 'nome', 'nome_disc', 'nota'])
        df_display = df_display.rename(columns={'nome': 'Tarefa', 'nome_disc': 'Disciplina', 'nota': 'Nota'})
        st.dataframe(df_display, use_container_width=True, hide_index=True)

        # [D]ELETE
        id_del_t = st.number_input('ID da Tarefa para remover', min_value=1, step=1)
        if st.button('Remover Tarefa'):
            api_delete('tarefas', id_del_t)
            st.rerun()

# --- DASHBOARD ---

def modulo_dashboard():
    st.header('Resumo de Desempenho')
    tarefas = api_get('tarefas')
    discs = api_get('disciplinas')
    if not tarefas or not discs:
        st.info('Cadastre dados para visualizar seu desempenho gráfico.')
        return

    df_t = pd.DataFrame(tarefas).reindex(columns=['id', 'nome', 'nota', 'disc_id'])
    df_d = pd.DataFrame(discs).reindex(columns=['id', 'nome'])
    df_plot = df_t.merge(df_d, left_on='disc_id', right_on='id', suffixes=('_t', '_d'))
    fig = px.bar(df_plot, x='nome_t', y='nota', color='nome_d', 
                 title='Minhas Notas por Matéria', text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

# ------------------------------------------
# ESTRUTURA PRINCIPAL DE NAVEGAÇÃO
# ------------------------------------------

st.set_page_config(page_title='EduTrack AI', layout='wide')
st.markdown("""
<style> 
.stApp {
    background-color: #2C2C2C;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
input {
    border: 2px solid #2563EB !important;
}
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    tela_acesso()
else:
    with st.sidebar:
        st.title('EduTrack AI')
        menu = st.radio('Gerenciar:', ['Painel Geral', 'Professores 👤', 'Disciplinas 📚', 'Tarefas/Notas 📝'])
        st.markdown('---')
        st.markdown("""
<style>
div.stButton button {
    background-color: #DC2626;
    color: white;
}
</style>
""", unsafe_allow_html=True)
        if st.button('Sair'):
            st.session_state.clear()
            st.rerun()

    match menu:
        case 'Painel Geral': modulo_dashboard()
        case 'Professores 👤': modulo_professores()
        case 'Disciplinas 📚': modulo_disciplinas()
        case 'Tarefas/Notas 📝': modulo_tarefas()
