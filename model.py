from typing import List, Optional

from sqlalchemy import (
    Date,
    ForeignKeyConstraint,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class Ameacas(Base):
    __tablename__ = "ameacas"
    __table_args__ = (PrimaryKeyConstraint("tid", name="ameacas_pkey"),)

    tid = mapped_column(Integer)
    hora_adicionado = mapped_column(Date, nullable=False)
    nome = mapped_column(String(70))
    categoria = mapped_column(String(20))
    risco = mapped_column(String(20))
    descricao = mapped_column(Text)
    wiki_sumario = mapped_column(Text)
    wiki_link = mapped_column(String(100))
    descontinuado = mapped_column(String(30))
    hora_atualizado = mapped_column(Date)
    hora_visto = mapped_column(Date)
    hora_descontinuado = mapped_column(Date)

    atributos: Mapped[List["Atributos"]] = relationship(
        "Atributos", uselist=True, back_populates="ameacas"
    )
    novidades: Mapped[List["Novidades"]] = relationship(
        "Novidades", uselist=True, back_populates="ameacas"
    )
    outrosnomes: Mapped[List["Outrosnomes"]] = relationship(
        "Outrosnomes", uselist=True, back_populates="ameacas"
    )
    relacionados: Mapped[List["Relacionados"]] = relationship(
        "Relacionados", uselist=True, back_populates="ameacas"
    )
    taticas_e_tecnicas: Mapped[List["TaticasETecnicas"]] = relationship(
        "TaticasETecnicas", uselist=True, back_populates="ameacas"
    )


class Atributos(Base):
    __tablename__ = "atributos"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tid"], ["ameacas.tid"], ondelete="CASCADE", name="atributos_tid_fkey"
        ),
        PrimaryKeyConstraint("atid", "tid", name="atributos_pkey"),
    )

    atid = mapped_column(Integer, nullable=False)
    tid = mapped_column(Integer, nullable=False)
    categoria = mapped_column(String(20))
    descricao = mapped_column(String(100))

    ameacas: Mapped["Ameacas"] = relationship("Ameacas", back_populates="atributos")


class Novidades(Base):
    __tablename__ = "novidades"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tid"], ["ameacas.tid"], ondelete="CASCADE", name="novidades_tid_fkey"
        ),
        PrimaryKeyConstraint("nid", name="novidades_pkey"),
    )

    nid = mapped_column(Integer)
    tid = mapped_column(Integer, nullable=False)
    titulo = mapped_column(Text)
    canal = mapped_column(String(100))
    icone = mapped_column(Text)
    link = mapped_column(Text)
    hora_adicionado = mapped_column(Date)

    ameacas: Mapped["Ameacas"] = relationship("Ameacas", back_populates="novidades")


class Outrosnomes(Base):
    __tablename__ = "outrosnomes"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tid"], ["ameacas.tid"], ondelete="CASCADE", name="outrosnomes_tid_fkey"
        ),
        PrimaryKeyConstraint("onid", "tid", name="outrosnomes_pkey"),
    )

    onid = mapped_column(Integer, nullable=False)
    tid = mapped_column(Integer, nullable=False)
    nomes = mapped_column(String(75))

    ameacas: Mapped["Ameacas"] = relationship("Ameacas", back_populates="outrosnomes")


class Relacionados(Base):
    __tablename__ = "relacionados"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tid"], ["ameacas.tid"], ondelete="CASCADE", name="relacionados_tid_fkey"
        ),
        PrimaryKeyConstraint("relid", "tid", name="relacionados_pkey"),
    )

    relid = mapped_column(Integer, nullable=False)
    tid = mapped_column(Integer, nullable=False)
    nome = mapped_column(String(50))
    categoria = mapped_column(String(20))
    risco = mapped_column(String(20))
    hora_link = mapped_column(Date)

    ameacas: Mapped["Ameacas"] = relationship("Ameacas", back_populates="relacionados")


class TaticasETecnicas(Base):
    __tablename__ = "taticas_e_tecnicas"
    __table_args__ = (
        ForeignKeyConstraint(
            ["tid"], ["ameacas.tid"], ondelete="CASCADE", name="ttps_tid_fkey"
        ),
        PrimaryKeyConstraint("ttpsid", name="ttps_pkey"),
    )

    ttpsid = mapped_column(Integer)
    categoria = mapped_column(String(50))
    descricao = mapped_column(String(75))
    tid = mapped_column(Integer)

    ameacas: Mapped[Optional["Ameacas"]] = relationship(
        "Ameacas", back_populates="taticas_e_tecnicas"
    )
