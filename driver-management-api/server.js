const http = require('http')
const url = require('url')

let users = [
  { id: 1, username: 'admin', email: 'admin@example.com', role: 'superadmin', is_active: true, created_at: new Date().toISOString() },
  { id: 2, username: 'ops', email: 'ops@example.com', role: 'manager', is_active: true, created_at: new Date().toISOString() },
  { id: 3, username: 'driver1', email: 'driver1@example.com', role: 'driver', is_active: true, created_at: new Date().toISOString() },
  { id: 4, username: 'auditor', email: 'auditor@example.com', role: 'auditor', is_active: true, created_at: new Date().toISOString() },
]

let sessions = [
  { id: 's1', device: 'Chrome Windows', ip: '127.0.0.1', created_at: new Date().toISOString(), last_active_at: new Date().toISOString() },
]

let auditLogs = []
let auditAlerts = []
let tasks = [
  { id: 101, customer: 'ACME', status: 'draft' },
  { id: 102, customer: 'Globex', status: 'onroad' },
]

function send(res, status, data, headers = {}) {
  const body = typeof data === 'string' ? data : JSON.stringify(data)
  res.writeHead(status, { 'Content-Type': 'application/json', ...headers })
  res.end(body)
}

function parseBody(req) {
  return new Promise((resolve) => {
    let data = ''
    req.on('data', (chunk) => (data += chunk))
    req.on('end', () => {
      try {
        resolve(data ? JSON.parse(data) : {})
      } catch {
        resolve({})
      }
    })
  })
}

function toCSV(rows) {
  if (!rows.length) return 'id,action,actor,resource,resource_id,created_at\n'
  const header = ['id','action','actor_name','resource','resource_id','created_at']
  const lines = [header.join(',')]
  for (const r of rows) {
    lines.push([r.id, r.action, r.actor_name || '', r.resource || '', r.resource_id || '', r.created_at || ''].join(','))
  }
  return lines.join('\n')
}

const server = http.createServer(async (req, res) => {
  const parsed = url.parse(req.url, true)
  const path = parsed.pathname || ''
  const method = req.method || 'GET'

  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*')
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  if (method === 'OPTIONS') return res.end()

  // Auth
  if (path === '/api/v1/auth/login' && method === 'POST') {
    const body = await parseBody(req)
    const user = users.find(u => u.username === (body.username || 'admin')) || users[0]
    return send(res, 200, { token: 'devtoken', user, expires_in: 3600 })
  }
  if (path === '/api/v1/auth/me' && method === 'GET') {
    return send(res, 200, { user: users[0] })
  }
  if (path === '/api/v1/auth' && method === 'GET') {
    return send(res, 200, users)
  }
  if (path.startsWith('/api/v1/auth/') && method === 'PUT') {
    const id = Number(path.split('/').pop())
    const body = await parseBody(req)
    const u = users.find(x => x.id === id)
    if (!u) return send(res, 404, { message: 'not found' })
    if (body.role) u.role = body.role
    return send(res, 200, u)
  }
  if (path === '/api/v1/auth/sessions' && method === 'GET') {
    return send(res, 200, sessions)
  }
  if (path === '/api/v1/auth/revoke-session' && method === 'POST') {
    const body = await parseBody(req)
    sessions = sessions.filter(s => s.id !== body.session_id)
    return send(res, 200, { message: 'revoked' })
  }

  // Audit
  if (path === '/api/v1/audit/logs' && method === 'GET') {
    const { format } = parsed.query
    if (format === 'csv') {
      const csv = toCSV(auditLogs)
      res.writeHead(200, { 'Content-Type': 'text/csv' })
      return res.end(csv)
    }
    return send(res, 200, auditLogs)
  }
  if (path === '/api/v1/audit/logs' && method === 'POST') {
    const body = await parseBody(req)
    const id = (auditLogs.slice(-1)[0]?.id || 0) + 1
    const item = { id, created_at: new Date().toISOString(), ...body }
    auditLogs.push(item)
    return send(res, 200, { id })
  }
  if (path === '/api/v1/audit/alerts' && method === 'POST') {
    const body = await parseBody(req)
    const id = (auditAlerts.slice(-1)[0]?.id || 0) + 1
    const item = { id, created_at: new Date().toISOString(), ...body }
    auditAlerts.push(item)
    return send(res, 200, { id })
  }

  // Tasks
  if (path === '/api/v1/tasks' && method === 'GET') {
    const { status } = parsed.query
    const list = status ? tasks.filter(t => t.status === status) : tasks
    return send(res, 200, list)
  }
  if (path.startsWith('/api/v1/tasks/') && method === 'GET') {
    const id = Number(path.split('/').pop())
    const t = tasks.find(x => x.id === id)
    return send(res, 200, t || { id, status: 'draft' })
  }

  send(res, 404, { message: 'not found' })
})

server.listen(8000, () => {
  console.log('API server listening on http://localhost:8000/api/v1')
})