# Checkpoint 02 — Modelar inscrições no banco

## O problema

A API da etapa anterior guarda eventos em memória. Agora o projeto precisa de um modelo persistente para eventos, usuários e inscrições. Nesta atividade você trabalha no banco; a API continuará em memória até o próximo checkpoint.

Antes de atualizar, conclua o Checkpoint 01 e confirme que os testes passaram no seu fork. Depois incorpore a atualização oficial conforme o README.

## Resultado esperado

O SQLite deve ter três tabelas: `events`, `users` e `registrations`. Cada inscrição liga um usuário a um evento. O mesmo usuário pode participar de eventos diferentes, mas não pode aparecer duas vezes no mesmo evento.

`events` tem `id`, `title`, `date` e `capacity`. `users` tem `id`, `name` e `email`. `registrations` tem `event_id` e `user_id` e pode ter um `id` próprio. A capacidade de um evento deve ser positiva. IDs usados em `registrations` devem existir nas tabelas relacionadas. A consulta em `database/participants.sql` recebe `:event_id` e devolve os nomes dos participantes em ordem alfabética.

## Onde trabalhar

- **Leia:** `app/database.py`, `app/models.py`, `database/seed.py`, `tests/test_database.py`.
- **Altere:** `app/models.py` e `database/participants.sql`.
- **Preserve:** testes, seed, `app/database.py` e workflow.

## Caminho sugerido

1. Desenhe as três tabelas e marque quais colunas são chaves primárias e estrangeiras.
2. Complete os modelos SQLAlchemy e execute `uv run --locked python scripts/check.py`.
3. Experimente criar o banco de exemplo com `uv run --locked python -m database.seed`.
4. Complete a consulta SQL e rode os testes acumulados novamente.
5. Faça commit, push na branch `aluno` e confira o Actions.

## Dicas graduais

<details><summary>1. Onde ficam as restrições?</summary>

`mapped_column` define colunas e chaves. Restrições que envolvem duas colunas podem ser definidas em `__table_args__`.

</details>

<details><summary>2. Como representar a inscrição?</summary>

`Registration` guarda `event_id` e `user_id`. Cada campo aponta para a tabela correspondente, e o par não pode se repetir.

</details>

<details><summary>3. Como listar os participantes?</summary>

A consulta precisa combinar `registrations` e `users` pelo ID do usuário, filtrar pelo ID do evento e ordenar pelo nome.

</details>

## Conclusão

Todos os testes antigos e novos devem passar localmente e no Actions. Confira no próprio banco o que acontece ao tentar inserir uma inscrição duplicada: a proteção deve existir nos dados, não apenas na API.
