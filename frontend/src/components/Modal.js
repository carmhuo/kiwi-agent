// Modal Component
export class Modal {
  constructor(options = {}) {
    this.title = options.title || '';
    this.content = options.content || '';
    this.size = options.size || 'medium'; // small, medium, large, fullscreen
    this.closable = options.closable !== false;
    this.backdrop = options.backdrop !== false;
    this.keyboard = options.keyboard !== false;
    this.onShow = options.onShow || (() => {});
    this.onHide = options.onHide || (() => {});
    this.onConfirm = options.onConfirm || null;
    this.onCancel = options.onCancel || null;
    
    this.isVisible = false;
    this.element = this.createElement();
    
    this.bindEvents();
  }

  createElement() {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.style.display = 'none';
    modal.innerHTML = this.getModalHTML();
    
    document.body.appendChild(modal);
    return modal;
  }

  getModalHTML() {
    const sizeClass = this.size !== 'medium' ? `modal-${this.size}` : '';
    
    return `
      <div class="modal-backdrop"></div>
      <div class="modal-dialog ${sizeClass}">
        <div class="modal-content">
          ${this.title ? `
            <div class="modal-header">
              <h3 class="modal-title">${this.title}</h3>
              ${this.closable ? '<button class="modal-close" type="button">&times;</button>' : ''}
            </div>
          ` : ''}
          <div class="modal-body">
            ${this.content}
          </div>
          ${this.onConfirm || this.onCancel ? `
            <div class="modal-footer">
              ${this.onCancel ? '<button class="btn btn-secondary modal-cancel">Cancel</button>' : ''}
              ${this.onConfirm ? '<button class="btn btn-primary modal-confirm">Confirm</button>' : ''}
            </div>
          ` : ''}
        </div>
      </div>
    `;
  }

  bindEvents() {
    // Close button
    if (this.closable) {
      const closeBtn = this.element.querySelector('.modal-close');
      if (closeBtn) {
        closeBtn.addEventListener('click', () => this.hide());
      }
    }

    // Backdrop click
    if (this.backdrop) {
      const backdrop = this.element.querySelector('.modal-backdrop');
      backdrop.addEventListener('click', () => this.hide());
    }

    // Keyboard events
    if (this.keyboard) {
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && this.isVisible) {
          this.hide();
        }
      });
    }

    // Action buttons
    const confirmBtn = this.element.querySelector('.modal-confirm');
    const cancelBtn = this.element.querySelector('.modal-cancel');
    
    if (confirmBtn && this.onConfirm) {
      confirmBtn.addEventListener('click', () => {
        const result = this.onConfirm();
        if (result !== false) {
          this.hide();
        }
      });
    }

    if (cancelBtn && this.onCancel) {
      cancelBtn.addEventListener('click', () => {
        const result = this.onCancel();
        if (result !== false) {
          this.hide();
        }
      });
    }
  }

  show() {
    if (this.isVisible) return;
    
    this.isVisible = true;
    this.element.style.display = 'flex';
    
    // Add animation class
    setTimeout(() => {
      this.element.classList.add('modal-show');
    }, 10);

    // Prevent body scroll
    document.body.style.overflow = 'hidden';
    
    // Focus management
    const firstFocusable = this.element.querySelector('button, input, textarea, select, [tabindex]:not([tabindex="-1"])');
    if (firstFocusable) {
      firstFocusable.focus();
    }

    this.onShow();
  }

  hide() {
    if (!this.isVisible) return;
    
    this.element.classList.remove('modal-show');
    
    setTimeout(() => {
      this.isVisible = false;
      this.element.style.display = 'none';
      document.body.style.overflow = '';
    }, 300);

    this.onHide();
  }

  setTitle(title) {
    this.title = title;
    const titleElement = this.element.querySelector('.modal-title');
    if (titleElement) {
      titleElement.textContent = title;
    }
  }

  setContent(content) {
    this.content = content;
    const bodyElement = this.element.querySelector('.modal-body');
    if (bodyElement) {
      bodyElement.innerHTML = content;
    }
  }

  setSize(size) {
    this.size = size;
    const dialog = this.element.querySelector('.modal-dialog');
    if (dialog) {
      // Remove existing size classes
      dialog.classList.remove('modal-small', 'modal-large', 'modal-fullscreen');
      
      // Add new size class
      if (size !== 'medium') {
        dialog.classList.add(`modal-${size}`);
      }
    }
  }

  destroy() {
    if (this.element && this.element.parentNode) {
      this.hide();
      setTimeout(() => {
        this.element.parentNode.removeChild(this.element);
      }, 300);
    }
  }

  // Static methods
  static alert(message, title = 'Alert') {
    return new Promise((resolve) => {
      const modal = new Modal({
        title,
        content: `<p>${message}</p>`,
        onConfirm: () => {
          resolve(true);
          modal.destroy();
        }
      });
      modal.show();
    });
  }

  static confirm(message, title = 'Confirm') {
    return new Promise((resolve) => {
      const modal = new Modal({
        title,
        content: `<p>${message}</p>`,
        onConfirm: () => {
          resolve(true);
          modal.destroy();
        },
        onCancel: () => {
          resolve(false);
          modal.destroy();
        }
      });
      modal.show();
    });
  }

  static prompt(message, defaultValue = '', title = 'Input') {
    return new Promise((resolve) => {
      const inputId = 'modal-prompt-input';
      const modal = new Modal({
        title,
        content: `
          <p>${message}</p>
          <input type="text" id="${inputId}" class="form-control" value="${defaultValue}" style="width: 100%; margin-top: 10px;">
        `,
        onConfirm: () => {
          const input = document.getElementById(inputId);
          resolve(input ? input.value : null);
          modal.destroy();
        },
        onCancel: () => {
          resolve(null);
          modal.destroy();
        }
      });
      modal.show();
      
      // Focus the input
      setTimeout(() => {
        const input = document.getElementById(inputId);
        if (input) {
          input.focus();
          input.select();
        }
      }, 100);
    });
  }
}

