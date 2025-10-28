import os
import json
from datetime import datetime # para debug
from config_ej import GEMINI_API_KEY, PDF_URL_EJS, OUTPUT_DIR, OUTPUT_JSON, PROCESSAR_POR_PAGINA, MAX_PAGINAS_POR_REQUISICAO, PAGINA_INICIAL_EJS, EXTRAIR_IMAGENS
from pdf_processor_ejs import PDFProcessorEJs

def configurar_ambiente():
    """Configura diretórios e configurações"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"✓ Diretório criado: {OUTPUT_DIR}")

    images_dir = os.path.join(OUTPUT_DIR, "images")
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
        print(f"✓ Diretório de imagens criado: {images_dir}")
    
    # Verifica API key
    if GEMINI_API_KEY == 'sua_chave_api_aqui':
        print("✗ ERRO: Configure sua GEMINI_API_KEY no arquivo config.py")
        print("Obtenha uma chave válida")
        return False
    
    return True

def processar_pdf_empresas_juniores(processador: PDFProcessorEJs, url_pdf: str):
    """Processa o PDF de empresas juniores"""
    print(f"\n{'='*60}")
    print(" PROCESSANDO PDF DE EMPRESAS JUNIORES")
    print(f" URL: {url_pdf}")
    print(f"{'='*60}")
    
    try:
        # Define caminhos de arquivo
        nome_pdf_local = "portfolio_empresas_juniores.pdf"
        caminho_pdf_local = os.path.join(OUTPUT_DIR, nome_pdf_local)
        caminho_json_saida = os.path.join(OUTPUT_DIR, OUTPUT_JSON)
        
        # Baixa o PDF se necessário
        if not os.path.exists(caminho_pdf_local) and url_pdf.startswith('http'):
            print("Baixando PDF...")
            processador.baixar_pdf_direto(url_pdf, caminho_pdf_local)
        elif os.path.exists(caminho_pdf_local):
            print("PDF já existe")
        else:
            # Assume que url_pdf é um caminho local
            caminho_pdf_local = url_pdf
            print(f"Usando PDF local: {caminho_pdf_local}")
        
        # Verifica se o PDF existe
        if not os.path.exists(caminho_pdf_local):
            print(f"✗ PDF não encontrado: {caminho_pdf_local}")
            return []
        
        # Extrair imagens se ativo
        if EXTRAIR_IMAGENS:
            print("\n EXTRAINDO IMAGENS DO PDF...")
            imagens_extraidas = processador.extrair_imagens_pdf(caminho_pdf_local, OUTPUT_DIR)
            if imagens_extraidas:
                print(f"✓ Total de imagens extraídas: {len(imagens_extraidas)}")
            else:
                print("ℹ Nenhuma imagem encontrada no PDF")

        # Processa o PDF
        if PROCESSAR_POR_PAGINA:
            print("Processamento página por página")
            print(f"   Páginas por requisição: {MAX_PAGINAS_POR_REQUISICAO}")
            print(f"   Página inicial: {PAGINA_INICIAL_EJS}")
            
            dados = processador.processar_pdf_paginado(
                caminho_pdf_local, 
                caminho_json_saida,
                MAX_PAGINAS_POR_REQUISICAO,
                PAGINA_INICIAL_EJS
            )
        else:
            print("Processamento único")
            dados = processador.processar_pdf_unico(caminho_pdf_local, caminho_json_saida)
        
        return dados
        
    except Exception as e:
        print(f"✗ ERRO ao processar PDF: {e}")
        import traceback
        traceback.print_exc()
        return []

def consolidar_dados_empresas(todos_dados: list, caminho_saida: str):
    """Consolida e remove duplicatas"""
    if not todos_dados:
        print("Nenhum dado para consolidar")
        return
    
    print(f"\nConsolidando dados de {len(todos_dados)} empresas...")
    
    # Remove duplicatas baseadas no nome
    empresas_unicas = []
    nomes_vistos = set()
    
    for empresa in todos_dados:
        nome = empresa.get('Nome', '').strip()
        if nome:
            nome_normalizado = nome.lower()
            if nome_normalizado not in nomes_vistos:
                nomes_vistos.add(nome_normalizado)
                empresas_unicas.append(empresa)
    
    dados_consolidados = {
        "metadados": {
            "data_processamento": datetime.now().isoformat(),
            "total_empresas_unicas": len(empresas_unicas),
            "total_empresas_bruto": len(todos_dados),
            "processamento_pagina": PROCESSAR_POR_PAGINA,
            "pagina_inicial": PAGINA_INICIAL_EJS
        },
        "empresas_juniores": empresas_unicas
    }
    
    try:
        with open(caminho_saida, 'w', encoding='utf-8') as f:
            json.dump(dados_consolidados, f, ensure_ascii=False, indent=2)
        
        print(f" -> Dados consolidados salvos em: {caminho_saida}")
        print(f"-> Empresas únicas: {len(empresas_unicas)}")
        print(f"->  Duplicatas removidas: {len(todos_dados) - len(empresas_unicas)}")
        
        # Estatísticas detalhadas
        if empresas_unicas:
            cursos = [ej.get('Cursos', '') for ej in empresas_unicas if ej.get('Cursos')]
            cursos_unicos = set(cursos)
            print(f"Cursos representados: {len(cursos_unicos)}")
            
            # Empresas com informações completas
            empresas_completas = sum(1 for ej in empresas_unicas 
                                   if ej.get('Nome') and ej.get('Cursos') and ej.get('Servicos'))
            print(f"Empresas com informações completas: {empresas_completas}/{len(empresas_unicas)}")
            
    except Exception as e:
        print(f"✗ Erro ao salvar dados consolidados: {e}")

def mostrar_estatisticas_finais(dados_empresas: list):
    """Mostra estatísticas finais detalhadas"""
    if not dados_empresas:
        print("\nNenhuma empresa foi extraída")
        return
    
    empresas_unicas = list({ej['Nome'].lower(): ej for ej in dados_empresas if ej.get('Nome')}.values())
    
    print(f"\n{'='*60}")
    print(" PROCESSAMENTO CONCLUÍDO")
    print(f"{'='*60}")
    print(f"Total de empresas juniores: {len(empresas_unicas)}")
    
    # Top empresas (consolidação de dados para análise)
    print(f"\n PRINCIPAIS EMPRESAS IDENTIFICADAS:")
    for i, empresa in enumerate(empresas_unicas[:10], 1):
        nome = empresa.get('Nome', 'Sem nome')
        cursos = empresa.get('Cursos', 'N/A')[:30] + "..." if len(empresa.get('Cursos', '')) > 30 else empresa.get('Cursos', 'N/A')
        print(f"  {i:2d}. {nome}")
        print(f"      📚 {cursos}")
    
    # Estatísticas por campo (consolidação de dados para análise)
    campos_preenchidos = {}
    for campo in ['Nome', 'Cursos', 'Sobre', 'Missao', 'Visao', 'Valores', 'Servicos', 'Site', 'Instagram']:
        preenchidos = sum(1 for ej in empresas_unicas if ej.get(campo) and ej.get(campo) not in ['', 'N/A'])
        campos_preenchidos[campo] = preenchidos
    
    print(f"\nESTATÍSTICAS POR CAMPO:")
    for campo, quantidade in campos_preenchidos.items():
        percentual = (quantidade / len(empresas_unicas)) * 100
        print(f"  {campo:10}: {quantidade:2d}/{len(empresas_unicas)} ({percentual:5.1f}%)")

def main():
    """Função principal"""
    print("=== EXTRATOR DE EMPRESAS JUNIORES UNB ===")
    
    if not configurar_ambiente():
        return
    
    # Inicializa o processador
    processador = PDFProcessorEJs(GEMINI_API_KEY)
    
    # Processa o PDF
    dados_empresas = processar_pdf_empresas_juniores(processador, PDF_URL_EJS)
    
    # Consolida resultados
    if dados_empresas:
        caminho_saida_consolidado = os.path.join(OUTPUT_DIR, OUTPUT_JSON)
        consolidar_dados_empresas(dados_empresas, caminho_saida_consolidado)
        mostrar_estatisticas_finais(dados_empresas)
    else:
        #debug messages
        print("\nNenhum dado foi extraído.")
        print("   Possíveis causas:")
        print("   - PDF não contém texto legível")
        print("   - Formato do PDF não suportado")
        print("   - Problema na API do Gemini")
        print("   - Modelo de Gemini usado não corresponde com a chave API")
        print("   - PDF não contém informações de empresas juniores")

if __name__ == "__main__":

    main()

