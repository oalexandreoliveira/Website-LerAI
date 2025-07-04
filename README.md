Ler AI - Classificação Automática de E-mails

Ler AI é uma aplicação web que utiliza aprendizado de máquina para classificar e-mails automaticamente em duas categorias: Produtivo e Improdutivo. 

A aplicação também gera respostas automáticas para facilitar o atendimento. Ela permite a análise de e-mails a partir de arquivos .txt ou .pdf, ou até mesmo texto colado diretamente na interface.

Este projeto foi desenvolvido com o intuito de automatizar o processo de triagem de e-mails, facilitando a comunicação e otimizando o tempo das equipes de atendimento.

Funcionalidades
Classificação de E-mails: A aplicação pode classificar e-mails como Produtivo (requere ação) ou Improdutivo (não requer ação).

Respostas Automáticas: A aplicação gera respostas sugeridas com base na classificação do e-mail.

Suporte a Arquivos: Aceita arquivos de e-mail no formato .txt e .pdf para processamento.

Interface Simples: A interface é amigável e permite ao usuário escolher um arquivo ou inserir o texto diretamente.

Tecnologias Utilizadas
Flask: Framework web utilizado para criar a API do backend.

scikit-learn: Biblioteca de aprendizado de máquina utilizada para construir o modelo de classificação.

PyMuPDF (fitz): Biblioteca usada para extrair texto de arquivos PDF.

HTML/CSS: Para a estruturação e estilização da interface web.

JavaScript (Fetch API): Para a comunicação assíncrona entre o frontend e o backend.

Como Rodar Localmente
Pré-requisitos
Python 3.9 ou superior instalado.

Bibliotecas necessárias:

Flask

Flask-CORS

scikit-learn

PyMuPDF

gunicorn (para deploy em produção)

outros pacotes listados no requirements.txt.

Passos
1) Clone o repositório:

bash
Copy
Edit
git clone https://github.com/seu-usuario/ler-ai.git
cd ler-ai

2) Crie um ambiente virtual:

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # Para Linux/Mac
venv\Scripts\activate  # Para Windows

3) Instale as dependências:

bash
Copy
Edit
pip install -r requirements.txt

4) Rode a aplicação localmente:

bash
Copy
Edit
flask run
Isso iniciará o servidor no http://127.0.0.1:5000. Você pode acessar a interface web através do seu navegador.

Para Rodar em Produção
Para rodar em produção, você pode usar o Gunicorn, que é um servidor WSGI para aplicações Python. Use o seguinte comando:

bash
Copy
Edit
gunicorn main:app
Isso fará o deploy da aplicação para o ambiente de produção.

Estrutura do Projeto
O projeto está organizado da seguinte forma:

ler-ai/
│
├── app.py              # Arquivo principal da aplicação Flask
├── requirements.txt    # Lista de dependências
├── templates/          # Arquivos HTML
│   └── index.html      # Página principal do site
├── static/             # Arquivos estáticos (CSS, JS, Imagens)
│   └── styles.css      # Estilo da página
│   └── logo.png        # Logo da aplicação
└── README.md           # Este arquivo
Como Contribuir
Fork o repositório.

Crie uma branch para sua funcionalidade (git checkout -b feature/nome-da-funcionalidade).

Faça suas modificações.

Realize os testes necessários.

Submeta um pull request explicando as alterações feitas.

Endpoints da API
POST /process-email
Esse endpoint é responsável por receber o e-mail (seja em formato de arquivo ou texto) e retornar a classificação e resposta sugerida.

Parâmetros:

email-file: Arquivo de e-mail (PDF ou TXT).

email-text: Texto do e-mail.

Resposta:

json
Copy
Edit
{
  "category": "Produtivo",
  "suggested_response": "Estamos analisando o seu caso, por favor, aguarde enquanto nossa equipe verifica a situação."
}
Erros Comuns
Formato de arquivo não suportado: O arquivo enviado não é um PDF ou TXT.

Texto vazio: O campo de texto do e-mail foi deixado vazio.

Erro no processamento: Qualquer erro inesperado ocorrido no backend.

Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
