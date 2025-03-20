Documentação do Projeto: API de Monitoramento de Pedidos de Delivery

1. Introdução

Esta API tem como objetivo o monitoramento de pedidos de delivery. Ela permite registrar pedidos, consultar estatísticas de entregas, atualizar status de pedidos e gerar relatórios detalhados sobre os pedidos.

2. Tecnologias Utilizadas

. FastAPI – Framework para criação da API.
. SQLite – Banco de dados utilizado para armazenar os dados dos pedidos.
. SQLAlchemy – ORM para interagir com o banco de dados.
. Pandas – Biblioteca utilizada para manipulação de dados e geração de relatórios.
. Uvicorn – Servidor ASGI para rodar a aplicação FastAPI.

3. Funcionalidades

Cadastrar Pedido

Método: POST
Endpoint: /pedidos/
Descrição: Cadastra um novo pedido na plataforma.
Exemplo de corpo:

{
  "cliente_nome": "João Silva",
  "status": "pendente"
}

Consultar Estatísticas 

. Método: GET
. Endpoint: /estatisticas
. Descrição: Obtém estatísticas sobre os pedidos, como tempo médio de entrega, total de pedidos por status e total de pedidos por dia.

4. Como Rodar o Projeto Localmente

Passos para Rodar o Projeto

. Clonar o Repositório

git clone https://github.com/matheussmends/api-delivery.git
cd api-delivery

. Criar um Ambiente Virtual

python -m venv venv

. Instalar Dependências

pip install -r requirements.txt

. Rodar o Servidor

uvicorn app.main:app --reload

Agora você pode acessar a API em http://localhost:8000.

5. Endpoints

POST /pedidos/

. Cria um novo pedido.
. Corpo da requisição:
{
  "cliente_nome": "João Silva",
  "status": "pendente"
}

GET /estatisticas

. Descrição: Retorna estatísticas sobre os pedidos.
. Resposta:
{
  "tempo_medio_entrega": 5.4,
  "total_pedidos_por_status": {
    "pendente": 3,
    "entregue": 5
  },
  "total_pedidos_por_dia": {
    "2025-03-20": 10
  }
}

6. Modelos de Dados

Tabela Pedidos

. id: Identificador único do pedido (inteiro, autoincremento).
. cliente_nome: Nome do cliente (string).
. status: Status do pedido (string: pendente, entregue, etc.).
. hora_pedido: Data e hora do pedido (datetime).
. hora_entrega: Data e hora de entrega (datetime)

7. Contribuições

Se alguém quiser contribuir para o projeto, basta seguir esses passos:

. Fazer um fork do repositório.
. Criar uma branch para sua feature: git checkout -b nome-da-feature.
. Adicionar suas mudanças e fazer commit: git commit -m 'Adicionando feature X'.
. Subir para o seu fork: git push origin nome-da-feature.
. Criar um Pull Request no repositório original.

8. Licença
