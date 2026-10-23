# Checkpoint 03 — Inscrever usuários pela API

## O problema

Sua API de eventos usa memória, e seus modelos relacionais já guardam eventos, usuários e inscrições. Agora faça esses dois lados trabalharem juntos. Ao terminar, a API lê e grava no SQLite e aceita inscrições quando há vaga.

Conclua os testes dos checkpoints anteriores antes de incorporar esta atualização.

## O que chegou nesta atualização

- `app/db_session.py` abre uma sessão SQLAlchemy por requisição e contém um exemplo de consulta.
- `app/registrations.py` define o contrato da nova rota, ainda sem a regra de negócio.
- `tests/test_integration.py` descreve persistência, inscrição e erros.

Nenhum desses arquivos substitui sua implementação anterior em `app/main.py` ou `app/models.py`.

## Comportamento esperado

Adapte `create_app` para aceitar opcionalmente uma URL SQLite. Cada instância criada sem URL deve ter dados isolados para os testes antigos. A aplicação iniciada pelo servidor deve usar o arquivo `events.db`, de modo que os eventos persistam após reinício. Consulte `make_engine` e `Base.metadata.create_all`.

As rotas `GET /events`, `GET /events/{id}` e `POST /events` devem usar os modelos do banco. Inclua `available_slots` nas respostas de eventos, calculado como `capacity - número de inscrições`.

Complete `POST /events/{event_id}/registrations` com `{"user_id": 1}`. Sucesso retorna **201** com `event_id` e `user_id`; evento ou usuário ausente retorna **404**; inscrição repetida ou evento lotado retorna **409**. Falhas não devem criar uma inscrição.

## Onde trabalhar

- **Leia:** `app/database.py`, `app/db_session.py`, `app/models.py`, `tests/test_integration.py`.
- **Altere:** sua implementação em `app/main.py` e a nova rota em `app/registrations.py`.
- **Preserve:** testes, seed, `app/database.py`, `app/db_session.py` e workflow.

## Caminho sugerido

1. Faça `create_app` criar um engine e tabelas e disponibilizar o engine para `get_session`.
2. Troque as rotas de eventos para usar o banco. Rode os testes antigos e o de persistência.
3. Inclua a rota de inscrições na aplicação e implemente uma verificação por vez.
4. Rode `uv run --locked python -m database.seed` para testar manualmente com o usuário `1`.
5. Rode `uv run --locked python scripts/check.py`, faça commit e push em `aluno`, confira o Actions.

## Dicas graduais

<details><summary>1. Por onde a sessão chega à rota?</summary>

O `get_session` usa o engine guardado em `request.app.state.engine`. O FastAPI entrega essa sessão por `Depends`.

</details>

<details><summary>2. Onde ficam as regras?</summary>

Uma chave estrangeira ou restrição única protege o banco. A aplicação também precisa consultar existência e vagas para devolver os erros HTTP definidos no contrato.

</details>

<details><summary>3. Quando atualizar as vagas?</summary>

Depois de gravar a inscrição, uma nova consulta deve encontrar uma inscrição a mais. A resposta de eventos calcula as vagas a partir do banco.

</details>

## Conclusão

Todos os testes acumulados passam localmente e no Actions do seu fork. Você consegue apontar onde a requisição entra, onde a regra de vagas é aplicada, onde a inscrição é gravada e de onde sai a resposta.
