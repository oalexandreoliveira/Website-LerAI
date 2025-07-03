from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import fitz  # PyMuPDF para lidar com PDFs
import os
from collections import Counter
import re

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
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")  # Usar o stream do arquivo enviado
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Função para ler o texto de um arquivo .txt
def extract_text_from_txt(txt_file):
    return txt_file.read().decode('utf-8')  # Lê o conteúdo do arquivo de texto

# Função simples para classificar o e-mail
def classify_email(text):
    prediction = model.predict([text])  # Previsão do modelo
    if prediction == 1:
        return "Produtivo", "Estamos analisando o seu caso, por favor, aguarde enquanto nossa equipe verifica a situação."
    else:
        return "Improdutivo", "Agradecemos seu contato! Se precisar de algo mais, estamos à disposição."

# Função para extrair o resumo do texto
def summarize_text(text):
    # Remove pontuação e converte para minúsculas
    text = re.sub(r'[^\w\s]', '', text.lower())
    words = text.split()
    
    # Conta a frequência de palavras
    word_freq = Counter(words)
    
    # Ordena as palavras por frequência
    most_common = word_freq.most_common(10)
    common_words = [word for word, _ in most_common]
    
    # Seleciona as frases que contêm as palavras mais comuns
    sentences = text.split('.')
    summary = []
    for sentence in sentences:
        for word in common_words:
            if word in sentence:
                summary.append(sentence.strip())
                break
    return ' '.join(summary[:3])  # Limita a 3 frases

@app.route('/process-email', methods=['POST'])
def process_email():
    # Verifica se o arquivo foi enviado
    if 'email-file' in request.files:
        email_file = request.files['email-file']
        file_extension = email_file.filename.split('.')[-1].lower()

        if file_extension == 'pdf':
            email_text = extract_text_from_pdf(email_file)  # Extrai o texto do PDF
        elif file_extension == 'txt':
            email_text = extract_text_from_txt(email_file)  # Extrai o texto do arquivo TXT
        else:
            return jsonify({"error": "Formato de arquivo não suportado!"}), 400
    else:
        email_text = request.form.get('email-text', '')  # Obtém o texto enviado via FormData

    if not email_text:
        return jsonify({"error": "E-mail não fornecido!"}), 400  # Certifica-se de que o texto não esteja vazio

    # Classifica o e-mail e gera a resposta
    category, suggested_response = classify_email(email_text)
    
    # Extrai o resumo do texto
    summary = summarize_text(email_text)

    return jsonify({
        "category": category,
        "suggested_response": suggested_response,
        "summary": summary  # Inclui o resumo do e-mail
    })

if __name__ == '__main__':
    app.run(debug=True)