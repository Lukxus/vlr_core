# Como criar um ambiente virtual
1. Criar a pasta onde ficarão os seus ambientes
2. Entrar nela
3. Abrir o terminal
4. python -m venv <nome_do_ambiente>

# Como ativar o ambiente
1. Entrar na pasta do ambiente
2. .\Scripts\activate

# Como instalar o Django
1. Recomendo fazer isso dentro do seu venv
2. pip install django

# Como iniciar um projeto Django
1. django-admin startproject <nome_projeto>

# Como configurar o intepretador do venv no pycharm
1. Abrir as setting
2. Navegue até Project: [Nome do Projeto] > Python Interpreter. 
3. Clique no ícone de engrenagem ao lado do campo do interpretador e selecione Add.... 
4. Escolha Existing Environment. 
5. Clique no ícone de pasta ou nos três pontos (...) para navegar até o diretório onde seu ambiente virtual está localizado. 
6. Navegue até o diretório do venc. 
7. Dentro desse diretório, selecione o executável do Python. No Windows, isso geralmente estará em D:\.virtualenvs\vlr_django\Scripts\python.exe. 
8. Clique em OK e depois em Apply para salvar as configurações.

# Como Rodar a aplicação
1. python manage.py runserver

# Como criar o app
1. django-admin startapp <nome_do_app>

# Configurando IDE - Pycharm
1. Instalar plugin do docker

# Guia de Instalação e Configuração do Docker com PostgreSQL para Projeto Django

## Parte 1: Instalação do Docker no Windows

1. **Baixar e instalar o Docker Desktop**:
   - Acesse o site oficial do Docker e faça o download do Docker Desktop para Windows.
   - Execute o instalador e siga as instruções para completar a instalação.

2. **Configurar o Docker Desktop**:
   - Inicie o Docker Desktop.
   - Habilite o WSL 2 como backend em **Settings** > **General** > **Use the WSL 2 based engine**.
   - Reinicie o Docker Desktop se necessário.

## Parte 2: Configuração do Projeto com Docker e PostgreSQL

1. **Criar Arquivo `.env`**:
   - Crie um arquivo `.env` na raiz do projeto e defina as variáveis de ambiente para o banco de dados PostgreSQL.

2. **Configurar Docker Compose**:
   - Crie ou edite o arquivo `docker-compose.yml` na raiz do projeto para definir os serviços do Docker, incluindo PostgreSQL.

3. **Configurar Django para usar PostgreSQL**:
   - No arquivo de configurações do Django (`settings.py`), configure o banco de dados para utilizar o PostgreSQL com as variáveis de ambiente definidas.

## Parte 3: Subir o Ambiente com Docker

1. **Subir o Docker Compose**:
   - Execute os comandos no terminal para subir o ambiente Docker.

## Parte 4: Gerenciamento dos Volumes e Zeragem da Base de Dados

### Configuração dos Volumes

Os dados do PostgreSQL são armazenados na pasta `volumes` dentro do seu projeto. Isso garante que os dados persistam mesmo que os contêineres sejam reiniciados.

### Zerando a Base de Dados

Para zerar a base de dados, você pode simplesmente apagar a pasta `pgdata` e subir os contêineres novamente. Isso recriará a estrutura do banco de dados com base nas variáveis de ambiente definidas.

1. **Pare os contêineres**:
   - `docker-compose down`

2. **Apague a pasta `pgdata`**:
   - `rm -rf pgdata`

3. **Suba os contêineres novamente**:
   - `docker-compose up -d`

## Parte 5: Conectar ao Banco de Dados com DBeaver

1. **Abrir o DBeaver**:
   - Inicie o DBeaver.

2. **Adicionar Nova Conexão**:
   - Clique em `Database` > `New Database Connection` e selecione `PostgreSQL`.

3. **Configurar a Conexão**:
   - Defina o host, porta, banco de dados, nome de usuário e senha conforme configurado no Docker Compose e no script SQL de inicialização.

4. **Testar Conexão**:
   - Clique em `Test Connection` para verificar se a conexão pode ser estabelecida e, se bem-sucedida, clique em `Finish` para salvar a conexão.

## Conclusão

Seguindo estes passos, você instalará o Docker no Windows, configurará um ambiente Docker com PostgreSQL para desenvolvimento de um projeto Django, e se conectará ao banco de dados usando DBeaver. Esta configuração simplifica a gestão do banco de dados durante o desenvolvimento e garante que você tenha um ambiente consistente. A configuração dos volumes permite uma fácil manutenção dos dados, e a possibilidade de zerar a base de dados simplesmente apagando a pasta `pgdata`.
