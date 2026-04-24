const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const permissaoService = {
  getRegras: async () => {
    const token = localStorage.getItem('reurb_access_token');

    console.log('TOKEN ENVIADO:', token); // 👈 NOVO

    const response = await fetch(`${API_URL}/api/permissoes/regras/`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    console.log('STATUS:', response.status); // 👈 NOVO

    if (!response.ok) {
      const erro = await response.text(); // 👈 NOVO
      console.error('ERRO BACKEND:', erro); // 👈 NOVO
      throw new Error('Erro ao buscar permissões');
    }

    return await response.json();
  },
};