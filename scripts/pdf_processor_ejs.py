"""
Classe e funções para extrair texto e imagens de PDFs e chamar Gemini para extrair campos.
Contém lógica de limpeza, prompts e processamento paginado/unificado para EJs.
"""
import json
import pdfplumber
import google.generativeai as genai
import os
import time
from typing import Dict, List
import re
import fitz
import requests
from config_ej import PAGINA_INICIAL_EJS

class PDFProcessorEJs:
    def __init__(self, gemini_api_key: str):
        self.gemini_api_key = gemini_api_key
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')

    def extrair_imagens_pdf(self, pdf_path: str, output_dir: str, empresas_com_id: List[Dict] = None) -> List[str]:  # pylint: disable=unused-argument
        """Extração de todas as imagens do PDF com novo sistema de nomenclatura"""
        print("\n📸 Extraindo imagens do PDF...")

        imagens_extraidas = []

        try:

            from config_ej import IMAGES_OUTPUT_DIR
            images_dir = IMAGES_OUTPUT_DIR

            # Criar diretório de imagens se não existir
            os.makedirs(images_dir, exist_ok=True)
            print(f"📁 Diretório de imagens: {images_dir}")

            # Abrir pdf com PyMuPDF
            pdf_document = fitz.open(pdf_path)
            
            # Criando mapeamento de página para ID da EJ
            pagina_para_id = {}
            if empresas_com_id:
                # Assumindo que cada EJ está em uma página específica
                for i, empresa in enumerate(empresas_com_id):
                    
                    pagina_ej = PAGINA_INICIAL_EJS + i
                    pagina_para_id[pagina_ej] = empresa.get('id')
                    print(f"  Mapeamento: Página {pagina_ej} → EJ {empresa.get('id')} - {empresa.get('Nome', 'Sem nome')}")
            
            total_images = 0
            
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                pagina_atual = page_num + 1
                
                # Pegar lista de imagens
                image_list = page.get_images()
                
                if image_list:
                    print(f"  Página {pagina_atual}: {len(image_list)} imagem(ns) encontrada(s)")
                    
                    # Verificar se esta página tem uma EJ associada
                    id_ej_pagina = pagina_para_id.get(pagina_atual)

                    # PULAR IMAGENS DE PÁGINAS SEM EJ (null)
                    if not id_ej_pagina:
                        print(f"    ⏭️  Pulando {len(image_list)} imagem(ns) da página {pagina_atual} (sem EJ associada)")
                        continue
                    
                    for img_index, img in enumerate(image_list):
                        # Pegar o XREF da imagem
                        xref = img[0]
                        
                        # extrair a imagem
                        base_image = pdf_document.extract_image(xref)
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]
                        
                        # SISTEMA DE NOMENCLATURA
                        if img_index == 0:
                            # Primeira imagem da página da EJ
                            image_filename = f"{id_ej_pagina}.{image_ext}"
                        else:
                            # Imagens subsequentes na mesma página da EJ
                            image_filename = f"{id_ej_pagina}-{img_index + 1}.{image_ext}"
                    
                        image_path = os.path.join(images_dir, image_filename)
                        
                        # Save the image
                        with open(image_path, "wb") as image_file:
                            image_file.write(image_bytes)
                        
                        imagens_extraidas.append({
                            "caminho": image_path,
                            "pagina": pagina_atual,
                            "numero": img_index + 1,
                            "formato": image_ext,
                            "tamanho": len(image_bytes),
                            "id_ej_associado": id_ej_pagina,
                            "nome_arquivo": image_filename
                        })
                        
                        total_images += 1
                        tipo_nome = "EJ" if id_ej_pagina else "página"
                        print(f"    💾 Salvo ({tipo_nome}): {image_filename}")
                else:
                    print(f"  Página {pagina_atual}: Nenhuma imagem encontrada")
            
            pdf_document.close()
            
            # Estatísticas do novo sistema
            imagens_com_ej = [img for img in imagens_extraidas if img['id_ej_associado']]
            
            print(f"\n✓ Extração de imagens concluída: {total_images} imagens salvas em '{images_dir}'")
            
            print("📊 Estatísticas do novo sistema:")
            print(f"   • Imagens associadas a EJs: {len(imagens_com_ej)}")
            
            if imagens_com_ej:
                print(f"   • IDs de EJs com imagens: {list(set(img['id_ej_associado'] for img in imagens_com_ej))}")
            
            return imagens_extraidas
            
        except Exception as e: # pylint: disable=broad-exception-caught
            print(f"✗ Erro ao extrair imagens do PDF: {e}")
            return []
    
    def baixar_pdf_direto(self, url: str, caminho_saida: str) -> str:
        """Baixa PDF de uma URL"""
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
            
        except Exception as e: # pylint: disable=broad-exception-caught
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
            
        except Exception as e: # pylint: disable=broad-exception-caught
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
    
    def criar_prompt_gemini(self, texto: str) -> str:
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
    
    def extrair_informacoes_gemini(self, texto: str, info_pagina: str = "") -> List[Dict]:  # pylint: disable=unused-argument
        """Usa Gemini API com tratamento robusto de erros JSON"""
        
        prompt = self.criar_prompt_gemini(texto)
        
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
                print("✓ Empresas identificadas neste lote:")
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
            except (json.JSONDecodeError, ValueError) as json_err:
                print("✗ Não foi possível corrigir o JSON")
                print(f"Erro: {json_err}")
                print(f"Resposta problemática: {texto_resposta[:500]}...")
                return []
                
        except Exception as e: # pylint: disable=broad-exception-caught
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

        # GERANDO IDs ÚNICOS PARA EJs
        print("\n🔢 Gerando IDs únicos para as empresas...")
        empresas_com_id = []
        for i, empresa in enumerate(todas_empresas):
            # Gera um ID formatado: "1" + (5*"0") + contador
            contador = i + 1
            id_ej = f"1{contador:05d}" 
            
            # Cria um novo dicionário com o ID como primeiro campo
            empresa_atualizada = {'id': id_ej, **empresa}
            
            # Adiciona à nova lista
            empresas_com_id.append(empresa_atualizada)
        
        # Atualiza a lista principal para ser salva
        todas_empresas = empresas_com_id 
        print(f"✓ IDs gerados para {len(todas_empresas)} empresas.")
        
        # EXTRAIR IMAGENS COM NOVO SISTEMA DE NOMENCLATURA
        from config_ej import OUTPUT_DIR, EXTRAIR_IMAGENS
        if EXTRAIR_IMAGENS:
            print("\n🖼️  EXTRAINDO IMAGENS COM NOVO SISTEMA DE NOMENCLATURA...")
            imagens_extraidas = self.extrair_imagens_pdf(pdf_path, OUTPUT_DIR, empresas_com_id)
            if imagens_extraidas:
                print(f"✓ Total de imagens extraídas: {len(imagens_extraidas)}")
            else:
                print("ℹ️  Nenhuma imagem encontrada no PDF")
        
        # Salvar resultados
        self.salvar_json(todas_empresas, saida_json)
        
        print("\n=== PROCESSAMENTO CONCLUÍDO ===")
        print(f"📄 Páginas processadas: {paginas_processadas}")
        print(f"🏢 Empresas juniores extraídas: {len(todas_empresas)}")
        print(f"💾 Arquivo salvo: {saida_json}")
        
        # Lista final de empresas
        if todas_empresas:
            print("\n📋 LISTA DE EMPRESAS IDENTIFICADAS:")
            for i, empresa in enumerate(todas_empresas, 1):
                nome = empresa.get('Nome', 'Sem nome')
                cursos = empresa.get('Cursos', 'N/A')
                id_ej = empresa.get('id', 'Sem ID')
                print(f"  {i:2d}. [{id_ej}] {nome} | {cursos}")
        
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
                
        except Exception as e: # pylint: disable=broad-exception-caught
            print(f"✗ Erro ao salvar JSON: {e}")