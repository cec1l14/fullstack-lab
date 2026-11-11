import { afterEach, expect, test, vi } from 'vitest'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import App from './App.jsx'

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
})

const event = { id: 1, title: 'Oficina de Web', date: '2026-10-10', capacity: 2, available_slots: 2 }
const response = (body, ok = true) => ({ ok, json: async () => body })

test('mostra carregamento e depois os eventos recebidos da API', async () => {
  let finish
  vi.stubGlobal('fetch', vi.fn(() => new Promise(resolve => { finish = resolve })))
  render(<App />)
  expect(screen.getByText(/carregando/i)).toBeInTheDocument()
  expect(fetch.mock.calls[0][0]).toBe('/api/events')
  finish(response([event]))
  expect(await screen.findByText('Oficina de Web')).toBeInTheDocument()
  expect(screen.getByText(/2 vagas/i)).toBeInTheDocument()
})

test('mostra lista vazia e erro de consulta', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValueOnce(response([])))
  const view = render(<App />)
  expect(await screen.findByText(/nenhum evento/i)).toBeInTheDocument()
  view.unmount()
  fetch.mockRejectedValueOnce(new Error('offline'))
  render(<App />)
  expect(await screen.findByRole('alert')).toHaveTextContent(/eventos/i)
})

test('inscreve o usuário, bloqueia clique repetido e atualiza vagas pelo servidor', async () => {
  let finishRegistration
  const fetchMock = vi.fn()
    .mockResolvedValueOnce(response([event]))
    .mockImplementationOnce(() => new Promise(resolve => { finishRegistration = resolve }))
    .mockResolvedValueOnce(response([{ ...event, available_slots: 1 }]))
  vi.stubGlobal('fetch', fetchMock)
  render(<App />)
  const button = await screen.findByRole('button', { name: /inscrever/i })
  fireEvent.change(screen.getByLabelText(/participante de demonstração/i), { target: { value: '2' } })
  fireEvent.click(button)
  expect(button).toBeDisabled()
  expect(fetchMock).toHaveBeenCalledTimes(2)
  expect(fetchMock).toHaveBeenNthCalledWith(2, '/api/events/1/registrations', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: 2 }),
  })
  finishRegistration(response({ event_id: 1, user_id: 2 }))
  expect(await screen.findByText(/1 vaga disponível/i)).toBeInTheDocument()
  expect(screen.getByRole('status')).toHaveTextContent(/inscrição realizada/i)
  expect(fetchMock).toHaveBeenCalledTimes(3)
})

test('não anuncia sucesso quando a inscrição falha', async () => {
  vi.stubGlobal('fetch', vi.fn()
    .mockResolvedValueOnce(response([event]))
    .mockResolvedValueOnce(response({ detail: 'Evento lotado' }, false)))
  render(<App />)
  fireEvent.click(await screen.findByRole('button', { name: /inscrever/i }))
  await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent(/evento lotado/i))
  expect(screen.queryByText(/inscrição realizada/i)).not.toBeInTheDocument()
  expect(fetch).toHaveBeenCalledTimes(2)
})
