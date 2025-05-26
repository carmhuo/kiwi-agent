#!/usr/bin/env python3
"""
Frontend build script for Kiwi SQL Generation Project
Handles CSS/JS bundling, minification, and asset optimization
"""

import os
import shutil
import json
import subprocess
import argparse
from pathlib import Path

class FrontendBuilder:
    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir) if root_dir else Path(__file__).parent
        self.src_dir = self.root_dir / 'src'
        self.dist_dir = self.root_dir / 'dist'
        self.build_dir = self.root_dir / 'build'
        
    def clean(self):
        """Clean build and dist directories"""
        print("🧹 Cleaning build directories...")
        
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
            
        self.dist_dir.mkdir(exist_ok=True)
        self.build_dir.mkdir(exist_ok=True)
        
        print("✅ Cleaned build directories")
    
    def copy_assets(self):
        """Copy static assets to dist directory"""
        print("📁 Copying static assets...")
        
        # Copy images
        src_images = self.src_dir / 'assets' / 'images'
        dist_images = self.dist_dir / 'assets' / 'images'
        if src_images.exists():
            shutil.copytree(src_images, dist_images, dirs_exist_ok=True)
        
        # Copy fonts if they exist
        src_fonts = self.src_dir / 'assets' / 'fonts'
        dist_fonts = self.dist_dir / 'assets' / 'fonts'
        if src_fonts.exists():
            shutil.copytree(src_fonts, dist_fonts, dirs_exist_ok=True)
            
        print("✅ Copied static assets")
    
    def bundle_css(self):
        """Bundle and minify CSS files"""
        print("🎨 Bundling CSS...")
        
        css_files = [
            self.src_dir / 'assets' / 'css' / 'base.css',
            self.src_dir / 'assets' / 'css' / 'chat.css',
            self.src_dir / 'assets' / 'css' / 'dashboard.css'
        ]
        
        # Create output directory
        output_dir = self.dist_dir / 'assets' / 'css'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Bundle CSS
        bundled_css = []
        for css_file in css_files:
            if css_file.exists():
                with open(css_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    bundled_css.append(f"/* {css_file.name} */\n{content}\n")
        
        # Write bundled CSS
        output_file = output_dir / 'bundle.css'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(bundled_css))
        
        # Also copy individual files for development
        for css_file in css_files:
            if css_file.exists():
                shutil.copy2(css_file, output_dir)
        
        print("✅ Bundled CSS")
    
    def bundle_js(self):
        """Bundle JavaScript modules"""
        print("📦 Bundling JavaScript...")
        
        # Create output directory
        output_dir = self.dist_dir / 'assets' / 'js'
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy main.js and modules
        src_js = self.src_dir / 'assets' / 'js'
        if src_js.exists():
            shutil.copytree(src_js, output_dir, dirs_exist_ok=True)
        
        # Copy components
        src_components = self.src_dir / 'components'
        dist_components = self.dist_dir / 'components'
        if src_components.exists():
            shutil.copytree(src_components, dist_components, dirs_exist_ok=True)
        
        print("✅ Bundled JavaScript")
    
    def process_templates(self):
        """Process and copy HTML templates"""
        print("📄 Processing templates...")
        
        src_templates = self.src_dir / 'templates'
        dist_templates = self.dist_dir / 'templates'
        
        if src_templates.exists():
            shutil.copytree(src_templates, dist_templates, dirs_exist_ok=True)
            
            # Update asset paths in templates for production
            for template_file in dist_templates.rglob('*.html'):
                self.update_template_paths(template_file)
        
        print("✅ Processed templates")
    
    def update_template_paths(self, template_file):
        """Update asset paths in HTML templates"""
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update CSS paths
        content = content.replace(
            'href="../../assets/css/',
            'href="/static/frontend/assets/css/'
        )
        
        # Update JS paths
        content = content.replace(
            'src="../../assets/js/',
            'src="/static/frontend/assets/js/'
        )
        
        # Update image paths
        content = content.replace(
            'src="../../assets/images/',
            'src="/static/frontend/assets/images/'
        )
        
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def generate_manifest(self):
        """Generate build manifest"""
        print("📋 Generating manifest...")
        
        manifest = {
            'version': '1.0.0',
            'build_time': str(Path().cwd()),
            'files': {
                'css': ['assets/css/bundle.css'],
                'js': ['assets/js/main.js'],
                'templates': []
            }
        }
        
        # Collect template files
        templates_dir = self.dist_dir / 'templates'
        if templates_dir.exists():
            for template_file in templates_dir.rglob('*.html'):
                rel_path = template_file.relative_to(self.dist_dir)
                manifest['files']['templates'].append(str(rel_path))
        
        # Write manifest
        manifest_file = self.dist_dir / 'manifest.json'
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2)
        
        print("✅ Generated manifest")
    
    def install_dependencies(self):
        """Install Node.js dependencies if package.json exists"""
        package_json = self.root_dir / 'package.json'
        if package_json.exists():
            print("📦 Installing Node.js dependencies...")
            try:
                subprocess.run(['npm', 'install'], cwd=self.root_dir, check=True)
                print("✅ Installed Node.js dependencies")
            except subprocess.CalledProcessError:
                print("⚠️  Failed to install Node.js dependencies")
            except FileNotFoundError:
                print("⚠️  npm not found, skipping Node.js dependencies")
    
    def run_vite_build(self):
        """Run Vite build if available"""
        vite_config = self.root_dir / 'vite.config.js'
        if vite_config.exists():
            print("⚡ Running Vite build...")
            try:
                subprocess.run(['npm', 'run', 'build'], cwd=self.root_dir, check=True)
                print("✅ Vite build completed")
                return True
            except subprocess.CalledProcessError:
                print("⚠️  Vite build failed, falling back to manual build")
            except FileNotFoundError:
                print("⚠️  npm not found, falling back to manual build")
        return False
    
    def build(self, use_vite=True):
        """Run complete build process"""
        print("🚀 Starting frontend build...")
        
        # Clean previous builds
        self.clean()
        
        # Try Vite build first if requested
        if use_vite and self.run_vite_build():
            print("✅ Frontend build completed with Vite")
            return
        
        # Fallback to manual build
        print("🔧 Running manual build...")
        
        # Install dependencies
        self.install_dependencies()
        
        # Copy assets
        self.copy_assets()
        
        # Bundle CSS and JS
        self.bundle_css()
        self.bundle_js()
        
        # Process templates
        self.process_templates()
        
        # Generate manifest
        self.generate_manifest()
        
        print("✅ Frontend build completed")
    
    def dev_build(self):
        """Development build (no minification)"""
        print("🔧 Running development build...")
        
        # Clean and create directories
        self.clean()
        
        # Copy everything as-is for development
        self.copy_assets()
        self.bundle_css()
        self.bundle_js()
        self.process_templates()
        self.generate_manifest()
        
        print("✅ Development build completed")
    
    def watch(self):
        """Watch for file changes and rebuild"""
        print("👀 Watching for file changes...")
        try:
            import time
            import watchdog.observers
            import watchdog.events
            
            class BuildHandler(watchdog.events.FileSystemEventHandler):
                def __init__(self, builder):
                    self.builder = builder
                    self.last_build = 0
                
                def on_modified(self, event):
                    if event.is_directory:
                        return
                    
                    # Debounce builds
                    now = time.time()
                    if now - self.last_build < 1:
                        return
                    
                    self.last_build = now
                    print(f"📝 File changed: {event.src_path}")
                    self.builder.dev_build()
            
            observer = watchdog.observers.Observer()
            observer.schedule(BuildHandler(self), str(self.src_dir), recursive=True)
            observer.start()
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()
            
        except ImportError:
            print("⚠️  watchdog not installed, install with: pip install watchdog")

def main():
    parser = argparse.ArgumentParser(description='Frontend build tool for Kiwi')
    parser.add_argument('command', choices=['build', 'dev', 'watch', 'clean'], 
                       help='Build command to run')
    parser.add_argument('--no-vite', action='store_true', 
                       help='Skip Vite build and use manual build')
    
    args = parser.parse_args()
    
    builder = FrontendBuilder()
    
    if args.command == 'build':
        builder.build(use_vite=not args.no_vite)
    elif args.command == 'dev':
        builder.dev_build()
    elif args.command == 'watch':
        builder.watch()
    elif args.command == 'clean':
        builder.clean()

if __name__ == '__main__':
    main()