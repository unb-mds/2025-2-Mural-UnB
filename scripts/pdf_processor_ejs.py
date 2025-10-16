import requests
import json
import pdfplumber
import google.generativeai as genai
import os
import time
from typing import Dict, List
import re

class PDFProcessorEJs:
    def __init__(self, gemini_api_key: str):
        self.gemini_api_key = gemini_api_key
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    def baixar_pdf_direto(self, url: str, caminho_saida: str) -> str:
        """Baixa PDF diretamente de uma URL"""
        try:
            print(f"Baixando PDF de {url}...")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()
            
            os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
            
            with open(caminho_saida, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✓ PDF baixado com sucesso: {caminho_saida}")
            return caminho_saida
            
        except Exception as e:
            print(f"✗ Erro ao baixar PDF: {e}")
            raise
    
    def extrair_texto_por_pagina(self, pdf_path: str, pagina_inicial: int = 1) -> List[Dict]:
        """Extrai texto do PDF página por página"""
        paginas_texto = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                print(f"PDF possui {len(pdf.pages)} páginas")
                
                for numero_pagina, pagina in enumerate(pdf.pages, 1):
                    if numero_pagina < pagina_inicial:
                        continue
                        
                    print(f"Extraindo texto da página {numero_pagina}...")
                    texto = pagina.extract_text()
                    
                    if texto and texto.strip():
                        # Limpa caracteres problemáticos
                        texto = self.limpar_texto(texto)
                        texto = self.juntar_palavras_hifenizadas(texto)
                        
                        paginas_texto.append({
                            "numero_pagina": numero_pagina,
                            "texto": texto.strip(),
                            "contagem_caracteres": len(texto)
                        })
                        print(f"  Página {numero_pagina}: {len(texto)} caracteres")
                    else:
                        print(f"  Página {numero_pagina}: vazia ou sem texto extraível")
            
            print(f"✓ Extraídas {len(paginas_texto)} páginas com conteúdo")
            return paginas_texto
            
        except Exception as e:
            print(f"✗ Erro ao extrair texto do PDF: {e}")
            return []
    
    def limpar_texto(self, texto: str) -> str:
        """Remove caracteres especiais problemáticos"""
        if not texto:
            return texto
        
        substituicoes = {
            '\u202f': ' ',   # Narrow no-break space
            '\xa0': ' ',     # Non-breaking space  
            '\u2013': '-',   # En dash
            '\u2014': '-',   # Em dash
            '\u2019': "'",   # Right single quotation mark
            '\u201c': '"',   # Left double quotation mark  
            '\u201d': '"',   # Right double quotation mark
        }
        
        for char_original, char_substituto in substituicoes.items():
            texto = texto.replace(char_original, char_substituto)
            
        return texto
    
    def juntar_palavras_hifenizadas(self, texto: str) -> str:
        """Remove hifenização de quebra de linha"""
        if not texto:
            return texto
        
        # Padrão: letra + hífen + espaço(s) + letra minúscula
        texto = re.sub(r'(\w)-\s+(\w)', r'\1\2', texto)
        return texto
    
    def criar_prompt_gemini(self, texto: str, info_pagina: str = "") -> str:
        """Criando prompt mais específico"""
        prompt = f"""
        ANALISE O TEXTO E EXTRAIA INFORMAÇÕES SOBRE EMPRESAS JUNIORES.

        TEXTO PARA ANÁLISE:
        {texto}

        INSTRUÇÕES:
        1. Identifique CADA empresa júnior mencionada no texto
        2. Para cada empresa, extraia as informações nos campos abaixo
        3. Se uma informação não for encontrada, use "N/A"
        4. Retorne APENAS um array JSON válido

        FORMATO DE SAÍDA EXATO:
        [
            {{
                "Nome": "nome completo da empresa",
                "Cursos": "cursos associados",
                "Sobre": "descrição e história", 
                "Missao": "missão",
                "Visao": "visão",
                "Valores": "valores e princípios",
                "Servicos": "serviços oferecidos",
                "Site": "site",
                "Instagram": "instagram"
            }}
        ]

        EXEMPLO:
        [
            {{
                "Nome": "Ábaco Consultoria",
                "Cursos": "Ciências Contábeis",
                "Sobre": "Fundada em 2018 por estudantes...",
                "Missao": "Transformar vidas por meio da contabilidade",
                "Visao": "Ser referência em consultoria contábil",
                "Valores": "Comprometimento, Companheirismo, Protagonismo",
                "Servicos": "Abertura de CNPJ, Consultoria financeira",
                "Site": "abacoconsultoria.com.br",
                "Instagram": "@abacoconsultoriajr"
            }}
        ]

        IMPORTANTE: 
        - Retorne SEMPRE um array, mesmo que tenha apenas uma empresa
        - Use double quotes para strings
        - Não inclua textos explicativos
        - Não use markdown ou code blocks
        """
        
        return prompt
    
    def extrair_informacoes_gemini(self, texto: str, info_pagina: str = "") -> List[Dict]:
        """Usa Gemini API com tratamento robusto de erros JSON"""
        
        prompt = self.criar_prompt_gemini(texto, info_pagina)
        
        try:
            print("Enviando requisição para Gemini API...")
            resposta = self.model.generate_content(prompt)
            texto_resposta = resposta.text.strip()
            
            print("Resposta bruta do Gemini recebida")
            print(f"Tamanho da resposta: {len(texto_resposta)} caracteres")
            
            # Limpa e processa a resposta
            texto_json = self.limpar_e_corrigir_json(texto_resposta)
            
            print("Processando JSON...")
            dados = json.loads(texto_json)
            
            # Garante que sempre retorne uma lista
            if isinstance(dados, dict):
                dados = [dados]
            
            # Log das empresas encontradas
            if dados:
                print(f"✓ Empresas identificadas neste lote:")
                for i, empresa in enumerate(dados, 1):
                    nome = empresa.get('Nome', 'Sem nome')
                    print(f"  {i}. {nome}")
            else:
                print("  Nenhuma empresa identificada neste lote")
            
            return dados
            
        except json.JSONDecodeError as e:
            print(f"✗ Erro ao decodificar JSON: {e}")
            print("Tentando corrigir JSON...")
            
            # Tenta corrigir o JSON
            try:
                texto_corrigido = self.corrigir_json(texto_resposta)
                dados = json.loads(texto_corrigido)
                print("✓ JSON corrigido com sucesso!")
                return dados if isinstance(dados, list) else [dados]
            except:
                print("✗ Não foi possível corrigir o JSON")
                print(f"Resposta problemática: {texto_resposta[:500]}...")
                return []
                
        except Exception as e:
            print(f"✗ Erro ao processar com Gemini: {e}")
            return []
    
    def limpar_e_corrigir_json(self, texto: str) -> str:
        """Limpa e corrige o JSON retornado pelo Gemini"""
        # Remove markdown code blocks
        texto = re.sub(r'```json\s*', '', texto)
        texto = re.sub(r'```\s*', '', texto)
        
        # Remove textos antes do primeiro [ ou {
        texto = re.sub(r'^[^{[]*', '', texto)
        
        # Remove textos depois do último ] ou }
        texto = re.sub(r'[^}\]]*$', '', texto)
        
        # Corrige vírgulas finais em arrays e objetos
        texto = re.sub(r',\s*]', ']', texto)
        texto = re.sub(r',\s*}', '}', texto)
        
        # Garante que é um array
        if not texto.strip().startswith('['):
            texto = '[' + texto + ']'
        
        return texto.strip()
    
    def corrigir_json(self, texto: str) -> str:
        """Tenta corrigir JSON malformado mais agressivamente"""
        print("Aplicando correções agressivas no JSON...")
        
        # Remove tudo que não é JSON
        linhas = texto.split('\n')
        linhas_json = []
        
        for linha in linhas:
            linha = linha.strip()
            if linha.startswith(('{', '[', '"', '}', ']')) or ':' in linha:
                linhas_json.append(linha)
        
        texto = ' '.join(linhas_json)
        
        # Corrige aspas simples para double quotes
        texto = re.sub(r"'([^']*)'", r'"\1"', texto)
        
        # Corrige vírgulas faltantes
        texto = re.sub(r'"\s*"', '", "', texto)  # Entre strings
        texto = re.sub(r'"\s*{', '", {', texto)  # Antes de objeto
        texto = re.sub(r'}\s*"', '}, "', texto)  # Depois de objeto
        
        # Garante que é um array
        if not texto.startswith('['):
            texto = '[' + texto + ']'
        
        return texto
    
    def processar_pdf_paginado(self, pdf_path: str, saida_json: str, max_paginas_por_requisicao: int = 2, pagina_inicial: int = 1):
        """Processa PDF página por página"""
        
        print("=== INICIANDO PROCESSAMENTO PAGINADO ===")
        
        # Extrair texto por página
        dados_paginas = self.extrair_texto_por_pagina(pdf_path, pagina_inicial)
        
        if not dados_paginas:
            print("✗ Nenhum texto extraído do PDF")
            return []
        
        todas_empresas = []
        paginas_processadas = 0
        
        # Processar em lotes menores para melhor qualidade
        for i in range(0, len(dados_paginas), max_paginas_por_requisicao):
            lote = dados_paginas[i:i + max_paginas_por_requisicao]
            texto_lote = ""
            
            for pagina in lote:
                texto_lote += f"\n\n--- PÁGINA {pagina['numero_pagina']} ---\n{pagina['texto']}\n"
            
            print(f"\n📖 Processando lote {i//max_paginas_por_requisicao + 1}")
            print(f"   Páginas: {i+1} a {i+len(lote)}")
            print(f"   Tamanho do texto: {len(texto_lote)} caracteres")
            
            empresas_lote = self.extrair_informacoes_gemini(
                texto_lote, 
                f"(páginas {i+1} a {i+len(lote)})"
            )
            
            # Verificar e evitar duplicatas
            empresas_novas = 0
            for empresa in empresas_lote:
                if not self.empresa_duplicada(empresa, todas_empresas):
                    todas_empresas.append(empresa)
                    empresas_novas += 1
            
            paginas_processadas += len(lote)
            print(f"   ✅ Empresas novas neste lote: {empresas_novas}")
            print(f"   📊 Total acumulado: {len(todas_empresas)} empresas")
            
            # Pausa para evitar rate limiting do LLM
            if i + max_paginas_por_requisicao < len(dados_paginas):
                print("   ⏳ Aguardando 3 segundos...")
                time.sleep(3)
        
        # Salvar resultados
        self.salvar_json(todas_empresas, saida_json)
        
        print(f"\n=== PROCESSAMENTO CONCLUÍDO ===")
        print(f"📄 Páginas processadas: {paginas_processadas}")
        print(f"🏢 Empresas juniores extraídas: {len(todas_empresas)}")
        print(f"💾 Arquivo salvo: {saida_json}")
        
        # Lista final de empresas
        if todas_empresas:
            print(f"\n📋 LISTA DE EMPRESAS IDENTIFICADAS:")
            for i, empresa in enumerate(todas_empresas, 1):
                nome = empresa.get('Nome', 'Sem nome')
                cursos = empresa.get('Cursos', 'N/A')
                print(f"  {i:2d}. {nome} | {cursos}")
        
        return todas_empresas
    
    def empresa_duplicada(self, nova_empresa: Dict, empresas_existentes: List[Dict]) -> bool:
        """Verifica se a empresa já existe na lista"""
        nome_nova = nova_empresa.get('Nome', '').strip().lower()
        if not nome_nova:
            return False
            
        for existente in empresas_existentes:
            nome_existente = existente.get('Nome', '').strip().lower()
            if nome_existente and nome_nova == nome_existente:
                return True
                
        return False
    
    def salvar_json(self, dados: List[Dict], nome_arquivo: str):
        """Salva os dados em arquivo JSON"""
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            print(f"✓ Dados salvos em {nome_arquivo}")
            
            # Estatísticas do arquivo salvo
            if dados:
                total_campos = sum(len(empresa) for empresa in dados)
                print(f"📊 Estatísticas: {len(dados)} empresas, {total_campos} campos totais")
                
        except Exception as e:

            print(f"✗ Erro ao salvar JSON: {e}")
