import os

# Configurações da API Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'sua_chave_aqui')

# URL do PDF das Empresas Juniores
PDF_URL_EJS = "https://unb.br/images/Noticias/2023/Documentos/PORTFLIO_EJS.pdf"

# Configurações de saída
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "EJs")
OUTPUT_JSON = "empresas_juniores_consolidadas.json"
IMAGES_DIR = "images" 

# Configurações do processamento
PROCESSAR_POR_PAGINA = True
MAX_PAGINAS_POR_REQUISICAO = 2
# pagina onde o processo começa, a página 10 é o sumário ent desse modo são evitados erros
PAGINA_INICIAL_EJS = 11  

# Configurações extrair imagens
EXTRAIR_IMAGENS = True
