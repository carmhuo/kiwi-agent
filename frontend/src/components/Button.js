// Button Component
export class Button {
  constructor(options = {}) {
    this.text = options.text || 'Button';
    this.type = options.type || 'primary';
    this.size = options.size || 'medium';
    this.disabled = options.disabled || false;
    this.onClick = options.onClick || (() => {});
    this.icon = options.icon || null;
    this.loading = options.loading || false;
    
    this.element = this.createElement();
  }

  createElement() {
    const button = document.createElement('button');
    button.className = this.getClasses();
    button.innerHTML = this.getContent();
    button.disabled = this.disabled || this.loading;
    
    button.addEventListener('click', (e) => {
      if (!this.disabled && !this.loading) {
        this.onClick(e);
      }
    });

    return button;
  }

  getClasses() {
    const classes = ['btn'];
    
    // Type classes
    switch (this.type) {
      case 'primary':
        classes.push('btn-primary');
        break;
      case 'secondary':
        classes.push('btn-secondary');
        break;
      case 'success':
        classes.push('btn-success');
        break;
      case 'warning':
        classes.push('btn-warning');
        break;
      case 'error':
        classes.push('btn-error');
        break;
      default:
        classes.push('btn-primary');
    }

    // Size classes
    switch (this.size) {
      case 'small':
        classes.push('btn-sm');
        break;
      case 'large':
        classes.push('btn-lg');
        break;
      case 'medium':
      default:
        // Default size, no additional class needed
        break;
    }

    // State classes
    if (this.disabled) classes.push('btn-disabled');
    if (this.loading) classes.push('btn-loading');

    return classes.join(' ');
  }

  getContent() {
    let content = '';
    
    if (this.loading) {
      content += '<span class="btn-spinner"></span>';
    } else if (this.icon) {
      content += `<span class="btn-icon">${this.icon}</span>`;
    }
    
    content += `<span class="btn-text">${this.text}</span>`;
    
    return content;
  }

  // Public methods
  setText(text) {
    this.text = text;
    this.element.innerHTML = this.getContent();
  }

  setLoading(loading) {
    this.loading = loading;
    this.element.disabled = this.disabled || loading;
    this.element.className = this.getClasses();
    this.element.innerHTML = this.getContent();
  }

  setDisabled(disabled) {
    this.disabled = disabled;
    this.element.disabled = disabled || this.loading;
    this.element.className = this.getClasses();
  }

  setType(type) {
    this.type = type;
    this.element.className = this.getClasses();
  }

  destroy() {
    if (this.element && this.element.parentNode) {
      this.element.parentNode.removeChild(this.element);
    }
  }

  // Static method to create button from existing element
  static fromElement(element, options = {}) {
    const button = new Button(options);
    
    // Copy attributes from existing element
    if (element.textContent) {
      button.text = element.textContent.trim();
    }
    
    if (element.disabled) {
      button.disabled = true;
    }

    // Replace existing element
    if (element.parentNode) {
      element.parentNode.replaceChild(button.element, element);
    }

    return button;
  }
}

// CSS for button component (to be included in main CSS)
export const ButtonCSS = `
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-lg);
  border: none;
  border-radius: var(--border-radius-md);
  font-family: inherit;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  line-height: 1;
  text-decoration: none;
  cursor: pointer;
  transition: all var(--transition-fast);
  position: relative;
  overflow: hidden;
}

.btn:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
}

.btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

/* Button Types */
.btn-primary {
  background-color: var(--primary-color);
  color: var(--white);
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-secondary {
  background-color: var(--white);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-secondary:hover:not(:disabled) {
  background-color: var(--light-gray);
  border-color: var(--primary-color);
}

.btn-success {
  background-color: var(--success-color);
  color: var(--white);
}

.btn-success:hover:not(:disabled) {
  background-color: #218838;
  transform: translateY(-1px);
}

.btn-warning {
  background-color: var(--warning-color);
  color: var(--black);
}

.btn-warning:hover:not(:disabled) {
  background-color: #e0a800;
  transform: translateY(-1px);
}

.btn-error {
  background-color: var(--error-color);
  color: var(--white);
}

.btn-error:hover:not(:disabled) {
  background-color: #c82333;
  transform: translateY(-1px);
}

/* Button Sizes */
.btn-sm {
  padding: var(--spacing-xs) var(--spacing-md);
  font-size: var(--font-size-sm);
}

.btn-lg {
  padding: var(--spacing-md) var(--spacing-xl);
  font-size: var(--font-size-lg);
}

/* Button States */
.btn-loading {
  pointer-events: none;
}

.btn-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.btn-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .btn {
    padding: var(--spacing-md) var(--spacing-lg);
  }
  
  .btn-sm {
    padding: var(--spacing-sm) var(--spacing-md);
  }
  
  .btn-lg {
    padding: var(--spacing-lg) var(--spacing-xl);
  }
}
`;