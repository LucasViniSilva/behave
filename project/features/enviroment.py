from pymongo import MongoClient

def before_scenario(context, scenario):
    # Conectar ao banco Mongo e limpar a collection antes de cada cenário
    client = MongoClient("mongodb://localhost:27017/")
    db = client["cadastro"]
    db["estabelecimentos"].delete_many({})

def after_all(context):
    print("✔ Testes finalizados!")
