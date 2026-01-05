![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)
![Django Version](https://img.shields.io/badge/django-5.0%2B-green)
![PostGIS](https://img.shields.io/badge/PostGIS-Spatial--DB-blue)
![License](https://img.shields.io/badge/license-MIT-brightgreen)


# Zé Delivery Backend Challenge - API de Parceiros (GIS)

Este projeto é uma solução para o [Desafio de Backend do Zé Delivery](https://github.com/ab-inbev-ze-company/ze-code-challenges/blob/master/backend_pt.md).

O objetivo é desenvolver uma API REST que gerencie parceiros (PDVs) e implemente uma funcionalidade de busca geoespacial avançada: localizar o parceiro mais próximo cuja área de cobertura inclua a localização do usuário.

## 🚀 Tecnologias Utilizadas

* **Linguagem:** Python 3.12+
* **Framework:** Django & Django REST Framework
* **Banco de Dados:** PostgreSQL + PostGIS (Extensão espacial)
* **Geospatial:** GeoDjango (GDAL/GEOS)
* **Containerização:** Docker & Docker Compose
* **Gerenciador de Pacotes:** uv / pip

## 🧠 A Lógica Geoespacial

O principal desafio deste projeto é a busca de parceiros (`/partner/search`). Não basta buscar o ponto mais próximo (distância euclidiana); é necessário respeitar as regras de negócio:

1.  **Cobertura (MultiPolygon):** Cada parceiro tem uma área de entrega definida.
2.  **Localização (Point):** O usuário está em uma coordenada específica.

**Algoritmo implementado:**
A busca utiliza consultas espaciais indexadas. O algoritmo realiza um join espacial onde primeiro filtramos os parceiros cuja coverage_area contém o ponto do usuário (ST_Contains) e, em seguida, calculamos a distância (ST_Distance) para retornar o PDV mais próximo.
1.  Filtra parceiros onde o ponto do usuário está **contido** na área de cobertura (`ST_Contains`).
2.  Calcula a distância entre o usuário e a loja (`ST_Distance`).
3.  Ordena pelo mais próximo e retorna o melhor resultado.

## 🛠️ Como Rodar o Projeto

### Pré-requisitos
* [Docker](https://www.docker.com/) e Docker Compose instalados.

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/SEU-REPO.git](https://github.com/SEU-USUARIO/SEU-REPO.git)
    cd SEU-REPO
    ```

2.  **Suba o ambiente com Docker:**
    Este comando irá construir a imagem (instalando GDAL e dependências de sistema) e subir o banco de dados PostGIS.
    ```bash
    docker compose up --build
    ```

3.  **Aplique as migrações:**
    Em um novo terminal, execute:
    ```bash
    docker compose exec web python manage.py migrate
    ```

## 📍 Documentação da API

### 1. Criar Parceiro
Cria um novo parceiro com endereço e área de cobertura.

* **URL:** `/partner/`
* **Método:** `POST`
* **Body (JSON):**
    ```json
    {
      "trading_name": "Adega da Esquina",
      "owner_name": "Zé da Silva",
      "document": "12.345.678/0001-90",
      "coverage_area": {
        "type": "MultiPolygon",
        "coordinates": [
          [[[-43.365, -22.996], [-43.365, -23.019], [-43.265, -23.019], [-43.365, -22.996]]]
        ]
      },
      "address": {
        "type": "Point",
        "coordinates": [-43.297, -23.013]
      }
    }
    ```

### 2. Buscar Parceiro por ID
Retorna os dados de um parceiro específico.

* **URL:** `/partner/<id>/`
* **Método:** `GET`
* **Exemplo:** `/partner/a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11/`

### 3. Buscar Parceiro Mais Próximo (GIS)
Busca o parceiro mais próximo que **atende** a região solicitada.

* **URL:** `/partner/search/`
* **Método:** `GET`
* **Parâmetros:**
    * `lat`: Latitude do cliente (ex: -23.013)
    * `long`: Longitude do cliente (ex: -43.297)
* **Exemplo:**
    ```
    GET /partner/search/?lat=-23.013&long=-43.297
    ```
## 🧠 Decisões de Arquitetura

Para este desafio, foram tomadas decisões visando escalabilidade e segurança:

* **UUID v4 como Chave Primária:** Optou-se por não utilizar IDs sequenciais (1, 2, 3...) do dataset original. O uso de UUIDs previne o "ID Enumeration", impedindo que terceiros descubram o volume total de parceiros na base e facilitando a integração de dados em ambientes distribuídos.
* **Índices Espaciais (GIST):** A API utiliza índices GIST nos campos de geometria para garantir que a busca por localização seja performática mesmo com milhares de registros.
* **Validação Única:** O campo `document` (CNPJ) é tratado como único, garantindo a integridade dos dados conforme as regras de negócio.

## 📥 Importação de Dados

Caso deseje carregar o dataset original (`partners.json`), os IDs originais serão ignorados em favor da geração automática de UUIDs pelo banco de dados.

```bash
docker compose exec web python manage.py import_pdvs data/pdvs.json
```

## 🧪 Como Testar

Recomenda-se o uso do **Insomnia** ou **Postman**.

1.  Certifique-se de que o Docker está rodando.
3.  Faça uma requisição `GET` na rota de busca com coordenadas próximas das que você criar 

---
Desenvolvido por [Giancarlo Brandalise](https://github.com/Giancarlo-BR)
