import { useState } from 'react'
import { listEvents, register } from './api.js'

// Esta tela já tem a estrutura visual. Sua tarefa é ligá-la à API e ao estado React.
// Consulte docs/checkpoint-04.md antes de substituir os dados de exemplo.
export default function App() {
  const [userId, setUserId] = useState(1)
  const example = { id: 0, title: 'Exemplo de evento', date: '2026-10-10', available_slots: 2 }

  return <main className="page">
    <header>
      <p className="eyebrow">Trilha · Laboratório Full Stack</p>
      <h1>Eventos</h1>
      <p>Encontre uma atividade e garanta sua vaga.</p>
    </header>

    <label className="user-picker">Participante de demonstração
      <select value={userId} onChange={event => setUserId(Number(event.target.value))}>
        <option value="1">Pessoa 1</option>
        <option value="2">Pessoa 2</option>
      </select>
    </label>

    <section aria-label="Lista de eventos" className="events">
      <article className="card">
        <p className="date">{example.date}</p>
        <h2>{example.title}</h2>
        <p>{example.available_slots} vagas disponíveis</p>
        <button type="button">Inscrever-se</button>
      </article>
    </section>
  </main>
}
