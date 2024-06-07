from time import sleep
import requests
import json
import operacoes_db
import model
from engine import get_db


def pegar_tid(a):
    return a.tid


def pegar_relid(a):
    return a.relid


def pegar_ameacas_nao_buscadas():
    ameacas = db.query(model.Ameacas).all()
    ameacas = list(map(pegar_tid, ameacas))
    relacionados = db.query(model.Relacionados).all()
    relacionados = list(map(pegar_relid, relacionados))
    return [item for item in relacionados if item not in ameacas]


def insert_no_banco(json_body):
    onid = (
        db.query(model.Outrosnomes).order_by(model.Outrosnomes.onid.desc()).first().onid
        + 1
        if db.query(model.Outrosnomes).order_by(model.Outrosnomes.onid.desc()).all()
        else 1
    )
    atid = (
        db.query(model.Atributos).order_by(model.Atributos.atid.desc()).first().atid + 1
        if db.query(model.Atributos).order_by(model.Atributos.atid.desc()).all()
        else 1
    )
    ttpsid = (
        db.query(model.TaticasETecnicas).order_by(model.TaticasETecnicas.ttpsid.desc()).first().ttpsid + 1
        if db.query(model.TaticasETecnicas).order_by(model.TaticasETecnicas.ttpsid.desc()).all()
        else 1
    )
    nid = (
        db.query(model.Novidades).order_by(model.Novidades.nid.desc()).first().nid + 1
        if db.query(model.Novidades).order_by(model.Novidades.nid.desc()).all()
        else 1
    )

    operacoes_db.insert_ameaca(
        tid=json_body["tid"],
        stamp_added=json_body["stamp_added"],
        threat=json_body["threat"],
        category=json_body["category"],
        risk=json_body["risk"],
        description=json_body["description"],
        wikisummary=json_body["wikisummary"],
        wikireference=json_body["wikireference"],
        retired=json_body["retired"],
        stamp_updated=json_body["stamp_updated"],
        stamp_seen=json_body["stamp_seen"],
        stamp_retired=json_body["stamp_retired"],
    )
    for othernames in json_body["othernames"]:
        operacoes_db.insert_outrosnomes(
            onid=onid,
            tid=json_body["tid"],
            nome=othernames,
        )
        onid += 1
    if len(json_body["attributes"]) > 0:
        for tipo, descricoes in json_body["attributes"].items():
            for descricao in descricoes:
                operacoes_db.insert_atributos(
                    atid=atid,
                    tid=json_body["tid"],
                    tipo=tipo,
                    descricao=descricao,
                )
                atid += 1
    if len(json_body["ttps"]) > 0:
        for tipo, descricoes in json_body["ttps"].items():
            for descricao in descricoes:
                operacoes_db.insert_TaticasETecnicas(
                    ttpsid=ttpsid,
                    tid=json_body["tid"],
                    tipo=tipo,
                    descricao=descricao,
                )
                ttpsid += 1
    for related in json_body["related"]:
        operacoes_db.insert_relacionados(
            tid=json_body["tid"],
            relid=related["tid"],
            category=related["category"],
            nome=related["name"],
            risk=related["risk"],
            stamp_linked=related["stamp_linked"],
        )
    if len(json_body["news"]) > 0:
        for news in json_body["news"]:
            operacoes_db.insert_novidades(
                nid=nid,
                tid=json_body["tid"],
                title=news["title"],
                channel=news["channel"],
                icon=news["icon"],
                stamp=news["stamp"],
                link=news["link"],
            )
            nid += 1


tokens = open("tokens.txt", "r").read().split("\n")
# X-Requests-Remaining-Second: 1
# X-Requests-Remaining-Day: 9
# X-Requests-Remaining-Month: 249
token = 0
# code 429 limit cached

db = next(get_db())
# i = 4#db.query(model.Ameacas).order_by(model.Ameacas.tid.desc()).first().tid + 1 if db.query(model.Ameacas).order_by(model.Ameacas.tid.desc()).all() else 1
i = int(open("tid.txt", "r").read())
while True:
    if i != 1 and db.query(model.Ameacas).filter(model.Ameacas.tid == i).first():
        i += 1
        continue
    ameacas_nao_buscadas = pegar_ameacas_nao_buscadas()
    if ameacas_nao_buscadas == []:
        threats_url = (
            f"https://pulsedive.com/api/info.php?tid={i}&pretty=1&key={tokens[token]}"
        )
        response = requests.get(threats_url)
        print(
            response.status_code,
            " - ",
            i - 1,
            " - day:",
            response.headers["X-Requests-Remaining-Day"],
            " - month:",
            response.headers["X-Requests-Remaining-Month"],
            " - token:",
            token,
            "error: " + json.loads(response.content)["error"]
            if "error" in json.loads(response.content).keys()
            else "ok",
        )
        i += 1
    else:
        threats_url = f"https://pulsedive.com/api/info.php?tid={ameacas_nao_buscadas[0]}&pretty=1&key={tokens[token]}"
        response = requests.get(threats_url)
        print(
            response.status_code,
            " - ",
            ameacas_nao_buscadas[0],
            " - i:",
            i,
            " - day:",
            response.headers["X-Requests-Remaining-Day"],
            " - month:",
            response.headers["X-Requests-Remaining-Month"],
            " - token:",
            token,
            "error: " + json.loads(response.content)["error"]
            if "error" in json.loads(response.content).keys()
            else "ok",
        )
    sleep(1)
    if response.status_code == 429:
        if len(tokens) - 1 == token:
            break
        i -= 1
        token += 1
    if response.status_code == 200:
        json_body = json.loads(response.content)
        insert_no_banco(json_body)

open("tid.txt", "w").write(str(i))
