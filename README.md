O projeto "Ubuntu Releases" é um script em Python que automatiza o processo de listagem e download de versões específicas do Ubuntu diretamente do site oficial. Aqui está uma descrição detalhada:

### Descrição do Código
O script apresenta as seguintes funcionalidades:
1. **Listagem de Versões Disponíveis:** Utilizando a biblioteca `BeautifulSoup`, o script acessa a página oficial de lançamentos do Ubuntu (`https://releases.ubuntu.com/`), extrai e exibe as versões disponíveis.
2. **Download de Arquivos ISO:** Permite ao usuário selecionar uma versão para baixar o arquivo ISO correspondente, exibindo uma barra de progresso visual com a biblioteca `tqdm`.

### Principais Componentes
- **Interface de Linha de Comando (CLI):** Mostra ASCII art temático do Ubuntu, lista as versões e guia o usuário para escolher qual ISO baixar.
- **Requisições HTTP:** Usa a biblioteca `requests` para acessar as informações online e gerenciar o download dos arquivos.
- **Gerenciamento de Downloads:** Baixa os arquivos em blocos, atualizando a barra de progresso para que o usuário acompanhe o status.

### Requisitos
- Python 3.x
- Dependências: `requests`, `beautifulsoup4`, `tqdm`

### Instruções de Uso
1. Clone o repositório.
2. Instale as dependências usando o `pip`.
3. Execute o script para listar e baixar as versões desejadas.

O projeto é uma solução simples, eficiente e prática para usuários que precisam baixar versões específicas do Ubuntu de maneira automatizada. Ele é licenciado sob a MIT License e está aberto a contribuições.
