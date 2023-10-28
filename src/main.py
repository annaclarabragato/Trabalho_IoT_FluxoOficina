import json
from fastapi import FastAPI, Request, Response
from datetime import datetime

app = FastAPI()

registros = []

@app.get("/")
def health_check():
    return {"status": "ok"}

# POST /registros
@app.post("/registros")
async def criar_registro(request: Request):
    # Recupera o body
    body = await request.body()
    # Converte para dictionary
    body = dict(json.loads(body))

    # Criamos uma variável de controle
    registro_existe = False
    # Percorremos a lista procurando se existe um registro
    # com a mesma placa
    for registro in registros:
        # Se existir, atualiza a variável de controle e para o loop
        if (registro.get("placa_veiculo") == body.get("placa_veiculo")):
            registro_existe = True
            break;
    # Se existir um registro, vai retornar uma mensagem
    if (registro_existe):
        content = json.dumps({"mensagem": "Registro Existente"})
        return Response(content=content,
                        status_code=400,
                        media_type="application/json")

    body["data_hora_entrada"] = datetime.now()

    registros.append(body)
    return body