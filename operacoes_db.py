import model
from engine import get_db
import datetime

db = next(get_db())


def insert_ameaca(
    tid: int,
    stamp_added: datetime.date,
    threat: str,
    category: str,
    risk: str,
    description: str,
    wikisummary: str,
    wikireference: str,
    retired: str,
    stamp_updated: datetime.date,
    stamp_seen: datetime.date,
    stamp_retired: datetime.date,
):
    ameaca = model.Ameacas(
        tid=tid,
        hora_adicionado=stamp_added,
        nome=threat,
        categoria=category,
        risco=risk,
        descricao=description,
        wiki_sumario=wikisummary,
        wiki_link=wikireference,
        descontinuado=retired,
        hora_atualizado=stamp_updated,
        hora_visto=stamp_seen,
        hora_descontinuado=stamp_retired,
    )
    if not db.query(model.Ameacas).filter(model.Ameacas.tid == tid).all():
        db.add(ameaca)
        db.commit()
        db.refresh(ameaca)


def insert_atributos(
    atid: int,
    tid: int,
    tipo: str,
    descricao: str,
):
    atributo = model.Atributos(
        atid=atid,
        tid=tid,
        categoria=tipo,
        descricao=descricao,
    )

    db.add(atributo)
    db.commit()
    db.refresh(atributo)


def insert_novidades(
    nid: int,
    tid: int,
    title: str,
    channel: str,
    icon: str,
    link: str,
    stamp: datetime.date,
):
    novidade = model.Novidades(
        nid=nid,
        tid=tid,
        titulo=title,
        canal=channel,
        icone=icon,
        link=link,
        hora_adicionado=stamp,
    )

    db.add(novidade)
    db.commit()
    db.refresh(novidade)


def insert_outrosnomes(
    onid: int,
    tid: int,
    nome: str,
):
    outrosnomes = model.Outrosnomes(
        onid=onid,
        tid=tid,
        nomes=nome,
    )

    db.add(outrosnomes)
    db.commit()
    db.refresh(outrosnomes)


def insert_relacionados(
    relid: int,
    tid: int,
    nome: str,
    category: str,
    risk: str,
    stamp_linked: datetime.date,
):
    relacionado = model.Relacionados(
        relid=relid,
        tid=tid,
        nome=nome,
        categoria=category,
        risco=risk,
        hora_link=stamp_linked,
    )

    db.add(relacionado)
    db.commit()
    db.refresh(relacionado)


def insert_TaticasETecnicas(
    ttpsid: int,
    tid: int,
    tipo: str,
    descricao: str,
):
    ttps = model.TaticasETecnicas(
        ttpsid=ttpsid,
        tid=tid,
        categoria=tipo,
        descricao=descricao,
    )

    db.add(ttps)
    db.commit()
    db.refresh(ttps)
