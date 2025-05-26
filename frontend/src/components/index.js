// Component exports
export { Button, ButtonCSS } from './Button.js';
export { Modal, ModalCSS } from './Modal.js';

// Component CSS aggregator
export const ComponentsCSS = `
/* Button Component Styles */
${ButtonCSS}

/* Modal Component Styles */
${ModalCSS}

/* Additional component utilities */
.component-loading {
  opacity: 0.6;
  pointer-events: none;
  position: relative;
}

.component-loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  margin: -10px 0 0 -10px;
  border: 2px solid var(--primary-color);
  border-radius: 50%;
  border-top-color: transparent;
  animation: componentSpin 1s linear infinite;
  z-index: 1000;
}

@keyframes componentSpin {
  to {
    transform: rotate(360deg);
  }
}

/* Component animations */
.component-fade-in {
  animation: componentFadeIn 0.3s ease-out;
}

.component-slide-in {
  animation: componentSlideIn 0.3s ease-out;
}

@keyframes componentFadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes componentSlideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Component responsive utilities */
.component-mobile-hidden {
  display: block;
}

.component-desktop-hidden {
  display: none;
}

@media (max-width: 768px) {
  .component-mobile-hidden {
    display: none;
  }
  
  .component-desktop-hidden {
    display: block;
  }
}
`;

// Component manager for easy initialization
export class ComponentManager {
  constructor() {
    this.components = new Map();
    this.initialized = false;
  }

  init() {
    if (this.initialized) return;
    
    // Inject component CSS
    this.injectCSS();
    
    // Auto-initialize components from data attributes
    this.autoInitialize();
    
    this.initialized = true;
  }

  injectCSS() {
    const existingStyle = document.getElementById('components-css');
    if (existingStyle) return;

    const style = document.createElement('style');
    style.id = 'components-css';
    style.textContent = ComponentsCSS;
    document.head.appendChild(style);
  }

  autoInitialize() {
    // Auto-initialize buttons
    document.querySelectorAll('[data-component="button"]').forEach(element => {
      const options = this.parseDataAttributes(element, 'button');
      const button = Button.fromElement(element, options);
      this.register(element.id || this.generateId(), button);
    });

    // Auto-initialize modals
    document.querySelectorAll('[data-component="modal"]').forEach(element => {
      const options = this.parseDataAttributes(element, 'modal');
      const modal = new Modal(options);
      this.register(element.id || this.generateId(), modal);
    });
  }

  parseDataAttributes(element, componentType) {
    const options = {};
    const prefix = `data-${componentType}-`;
    
    Array.from(element.attributes).forEach(attr => {
      if (attr.name.startsWith(prefix)) {
        const key = attr.name.substring(prefix.length).replace(/-([a-z])/g, (g) => g[1].toUpperCase());
        let value = attr.value;
        
        // Try to parse as JSON, fallback to string
        try {
          value = JSON.parse(value);
        } catch (e) {
          // Keep as string
        }
        
        options[key] = value;
      }
    });

    return options;
  }

  register(id, component) {
    this.components.set(id, component);
  }

  get(id) {
    return this.components.get(id);
  }

  destroy(id) {
    const component = this.components.get(id);
    if (component && typeof component.destroy === 'function') {
      component.destroy();
    }
    this.components.delete(id);
  }

  destroyAll() {
    this.components.forEach((component, id) => {
      this.destroy(id);
    });
  }

  generateId() {
    return 'component-' + Math.random().toString(36).substr(2, 9);
  }
}

// Global component manager instance
export const componentManager = new ComponentManager();

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => componentManager.init());
} else {
  componentManager.init();
}