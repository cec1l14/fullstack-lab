// O proxy do Vite encaminha /api para a FastAPI local, sem configurar CORS.
async function request(path, options) {
  const response = await fetch(`/api${path}`, options)
  const body = await response.json()
  if (!response.ok) throw new Error(body.detail || 'Não foi possível concluir a operação.')
  return body
}

export const listEvents = () => request('/events')

export const register = (eventId, userId) => request(`/events/${eventId}/registrations`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ user_id: userId }),
})
