import itertools
import json
from PyPDF2 import PdfReader
import nltk

# Certifique-se de baixar o tokenizer do NLTK (execute apenas uma vez)
nltk.download('punkt')

# Função para extrair texto do PDF
def extrair_texto_pdf(caminho_pdf):
    """
    Lê um arquivo PDF e retorna o texto concatenado de todas as páginas.
    """
    try:
        reader = PdfReader(caminho_pdf)
        texto = "".join(page.extract_text() for page in reader.pages if page.extract_text())
        return texto
    except Exception as e:
        raise ValueError(f"Erro ao ler o PDF: {e}")

# Função para dividir o texto em frases
def dividir_em_frases(texto):
    """
    Divide o texto em frases usando o NLTK.
    """
    return nltk.sent_tokenize(texto)

# Função para gerar pares de termos
def gerar_pares_termos(vetor_termos):
    """
    Gera todos os pares possíveis (combinações de 2) a partir de um vetor de termos.
    """
    return list(itertools.combinations(vetor_termos, 2))

# Função para buscar relações semânticas
def buscar_relacoes(frases, pares_termos, limite_relacoes=None):
    """
    Busca pares de termos nas frases fornecidas.
    """
    relacoes_identificadas = []
    for frase in frases:
        for termo1, termo2 in pares_termos:
            if termo1 in frase and termo2 in frase:
                relacao = {"frase": frase, "termo1": termo1, "termo2": termo2}
                relacoes_identificadas.append(relacao)
                if limite_relacoes and len(relacoes_identificadas) >= limite_relacoes:
                    return relacoes_identificadas  # Limite atingido
    return relacoes_identificadas

# Função para salvar as relações em um arquivo JSON
"""
def salvar_relacoes_em_json(relacoes, caminho_arquivo):
    
    #Salva as relações identificadas em um arquivo JSON.
    
    try:
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(relacoes, arquivo, indent=4, ensure_ascii=False)
        print(f"Relações salvas com sucesso em {caminho_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar relações: {e}")
"""

# Função principal
def executar_busca(caminho_pdf, vetor_termos, caminho_saida="relacoes_identificadas.json", limite_relacoes=None):
    """
    Executa o fluxo completo: extrai texto do PDF, divide em frases, busca relações e salva em JSON.
    """
    print(">>> Iniciando análise do PDF...")
    texto = extrair_texto_pdf(caminho_pdf)
    print(">>> Texto extraído do PDF com sucesso!")

    frases = dividir_em_frases(texto)
    print(f">>> Texto dividido em {len(frases)} frases.")

    pares_termos = gerar_pares_termos(vetor_termos)
    print(f">>> Gerados {len(pares_termos)} pares de termos.")

    print(">>> Buscando relações semânticas...")
    relacoes = buscar_relacoes(frases, pares_termos, limite_relacoes=limite_relacoes)
    print(f">>> Encontradas {len(relacoes)} relações.")

    salvar_relacoes_em_json(relacoes, caminho_saida)
    print(">>> Processo concluído com sucesso!")

# Exemplo de uso
"""
if __name__ == "__main__":
    # Caminho do PDF
    caminho_pdf = "exemplo.pdf"  # Substitua pelo seu arquivo PDF

    # Vetor de termos
    vetor_termos = ["termo1", "termo2", "termo3", "termo4"]

    # Caminho do arquivo JSON de saída
    caminho_saida = "relacoes_identificadas.json"

    # Executar o fluxo
    executar_busca(caminho_pdf, vetor_termos, caminho_saida, limite_relacoes=10)
"""
