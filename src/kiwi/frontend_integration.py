"""
Frontend Integration Module for Kiwi SQL Generation Project
Handles integration between the new frontend structure and Flask/FastAPI backends
"""

import os
import json
from pathlib import Path
from flask import Flask, render_template_string, send_from_directory, url_for

class FrontendIntegration:
    """Handles frontend integration for Flask and FastAPI applications"""
    
    def __init__(self, app=None, frontend_dir=None):
        self.app = app
        self.frontend_dir = Path(frontend_dir) if frontend_dir else self._find_frontend_dir()
        self.dist_dir = self.frontend_dir / 'dist'
        self.manifest = self._load_manifest()
        
        if app:
            self.init_app(app)
    
    def _find_frontend_dir(self):
        """Find the frontend directory relative to the current file"""
        current_dir = Path(__file__).parent
        # Go up to project root and find frontend directory
        project_root = current_dir.parent.parent.parent
        frontend_dir = project_root / 'frontend'
        
        if not frontend_dir.exists():
            raise FileNotFoundError(f"Frontend directory not found at {frontend_dir}")
        
        return frontend_dir
    
    def _load_manifest(self):
        """Load the frontend build manifest"""
        manifest_file = self.dist_dir / 'manifest.json'
        if manifest_file.exists():
            with open(manifest_file, 'r') as f:
                return json.load(f)
        return {}
    
    def init_app(self, app):
        """Initialize the Flask app with frontend integration"""
        self.app = app
        
        # Register static file routes
        self._register_static_routes()
        
        # Register template routes
        self._register_template_routes()
        
        # Add template globals
        self._add_template_globals()
    
    def _register_static_routes(self):
        """Register routes for serving static frontend assets"""
        
        @self.app.route('/static/frontend/<path:filename>')
        def frontend_static(filename):
            """Serve frontend static files"""
            return send_from_directory(self.dist_dir, filename)
        
        @self.app.route('/assets/<path:filename>')
        def frontend_assets(filename):
            """Serve frontend assets with shorter URL"""
            return send_from_directory(self.dist_dir / 'assets', filename)
    
    def _register_template_routes(self):
        """Register routes for frontend templates"""
        
        @self.app.route('/')
        def index():
            """Serve the main index page"""
            return self.render_template('base/index.html')
        
        @self.app.route('/chat')
        def chat():
            """Serve the chat interface"""
            return self.render_template('chat/chat.html')
        
        @self.app.route('/dashboard')
        def dashboard():
            """Serve the dashboard"""
            return self.render_template('dashboard/dashboard.html')
    
    def _add_template_globals(self):
        """Add global functions and variables to templates"""
        
        @self.app.template_global()
        def frontend_asset(asset_type, filename=None):
            """Get frontend asset URL"""
            if asset_type == 'css':
                if filename:
                    return url_for('frontend_static', filename=f'assets/css/{filename}')
                else:
                    # Return bundled CSS
                    return url_for('frontend_static', filename='assets/css/bundle.css')
            elif asset_type == 'js':
                if filename:
                    return url_for('frontend_static', filename=f'assets/js/{filename}')
                else:
                    # Return main JS
                    return url_for('frontend_static', filename='assets/js/main.js')
            elif asset_type == 'img':
                return url_for('frontend_static', filename=f'assets/images/{filename}')
            return ''
        
        @self.app.template_global()
        def frontend_version():
            """Get frontend version from manifest"""
            return self.manifest.get('version', '1.0.0')
    
    def render_template(self, template_path, **context):
        """Render a frontend template"""
        template_file = self.dist_dir / 'templates' / template_path
        
        if not template_file.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        with open(template_file, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Update asset paths for Flask
        template_content = self._update_template_paths(template_content)
        
        return render_template_string(template_content, **context)
    
    def _update_template_paths(self, content):
        """Update template paths for Flask URL routing"""
        # Update CSS paths
        content = content.replace(
            'href="/static/frontend/assets/css/',
            f'href="{url_for("frontend_static", filename="assets/css/", _external=False)}'
        )
        
        # Update JS paths
        content = content.replace(
            'src="/static/frontend/assets/js/',
            f'src="{url_for("frontend_static", filename="assets/js/", _external=False)}'
        )
        
        # Update image paths
        content = content.replace(
            'src="/static/frontend/assets/images/',
            f'src="{url_for("frontend_static", filename="assets/images/", _external=False)}'
        )
        
        return content
    
    def get_template_path(self, template_name):
        """Get the full path to a template file"""
        return self.dist_dir / 'templates' / template_name
    
    def list_templates(self):
        """List all available templates"""
        templates_dir = self.dist_dir / 'templates'
        if not templates_dir.exists():
            return []
        
        templates = []
        for template_file in templates_dir.rglob('*.html'):
            rel_path = template_file.relative_to(templates_dir)
            templates.append(str(rel_path))
        
        return templates
    
    def rebuild_frontend(self):
        """Trigger a frontend rebuild (development only)"""
        if self.app.debug:
            import subprocess
            try:
                subprocess.run([
                    'python', 
                    str(self.frontend_dir / 'build.py'), 
                    'dev'
                ], check=True)
                self.manifest = self._load_manifest()
                return True
            except subprocess.CalledProcessError:
                return False
        return False


class FastAPIIntegration:
    """FastAPI integration for the frontend"""
    
    def __init__(self, app=None, frontend_dir=None):
        self.app = app
        self.frontend_dir = Path(frontend_dir) if frontend_dir else self._find_frontend_dir()
        self.dist_dir = self.frontend_dir / 'dist'
        self.manifest = self._load_manifest()
        
        if app:
            self.init_app(app)
    
    def _find_frontend_dir(self):
        """Find the frontend directory relative to the current file"""
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent.parent
        frontend_dir = project_root / 'frontend'
        
        if not frontend_dir.exists():
            raise FileNotFoundError(f"Frontend directory not found at {frontend_dir}")
        
        return frontend_dir
    
    def _load_manifest(self):
        """Load the frontend build manifest"""
        manifest_file = self.dist_dir / 'manifest.json'
        if manifest_file.exists():
            with open(manifest_file, 'r') as f:
                return json.load(f)
        return {}
    
    def init_app(self, app):
        """Initialize FastAPI app with frontend integration"""
        from fastapi import FastAPI
        from fastapi.staticfiles import StaticFiles
        from fastapi.responses import FileResponse
        
        self.app = app
        
        # Mount static files
        app.mount("/static/frontend", StaticFiles(directory=str(self.dist_dir)), name="frontend")
        app.mount("/assets", StaticFiles(directory=str(self.dist_dir / "assets")), name="assets")
        
        # Add template routes
        self._register_routes()
    
    def _register_routes(self):
        """Register FastAPI routes for templates"""
        
        @self.app.get("/")
        async def index():
            """Serve the main index page"""
            return self.serve_template('base/index.html')
        
        @self.app.get("/chat")
        async def chat():
            """Serve the chat interface"""
            return self.serve_template('chat/chat.html')
        
        @self.app.get("/dashboard")
        async def dashboard():
            """Serve the dashboard"""
            return self.serve_template('dashboard/dashboard.html')
    
    def serve_template(self, template_path):
        """Serve a template file"""
        from fastapi.responses import FileResponse
        
        template_file = self.dist_dir / 'templates' / template_path
        
        if not template_file.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        return FileResponse(template_file, media_type='text/html')


def create_flask_integration(app, frontend_dir=None):
    """Create and configure Flask frontend integration"""
    integration = FrontendIntegration(app, frontend_dir)
    return integration


def create_fastapi_integration(app, frontend_dir=None):
    """Create and configure FastAPI frontend integration"""
    integration = FastAPIIntegration(app, frontend_dir)
    return integration


# Utility functions for template rendering
def render_chat_template(**context):
    """Render the chat template with context"""
    integration = FrontendIntegration()
    return integration.render_template('chat/chat.html', **context)


def render_dashboard_template(**context):
    """Render the dashboard template with context"""
    integration = FrontendIntegration()
    return integration.render_template('dashboard/dashboard.html', **context)


def get_frontend_assets():
    """Get list of frontend assets for manual inclusion"""
    integration = FrontendIntegration()
    return {
        'css': [
            '/static/frontend/assets/css/bundle.css'
        ],
        'js': [
            '/static/frontend/assets/js/main.js'
        ],
        'version': integration.manifest.get('version', '1.0.0')
    }