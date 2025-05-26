"""
Enhanced Flask App with Modern Frontend Integration
Extends the existing VannaFlaskApp with the new frontend structure
"""

import os
from pathlib import Path
from flask import Flask, render_template_string, send_from_directory, url_for

from kiwi.flask_app import VannaFlaskApp
from kiwi.frontend_integration import FrontendIntegration


class KiwiFlaskApp(VannaFlaskApp):
    """Enhanced Flask app with modern frontend integration"""
    
    def __init__(self, *args, **kwargs):
        # Extract frontend-specific parameters
        self.frontend_dir = kwargs.pop('frontend_dir', None)
        self.use_modern_frontend = kwargs.pop('use_modern_frontend', True)
        
        # Initialize parent class
        super().__init__(*args, **kwargs)
        
        # Initialize frontend integration if enabled
        if self.use_modern_frontend:
            self.frontend_integration = FrontendIntegration(
                app=self.flask_app, 
                frontend_dir=self.frontend_dir
            )
            self._setup_modern_routes()
    
    def _setup_modern_routes(self):
        """Setup routes for the modern frontend"""
        
        # Override the default route to serve the new frontend
        @self.flask_app.route("/", defaults={"path": ""})
        @self.flask_app.route("/<path:path>")
        def serve_frontend(path: str):
            """Serve the modern frontend"""
            
            # Handle specific routes
            if path == "" or path == "index.html":
                return self.frontend_integration.render_template('base/index.html')
            elif path == "chat" or path == "chat.html":
                return self.frontend_integration.render_template('chat/chat.html')
            elif path == "dashboard" or path == "dashboard.html":
                return self.frontend_integration.render_template('dashboard/dashboard.html')
            
            # For other paths, try to serve from frontend first
            try:
                return self.frontend_integration.render_template(f'{path}')
            except FileNotFoundError:
                # Fall back to original behavior for API routes and other assets
                if path.startswith('api/'):
                    # Let Flask handle API routes normally
                    return super().hello(path)
                
                # For other files, try to serve as static assets
                try:
                    return send_from_directory(
                        self.frontend_integration.dist_dir, 
                        path
                    )
                except FileNotFoundError:
                    # Final fallback to original behavior
                    return super().hello(path)
        
        # Add a route for the legacy chat interface (for backward compatibility)
        @self.flask_app.route("/legacy-chat")
        def legacy_chat():
            """Serve the legacy chat interface"""
            return super().hello("")
        
        # Add API route for frontend rebuild (development only)
        @self.flask_app.route("/api/frontend/rebuild", methods=["POST"])
        def rebuild_frontend():
            """Rebuild the frontend (development only)"""
            if self.flask_app.debug:
                success = self.frontend_integration.rebuild_frontend()
                return {"success": success, "message": "Frontend rebuilt" if success else "Rebuild failed"}
            return {"error": "Not available in production"}, 403
        
        # Add route to list available templates
        @self.flask_app.route("/api/frontend/templates")
        def list_templates():
            """List available frontend templates"""
            templates = self.frontend_integration.list_templates()
            return {"templates": templates}
    
    def run(self, host="localhost", port=8084, debug=None, **kwargs):
        """Run the Flask app with enhanced configuration"""
        
        # Use debug mode from initialization if not specified
        if debug is None:
            debug = self.debug
        
        # Set Flask app debug mode
        self.flask_app.debug = debug
        
        # Print startup information
        print(f"🥝 Kiwi SQL Assistant starting...")
        print(f"📍 Server: http://{host}:{port}")
        
        if self.use_modern_frontend:
            print(f"🎨 Modern Frontend: Enabled")
            print(f"📁 Frontend Dir: {self.frontend_integration.frontend_dir}")
            print(f"🔗 Available routes:")
            print(f"   • Home: http://{host}:{port}/")
            print(f"   • Chat: http://{host}:{port}/chat")
            print(f"   • Dashboard: http://{host}:{port}/dashboard")
            print(f"   • Legacy Chat: http://{host}:{port}/legacy-chat")
        else:
            print(f"🎨 Modern Frontend: Disabled (using legacy)")
        
        print(f"🔧 Debug Mode: {'Enabled' if debug else 'Disabled'}")
        print(f"🚀 Starting server...")
        
        # Run the Flask app
        self.flask_app.run(
            host=host, 
            port=port, 
            debug=debug,
            use_reloader=False,
            **kwargs
        )


def create_app(vn, **kwargs):
    """Factory function to create a Kiwi Flask app"""
    
    # Set default values for enhanced features
    defaults = {
        'use_modern_frontend': True,
        'debug': True,
        'allow_llm_to_see_data': False,
        'chart': True,
        'title': 'Kiwi SQL Assistant',
        'subtitle': 'AI-powered SQL generation and database querying',
        'show_training_data': True,
        'suggested_questions': True,
        'sql': True,
        'table': True,
        'csv_download': True,
        'redraw_chart': True,
        'auto_fix_sql': True,
        'ask_results_correct': True,
        'followup_questions': True,
        'summarization': True,
    }
    
    # Merge defaults with provided kwargs
    config = {**defaults, **kwargs}
    
    # Create and return the app
    app = KiwiFlaskApp(vn=vn, **config)
    return app


def create_simple_app(vn, host="localhost", port=8084, debug=True):
    """Create and run a simple Kiwi Flask app with minimal configuration"""
    
    app = create_app(
        vn=vn,
        debug=debug,
        use_modern_frontend=True
    )
    
    app.run(host=host, port=port, debug=debug, use_reloader=False)
    return app


# Backward compatibility
def create_legacy_app(vn, **kwargs):
    """Create a Kiwi Flask app with legacy frontend only"""
    kwargs['use_modern_frontend'] = False
    return create_app(vn=vn, **kwargs)


if __name__ == "__main__":
    # Example usage
    from kiwi.base import VannaBase
    
    # This would normally be your configured Vanna instance
    class DemoVanna(VannaBase):
        def __init__(self):
            pass
        
        def generate_sql(self, question, **kwargs):
            return f"SELECT * FROM demo WHERE question = '{question}'"
        
        def is_sql_valid(self, sql):
            return True
        
        def run_sql(self, sql):
            return [{"demo": "data"}]
    
    # Create and run the app
    vn = DemoVanna()
    app = create_simple_app(vn, debug=True)