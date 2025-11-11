// site/src/utils/dataService.ts

export async function fetchData<T>(fileName: string): Promise<T | null> {
  // O fetch padrão busca a partir da pasta 'public'
  const path = `/${fileName}`;

  console.log(`[DataService] Fetching: ${path}`);

  try {
    const response = await fetch(path);

    // Se a resposta não for OK (ex: 404 Not Found), lança um erro
    if (!response.ok) {
      throw new Error(`Falha ao buscar ${fileName}: ${response.status} ${response.statusText}`);
    }

    // Parseia a resposta como JSON
    const data: T = await response.json();
    return data;
  } catch (error) {
    console.error(`[DataService] Erro ao carregar ${fileName}:`, error);
    return null; // Retorna nulo para o hook/componente saber que falhou
  }
}