// CSS for modal component
export const ModalCSS = `
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.modal.modal-show {
  opacity: 1;
}

.modal-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(2px);
}

.modal-dialog {
  position: relative;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  transform: scale(0.9) translateY(-20px);
  transition: transform 0.3s ease;
}

.modal.modal-show .modal-dialog {
  transform: scale(1) translateY(0);
}

.modal-content {
  background-color: var(--white);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  max-height: 90vh;
}

.modal-header {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border-light);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-shrink: 0;
}

.modal-title {
  margin: 0;
  color: var(--text-primary);
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  color: var(--text-secondary);
  transition: all var(--transition-fast);
}

.modal-close:hover {
  background-color: var(--light-gray);
  color: var(--text-primary);
}

.modal-body {
  padding: var(--spacing-lg);
  overflow-y: auto;
  flex: 1;
}

.modal-footer {
  padding: var(--spacing-lg);
  border-top: 1px solid var(--border-light);
  display: flex;
  gap: var(--spacing-sm);
  justify-content: flex-end;
  flex-shrink: 0;
}

/* Modal Sizes */
.modal-small {
  max-width: 300px;
}

.modal-large {
  max-width: 800px;
}

.modal-fullscreen {
  max-width: 95vw;
  width: 95vw;
  max-height: 95vh;
  height: 95vh;
}

.modal-fullscreen .modal-content {
  height: 100%;
}

/* Form elements in modal */
.modal .form-control {
  width: 100%;
  padding: var(--spacing-sm);
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-base);
  transition: border-color var(--transition-fast);
}

.modal .form-control:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

/* Responsive */
@media (max-width: 768px) {
  .modal-dialog {
    width: 95%;
    margin: var(--spacing-md);
  }
  
  .modal-large,
  .modal-fullscreen {
    max-width: 95vw;
    width: 95vw;
  }
  
  .modal-header,
  .modal-body,
  .modal-footer {
    padding: var(--spacing-md);
  }
  
  .modal-footer {
    flex-direction: column;
  }
  
  .modal-footer .btn {
    width: 100%;
  }
}

/* Animation for modal content */
@keyframes modalSlideIn {
  from {
    transform: scale(0.9) translateY(-20px);
    opacity: 0;
  }
  to {
    transform: scale(1) translateY(0);
    opacity: 1;
  }
}

.modal.modal-show .modal-dialog {
  animation: modalSlideIn 0.3s ease;
}
`;