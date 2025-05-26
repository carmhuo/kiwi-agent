// API Client Module
export class APIClient {
  constructor(baseURL = '') {
    this.baseURL = baseURL;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
  }

  async sendMessage(message, options = {}) {
    const endpoint = options.endpoint || this.detectEndpoint();
    const url = `${this.baseURL}${endpoint}`;
    
    const requestBody = {
      messages: [{ role: 'user', content: message }],
      ...options.params
    };

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          ...this.defaultHeaders,
          'Accept': options.stream ? 'text/event-stream' : 'application/json',
          ...options.headers
        },
        body: JSON.stringify(requestBody)
      });

      if (!response.ok) {
        const errorData = await this.parseErrorResponse(response);
        throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
      }

      if (options.stream || response.headers.get('content-type')?.includes('text/event-stream')) {
        return { stream: response.body };
      } else {
        const data = await response.json();
        return data;
      }
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  async sendStreamingMessage(message, options = {}) {
    return this.sendMessage(message, { ...options, stream: true });
  }

  async querySQL(query, options = {}) {
    const endpoint = '/api/query';
    const url = `${this.baseURL}${endpoint}`;

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          ...this.defaultHeaders,
          ...options.headers
        },
        body: JSON.stringify({ query, ...options.params })
      });

      if (!response.ok) {
        const errorData = await this.parseErrorResponse(response);
        throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('SQL query failed:', error);
      throw error;
    }
  }

  async getSchema(options = {}) {
    const endpoint = '/api/schema';
    const url = `${this.baseURL}${endpoint}`;

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          ...this.defaultHeaders,
          ...options.headers
        }
      });

      if (!response.ok) {
        const errorData = await this.parseErrorResponse(response);
        throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Schema request failed:', error);
      throw error;
    }
  }

  async uploadFile(file, options = {}) {
    const endpoint = options.endpoint || '/api/upload';
    const url = `${this.baseURL}${endpoint}`;

    const formData = new FormData();
    formData.append('file', file);
    
    if (options.params) {
      Object.keys(options.params).forEach(key => {
        formData.append(key, options.params[key]);
      });
    }

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          // Don't set Content-Type for FormData, let browser set it
          ...options.headers
        },
        body: formData
      });

      if (!response.ok) {
        const errorData = await this.parseErrorResponse(response);
        throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('File upload failed:', error);
      throw error;
    }
  }

  async healthCheck() {
    const endpoint = '/api/health';
    const url = `${this.baseURL}${endpoint}`;

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: this.defaultHeaders
      });

      return {
        status: response.ok ? 'healthy' : 'unhealthy',
        statusCode: response.status,
        data: response.ok ? await response.json() : null
      };
    } catch (error) {
      return {
        status: 'error',
        error: error.message
      };
    }
  }

  detectEndpoint() {
    // Try to detect which backend is available
    const currentPath = window.location.pathname;
    
    // Check if we're on a FastAPI route
    if (currentPath.includes('/api/') || document.body.dataset.backend === 'fastapi') {
      return '/api/astream';
    }
    
    // Default to Flask route
    return '/chat';
  }

  async parseErrorResponse(response) {
    try {
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      } else {
        const text = await response.text();
        return { message: text || response.statusText };
      }
    } catch (error) {
      return { message: response.statusText || 'Unknown error' };
    }
  }

  setBaseURL(baseURL) {
    this.baseURL = baseURL;
  }

  setDefaultHeaders(headers) {
    this.defaultHeaders = { ...this.defaultHeaders, ...headers };
  }

  // Utility method for making custom requests
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const config = {
      method: 'GET',
      headers: this.defaultHeaders,
      ...options
    };

    if (config.body && typeof config.body === 'object' && !(config.body instanceof FormData)) {
      config.body = JSON.stringify(config.body);
    }

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData = await this.parseErrorResponse(response);
        throw new Error(errorData.message || `HTTP ${response.status}: ${response.statusText}`);
      }

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      } else {
        return await response.text();
      }
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }
}