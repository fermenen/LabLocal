// Carga dinámica de dependencias de renderizado
function _loadScript(src) {
  return new Promise((resolve, reject) => {
    const s = document.createElement('script')
    s.src = src
    s.onload = resolve
    s.onerror = reject
    document.head.appendChild(s)
  })
}
Promise.all([
  _loadScript('https://cdn.jsdelivr.net/npm/marked/marked.min.js'),
  _loadScript('https://cdn.jsdelivr.net/npm/dompurify@2.4.0/dist/purify.min.js'),
]).catch(e => console.warn('ai_chat: error cargando dependencias de markdown', e))

// AI chat logic extracted from template — reads CSRF from cookie
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

const AI_CSRF = getCookie('csrftoken') || '';

function aiChat() {
  return {
    view: 'home',
    conversations: [],
    conversationsLoaded: false,
    activeConv: null,
    messages: [],
    input: '',
    loading: false,
    loadingMsgs: false,
    sending: false,
    streamingText: '',

    jsonHeaders() {
      return { 'Content-Type': 'application/json', 'X-CSRFToken': AI_CSRF }
    },

    async init() {
      this.$watch('$store.aiPanel.open', val => {
        if (val) this.onPanelOpen()
        this.updateHash()
      })
      // react to hash changes (back/forward navigation)
      window.addEventListener('hashchange', () => this.handleHashChange())
      // on load, apply current hash
      this.handleHashChange()
    },

    updateHash() {
      try {
        if (!$store || !$store.aiPanel) return
      } catch (e) {}
      // If panel is closed, clear hash
      const panelOpen = (window.Alpine && Alpine.store && Alpine.store('aiPanel') && Alpine.store('aiPanel').open) || false
      if (!panelOpen) {
        if (location.hash) location.hash = ''
        return
      }

      if (this.view === 'home') {
        if (location.hash !== '#chats') location.hash = '#chats'
        return
      }

      if (this.view === 'conversation' && this.activeConv && this.activeConv.id) {
        const h = `#conversation/${this.activeConv.id}`
        if (location.hash !== h) location.hash = h
      }
    },

    handleHashChange() {
      const h = (location.hash || '').replace(/^#/, '')
      if (!h) {
        // close panel
        if (window.Alpine && Alpine.store) Alpine.store('aiPanel').setOpen(false)
        return
      }

      const parts = h.split('/')
      if (parts[0] === 'chats') {
        if (window.Alpine && Alpine.store) Alpine.store('aiPanel').setOpen(true)
        this.view = 'home'
        // load conversations if needed
        this.loadConversations()
        return
      }

      if (parts[0] === 'conversation' && parts[1]) {
        const id = parts[1]
        if (window.Alpine && Alpine.store) Alpine.store('aiPanel').setOpen(true)
        this.view = 'conversation'
        // try to open existing conv or fetch messages by id
        const found = this.conversations.find(c => String(c.id) === String(id))
        if (found) {
          this.openConversation(found)
        } else {
          this.openConversationById(id)
        }
        return
      }
    },

    async openConversationById(id) {
      this.activeConv = { id }
      this.view = 'conversation'
      this.messages = []
      this.loadingMsgs = true
      try {
        const r = await fetch(`/ai/conversations/${id}/messages/`, { headers: this.jsonHeaders() })
        if (!r.ok) throw new Error(r.status)
        const data = await r.json()
        this.messages = data.items || []
        this.$nextTick(() => this.scrollBottom())
        this.updateHash()
      } catch(e) { console.error('openConversationById', e) }
      finally { this.loadingMsgs = false }
    },

    async onPanelOpen() {
      if (this.view === 'home') await this.loadConversations()
    },

    async loadConversations(force = false) {
      if (!force && this.conversationsLoaded) return
      if (this._loadingConversations) return
      this._loadingConversations = true
      console.debug('aiChat: loadConversations start', { force })
      this.loading = true
      try {
        const r = await fetch('/ai/conversations/', { headers: this.jsonHeaders() })
        if (!r.ok) throw new Error(r.status)
        const data = await r.json()
        this.conversations = (data.items || []).sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))
        this.conversationsLoaded = true
      } catch(e) { console.error('loadConversations', e) }
      finally { this.loading = false; this._loadingConversations = false; console.debug('aiChat: loadConversations end') }
    },

    async newConversation() {
      this.loading = true
      try {
        const r = await fetch('/ai/conversations/', {
          method: 'POST',
          headers: this.jsonHeaders(),
          body: JSON.stringify({ title: null }),
        })
        if (!r.ok) throw new Error(r.status)
        const conv = await r.json()
        this.activeConv = conv
        this.messages = []
        this.view = 'conversation'
        this.updateHash()
      } catch(e) { console.error('newConversation', e) }
      finally { this.loading = false }
    },

    async openConversation(conv) {
      this.activeConv = conv
      this.view = 'conversation'
      this.messages = []
      this.loadingMsgs = true
      try {
        const r = await fetch(`/ai/conversations/${conv.id}/messages/`, { headers: this.jsonHeaders() })
        if (!r.ok) throw new Error(r.status)
        const data = await r.json()
        this.messages = data.items || []
        this.$nextTick(() => this.scrollBottom())
        this.updateHash()
      } catch(e) { console.error('openConversation', e) }
      finally { this.loadingMsgs = false }
    },

    async sendMessage() {
      const text = this.input.trim()
      if (!text || this.sending) return

      if (this.view === 'home' || !this.activeConv) {
        await this.newConversation()
        if (!this.activeConv) return
      }

      this.input = ''
      this.sending = true
      this.streamingText = ''

      this.messages.push({ id: Date.now(), role: 'user', content: text })
      this.$nextTick(() => this.scrollBottom())

      try {
        const r = await fetch(`/ai/conversations/${this.activeConv.id}/messages/`, {
          method: 'POST',
          headers: this.jsonHeaders(),
          body: JSON.stringify({ content: text }),
        })
        if (!r.ok) throw new Error(r.status)

        const reader = r.body.getReader()
        const decoder = new TextDecoder()
        let buffer = ''
        let hadError = false

        while (true) {
          const { done, value } = await reader.read()
          if (done) break

          buffer += decoder.decode(value, { stream: true })
          const lines = buffer.split('\n')
          buffer = lines.pop()

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const chunk = line.slice(6)
                if (chunk.startsWith('{')) {
                // JSON final del evento — puede contener información o error
                try {
                  // If we have accumulated streamingText, flush it as a completed assistant message
                  if (this.streamingText && !hadError) {
                    this.messages.push({ id: Date.now() + 1, role: 'assistant', content: this.streamingText })
                    this.streamingText = ''
                    this.$nextTick(() => this.scrollBottom())
                  }

                  const obj = JSON.parse(chunk)
                  // Ignore normal completion messages like {"message":"Stream complete"}
                  const isStreamComplete = obj.message && /stream complete/i.test(String(obj.message))

                  if (isStreamComplete) {
                    // not an error — already flushed streaming text above
                    continue
                  }

                  // Determine if object represents an actual error
                  let detail = null
                  if (obj.type === 'error') detail = obj.detail || obj.error || obj.message || null
                  else if (obj.error) detail = obj.error
                  else if (obj.detail && /error/i.test(String(obj.detail))) detail = obj.detail
                  else if (obj.message && /error/i.test(String(obj.message))) detail = obj.message

                  if (detail) {
                    hadError = true
                    this.streamingText = ''
                    this.messages.push({ id: Date.now() + 1, role: 'assistant', content: String(detail), error: true })
                    this.$nextTick(() => this.scrollBottom())
                  }
                } catch(parseErr) {
                  // ignore parse errors and continue
                }
                continue
              }
              this.streamingText += chunk
              this.$nextTick(() => this.scrollBottom())
            }
          }
        }

        if (this.streamingText && !hadError) {
          this.messages.push({ id: Date.now() + 1, role: 'assistant', content: this.streamingText })
          this.streamingText = ''
          this.$nextTick(() => this.scrollBottom())
        }

      } catch(e) {
        console.error('sendMessage', e)
        this.streamingText = ''
        this.messages.push({ id: Date.now() + 1, role: 'assistant', content: 'Error al conectar con el servicio de IA.', error: true })
      } finally {
        this.sending = false
      }
    },

    backToHome() {
      this.view = 'home'
      this.activeConv = null
      this.messages = []
      this.streamingText = ''
      this.loadConversations(true)
      this.updateHash()
    },

    scrollBottom() {
      const el = this.$refs.msgList
      if (el) el.scrollTop = el.scrollHeight
    },

    greeting() {
      const h = new Date().getHours()
      if (h < 14) return 'Buenos días'
      if (h < 21) return 'Buenas tardes'
      return 'Buenas noches'
    },

    formatDate(iso) {
      if (!iso) return ''
      const d = new Date(iso)
      const date = d.toLocaleDateString('es-ES', { day: 'numeric', month: 'short' })
      const time = d.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })
      return `${date} · ${time}`
    },

    renderMessage(text) {
      if (!text && text !== 0) return ''
      try {
        // Normalize escaped unicode and other escape sequences coming from SSE
        let normalized = String(text)
        // Replace unicode escapes \\uXXXX
        normalized = normalized.replace(/\\u([0-9a-fA-F]{4})/g, function(match, grp) {
          return String.fromCharCode(parseInt(grp, 16))
        })
        // Common escaped sequences (\\n, \\t, \\r)
        normalized = normalized.replace(/\\n/g, '\\n').replace(/\\r/g, '\\r').replace(/\\t/g, '\\t')

        // Convert markdown to HTML and sanitize
        const raw = (typeof marked !== 'undefined') ? marked.parse(normalized) : normalized.replace(/\\n/g, '<br>')
        if (typeof DOMPurify !== 'undefined') return DOMPurify.sanitize(raw)
        return raw
      } catch (e) {
        return String(text).replace(/\\n/g, '<br>')
      }
    },
  }
}
