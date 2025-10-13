import json
import google.generativeai as genai
import numpy as np
import os
from dotenv import load_dotenv

# --- Opcao usando dotenv
# Caregando variáveis de ambiente do arquivo .env
load_dotenv()

# Chave Privada da API do Google Gemini (usando .env)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')  # Substitua pela sua chave real ou use variáveis de ambiente

# --- Opcao sem usar dotenv
# Chave Privada da API do Google Gemini (hardcoded - não recomendado para produção)
GOOGLE_API_KEY = 'Sua_Chave_Aqui'  # Substitua pela sua chave real (solicitar para o TIAGO caso nn tenha)


genai.configure(api_key=GOOGLE_API_KEY)

INPUT_JSON_FILE = 'tags.json'
OUTPUT_JSON_FILE = 'tags_with_embeddings_gemini.json'


def get_embedding(text, model='models/text-embedding-004'):
  """Gera o embedding para um dado texto usando a API do Gemini."""
  try:
    embedding = genai.embed_content(model=model, content=text)
    return embedding['embedding']
  except Exception as e:
    print(f"Erro ao gerar embedding para o texto: '{text[:30]}...'")
    print(f"Erro: {e}")
    return None

def process_tags(data):
  """Itera sobre as tags, gera e adiciona os embeddings."""
  for categoria in data['categorias']:
    # Algumas categorias podem não ter subcategorias
    subcategorias = categoria.get('subcategorias', [])
    if not subcategorias:
        # Trata o caso de categorias sem subcategorias (como Soft Skills)
        for tag in categoria.get('tags', []):
          
          input_text = f"{tag['label']}: {tag.get('description', '')}"
          print(f"Processando tag: {tag['label']}")
          
          embedding_vector = get_embedding(input_text)
          
          if embedding_vector:
            tag['embedding'] = embedding_vector
    else:
        for subcategoria in subcategorias:
            for tag in subcategoria['tags']:

                input_text = f"{tag['label']}: {tag.get('description', '')}"
                print(f"Processando tag: {tag['label']}")
                
                embedding_vector = get_embedding(input_text)
                
                if embedding_vector:
                    tag['embedding'] = embedding_vector
  return data

if __name__ == "__main__":
  print("Carregando o arquivo JSON de tags...")
  with open(INPUT_JSON_FILE, 'r', encoding='utf-8') as f:
    tags_data = json.load(f)

  print("Iniciando a geração de embeddings com o modelo Gemini...")
  tags_with_embeddings = process_tags(tags_data)

  print(f"\nSalvando os dados com embeddings em '{OUTPUT_JSON_FILE}'...")
  with open(OUTPUT_JSON_FILE, 'w', encoding='utf-8') as f:
    json.dump(tags_with_embeddings, f, indent=2, ensure_ascii=False)
  
  print("Processo concluído com sucesso")