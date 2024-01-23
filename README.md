# etl-docker-postgres

Como configurar o ambiente:

clone o repositório para sua máquina

```
git clone https://github.com/arthurferreira1/etl-docker-postgres.git
```
Você precisará ter o docker desktop instalado no seu computador: https://www.docker.com/products/docker-desktop/

Navegue até a pasta que você fez o clone e faça o build do docker-compose com os conteiners que precisamos para aplicação rodar.
```
docker compose up
```
Acesse o airflow
```
localhost:8080
```
Certifique-se que a DAG está rodando com sucesso

Após isso, basta conectar seu Power BI na tabela etl-airflow
