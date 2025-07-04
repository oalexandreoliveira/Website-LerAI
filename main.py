from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import fitz  # PyMuPDF para lidar com PDFs
import os

app = Flask(__name__)
CORS(app)  # Permite requisições de qualquer origem

# Exemplo de dados para treinar o modelo
train_data = [
    "Gostaria de saber o status do meu pedido",  # Produtivo
    "Qual o prazo de entrega do produto?",  # Produtivo
    "Me envie um orçamento para o serviço",  # Produtivo
    "Parabéns pelo seu aniversário!",  # Improdutivo
    "Feliz Natal e um próspero Ano Novo!",  # Improdutivo
    "Agradeço pelo apoio e carinho",  # Improdutivo
]

# Rótulos para os dados de treinamento (1 = Produtivo, 0 = Improdutivo)
train_labels = [1, 1, 1, 0, 0, 0]

# Criando um pipeline para classificação
model = make_pipeline(TfidfVectorizer(), LogisticRegression())
model.fit(train_data, train_labels)

# Função para ler o texto de um PDF
def extract_text_from_pdf(pdf_file):
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")  # Usar o stream do arquivo enviado
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Erro ao extrair texto do PDF: {str(e)}"

# Função para ler o texto de um arquivo .txt
def extract_text_from_txt(txt_file):
    try:
        return txt_file.read().decode('utf-8')  # Lê o conteúdo do arquivo de texto
    except Exception as e:
        return f"Erro ao extrair texto do TXT: {str(e)}"

# Função simples para classificar o e-mail
def classify_email(text):
    try:
        prediction = model.predict([text])  # Previsão do modelo
        if prediction == 1:
            return "Produtivo", "Estamos analisando o seu caso, por favor, aguarde enquanto nossa equipe verifica a situação."
        else:
            return "Improdutivo", "Agradecemos seu contato! Se precisar de algo mais, estamos à disposição."
    except Exception as e:
        return "Erro", f"Erro ao classificar o e-mail: {str(e)}"

@app.route('/process-email', methods=['POST'])
def process_email():
    try:
        email_text = None
        
        # Verifica se o arquivo foi enviado (PDF ou TXT)
        if 'email-file' in request.files:
            email_file = request.files['email-file']
            file_extension = email_file.filename.split('.')[-1].lower()

            if file_extension == 'pdf':
                email_text = extract_text_from_pdf(email_file)  # Extrai o texto do PDF
            elif file_extension == 'txt':
                email_text = extract_text_from_txt(email_file)  # Extrai o texto do arquivo TXT
            else:
                return jsonify({"error": "Formato de arquivo não suportado!"}), 400
        # Verifica se o texto foi enviado diretamente no formulário
        elif 'email-text' in request.form:
            email_text = request.form['email-text'].strip()  # Obtém o texto enviado via FormData
            if not email_text:
                return jsonify({"error": "Texto vazio, forneça o conteúdo do e-mail!"}), 400

        if not email_text:
            return jsonify({"error": "E-mail não fornecido ou mal formatado!"}), 400  # Certifica-se de que o texto não esteja vazio

        # Classifica o e-mail e gera a resposta
        category, suggested_response = classify_email(email_text)

        return jsonify({
            "category": category,
            "suggested_response": suggested_response
        })
    
    except Exception as e:
        return jsonify({"error": f"Erro no processamento: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
