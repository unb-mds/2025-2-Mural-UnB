import fitz  # PyMuPDF
import re
import csv
import os

def limpar_texto(texto):
    """
    Remove caracteres especiais problemáticos do texto
    """
    if not texto:
        return texto
    # Remove espaços não-quebráveis e outros caracteres Unicode problemáticos
    texto = texto.replace('\u202f', ' ')  # Narrow no-break space
    texto = texto.replace('\xa0', ' ')    # Non-breaking space
    texto = texto.replace('\u2013', '-')  # En dash
    texto = texto.replace('\u2014', '-')  # Em dash
    texto = texto.replace('\u2019', "'")  # Right single quotation mark
    texto = texto.replace('\u201c', '"')  # Left double quotation mark
    texto = texto.replace('\u201d', '"')  # Right double quotation mark
    return texto

def juntar_palavras_hifenizadas(texto):
    """
    Remove hifenização de quebra de linha
    Exemplo: 'pesqui- sadores' -> 'pesquisadores'
    """
    if not texto:
        return texto
    # Padrão: letra + hífen + espaço(s) + letra minúscula
    # Isso indica quebra de palavra no final da linha
    texto = re.sub(r'(\w)-\s+(\w)', r'\1\2', texto)
    return texto

def extrair_laboratorios_fga_pdf(pdf_path, pagina_inicial=13):
    doc = fitz.open(pdf_path)
    idx_inicial = pagina_inicial - 1
    texto_completo = ""
    for num_pagina in range(idx_inicial, len(doc)):
        texto_pagina = doc[num_pagina].get_text()
        # Limpa caracteres especiais
        texto_completo += limpar_texto(texto_pagina)
    doc.close()
    # Lista para armazenar laboratórios
    laboratorios = []
    labs_fga = []
    # Divide o texto em linhas para análise
    linhas = texto_completo.split('\n')
    lab_atual = None
    i = 0
    while i < len(linhas):
        linha = linhas[i].strip()
        if not linha:
            i += 1
            continue
        
        # VERIFICA CABEÇALHOS DE SEÇÃO (antes de processar laboratórios)
        if (re.match(r'^\d+\.\d+(\.\d+)*\.', linha) or  # Numeração de seção (1.2.5.)
            re.match(r'^[_\-]{20,}$', linha)):  # Linha de separação longa
            # Salva o laboratório atual se existir
            if lab_atual:
                laboratorios.append(lab_atual)
                texto_completo_lab = f"{lab_atual['nome']} {lab_atual['coordenador']} {lab_atual['contato']} {lab_atual['descricao']}"
                if 'FGA' in texto_completo_lab.upper():
                    labs_fga.append(lab_atual)
                lab_atual = None
            i += 1
            continue
        
        # CASO ESPECIAL: Número sozinho em uma linha (labs 1-9)
        if re.match(r'^(\d+)\.$', linha):
            numero_lab = re.match(r'^(\d+)\.$', linha).group(1)
            if i + 1 < len(linhas):
                proxima_linha = linhas[i + 1].strip()
                if (proxima_linha and 
                    not proxima_linha.startswith('COORDENADOR:') and
                    not proxima_linha.startswith('COORDENADORES:') and
                    not proxima_linha.startswith('CONTATO:') and
                    not proxima_linha.startswith('DESCRIÇÃO:') and
                    not proxima_linha.startswith('DESCRICAO:')):
                    # Salva o laboratório anterior se existir
                    if lab_atual:
                        laboratorios.append(lab_atual)
                        # Verifica se é da FGA
                        texto_completo_lab = f"{lab_atual['nome']} {lab_atual['coordenador']} {lab_atual['contato']} {lab_atual['descricao']}"
                        if 'FGA' in texto_completo_lab.upper():
                            labs_fga.append(lab_atual)
                    # Cria novo laboratório
                    lab_atual = {
                        'nome': proxima_linha,
                        'coordenador': '',
                        'contato': '',
                        'descricao': ''
                    }
                    i += 2
                    continue
        
        # CASO NORMAL: Número e nome na mesma linha (labs 10+)
        padrao_numero_simples = re.match(r'^(\d+)\.\s+(.+)', linha)
        if padrao_numero_simples:
            numero_lab = padrao_numero_simples.group(1)
            nome_sem_numero = padrao_numero_simples.group(2).strip()
            # FILTRO 1: Rejeita sub-numeração
            if re.match(r'^\d+\.\d+', linha):
                i += 1
                continue

            # FILTRO 2: Rejeita cabeçalhos em MAIÚSCULAS
            palavras_significativas = [p for p in nome_sem_numero.split() 
                                       if len(p) > 2 and p.isalpha()]
            if palavras_significativas:
                maiusculas = sum(1 for p in palavras_significativas if p.isupper())
                if maiusculas / len(palavras_significativas) > 0.7:
                    i += 1
                    continue

            # Aceita se tiver pelo menos 10 caracteres e menos de 200
            if len(nome_sem_numero) > 10 and len(nome_sem_numero) < 200:
                # Se o nome termina com hífen, verifica se a sigla está na próxima linha
                if nome_sem_numero.endswith('-') and i + 1 < len(linhas):
                    proxima = linhas[i + 1].strip()
                    # Se a próxima linha é curta (provável sigla) e não é um campo, adiciona ao nome
                    if (proxima and len(proxima) < 30 and 
                        not proxima.startswith('COORDENADOR:') and
                        not proxima.startswith('COORDENADORES:') and
                        not proxima.startswith('CONTATO:') and
                        not proxima.startswith('DESCRIÇÃO:') and
                        not proxima.startswith('DESCRICAO:')):
                        nome_sem_numero += ' ' + proxima
                        i += 1  # Pula a próxima linha já que foi incorporada
                # Salva o laboratório anterior se existir
                if lab_atual:
                    laboratorios.append(lab_atual)
                    # Verifica se é da FGA
                    texto_completo_lab = f"{lab_atual['nome']} {lab_atual['coordenador']} {lab_atual['contato']} {lab_atual['descricao']}"
                    if 'FGA' in texto_completo_lab.upper():
                        labs_fga.append(lab_atual)
                # Cria novo laboratório
                lab_atual = {
                    'nome': nome_sem_numero,
                    'coordenador': '',
                    'contato': '',
                    'descricao': ''
                }
        # Se estamos rastreando um laboratório, tenta preencher informações
        elif lab_atual:
            # COORDENADOR ou COORDENADORES (singular e plural)
            if (linha.startswith('COORDENADOR:') or 
                linha.startswith('COORDENADORES:') or 
                linha.startswith('RESPONSÁVEL:') or
                linha.startswith('RESPONSÁVEIS:')):
                coordenador_texto = linha.split(':', 1)[1].strip() if ':' in linha else ''
                # Remove todos os IDs Lattes (pode haver múltiplos)
                coordenador_texto = re.sub(r'\s*\(ID Lattes:\s*\d+\)', '', coordenador_texto, flags=re.IGNORECASE)
                # Remove IDs Lattes incompletos (casos onde o parêntese fecha em outra linha)
                coordenador_texto = re.sub(r'\s*\(ID\s*$', '', coordenador_texto)
                coordenador_texto = re.sub(r'\s*\(ID Lattes:.*$', '', coordenador_texto)
                # Se já existe um coordenador, adiciona o novo separado por vírgula
                if lab_atual['coordenador']:
                    lab_atual['coordenador'] += ', ' + coordenador_texto.strip()
                else:
                    lab_atual['coordenador'] = coordenador_texto.strip()
            # CONTATO
            elif linha.startswith('CONTATO:'):
                lab_atual['contato'] = linha.split(':', 1)[1].strip() if ':' in linha else ''
            # DESCRIÇÃO
            elif linha.startswith('DESCRIÇÃO:') or linha.startswith('DESCRICAO:'):
                descricao = linha.split(':', 1)[1].strip() if ':' in linha else ''
                # Captura descrição em múltiplas linhas
                j = i + 1
                while j < len(linhas):
                    proxima_linha = linhas[j].strip()
                    # Verifica se encontrou cabeçalho de seção (termina processamento do lab atual)
                    if proxima_linha and re.match(r'^\d+\.\d+(\.\d+)*\.', proxima_linha):
                        break
                    
                    # Para se encontrar uma nova seção ou marcadores de fim
                    if proxima_linha and (':' in proxima_linha and 
                        any(proxima_linha.startswith(palavra) for palavra in 
                            ['GRUPOS', 'EQUIPAMENTOS', 'COORDENADOR', 'COORDENADORES', 
                             'CONTATO', 'LABORATÓRIO', 'NÚCLEO', 'CENTRO'])):
                        break

                    # Para se encontrar marcadores de rodapé ou nova seção
                    if proxima_linha:
                        # Detecta início de seção (letra + hífen + maiúsculas)
                        if re.match(r'^[IVX]+\s*-\s*[A-ZÀÁÂÃÉÊÍÓÔÕÚÇ\s]+$', proxima_linha):
                            break
                        # Detecta rodapé institucional
                        if any(palavra in proxima_linha.upper() for palavra in 
                               ['UNIVERSIDADE DE BRASÍLIA', 'PORTFÓLIO', 'INFRAESTRUTURA DE PESQUISA', 
                                'DPI CPAIP', 'CIÊNCIAS EXATAS E TECNOLÓGICAS', 'CIÊNCIAS EXATAS E DA TERRA']):
                            break

                        # Detecta linhas de separação (muitos underscores ou hífens)
                        if re.match(r'^[_\-]{10,}$', proxima_linha):
                            break

                        descricao += ' ' + proxima_linha
                    j += 1
                # Remove classificação
                descricao = re.sub(r'\s+CLASSIFICA[ÇC][ÃA]O:.*$', '', descricao, flags=re.IGNORECASE)
                descricao = re.sub(r'\s+Laborat[óo]rio de Pesquisa\s*$', '', descricao, flags=re.IGNORECASE)
                # Remove fragmentos de rodapé que podem ter sido capturados
                descricao = re.sub(r'\s+[IVX]+\s*-\s*CIÊNCIAS.*$', '', descricao, flags=re.IGNORECASE)
                descricao = re.sub(r'\s+UNIVERSIDADE DE BRASÍLIA.*$', '', descricao, flags=re.IGNORECASE)
                descricao = re.sub(r'\s+PORTFÓLIO.*$', '', descricao, flags=re.IGNORECASE)
                # Remove hifenização de quebra de linha
                descricao = juntar_palavras_hifenizadas(descricao)
                lab_atual['descricao'] = descricao.strip()
                i = j - 1
        i += 1
    # Adiciona o último laboratório
    if lab_atual:
        laboratorios.append(lab_atual)
        texto_completo_lab = f"{lab_atual['nome']} {lab_atual['coordenador']} {lab_atual['contato']} {lab_atual['descricao']}"
        if 'FGA' in texto_completo_lab.upper():
            labs_fga.append(lab_atual)
    return labs_fga

