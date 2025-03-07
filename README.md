ETL desafio BIX Tecnologia

Este documento tem como objetivo explicar o funcionamento do pipeline implementado para o desafio. O projeto consiste em buscar dados em diferentes fontes (Banco Postgres, google storage e API) e aloca-los em um banco de dados local.

As tecnologias utilizadas para solução do desafio são:

- PostgreSQL
- Python (Bibliotecas específicas)
- Airflow
- Docker 

O pipeline criado utiliza-se do Airflow para orquestrar o processo de busca dos dados raw e trazê-los para o banco em production. Os dados são encontrados em um banco de dados PostgreSQL hospedado pela Bix Tecnologia, em um arquivo ".parquet" salvo em um google storage e em uma API fornecida pela Bix Tecnologia. O Pipeline consiste em buscar os dados de cada fonte utilizando módulos escritos em Python usando as bibliotecas necessárias e salvar cada tabela em um banco de dados PostgreSQL local em uma estrutura de Data Warehouse.

O diretório "airflow" do projeto contem o subdiretório "dags" onde estão alocados os principais módulos de processo do orquestrador. O diretório "modules" possui os módulos implementados para buscar os dados nas diferentes fontes fornecidas. Os módulos são:

- orders.py: busca os dados das vendas realizadas
- employee.py: busca os dados dos funcionários da empresa
- category.py: busca os dados das categorias das vendas realizadas

Já o diretório "dags" contém o arquivo principal chamado "etl.py", onde são utilizados os módulos para busca dos dados e cria-se o proceso no Airflow com o scheduler para rodar diariamente às 4:30 AM.

Todo o processo é realizado em um container docker com a imagem específica para o Airflow, disponível no site do mesmo com as bibliotecas python necessárias para rodar o projeto. Os arquivos "dockerfile" e "docker-compose.yml" são responsáveis por criar a imagem e rodar a aplicação que pode ser acessada via navegador através do link "https://localhost:8080". Vídeo sobre como utilizar Airflow com Docker: https://www.youtube.com/watch?v=N3Tdmt1SRTM&t=378s

!!!IMPORTANTE !!!

Requisitos para a execução do projeto:

- Python: versão 3.9 ou acima
- Docker Desktop
- Postgres: versão 16 ou acima
- WSL 2

Ferramentas recomendadas:

- DBeaver: recomendado para conexão com o banco de dados local e com o banco postgres de origem para validar o movimento dos dados

Para rodar, é necessário que o Docker Desktop e WSL2 estejam instalados localmente. O projeto pode ser executado na pasta pelos comandos:

- "docker build -f dockerfile -t desafiobix:latest ." (Para criar a imagem)

- "docker compose -f docker-compose.yml up" (Para rodar o container com o Airflow)

Assim que o container do Airflow estiver rodando, um diretório chamado "airflow" será automaticamente criado. 
Dentro desse diretório, deve-se criar um subdiretório chamado "dags", onde será criado o script python com o fluxo principal dos dados.

Para testar o seu código, você pode executá-lo na interface web do airflow acessando via 'https://localhost:8080'

Outra forma é, através do terminal, utilizar os comandos:

- docker exec -it desafiobix-desafiobix-airflow-1 bash (Para acessar o terminal interno do airflow no docker)
- airflow dags test nome_da_sua_dag (Para rodar um teste no fluxo principal acompanhando os logs das atividades)

