import requests
from behave import given, when, then
from urllib.parse import urlencode

BASE_URL = "http://localhost:8000/estabelecimentos"

@given('que eu tenho um estabelecimento com nome "{nome}" e localização válida')
def step_impl(context, nome):
    context.payload = {
        "nome": nome,
        "latitude": -23.5505,
        "longitude": -46.6333
    }

@given('existe um estabelecimento "{nome}" na localização ({lat}, {lon})')
def step_impl(context, nome, lat, lon):
    requests.post(BASE_URL, json={
        "nome": nome,
        "latitude": float(lat),
        "longitude": float(lon)
    })

@given('eu tento cadastrar "{nome}" na localização ({lat}, {lon})')
def step_impl(context, nome, lat, lon):
    context.payload = {
        "nome": nome,
        "latitude": float(lat),
        "longitude": float(lon)
    }

@when('eu envio os dados para a API de cadastro')
def step_impl(context):
    context.response = requests.post(BASE_URL, json=context.payload)

@then('o sistema deve retornar status {status_code:d} e confirmar o cadastro')
def step_impl(context, status_code):
    assert context.response.status_code == status_code
    assert "id" in context.response.json()

@then('o sistema deve retornar erro de distância mínima')
def step_impl(context):
    assert context.response.status_code == 400
    assert "distância mínima" in context.response.text.lower()

@given('que existem 2 estabelecimentos cadastrados')
def step_impl(context):
    requests.post(BASE_URL, json={"nome": "Loja 1", "latitude": -23.5505, "longitude": -46.6333})
    requests.post(BASE_URL, json={"nome": "Loja 2", "latitude": -23.5510, "longitude": -46.6340})

@when('eu acesso a API de listagem')
def step_impl(context):
    context.response = requests.get(BASE_URL)

@then('o sistema deve retornar uma lista com {count:d} estabelecimentos')
def step_impl(context, count):
    assert context.response.status_code == 200
    assert len(context.response.json()) == count

@given('que existe um estabelecimento com nome "{nome}"')
def step_impl(context, nome):
    requests.post(BASE_URL, json={"nome": nome, "latitude": -23.5505, "longitude": -46.6333})

@when('eu faço uma requisição de busca com o nome "{nome}"')
def step_impl(context, nome):
    query = urlencode({"nome": nome})
    context.response = requests.get(f"{BASE_URL}/buscar?{query}")

@then('o sistema deve retornar os dados do estabelecimento correspondente')
def step_impl(context):
    assert context.response.status_code == 200
    assert "nome" in context.response.json()

@when('eu envio uma requisição para atualizar seu endereço')
def step_impl(context):
    context.response = requests.put(f"{BASE_URL}/1", json={"latitude": -23.5510, "longitude": -46.6340})

@then('o sistema deve confirmar a atualização com status 200')
def step_impl(context):
    assert context.response.status_code == 200

@when('eu envio uma requisição de exclusão')
def step_impl(context):
    context.response = requests.delete(f"{BASE_URL}/1")

@then('o sistema deve retornar status 204 e confirmar a exclusão')
def step_impl(context):
    assert context.response.status_code == 204

@given('que eu tenho um estabelecimento com latitude {lat} e longitude {lon}')
def step_impl(context, lat, lon):
    context.payload = {
        "nome": "Invalido",
        "latitude": float(lat),
        "longitude": float(lon)
    }

@then('o sistema deve retornar erro de validação')
def step_impl(context):
    assert context.response.status_code == 422 or context.response.status_code == 400

@when('eu solicito um relatório com raio de {raio} km a partir de ({lat}, {lon})')
def step_impl(context, raio, lat, lon):
    query = urlencode({
        "latitude": float(lat),
        "longitude": float(lon),
        "raio_km": float(raio)
    })
    context.response = requests.get(f"{BASE_URL}/relatorio?{query}")

@then('o sistema deve retornar apenas os estabelecimentos dentro desse raio')
def step_impl(context):
    assert context.response.status_code == 200
    assert isinstance(context.response.json(), list)

@given('que eu tenho um payload sem o campo nome')
def step_impl(context):
    context.payload = {
        "latitude": -23.5505,
        "longitude": -46.6333
    }

@then('o sistema deve retornar erro de campo obrigatório')
def step_impl(context):
    assert context.response.status_code == 422

@when('eu faço uma requisição para uma rota inexistente "{rota}"')
def step_impl(context, rota):
    context.response = requests.get(f"http://localhost:8000{rota}")

@then('o sistema deve retornar status 404')
def step_impl(context):
    assert context.response.status_code == 404
