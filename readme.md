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