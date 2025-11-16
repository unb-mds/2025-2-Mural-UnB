"""
Gera embeddings das tags usando a API Gemini e salva em JSON.
Lê `tags.json`, solicita embeddings e grava `tags_with_embeddings_gemini.json`.
"""

import json
import google.generativeai as genai
import os
from dotenv import load_dotenv

# --- Configuração ---
# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Chave Privada da API do Google Gemini (usando .env)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("ERRO: GOOGLE_API_KEY não foi encontrada. Verifique seu arquivo .env")
    # Em um script real, você poderia 'exit(1)' aqui
else:
    genai.configure(api_key=GOOGLE_API_KEY)

# Define os caminhos dos arquivos
INPUT_JSON_FILE = "data/mock/tags_no_embeddings.json" # Corrigindo o caminho
OUTPUT_JSON_FILE = "data/mock/tags_with_embeddings_gemini.json" # Corrigindo o caminho


def get_embedding(text, model="models/text-embedding-004"):
    """Gera o embedding para um dado texto."""
    try:
        embedding = genai.embed_content(model=model, content=text)
        return embedding["embedding"]
    except Exception as e:  # pylint: disable=broad-exception-caught
        print(f"Erro ao gerar embedding para o texto: '{text[:30]}...'")
        print(f"Erro: {e}")
        return None


def process_tags(data):
    """Itera sobre as tags, gera e adiciona os embeddings."""
    for categoria in data.get("categorias", []):
        subcategorias = categoria.get("subcategorias", [])
        
        tags_para_processar = []
        if not subcategorias:
            # Caso 1: Tags direto na categoria (ex: Soft Skills)
            tags_para_processar = categoria.get("tags", [])
        else:
            # Caso 2: Tags dentro de subcategorias
            for subcategoria in subcategorias:
                tags_para_processar.extend(subcategoria.get("tags", []))
        
        # Processa as tags encontradas
        for tag in tags_para_processar:
            # Pula se já tiver um embedding (ou se não for um dicionário válido)
            if not isinstance(tag, dict) or tag.get("embedding"):
                continue
                
            input_text = f"{tag.get('label', '')}: {tag.get('description', '')}"
            print(f"Processando tag: {tag.get('label')}")

            embedding_vector = get_embedding(input_text)

            if embedding_vector:
                tag["embedding"] = embedding_vector
                
    return data

#
# --- LÓGICA PRINCIPAL MOVIDA PARA UMA FUNÇÃO ---
#
def main():
    """
    Função principal que orquestra a leitura, processamento e escrita.
    """
    print("Carregando o arquivo JSON de tags...")
    
    # Garante que a pasta de dados exista
    os.makedirs(os.path.dirname(INPUT_JSON_FILE), exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUT_JSON_FILE), exist_ok=True)

    try:
        with open(INPUT_JSON_FILE, "r", encoding="utf-8") as f:
            tags_data = json.load(f)
    except FileNotFoundError:
        print(f"ERRO: Arquivo de entrada não encontrado: {INPUT_JSON_FILE}")
        return
    except json.JSONDecodeError:
        print(f"ERRO: Arquivo de entrada não é um JSON válido: {INPUT_JSON_FILE}")
        return

    print("Iniciando a geração de embeddings com o modelo Gemini...")
    tags_with_embeddings = process_tags(tags_data)

    print(f"\nSalvando os dados com embeddings em '{OUTPUT_JSON_FILE}'...")
    try:
        with open(OUTPUT_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(tags_with_embeddings, f, indent=2, ensure_ascii=False)
    except IOError as e:
        print(f"ERRO: Não foi possível escrever no arquivo de saída: {e}")
        return

    print("Processo concluído com sucesso")

#
# --- Bloco de Execução ---
# (Só roda 'main()' quando o script é executado diretamente)
#
if __name__ == "__main__":
    main()