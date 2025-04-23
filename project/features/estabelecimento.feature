Feature: Gerenciamento de estabelecimentos

  Como um administrador do sistema
  Eu quero cadastrar, listar e validar estabelecimentos
  Eu possa manter um controle geográfico eficaz

  Scenario: Cadastrar um novo estabelecimento com dados válidos
    Given que eu tenho um estabelecimento com nome "Loja A" e localização válida
    When eu envio os dados para a API de cadastro
    Then o sistema deve retornar status 201 e confirmar o cadastro

  Scenario: Cadastrar um estabelecimento muito próximo de outro existente
    Given que existe um estabelecimento "Loja A" na localização (10, 10)
    And eu tento cadastrar "Loja B" na localização (10.0001, 10.0001)
    When eu envio os dados para a API de cadastro
    Then o sistema deve retornar erro de distância mínima

  Scenario: Listar todos os estabelecimentos cadastrados
    Given que existem 2 estabelecimentos cadastrados
    When eu acesso a API de listagem
    Then o sistema deve retornar uma lista com 2 estabelecimentos

  Scenario: Buscar um estabelecimento por nome
    Given que existe um estabelecimento com nome "Mercado Central"
    When eu faço uma requisição de busca com o nome "Mercado Central"
    Then o sistema deve retornar os dados do estabelecimento correspondente

  Scenario: Atualizar os dados de um estabelecimento
    Given que existe um estabelecimento chamado "Farmácia Vida"
    When eu envio uma requisição para atualizar seu endereço
    Then o sistema deve confirmar a atualização com status 200

  Scenario: Remover um estabelecimento existente
    Given que existe um estabelecimento chamado "Padaria Sol"
    When eu envio uma requisição de exclusão
    Then o sistema deve retornar status 204 e confirmar a exclusão

  Scenario: Cadastrar estabelecimento com coordenadas inválidas
    Given que eu tenho um estabelecimento com latitude 999 e longitude 999
    When eu envio os dados para a API
    Then o sistema deve retornar erro de validação

  Scenario: Gerar relatório de estabelecimentos por raio de distância
    Given que existem estabelecimentos cadastrados em diferentes regiões
    When eu solicito um relatório com raio de 5 km a partir de (20, 20)
    Then o sistema deve retornar apenas os estabelecimentos dentro desse raio

  Scenario: Tentar cadastrar um estabelecimento sem nome
    Given que eu tenho um payload sem o campo nome
    When eu envio os dados para a API
    Then o sistema deve retornar erro de campo obrigatório

  Scenario: Verificar resposta para rota inexistente
    When eu faço uma requisição para uma rota inexistente "/inexistente"
    Then o sistema deve retornar status 404
