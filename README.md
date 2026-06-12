# 🎓 EduTrack – Gestão Acadêmica Inteligente

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Xano](https://img.shields.io/badge/Xano-00C7B7?style=for-the-badge&logo=xano&logoColor=white)
![SendGrid](https://img.shields.io/badge/SendGrid-0066CC?style=for-the-badge&logo=sendgrid&logoColor=white)

## 📌 O que é o EduTrack?

O **EduTrack** é um aplicativo web **sucinto, leve e poderoso**, construído sob medida para **gerenciar a vida acadêmica**. Ele nasceu de um projeto acadêmico (idealizado por alunos, para alunos) e evoluiu para uma ferramenta completa que permite organizar disciplinas, professores, tarefas e notas em um só lugar.

Com uma interface limpa e menus intuitivos, o EduTrack ajuda você a:

- ✅ Contabilizar cargas horárias e créditos cursados  
- 📚 Mapear conteúdos e atividades enviadas por professores  
- 📊 Acompanhar seu desempenho por meio de dashboards visuais  
- 🔄 Compartilhar informações com colegas, professores ou responsáveis  

Diferente de plataformas como Google Classroom (focadas em turmas e instituições), o EduTrack tem um **caráter mais individual e flexível**: uma turma inteira pode se cadastrar usando uma única conta gratuita, e cada aluno personaliza seu ambiente como preferir.

---

## 👥 A quem o EduTrack atende?

- **Alunos** de ensino médio, graduação e pós‑graduação – que desejam manter suas responsabilidades em ordem e ter uma visão clara do seu desempenho.
- **Professores** que querem acompanhar o progresso de seus alunos de forma mais ativa e personalizada.
- **Responsáveis** que necessitam de transparência sobre o rendimento e as atividades dos estudantes.

O EduTrack foi pensado para **facilitar a comunicação entre todos os envolvidos no processo de aprendizado**, sem burocracia e de forma acessível.

---

## ⚙️ Funcionalidades do Projeto

### ☁️ Sistema em Nuvem
- Hospedado no **Streamlit Cloud**, acessível de qualquer lugar através do link:  
  👉 **[https://edutrack-team.streamlit.app/](https://edutrack-team.streamlit.app/)**
- Não exige instalação local – basta um navegador moderno.

### 🔐 Login e Cadastro de Usuários
- Criação de conta com **nome, e‑mail e senha**.
- Autenticação segura via API do **Xano**.
- Sessões persistentes com **cookies** (opção "manter login mesmo após fechar a aba").

### 🔁 Recuperação de Senha
- Esqueceu a senha?
- Integração com **SendGrid** e **endpoints públicos do Xano** para envio de e‑mail de redefinição.
- Fluxo seguro com token temporário e polling para atualização da senha.

### 📚 Gestão de Disciplinas
- **Criar** disciplinas com nome e professor responsável.
- **Editar** e **excluir** disciplinas a qualquer momento.
- Visualização rápida de todas as disciplinas cadastradas.

### 👨‍🏫 Gestão de Professores
- Cadastro de professores com **nome** e **e‑mail**.
- Atualização ou remoção de professores.
- Associação automática com as disciplinas.

### ✅ Gestão de Tarefas e Notas
- **Lançar atividades** com nome, disciplina e nota obtida.
- **Editar** ou **excluir** lançamentos.
- Quadro de notas completo para acompanhamento.

### 📊 Dashboard de Desempenho
- Gráfico de barras interativo (Plotly) mostrando as **notas por disciplina**.
- Visão geral clara do progresso acadêmico.

### 🔄 Persistência de Sessão
- Utiliza `streamlit-cookies-manager` para manter o login ativo mesmo após fechar e reabrir o navegador.
- Logout limpa o cookie e redireciona para a tela de login.

---

## 🛠️ Tecnologias Utilizadas

| Camada          | Tecnologia                                 |
|----------------|---------------------------------------------|
| Frontend       | Streamlit (Python)                         |
| Backend/API    | Xano (low‑code, backend‑as‑a‑service)     |
| E‑mail         | SendGrid (templates dinâmicos)             |
| Autenticação   | JWT + Cookies                              |
| Gráficos       | Plotly + Pandas                            |
| Deploy         | Streamlit Cloud                            |

---

## 📋 Pré‑requisitos (para rodar localmente)

- **Python 3.9+**
- **RAM:** 4GB (recomendado 8GB)
- **Sistema operacional:** Windows, macOS ou Linux (32/64 bits)
- **Navegador ideal:** Firefox, Chrome ou Edge atualizados
- **Conta no Xano e SendGrid** (para chaves de API)

> 💡 O aplicativo é leve, pois os dados são armazenados externamente (Xano) e não consomem espaço local.

---

## 🚀 Como Executar Localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/edutrack-team.git
   cd edutrack-team
Crie um ambiente virtual e instale as dependências:

bash
python -m venv venv
source venv/bin/activate   # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
Configure os segredos (crie a pasta .streamlit/ e o arquivo secrets.toml):

toml
SENDGRID_API_KEY = "sua_chave_aqui"
Execute o app:

bash
streamlit run app.py
Acesse http://localhost:8501

⚠️ Lembre‑se de:
🔄 Reiniciar a página sempre que uma atualização for anunciada.

📥 Manter as credenciais de cadastro seguras.

🐞 Contactar a equipe caso encontre um bug.

⏳ Aguardar o sistema reativar quando estiver suspenso (apenas no Cloud).

🔔 Permitir notificações (quando solicitado).

🔗 Verificar se o link de acesso é legítimo (evitar phishing).

📬 Contato & Suporte
Equipe EduTrack – edutrackguerra@gmail.com

Issues – Use o GitHub Issues

📄 Licença
Este projeto é de uso educacional e livre para adaptações, desde que mantidos os créditos aos autores originais.

Desenvolvido com 💙 por alunos, para alunos.
EduTrack – organize, aprenda, evolua.
