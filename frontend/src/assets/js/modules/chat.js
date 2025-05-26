// Chat Interface Module
export class ChatInterface {
  constructor(container, apiClient) {
    this.container = container;
    this.apiClient = apiClient;
    this.messages = [];
    this.isLoading = false;
    
    // DOM elements
    this.messagesContainer = null;
    this.inputField = null;
    this.sendButton = null;
    this.loadingIndicator = null;
  }

  initialize() {
    this.setupDOM();
    this.bindEvents();
    this.addWelcomeMessage();
  }

  setupDOM() {
    // Get DOM elements
    this.messagesContainer = this.container.querySelector('#messages') || 
                           this.container.querySelector('.chat-messages');
    this.inputField = this.container.querySelector('#userInput') || 
                     this.container.querySelector('.chat-input');
    this.sendButton = this.container.querySelector('#sendButton') || 
                     this.container.querySelector('.chat-send-button');
    this.loadingIndicator = this.container.querySelector('#loadingIndicator') || 
                           this.container.querySelector('.loading-indicator');

    if (!this.messagesContainer || !this.inputField || !this.sendButton) {
      console.error('Required chat elements not found');
      return;
    }

    // Set up loading indicator if it doesn't exist
    if (!this.loadingIndicator) {
      this.loadingIndicator = this.createLoadingIndicator();
      this.container.appendChild(this.loadingIndicator);
    }
  }

  bindEvents() {
    // Send button click
    this.sendButton.addEventListener('click', () => this.sendMessage());
    
    // Enter key press
    this.inputField.addEventListener('keypress', (event) => {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        this.sendMessage();
      }
    });

    // Auto-resize textarea
    this.inputField.addEventListener('input', () => this.autoResizeInput());
  }

  async sendMessage() {
    const messageText = this.inputField.value.trim();
    if (!messageText || this.isLoading) return;

    // Add user message to UI
    this.addMessage(messageText, 'user');
    this.inputField.value = '';
    this.setLoading(true);

    try {
      // Send message to API
      const response = await this.apiClient.sendMessage(messageText);
      
      if (response.stream) {
        // Handle streaming response
        await this.handleStreamingResponse(response.stream);
      } else {
        // Handle regular response
        this.addMessage(response.content, 'assistant');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      this.addMessage(`Error: ${error.message}`, 'error');
    } finally {
      this.setLoading(false);
    }
  }

  async handleStreamingResponse(stream) {
    const assistantMessage = this.addMessage('', 'assistant', true);
    const contentElement = assistantMessage.querySelector('.message-content');
    
    try {
      const reader = stream.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        
        // Process complete events
        let position;
        while ((position = buffer.indexOf('\n\n')) >= 0) {
          const eventString = buffer.substring(0, position);
          buffer = buffer.substring(position + 2);

          if (eventString.startsWith('data: ')) {
            const jsonData = eventString.substring(6);
            try {
              const eventData = JSON.parse(jsonData);
              if (eventData.content) {
                contentElement.textContent += eventData.content;
                this.scrollToBottom();
              }
            } catch (e) {
              console.error('Error parsing streaming JSON:', e);
            }
          }
        }
      }
    } catch (error) {
      console.error('Streaming error:', error);
      contentElement.textContent += ` [Streaming error: ${error.message}]`;
    }
  }

  addMessage(content, type, isStreaming = false) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${type}`;
    
    const messageBubble = document.createElement('div');
    messageBubble.className = 'message-bubble';
    
    if (type !== 'error') {
      const authorElement = document.createElement('div');
      authorElement.className = 'message-author';
      authorElement.textContent = type === 'user' ? 'You' : 'Assistant';
      messageBubble.appendChild(authorElement);
    }
    
    const contentElement = document.createElement('div');
    contentElement.className = 'message-content';
    
    if (type === 'error') {
      messageBubble.className += ' error-message';
      contentElement.textContent = content;
    } else {
      contentElement.textContent = content;
    }
    
    messageBubble.appendChild(contentElement);
    messageElement.appendChild(messageBubble);
    
    this.messagesContainer.appendChild(messageElement);
    this.scrollToBottom();
    
    // Store message
    this.messages.push({ content, type, timestamp: new Date() });
    
    return messageElement;
  }

  addWelcomeMessage() {
    const welcomeText = "Hello! I'm your AI assistant for SQL generation. How can I help you today?";
    this.addMessage(welcomeText, 'assistant');
  }

  setLoading(loading) {
    this.isLoading = loading;
    this.sendButton.disabled = loading;
    
    if (this.loadingIndicator) {
      this.loadingIndicator.style.display = loading ? 'flex' : 'none';
    }
    
    if (loading) {
      this.sendButton.textContent = '...';
    } else {
      this.sendButton.textContent = 'Send';
    }
  }

  autoResizeInput() {
    this.inputField.style.height = 'auto';
    this.inputField.style.height = Math.min(this.inputField.scrollHeight, 120) + 'px';
  }

  scrollToBottom() {
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
  }

  createLoadingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'loading-indicator';
    indicator.style.display = 'none';
    indicator.innerHTML = `
      <span>AI is thinking</span>
      <div class="loading-dots">
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
        <div class="loading-dot"></div>
      </div>
    `;
    return indicator;
  }

  // Public methods for external control
  clearMessages() {
    this.messagesContainer.innerHTML = '';
    this.messages = [];
    this.addWelcomeMessage();
  }

  getMessages() {
    return [...this.messages];
  }

  setAPIClient(apiClient) {
    this.apiClient = apiClient;
  }
}