def filtrar_labs_fga(pdf_path, csv_saida):
    # Extrai laboratórios da FGA do PDF
    labs_fga = extrair_laboratorios_fga_pdf(pdf_path)
    # Detecta quando a descrição menciona um lab diferente do nome
    labs_fga_filtrados = []
    for lab in labs_fga:
        # Se a descrição menciona FGA, OK
        if 'FGA' in lab['descricao'].upper():
            # Verifica se a descrição fala de um lab diferente
            nome_curto = lab['nome'].split('-')[0].strip().split()[0:3]  # Primeiras palavras do nome
            primeira_frase_desc = lab['descricao'].split('.')[0] if lab['descricao'] else ""
            nome_keywords = [palavra.lower() for palavra in nome_curto if len(palavra) > 3]
            desc_lower = primeira_frase_desc.lower()
            # Verifica se pelo menos uma palavra do nome aparece na descrição
            tem_match = any(keyword in desc_lower for keyword in nome_keywords)
            sigla_match = re.match(r'^O\s+([A-Z]+),', primeira_frase_desc)
            if sigla_match:
                sigla_desc = sigla_match.group(1)
                if sigla_desc not in lab['nome']:
                    continue

            labs_fga_filtrados.append(lab)
    # Remove duplicatas baseando-se no nome do laboratório
    labs_unicos = {}
    for lab in labs_fga_filtrados:
        nome_normalizado = lab['nome'].strip().upper()
        if nome_normalizado not in labs_unicos:
            labs_unicos[nome_normalizado] = lab
    labs_fga_final = list(labs_unicos.values())
    print()
    print(f"RESULTADO: {len(labs_fga_final)} laboratorios da FGA ")
    print()
    if labs_fga_final:
        # Salva no CSV de saída
        with open(csv_saida, 'w', newline='', encoding='utf-8') as f:
            campos = ['nome', 'coordenador', 'contato', 'descricao']
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            writer.writerows(labs_fga_final)

def main():
    # Caminhos
    script_dir = os.path.dirname(__file__)
    pdf_path = os.path.join(script_dir, "..", "data", "Labs", "Portfolio_Infraestrutura_UnB.pdf")
    csv_saida = os.path.join(script_dir, "..", "data", "Labs", "labs_fga.csv")
    # Verifica se o PDF existe
    if not os.path.exists(pdf_path):
        print(f"ERRO: PDF não encontrado em {pdf_path}")
        print("Baixe o PDF primeiro executando o script labs_pdf.py")
        return
    
    try:
        filtrar_labs_fga(pdf_path, csv_saida)
    except Exception as e:
        print(f"\nERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
