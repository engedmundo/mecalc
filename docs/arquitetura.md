# Arquitetura

## Visão em camadas

O projeto é dividido em camadas com dependências em **um único sentido**: as camadas de cima conhecem as de baixo, nunca o contrário.

```text
┌─────────────────────────────────────────────────────┐
│  app/  — Interface (Streamlit)                      │
│  Coleta entradas, chama o núcleo, exibe resultados  │
└──────────────┬────────────────────────┬─────────────┘
               │                        │
┌──────────────▼──────────┐  ┌──────────▼─────────────┐
│  data/  e  history/     │  │  Núcleo de cálculo     │
│  Consulta de referência │  │  strength/, fluids/... │
│  e histórico            │  │  Python puro           │
└──────────────┬──────────┘  └────────────────────────┘
               │
┌──────────────▼──────────┐
│  db/  — SQLAlchemy      │
│  Modelos, engine,       │
│  migrations (Alembic)   │
└─────────────────────────┘
```

**Regra fundamental:** o núcleo de cálculo **não depende** de banco de dados nem de interface. As funções recebem números e devolvem resultados. Com isso:

- os testes são simples e rápidos, sem banco envolvido;
- quem usa a biblioteca pode passar valores próprios (de um ensaio de laboratório, por exemplo);
- a interface pode ser trocada no futuro sem reescrever os cálculos.

## Estrutura de pastas

```text
calculadora_tecnica/
├── pyproject.toml              # dependências e metadados (uv)
├── README.md
├── LICENSE
├── CHANGELOG.md
├── src/mecalc/
│   ├── units.py                # registro de unidades (pint)
│   ├── report.py               # CalcReport: memorial de cálculo
│   ├── strength/               # resistência dos materiais
│   ├── machine_elements/       # elementos de máquinas
│   ├── fluids/                 # mecânica dos fluidos
│   ├── thermal/                # transferência de calor
│   ├── tolerances/             # ajustes ISO 286
│   ├── db/
│   │   ├── engine.py           # engine e sessão; URL via variável de ambiente
│   │   ├── models.py           # modelos ORM
│   │   └── migrations/         # Alembic
│   ├── data/
│   │   ├── sources/*.csv       # tabelas de referência (fonte da verdade)
│   │   ├── seed.py             # carga dos CSVs no banco
│   │   └── reference.py        # consultas; devolve dataclasses
│   └── history/
│       ├── base.py             # interface HistoryRepository
│       ├── session.py          # histórico em memória
│       └── sql.py              # histórico persistente (SQLAlchemy)
├── app/
│   ├── Home.py                 # página inicial
│   ├── pages/                  # uma página por cálculo
│   └── components/             # widgets reaproveitáveis
├── tests/                      # espelha a estrutura de src/mecalc
├── docs/                       # documentação (MkDocs Material)
└── .github/workflows/          # integração contínua
```
