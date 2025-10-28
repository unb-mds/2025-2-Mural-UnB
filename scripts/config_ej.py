import os
import google.generativeai as genai

# Configurações da API Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'sua_chave_aqui') # <- mudar valor sua_chave_aqui nessa instância

if GEMINI_API_KEY and GEMINI_API_KEY != 'sua_chave_aqui':
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("⚠️  AVISO: GEMINI_API_KEY não configurada ou está com valor padrão")
    print("   A API do Gemini não será configurada até que você:")
    print("   - Configure a variável de ambiente GEMINI_API_KEY")
    print("   - OU atualize 'sua_chave_aqui' no arquivo config_ej.py")

# URL do PDF das Empresas Juniores
PDF_URL_EJS = "https://unb.br/images/Noticias/2023/Documentos/PORTFLIO_EJS.pdf"

# Configurações de saída
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "EJs")
OUTPUT_JSON = "empresas_juniores_consolidadas.json"
IMAGES_DIR = "images" 

# Configurações do processamento
PROCESSAR_POR_PAGINA = True
MAX_PAGINAS_POR_REQUISICAO = 10
# pagina onde o processo começa, a página 10 é o sumário ent desse modo são evitados erros
PAGINA_INICIAL_EJS = 11  

# Configurações extrair imagens
EXTRAIR_IMAGENS = True
