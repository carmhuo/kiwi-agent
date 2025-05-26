// Main JavaScript entry point
import { ChatInterface } from './modules/chat.js';
import { APIClient } from './modules/api.js';
import { Utils } from './modules/utils.js';
import { componentManager, Button, Modal } from '../components/index.js';

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  console.log('Kiwi Frontend initialized');
  
  // Initialize component system
  componentManager.init();
  
  // Initialize components based on page
  const currentPage = document.body.dataset.page;
  
  switch (currentPage) {
    case 'chat':
      initializeChatPage();
      break;
    case 'dashboard':
      initializeDashboardPage();
      break;
    default:
      initializeDefaultPage();
  }
});

function initializeChatPage() {
  const chatContainer = document.getElementById('chatContainer');
  if (chatContainer) {
    const apiClient = new APIClient();
    const chatInterface = new ChatInterface(chatContainer, apiClient);
    chatInterface.initialize();
  }
}

function initializeDashboardPage() {
  console.log('Dashboard page initialized');
  // Dashboard-specific initialization
}

function initializeDefaultPage() {
  console.log('Default page initialized');
  // Default page initialization
}

// Global error handler
window.addEventListener('error', function(event) {
  console.error('Global error:', event.error);
  Utils.showNotification('An unexpected error occurred', 'error');
});

// Global unhandled promise rejection handler
window.addEventListener('unhandledrejection', function(event) {
  console.error('Unhandled promise rejection:', event.reason);
  Utils.showNotification('An unexpected error occurred', 'error');
  event.preventDefault();
});

// Export for global access if needed
window.KiwiApp = {
  ChatInterface,
  APIClient,
  Utils,
  componentManager,
  Button,
  Modal
};