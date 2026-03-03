"""ConfigManager - Configuration templating

IntentHash¹¹: 0x6E9B4D1F_P3_1_ATLAS_COMPLETE_20260303T0319Z

Manages configuration templates for IaC.
"""

import json
import os
from typing import Dict, Any, List, Tuple


class ConfigManager:
    """Manage IaC configuration templates"""
    
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = templates_dir
        self.templates = {}
        self._load_templates()
    
    def _load_templates(self):
        """Load configuration templates"""
        templates_path = os.path.join(self.templates_dir, "templates.json")
        
        if os.path.exists(templates_path):
            with open(templates_path, 'r') as f:
                data = json.load(f)
                self.templates = data.get('templates', {})
    
    def register_template(
        self,
        template_name: str,
        template_type: str,
        template_content: str,
        variables: Dict[str, Any]
    ) -> Tuple[str, str]:
        """Register configuration template
        
        Args:
            template_name: Template name
            template_type: Template type (terraform, kubernetes, docker-compose)
            template_content: Template content
            variables: Template variables
        
        Returns:
            Tuple of (status: SUCCESS/FAILED, template_id)
        """
        try:
            template_id = f"{template_type}_{template_name}"
            
            self.templates[template_id] = {
                'template_id': template_id,
                'template_name': template_name,
                'template_type': template_type,
                'template_content': template_content,
                'variables': variables
            }
            
            self._save_templates()
            
            return 'SUCCESS', template_id
        
        except Exception as e:
            return 'FAILED', ''
    
    def render_template(
        self,
        template_id: str,
        values: Dict[str, Any]
    ) -> Tuple[str, str]:
        """Render template with values
        
        Args:
            template_id: Template identifier
            values: Variable values
        
        Returns:
            Tuple of (status: SUCCESS/FAILED, rendered_content)
        """
        try:
            if template_id not in self.templates:
                return 'FAILED', ''
            
            template = self.templates[template_id]
            content = template['template_content']
            
            # Simple variable substitution (stub)
            for key, value in values.items():
                content = content.replace(f"{{{{ {key} }}}}", str(value))
            
            return 'SUCCESS', content
        
        except Exception as e:
            return 'FAILED', ''
    
    def get_template(
        self,
        template_id: str
    ) -> Tuple[str, Dict[str, Any]]:
        """Get template by ID
        
        Args:
            template_id: Template identifier
        
        Returns:
            Tuple of (status: SUCCESS/FAILED, template)
        """
        template = self.templates.get(template_id)
        
        if template:
            return 'SUCCESS', template
        else:
            return 'FAILED', {}
    
    def list_templates(
        self,
        template_type: str = None
    ) -> List[Dict[str, Any]]:
        """List templates
        
        Args:
            template_type: Filter by template type
        
        Returns:
            List of templates
        """
        templates = list(self.templates.values())
        
        if template_type:
            templates = [t for t in templates if t['template_type'] == template_type]
        
        return templates
    
    def _save_templates(self):
        """Save templates"""
        os.makedirs(self.templates_dir, exist_ok=True)
        templates_path = os.path.join(self.templates_dir, "templates.json")
        
        with open(templates_path, 'w') as f:
            json.dump({'templates': self.templates}, f, indent=2)
