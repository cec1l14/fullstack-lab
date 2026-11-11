# Checkpoint 04 — Inscrever pela interface

## O problema

Até aqui, uma pessoa precisava conhecer a API para ver eventos e fazer uma inscrição. Agora ela deve conseguir usar uma tela. Este checkpoint encerra as quatro atividades progressivas: ele consome a API e o banco que você já construiu, sem acessar SQLite pelo navegador.

Conclua os testes dos checkpoints anteriores antes de incorporar esta atualização.

## O que chegou nesta atualização

- `frontend/` contém uma aplicação React com layout, estilos e dois participantes de demonstração.
- `frontend/src/api.js` mostra como chamar a API. O Vite encaminha `/api` à FastAPI local; mantenha os dois servidores rodando para experimentar no navegador.
- `frontend/src/App.jsx` mostra dados fictícios e um botão sem ação. Este é o ponto principal de trabalho.
- `frontend/src/App.test.jsx` verifica o comportamento da tela. O comando completo de testes e o Actions agora incluem React.

Nenhum arquivo novo substitui sua implementação de backend. Ao fazer o merge, preserve o código que você já escreveu em `app/main.py`, `app/models.py` e `app/registrations.py`.

## Comportamento esperado

Ao abrir a página, busque `GET /events` e mostre um estado de carregamento até receber a resposta. Renderize os eventos reais com título, data e `available_slots`. Se a lista vier vazia, diga que não há eventos; se a busca falhar, mostre um erro visível.

Ao escolher um dos usuários de demonstração e clicar em **Inscrever-se**, envie `POST /events/{id}/registrations` com `{"user_id": 1}` ou `2`. Enquanto a requisição estiver pendente, desabilite o botão daquele evento para impedir outro envio. Se der certo, mostre confirmação e consulte `GET /events` novamente; a quantidade de vagas exibida deve vir dessa nova resposta. Se der erro, mostre a mensagem e não anuncie sucesso. Um evento sem vagas não deve oferecer uma ação ativa.

Exemplo: um evento com `available_slots: 2` aparece com **2 vagas disponíveis**. Após uma inscrição bem-sucedida, a nova lista pode trazer `available_slots: 1`; a tela passa a mostrar **1 vaga disponível**. Uma resposta `409` por evento lotado aparece como erro, sem mudar vagas localmente.

## Onde trabalhar

- **Leia:** `frontend/src/App.jsx`, `frontend/src/api.js`, `frontend/src/App.test.jsx` e o [README](../README.md).
- **Altere:** `frontend/src/App.jsx`. É permitido ajustar `frontend/src/style.css` se a sua solução precisar de uma pequena mudança visual.
- **Preserve:** testes, API, banco, seed, `frontend/src/api.js` e workflow.

## Caminho sugerido

1. Instale as dependências com `npm ci --prefix frontend` e rode `uv run --locked python scripts/check.py` para ver as falhas novas.
2. Use `useEffect` para carregar eventos e `useState` para guardar lista, carregamento e erro. Substitua o cartão fictício por um `map`.
3. Ligue o botão a `register(id, userId)` e guarde qual evento está enviando. Evite uma segunda chamada enquanto a primeira está pendente.
4. Após sucesso, chame `listEvents()` de novo antes de mostrar a nova quantidade de vagas.
5. Rode `uv run --locked python -m database.seed`, inicie backend e frontend em terminais separados e tente se inscrever no navegador.
6. Rode `uv run --locked python scripts/check.py`, faça commit e push em `aluno`, confira o Actions.

## Dicas graduais

<details><summary>1. Onde os dados ficam?</summary>

`listEvents()` devolve a lista da API. Guarde-a em estado React. Durante a busca, mostre um texto de carregamento; uma lista vazia deve ter mensagem própria.

</details>

<details><summary>2. Como distinguir um erro HTTP?</summary>

As funções de `api.js` lançam `Error` quando a resposta não é de sucesso. Use `try/catch`, apresente `error.message` e mantenha a tela utilizável.

</details>

<details><summary>3. De onde vêm as vagas após a inscrição?</summary>

Chame `listEvents()` depois de `register(...)` e substitua a lista pelo resultado. Não subtraia uma vaga somente no estado local: o servidor guarda a quantidade real.

</details>

## Conclusão

Os testes Python e React passam com `uv run --locked python scripts/check.py`, o Actions do seu fork está verde no último commit de `aluno`, e você consegue explicar o percurso clique → chamada HTTP → regra do backend → banco → nova resposta → tela.
