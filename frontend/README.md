# Kiwi Frontend

Modern frontend structure for the Kiwi SQL Generation Project.

## Quick Start

### Option 1: Run Demo (Fastest)

```bash
# From project root
python run_frontend_demo.py
```

Then visit: http://localhost:12000

### Option 2: Development Setup

1. Build frontend:
```bash
cd frontend
python build.py dev
```

2. Run with your Vanna instance:
```bash
from kiwi.flask_app.frontend_app import create_app
app = create_app(vn=your_vanna_instance)
app.run(host="0.0.0.0", port=8080)
```

## Directory Structure

```
frontend/
├── src/                    # Source files
│   ├── assets/            # Static assets
│   │   ├── css/          # Stylesheets
│   │   ├── js/           # JavaScript modules
│   │   ├── images/       # Images and icons
│   │   └── fonts/        # Font files
│   ├── templates/        # HTML templates
│   │   ├── base/         # Base templates
│   │   ├── chat/         # Chat interface
│   │   └── dashboard/    # Dashboard views
│   └── components/       # Reusable UI components
├── dist/                 # Built/compiled files
├── build/                # Build artifacts
├── package.json          # Node.js dependencies
├── vite.config.js        # Vite configuration
├── build.py              # Python build script
└── README.md            # This file
```

## Features

- 🎨 **Modern Design**: Clean, responsive interface
- 📱 **Mobile-Friendly**: Works on all devices
- ⚡ **Fast Loading**: Optimized assets and caching
- 🔧 **Component-Based**: Reusable UI components
- 📊 **Interactive Dashboard**: Real-time analytics
- 💬 **Enhanced Chat**: Streaming responses, syntax highlighting
- 🎯 **Accessible**: WCAG compliant
- 🔄 **Real-time Updates**: WebSocket support
- 📈 **Data Visualization**: Charts and graphs
- 🛡️ **Secure**: XSS protection and input validation

## Build Commands

```bash
# Development build (fast, unminified)
python build.py dev

# Production build (optimized, minified)
python build.py build

# Watch for changes (auto-rebuild)
python build.py watch

# Clean build directories
python build.py clean

# Use Vite (if Node.js is available)
npm run dev        # Development server
npm run build      # Production build
npm run preview    # Preview production build
```

## Templates

### Chat Interface (`chat/chat.html`)

Enhanced chat interface with:
- Real-time messaging with WebSocket support
- Streaming response handling
- Code syntax highlighting
- File upload and export
- Responsive design
- Accessibility features

### Dashboard (`dashboard/dashboard.html`)

Comprehensive dashboard featuring:
- Query analytics and metrics
- Interactive charts (Chart.js)
- System status monitoring
- Real-time updates
- Responsive grid layout

### Base Template (`base/index.html`)

Landing page with:
- Feature overview and navigation
- Responsive hero section
- Technology showcase

## Component System

### Creating Components

```javascript
// components/MyComponent.js
export class MyComponent {
  constructor(options = {}) {
    this.element = this.createElement();
  }
  
  createElement() {
    const element = document.createElement('div');
    element.className = 'my-component';
    return element;
  }
}
```

### Using Components

```javascript
import { Button, Modal } from './components/index.js';

// Programmatic usage
const button = new Button({
  text: 'Click me',
  type: 'primary',
  onClick: () => Modal.alert('Hello!')
});

// Auto-initialization via data attributes
<div data-component="button" data-button-text="Click me"></div>
```

## API Integration

```javascript
import { APIClient } from './modules/api.js';

const client = new APIClient();

// Send message
const response = await client.sendMessage('Show top customers');

// Stream response
const stream = await client.sendStreamingMessage('Generate complex query');

// Upload file
const result = await client.uploadFile(file);
```

## Styling

### CSS Variables

```css
:root {
  --primary-color: #007bff;
  --success-color: #28a745;
  --spacing-md: 1rem;
  --border-radius-md: 0.375rem;
}
```

### Utility Classes

```css
.d-flex { display: flex; }
.p-3 { padding: var(--spacing-md); }
.text-center { text-align: center; }
.text-primary { color: var(--primary-color); }
```

## Integration with Backend

### Flask Integration

```python
from kiwi.flask_app.frontend_app import create_app

app = create_app(vn=your_vanna_instance)
app.run(host="0.0.0.0", port=8080)
```

### FastAPI Integration

```python
from kiwi.frontend_integration import create_fastapi_integration

app = FastAPI()
create_fastapi_integration(app)
```

## Deployment

### Development

```bash
# Quick demo
python run_frontend_demo.py

# Custom setup
from kiwi.flask_app.frontend_app import create_app
app = create_app(vn=vanna_instance, debug=True)
app.run(host="0.0.0.0", port=8080)
```

### Production

1. **Build frontend**:
```bash
python frontend/build.py build
```

2. **Configure web server** (nginx example):
```nginx
location /static/frontend/ {
    alias /path/to/kiwi/frontend/dist/;
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

3. **Flask app**:
```python
app = create_app(vn=vanna_instance, debug=False)
app.run(host="0.0.0.0", port=8080)
```

## Browser Support

| Browser | Version | Status |
|---------|---------|--------|
| Chrome  | 90+     | ✅ Full |
| Firefox | 88+     | ✅ Full |
| Safari  | 14+     | ✅ Full |
| Edge    | 90+     | ✅ Full |

## Troubleshooting

### Common Issues

1. **Build fails**:
```bash
python frontend/build.py clean
python frontend/build.py dev
```

2. **Assets not loading**:
   - Check file paths in templates
   - Verify Flask static route configuration
   - Check browser console for 404 errors

3. **JavaScript errors**:
   - Check browser console
   - Verify module imports
   - Check for syntax errors

### Debug Mode

```python
# Enable debug mode
app = create_app(vn=vanna_instance, debug=True)

# Frontend rebuild endpoint (debug only)
POST /api/frontend/rebuild
```

## Contributing

### Code Style

- **JavaScript**: ES6+ modules, async/await
- **CSS**: BEM methodology, CSS variables
- **HTML**: Semantic markup, accessibility attributes
- **Python**: PEP 8, type hints

### Development Setup

```bash
# Clone repository
git clone https://github.com/carmhuo/kiwi.git
cd kiwi

# Setup frontend
cd frontend
python build.py dev

# Test changes
cd ..
python run_frontend_demo.py
```

## License

This project is licensed under the same license as the main Kiwi project.