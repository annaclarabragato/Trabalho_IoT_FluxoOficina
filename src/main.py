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


   #GET apresentando todos os registros

@app.get("/registros")
def listar ():
    return{"registros":registros}


 #patch

@app.patch("/registros/{placa}/finalizar")
async def finalizar(placa: str, request: Request):
    #recupera o body
    body = await request.body()
    #converte para dictionary
    body = dict(json.loads(body))

    #criando uma variável de controle
    registro_existe = None

    for registro in registros:
        if (registro.get("placa_veiculo") == placa):
            registro_existe = registro
            break

    if (not registro_existe):
        content = json.dumps({"mensagem": "Registro não existe"})
        return Response(content=content,
                        status_code=404,
                        media_type="application/json")

    #obtenho o horario
    peso_final = body.get("horario_final", 0)

    indice = registros.index(registro_existe)

    registros[indice]["data_hora_saida"] = datetime.now()

    return registros[indice]


#Deletando registros:
@app.delete("/registros/{placa}/excluir")
def excluir_registro(placa: str):
    registro_encontrado = None

    for registro in registros:
        if registro.get("placa_veiculo") == placa:
            registro_encontrado = registro
            break

    if not registro_encontrado:
        raise HTTPException(status_code=404, detail="Registro não encontrado")

    if "data_hora_saida" in registro_encontrado:
        raise HTTPException(status_code=400, detail="Registro já foi finalizado e não pode ser excluído")

    registros.remove(registro_encontrado)

    return {"mensagem": "Registro excluído com sucesso"}



# GET - apresentando todos os registros de veiculos que estão ainda em manutenção e não foram finalizados: 
@app.get("/registros/nao_finalizados")
def listar_nao_finalizados():
    registros_nao_finalizados = []
    for registro in registros:
        if registro.get("data_hora_saida") is None:
            registros_nao_finalizados.append(registro)

    return {"registros_nao_finalizados": registros_nao_finalizados}