import { useEffect, useState } from 'react'
import { listEvents, register } from './api.js'

// Esta tela já tem a estrutura visual. Sua tarefa é ligá-la à API e ao estado React.
// Consulte docs/checkpoint-04.md antes de substituir os dados de exemplo.
export default function App() {
  // const example = { id: 0, title: 'Exemplo de evento', date: '2026-10-10', available_slots: 2 }
  const [userId, setUserId] = useState(1)
  const [events, setEvents] = useState(null)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [submittingId, setSubmittingId] = useState(null)

  useEffect(() => {
    listEvents()
      .then(setEvents)
      .catch(() => {
        setEvents([])
        setError('Não foi possível carregar os eventos.')
      })
  }, [])

  function handleRegister(eventId) {
  setSubmittingId(eventId)
  setError('')
  setSuccess('')
  register(eventId, userId)
    .then(() => listEvents())
    .then(list => {
      setEvents(list)
      setSuccess('Inscrição realizada com sucesso!')
    })
    .catch(err => setError(err.message))
    .then(() => setSubmittingId(null))
}

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

    {error && <p role="alert">{error}</p>}
    {success && <p role="status">{success}</p>}

    <section aria-label="Lista de eventos" className="events">
      {events === null && <p>Carregando eventos</p>}
      {events?.length === 0 && !error && <p>Nenhum evento disponível.</p>}
      {events?.map(event => (
        <article className="card" key={event.id}>
          <p className="date">{event.date}</p>
          <h2>{event.title}</h2>
          <p>
            {event.available_slots}{' '}
            {event.available_slots === 1 ? 'vaga disponível' : 'vagas disponíveis'}
          </p>
          <button
            type="button"
            disabled={submittingId === event.id || event.available_slots === 0}
            onClick={() => handleRegister(event.id)}
          >
            Inscrever-se
          </button>
        </article>
      ))}
    </section>
  </main>
}
