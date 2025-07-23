"""
Visual Theme Generator - Dynamic Graphics and Themed Environments
Revolutionary system for generating theme-specific visuals, graphics, and environments

This module provides:
- Dynamic asset generation based on themes
- Procedural background and environment creation
- Theme-specific color palettes and styling
- Animated effects and particle systems
- Responsive visual elements for all devices
"""

import json
import random
import math
from typing import Dict, List, Any, Tuple

class VisualThemeGenerator:
    """Generates dynamic visuals and themed environments for games"""
    
    def __init__(self):
        # Theme-specific visual configurations
        self.theme_configs = {
            'fantasy': {
                'color_palette': {
                    'primary': '#9370db',
                    'secondary': '#dda0dd',
                    'accent': '#ff69b4',
                    'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    'text': '#ffffff',
                    'glow': '#9370db',
                    'particle': '#ffd700'
                },
                'visual_effects': {
                    'magical_particles': True,
                    'glowing_effects': True,
                    'mystical_aura': True,
                    'sparkle_trails': True
                },
                'environment_elements': {
                    'floating_crystals': True,
                    'magical_runes': True,
                    'enchanted_trees': True,
                    'mystical_fog': True
                }
            },
            'space': {
                'color_palette': {
                    'primary': '#00bfff',
                    'secondary': '#1e90ff',
                    'accent': '#00ffff',
                    'background': 'linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 100%)',
                    'text': '#ffffff',
                    'glow': '#00ffff',
                    'particle': '#ffffff'
                },
                'visual_effects': {
                    'star_field': True,
                    'laser_effects': True,
                    'cosmic_particles': True,
                    'warp_effects': True
                },
                'environment_elements': {
                    'asteroid_field': True,
                    'nebula_clouds': True,
                    'space_stations': True,
                    'planet_surfaces': True
                }
            },
            'underwater': {
                'color_palette': {
                    'primary': '#20b2aa',
                    'secondary': '#87ceeb',
                    'accent': '#00ced1',
                    'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    'text': '#ffffff',
                    'glow': '#20b2aa',
                    'particle': '#87ceeb'
                },
                'visual_effects': {
                    'bubble_effects': True,
                    'water_distortion': True,
                    'flowing_movement': True,
                    'light_rays': True
                },
                'environment_elements': {
                    'coral_reefs': True,
                    'seaweed_forests': True,
                    'underwater_caves': True,
                    'treasure_chests': True
                }
            },
            'cyberpunk': {
                'color_palette': {
                    'primary': '#ff00ff',
                    'secondary': '#00ffff',
                    'accent': '#ffff00',
                    'background': 'linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 100%)',
                    'text': '#ffffff',
                    'glow': '#ff00ff',
                    'particle': '#00ffff'
                },
                'visual_effects': {
                    'neon_glow': True,
                    'digital_glitch': True,
                    'holographic_ui': True,
                    'circuit_patterns': True
                },
                'environment_elements': {
                    'neon_signs': True,
                    'digital_billboards': True,
                    'cyber_architecture': True,
                    'data_streams': True
                }
            },
            'steampunk': {
                'color_palette': {
                    'primary': '#cd853f',
                    'secondary': '#daa520',
                    'accent': '#ff8c00',
                    'background': 'linear-gradient(135deg, #8b4513 0%, #a0522d 100%)',
                    'text': '#ffffff',
                    'glow': '#ffd700',
                    'particle': '#cd853f'
                },
                'visual_effects': {
                    'steam_effects': True,
                    'gear_animations': True,
                    'brass_reflections': True,
                    'mechanical_movements': True
                },
                'environment_elements': {
                    'clockwork_gears': True,
                    'steam_pipes': True,
                    'brass_machinery': True,
                    'airship_elements': True
                }
            },
            'horror': {
                'color_palette': {
                    'primary': '#8b0000',
                    'secondary': '#2f2f2f',
                    'accent': '#ff4500',
                    'background': 'linear-gradient(135deg, #000000 0%, #2f2f2f 100%)',
                    'text': '#ffffff',
                    'glow': '#ff0000',
                    'particle': '#8b0000'
                },
                'visual_effects': {
                    'shadow_effects': True,
                    'blood_splatters': True,
                    'flickering_lights': True,
                    'ghostly_apparitions': True
                },
                'environment_elements': {
                    'haunted_trees': True,
                    'abandoned_buildings': True,
                    'graveyard_elements': True,
                    'fog_effects': True
                }
            }
        }
        
        # Entity visual templates
        self.entity_templates = {
            'characters': {
                'fantasy': {
                    'fairy': {'color': '#ff69b4', 'glow': True, 'particles': 'sparkles'},
                    'wizard': {'color': '#9370db', 'glow': True, 'particles': 'magic'},
                    'knight': {'color': '#c0c0c0', 'glow': False, 'particles': None}
                },
                'space': {
                    'astronaut': {'color': '#ffffff', 'glow': True, 'particles': 'stars'},
                    'alien': {'color': '#00ff00', 'glow': True, 'particles': 'energy'},
                    'robot': {'color': '#c0c0c0', 'glow': True, 'particles': 'sparks'}
                },
                'underwater': {
                    'mermaid': {'color': '#20b2aa', 'glow': True, 'particles': 'bubbles'},
                    'diver': {'color': '#4682b4', 'glow': False, 'particles': 'bubbles'},
                    'sea_creature': {'color': '#87ceeb', 'glow': True, 'particles': 'water'}
                }
            },
            'enemies': {
                'fantasy': {
                    'dragon': {'color': '#ff0000', 'glow': True, 'particles': 'fire'},
                    'demon': {'color': '#8b0000', 'glow': True, 'particles': 'darkness'},
                    'orc': {'color': '#228b22', 'glow': False, 'particles': None}
                },
                'space': {
                    'alien_ship': {'color': '#ff0000', 'glow': True, 'particles': 'energy'},
                    'space_monster': {'color': '#800080', 'glow': True, 'particles': 'cosmic'},
                    'robot_enemy': {'color': '#ff4500', 'glow': True, 'particles': 'sparks'}
                },
                'underwater': {
                    'shark': {'color': '#2f4f4f', 'glow': False, 'particles': 'bubbles'},
                    'octopus': {'color': '#800080', 'glow': True, 'particles': 'ink'},
                    'electric_eel': {'color': '#ffff00', 'glow': True, 'particles': 'electricity'}
                }
            },
            'objects': {
                'fantasy': {
                    'crystal': {'color': '#9370db', 'glow': True, 'particles': 'sparkles'},
                    'potion': {'color': '#00ff00', 'glow': True, 'particles': 'magic'},
                    'treasure': {'color': '#ffd700', 'glow': True, 'particles': 'gold'}
                },
                'space': {
                    'energy_crystal': {'color': '#00ffff', 'glow': True, 'particles': 'energy'},
                    'tech_device': {'color': '#c0c0c0', 'glow': True, 'particles': 'sparks'},
                    'alien_artifact': {'color': '#ff00ff', 'glow': True, 'particles': 'cosmic'}
                },
                'underwater': {
                    'pearl': {'color': '#ffffff', 'glow': True, 'particles': 'shimmer'},
                    'coral': {'color': '#ff7f50', 'glow': False, 'particles': None},
                    'treasure_chest': {'color': '#daa520', 'glow': True, 'particles': 'gold'}
                }
            }
        }
    
    def generate_themed_assets(self, theme: str, entities: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Generate custom sprites, backgrounds, and animations for a specific theme
        
        Args:
            theme: Visual theme (fantasy, space, underwater, etc.)
            entities: Dictionary of entity types and their names
            
        Returns:
            Complete asset specification for the theme
        """
        theme_config = self.theme_configs.get(theme, self.theme_configs['fantasy'])
        
        assets = {
            'theme': theme,
            'color_palette': theme_config['color_palette'],
            'background': self._generate_background(theme),
            'entities': self._generate_entity_assets(theme, entities),
            'ui_elements': self._generate_ui_assets(theme),
            'particle_effects': self._generate_particle_effects(theme),
            'animations': self._generate_animations(theme),
            'css_styles': self._generate_css_styles(theme),
            'svg_graphics': self._generate_svg_graphics(theme, entities)
        }
        
        return assets
    
    def _generate_background(self, theme: str) -> Dict[str, Any]:
        """Generate themed background specification"""
        theme_config = self.theme_configs.get(theme, self.theme_configs['fantasy'])
        
        background = {
            'type': 'gradient_with_elements',
            'gradient': theme_config['color_palette']['background'],
            'elements': self._generate_background_elements(theme),
            'animation': self._generate_background_animation(theme),
            'responsive': True
        }
        
        return background
    
    def _generate_background_elements(self, theme: str) -> List[Dict[str, Any]]:
        """Generate background decorative elements"""
        elements = []
        
        if theme == 'fantasy':
            elements = [
                {'type': 'floating_particles', 'color': '#ffd700', 'count': 20, 'animation': 'float'},
                {'type': 'mystical_runes', 'color': '#9370db', 'count': 5, 'animation': 'glow'},
                {'type': 'magical_circles', 'color': '#ff69b4', 'count': 3, 'animation': 'rotate'}
            ]
        elif theme == 'space':
            elements = [
                {'type': 'stars', 'color': '#ffffff', 'count': 100, 'animation': 'twinkle'},
                {'type': 'nebula_clouds', 'color': '#9370db', 'count': 3, 'animation': 'drift'},
                {'type': 'distant_planets', 'color': '#ff6b6b', 'count': 2, 'animation': 'orbit'}
            ]
        elif theme == 'underwater':
            elements = [
                {'type': 'bubbles', 'color': '#87ceeb', 'count': 30, 'animation': 'rise'},
                {'type': 'seaweed', 'color': '#228b22', 'count': 8, 'animation': 'sway'},
                {'type': 'light_rays', 'color': '#ffffff', 'count': 5, 'animation': 'shimmer'}
            ]
        elif theme == 'cyberpunk':
            elements = [
                {'type': 'neon_lines', 'color': '#ff00ff', 'count': 10, 'animation': 'pulse'},
                {'type': 'digital_rain', 'color': '#00ff00', 'count': 50, 'animation': 'fall'},
                {'type': 'circuit_patterns', 'color': '#00ffff', 'count': 5, 'animation': 'flow'}
            ]
        elif theme == 'steampunk':
            elements = [
                {'type': 'steam_clouds', 'color': '#f5f5f5', 'count': 8, 'animation': 'drift'},
                {'type': 'gears', 'color': '#cd853f', 'count': 6, 'animation': 'rotate'},
                {'type': 'brass_pipes', 'color': '#daa520', 'count': 4, 'animation': 'static'}
            ]
        
        return elements
    
    def _generate_background_animation(self, theme: str) -> Dict[str, Any]:
        """Generate background animation specifications"""
        animations = {
            'fantasy': {
                'type': 'magical_shimmer',
                'duration': '10s',
                'easing': 'ease-in-out',
                'infinite': True
            },
            'space': {
                'type': 'cosmic_drift',
                'duration': '20s',
                'easing': 'linear',
                'infinite': True
            },
            'underwater': {
                'type': 'water_flow',
                'duration': '15s',
                'easing': 'ease-in-out',
                'infinite': True
            },
            'cyberpunk': {
                'type': 'digital_pulse',
                'duration': '5s',
                'easing': 'ease-in-out',
                'infinite': True
            },
            'steampunk': {
                'type': 'mechanical_rhythm',
                'duration': '8s',
                'easing': 'ease-in-out',
                'infinite': True
            }
        }
        
        return animations.get(theme, animations['fantasy'])
    
    def _generate_entity_assets(self, theme: str, entities: Dict[str, List[str]]) -> Dict[str, Any]:
        """Generate visual assets for game entities"""
        entity_assets = {}
        
        for entity_type, entity_list in entities.items():
            entity_assets[entity_type] = {}
            
            for entity_name in entity_list:
                # Get template or create default
                template = self._get_entity_template(theme, entity_type, entity_name)
                
                entity_assets[entity_type][entity_name] = {
                    'visual_spec': template,
                    'svg_definition': self._generate_entity_svg(theme, entity_type, entity_name, template),
                    'css_class': f"{theme}_{entity_type}_{entity_name}",
                    'animation': self._generate_entity_animation(theme, entity_type, entity_name)
                }
        
        return entity_assets
    
    def _get_entity_template(self, theme: str, entity_type: str, entity_name: str) -> Dict[str, Any]:
        """Get or create entity visual template"""
        templates = self.entity_templates.get(entity_type, {}).get(theme, {})
        
        if entity_name in templates:
            return templates[entity_name]
        
        # Generate default template based on theme
        theme_config = self.theme_configs.get(theme, self.theme_configs['fantasy'])
        
        return {
            'color': theme_config['color_palette']['primary'],
            'glow': True,
            'particles': 'default'
        }
    
    def _generate_entity_svg(self, theme: str, entity_type: str, entity_name: str, template: Dict[str, Any]) -> str:
        """Generate SVG definition for entity"""
        color = template.get('color', '#ffffff')
        glow = template.get('glow', False)
        
        # Basic SVG shapes based on entity type
        if entity_type == 'characters':
            if 'fairy' in entity_name:
                svg = f'''
                <g class="{theme}_{entity_type}_{entity_name}">
                    <circle cx="15" cy="15" r="8" fill="{color}" {self._get_glow_filter(glow)}/>
                    <path d="M8,15 Q15,5 22,15 Q15,25 8,15" fill="{color}" opacity="0.7"/>
                    <path d="M8,15 Q15,25 22,15 Q15,5 8,15" fill="{color}" opacity="0.7"/>
                </g>
                '''
            elif 'mermaid' in entity_name:
                svg = f'''
                <g class="{theme}_{entity_type}_{entity_name}">
                    <circle cx="15" cy="10" r="6" fill="{color}" {self._get_glow_filter(glow)}/>
                    <path d="M9,16 Q15,20 21,16 Q18,25 15,22 Q12,25 9,16" fill="{color}"/>
                </g>
                '''
            else:
                svg = f'''
                <g class="{theme}_{entity_type}_{entity_name}">
                    <circle cx="15" cy="15" r="10" fill="{color}" {self._get_glow_filter(glow)}/>
                </g>
                '''
        elif entity_type == 'enemies':
            svg = f'''
            <g class="{theme}_{entity_type}_{entity_name}">
                <polygon points="15,5 25,20 5,20" fill="{color}" {self._get_glow_filter(glow)}/>
            </g>
            '''
        elif entity_type == 'objects':
            if 'crystal' in entity_name or 'gem' in entity_name:
                svg = f'''
                <g class="{theme}_{entity_type}_{entity_name}">
                    <polygon points="15,5 20,10 20,20 10,20 10,10" fill="{color}" {self._get_glow_filter(glow)}/>
                </g>
                '''
            elif 'pearl' in entity_name:
                svg = f'''
                <g class="{theme}_{entity_type}_{entity_name}">
                    <circle cx="15" cy="15" r="8" fill="{color}" {self._get_glow_filter(glow)}/>
                </g>
                '''
            else:
                svg = f'''
                <g class="{theme}_{entity_type}_{entity_name}">
                    <rect x="10" y="10" width="10" height="10" fill="{color}" {self._get_glow_filter(glow)}/>
                </g>
                '''
        else:
            svg = f'''
            <g class="{theme}_{entity_type}_{entity_name}">
                <rect x="10" y="10" width="10" height="10" fill="{color}" {self._get_glow_filter(glow)}/>
            </g>
            '''
        
        return svg
    
    def _get_glow_filter(self, has_glow: bool) -> str:
        """Generate glow filter for SVG elements"""
        if not has_glow:
            return ''
        
        return 'filter="drop-shadow(0 0 5px currentColor)"'
    
    def _generate_entity_animation(self, theme: str, entity_type: str, entity_name: str) -> Dict[str, Any]:
        """Generate animation specifications for entities"""
        animations = {
            'characters': {
                'fairy': {'type': 'float', 'duration': '3s', 'amplitude': '5px'},
                'mermaid': {'type': 'swim', 'duration': '4s', 'amplitude': '3px'},
                'default': {'type': 'idle', 'duration': '2s', 'amplitude': '2px'}
            },
            'enemies': {
                'default': {'type': 'menace', 'duration': '2s', 'amplitude': '3px'}
            },
            'objects': {
                'crystal': {'type': 'sparkle', 'duration': '2s', 'amplitude': '0px'},
                'gem': {'type': 'sparkle', 'duration': '2s', 'amplitude': '0px'},
                'pearl': {'type': 'shimmer', 'duration': '3s', 'amplitude': '0px'},
                'default': {'type': 'pulse', 'duration': '2s', 'amplitude': '0px'}
            }
        }
        
        entity_animations = animations.get(entity_type, {})
        return entity_animations.get(entity_name, entity_animations.get('default', {'type': 'static'}))
    
    def _generate_ui_assets(self, theme: str) -> Dict[str, Any]:
        """Generate UI element specifications"""
        theme_config = self.theme_configs.get(theme, self.theme_configs['fantasy'])
        
        ui_assets = {
            'buttons': self._generate_button_styles(theme_config),
            'panels': self._generate_panel_styles(theme_config),
            'text': self._generate_text_styles(theme_config),
            'progress_bars': self._generate_progress_bar_styles(theme_config),
            'icons': self._generate_icon_styles(theme_config)
        }
        
        return ui_assets
    
    def _generate_button_styles(self, theme_config: Dict[str, Any]) -> Dict[str, str]:
        """Generate button styling"""
        colors = theme_config['color_palette']
        
        return {
            'background': f"linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%)",
            'border': f"2px solid {colors['accent']}",
            'color': colors['text'],
            'border_radius': '8px',
            'box_shadow': f"0 4px 15px rgba(0, 0, 0, 0.3), 0 0 10px {colors['glow']}",
            'hover_transform': 'translateY(-2px)',
            'hover_box_shadow': f"0 6px 20px rgba(0, 0, 0, 0.4), 0 0 15px {colors['glow']}"
        }
    
    def _generate_panel_styles(self, theme_config: Dict[str, Any]) -> Dict[str, str]:
        """Generate panel styling"""
        colors = theme_config['color_palette']
        
        return {
            'background': 'rgba(255, 255, 255, 0.1)',
            'border': f"1px solid rgba(255, 255, 255, 0.2)",
            'border_radius': '15px',
            'backdrop_filter': 'blur(10px)',
            'box_shadow': f"0 8px 32px rgba(0, 0, 0, 0.3), inset 0 0 20px {colors['glow']}40"
        }
    
    def _generate_text_styles(self, theme_config: Dict[str, Any]) -> Dict[str, str]:
        """Generate text styling"""
        colors = theme_config['color_palette']
        
        return {
            'color': colors['text'],
            'text_shadow': f"2px 2px 4px rgba(0, 0, 0, 0.8), 0 0 10px {colors['glow']}",
            'font_family': 'Arial, sans-serif',
            'font_weight': 'bold'
        }
    
    def _generate_progress_bar_styles(self, theme_config: Dict[str, Any]) -> Dict[str, str]:
        """Generate progress bar styling"""
        colors = theme_config['color_palette']
        
        return {
            'background': 'rgba(0, 0, 0, 0.3)',
            'fill': f"linear-gradient(90deg, {colors['primary']} 0%, {colors['accent']} 100%)",
            'border': f"1px solid {colors['secondary']}",
            'border_radius': '10px',
            'box_shadow': f"inset 0 0 10px {colors['glow']}40"
        }
    
    def _generate_icon_styles(self, theme_config: Dict[str, Any]) -> Dict[str, str]:
        """Generate icon styling"""
        colors = theme_config['color_palette']
        
        return {
            'color': colors['accent'],
            'filter': f"drop-shadow(0 0 5px {colors['glow']})",
            'transition': 'all 0.3s ease'
        }
    
    def _generate_particle_effects(self, theme: str) -> Dict[str, Any]:
        """Generate particle effect specifications"""
        theme_config = self.theme_configs.get(theme, self.theme_configs['fantasy'])
        effects = theme_config.get('visual_effects', {})
        
        particle_effects = {}
        
        if effects.get('magical_particles'):
            particle_effects['magical_sparkles'] = {
                'count': 20,
                'color': theme_config['color_palette']['particle'],
                'size': '2px',
                'animation': 'sparkle',
                'duration': '2s',
                'spawn_rate': '0.1s'
            }
        
        if effects.get('star_field'):
            particle_effects['stars'] = {
                'count': 100,
                'color': '#ffffff',
                'size': '1px',
                'animation': 'twinkle',
                'duration': '3s',
                'spawn_rate': 'static'
            }
        
        if effects.get('bubble_effects'):
            particle_effects['bubbles'] = {
                'count': 15,
                'color': theme_config['color_palette']['particle'],
                'size': '4px',
                'animation': 'rise',
                'duration': '4s',
                'spawn_rate': '0.5s'
            }
        
        if effects.get('neon_glow'):
            particle_effects['neon_particles'] = {
                'count': 30,
                'color': theme_config['color_palette']['glow'],
                'size': '3px',
                'animation': 'pulse',
                'duration': '1s',
                'spawn_rate': '0.2s'
            }
        
        return particle_effects
    
    def _generate_animations(self, theme: str) -> Dict[str, Any]:
        """Generate animation specifications"""
        animations = {
            'float': {
                'keyframes': {
                    '0%': 'transform: translateY(0px)',
                    '50%': 'transform: translateY(-10px)',
                    '100%': 'transform: translateY(0px)'
                },
                'duration': '3s',
                'timing_function': 'ease-in-out',
                'iteration_count': 'infinite'
            },
            'sparkle': {
                'keyframes': {
                    '0%': 'opacity: 0; transform: scale(0)',
                    '50%': 'opacity: 1; transform: scale(1)',
                    '100%': 'opacity: 0; transform: scale(0)'
                },
                'duration': '2s',
                'timing_function': 'ease-in-out',
                'iteration_count': 'infinite'
            },
            'pulse': {
                'keyframes': {
                    '0%': 'transform: scale(1); opacity: 1',
                    '50%': 'transform: scale(1.1); opacity: 0.8',
                    '100%': 'transform: scale(1); opacity: 1'
                },
                'duration': '2s',
                'timing_function': 'ease-in-out',
                'iteration_count': 'infinite'
            },
            'rotate': {
                'keyframes': {
                    '0%': 'transform: rotate(0deg)',
                    '100%': 'transform: rotate(360deg)'
                },
                'duration': '10s',
                'timing_function': 'linear',
                'iteration_count': 'infinite'
            },
            'glow': {
                'keyframes': {
                    '0%': 'filter: brightness(1) drop-shadow(0 0 5px currentColor)',
                    '50%': 'filter: brightness(1.3) drop-shadow(0 0 15px currentColor)',
                    '100%': 'filter: brightness(1) drop-shadow(0 0 5px currentColor)'
                },
                'duration': '3s',
                'timing_function': 'ease-in-out',
                'iteration_count': 'infinite'
            }
        }
        
        return animations
    
    def _generate_css_styles(self, theme: str) -> str:
        """Generate complete CSS stylesheet for the theme"""
        theme_config = self.theme_configs.get(theme, self.theme_configs['fantasy'])
        colors = theme_config['color_palette']
        
        css = f'''
        /* {theme.title()} Theme Styles */
        .{theme}-theme {{
            --primary-color: {colors['primary']};
            --secondary-color: {colors['secondary']};
            --accent-color: {colors['accent']};
            --background: {colors['background']};
            --text-color: {colors['text']};
            --glow-color: {colors['glow']};
            --particle-color: {colors['particle']};
        }}
        
        .{theme}-background {{
            background: {colors['background']};
            min-height: 100vh;
            position: relative;
            overflow: hidden;
        }}
        
        .{theme}-panel {{
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            backdrop-filter: blur(10px);
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }}
        
        .{theme}-button {{
            background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
            border: 2px solid {colors['accent']};
            color: {colors['text']};
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3), 0 0 10px {colors['glow']};
        }}
        
        .{theme}-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4), 0 0 15px {colors['glow']};
        }}
        
        .{theme}-text {{
            color: {colors['text']};
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8), 0 0 10px {colors['glow']};
            font-family: Arial, sans-serif;
            font-weight: bold;
        }}
        
        .{theme}-glow {{
            filter: drop-shadow(0 0 10px {colors['glow']});
        }}
        
        /* Animations */
        @keyframes {theme}-float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
        }}
        
        @keyframes {theme}-sparkle {{
            0%, 100% {{ opacity: 0; transform: scale(0); }}
            50% {{ opacity: 1; transform: scale(1); }}
        }}
        
        @keyframes {theme}-pulse {{
            0%, 100% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.1); opacity: 0.8; }}
        }}
        
        @keyframes {theme}-glow {{
            0%, 100% {{ filter: brightness(1) drop-shadow(0 0 5px {colors['glow']}); }}
            50% {{ filter: brightness(1.3) drop-shadow(0 0 15px {colors['glow']}); }}
        }}
        
        .{theme}-float {{ animation: {theme}-float 3s ease-in-out infinite; }}
        .{theme}-sparkle {{ animation: {theme}-sparkle 2s ease-in-out infinite; }}
        .{theme}-pulse {{ animation: {theme}-pulse 2s ease-in-out infinite; }}
        .{theme}-glow-animation {{ animation: {theme}-glow 3s ease-in-out infinite; }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .{theme}-panel {{
                padding: 1rem;
                margin: 0.5rem;
            }}
            
            .{theme}-button {{
                padding: 8px 16px;
                font-size: 14px;
            }}
        }}
        '''
        
        return css
    
    def _generate_svg_graphics(self, theme: str, entities: Dict[str, List[str]]) -> str:
        """Generate SVG graphics definitions"""
        svg_defs = f'''
        <defs>
            <!-- {theme.title()} Theme SVG Definitions -->
            
            <!-- Gradients -->
            <linearGradient id="{theme}-primary-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:{self.theme_configs[theme]['color_palette']['primary']};stop-opacity:1" />
                <stop offset="100%" style="stop-color:{self.theme_configs[theme]['color_palette']['secondary']};stop-opacity:1" />
            </linearGradient>
            
            <!-- Filters -->
            <filter id="{theme}-glow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                <feMerge> 
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
            
            <!-- Patterns -->
            <pattern id="{theme}-pattern" patternUnits="userSpaceOnUse" width="20" height="20">
                <circle cx="10" cy="10" r="2" fill="{self.theme_configs[theme]['color_palette']['accent']}" opacity="0.3"/>
            </pattern>
        </defs>
        '''
        
        return svg_defs
    
    def create_themed_environment(self, theme: str) -> Dict[str, Any]:
        """
        Create a complete themed environment specification
        
        Args:
            theme: Visual theme to create environment for
            
        Returns:
            Complete environment specification including all visual elements
        """
        theme_config = self.theme_configs.get(theme, self.theme_configs['fantasy'])
        
        environment = {
            'theme': theme,
            'background_layers': self._create_background_layers(theme),
            'environmental_objects': self._create_environmental_objects(theme),
            'lighting_setup': self._create_lighting_setup(theme),
            'particle_systems': self._create_particle_systems(theme),
            'audio_atmosphere': self._create_audio_atmosphere(theme),
            'interactive_elements': self._create_interactive_elements(theme),
            'responsive_adaptations': self._create_responsive_adaptations(theme)
        }
        
        return environment
    
    def _create_background_layers(self, theme: str) -> List[Dict[str, Any]]:
        """Create layered background system"""
        layers = []
        
        if theme == 'fantasy':
            layers = [
                {'layer': 'sky', 'type': 'gradient', 'colors': ['#667eea', '#764ba2'], 'z_index': 1},
                {'layer': 'clouds', 'type': 'moving_shapes', 'color': '#ffffff', 'opacity': 0.3, 'z_index': 2},
                {'layer': 'mountains', 'type': 'silhouette', 'color': '#4b0082', 'z_index': 3},
                {'layer': 'trees', 'type': 'forest', 'color': '#228b22', 'z_index': 4}
            ]
        elif theme == 'space':
            layers = [
                {'layer': 'deep_space', 'type': 'gradient', 'colors': ['#0c0c0c', '#1a1a2e'], 'z_index': 1},
                {'layer': 'stars', 'type': 'particles', 'color': '#ffffff', 'count': 200, 'z_index': 2},
                {'layer': 'nebula', 'type': 'cloud_effect', 'color': '#9370db', 'opacity': 0.4, 'z_index': 3},
                {'layer': 'planets', 'type': 'distant_objects', 'color': '#ff6b6b', 'z_index': 4}
            ]
        elif theme == 'underwater':
            layers = [
                {'layer': 'water_depth', 'type': 'gradient', 'colors': ['#667eea', '#764ba2'], 'z_index': 1},
                {'layer': 'light_rays', 'type': 'light_beams', 'color': '#ffffff', 'opacity': 0.2, 'z_index': 2},
                {'layer': 'coral_reef', 'type': 'coral_formations', 'color': '#ff7f50', 'z_index': 3},
                {'layer': 'seaweed', 'type': 'plant_life', 'color': '#228b22', 'z_index': 4}
            ]
        
        return layers
    
    def _create_environmental_objects(self, theme: str) -> List[Dict[str, Any]]:
        """Create environmental decoration objects"""
        objects = []
        
        if theme == 'fantasy':
            objects = [
                {'type': 'floating_crystal', 'count': 5, 'animation': 'float', 'glow': True},
                {'type': 'magical_rune', 'count': 8, 'animation': 'pulse', 'glow': True},
                {'type': 'fairy_light', 'count': 15, 'animation': 'sparkle', 'glow': True}
            ]
        elif theme == 'space':
            objects = [
                {'type': 'asteroid', 'count': 10, 'animation': 'drift', 'glow': False},
                {'type': 'space_debris', 'count': 20, 'animation': 'tumble', 'glow': False},
                {'type': 'energy_field', 'count': 3, 'animation': 'pulse', 'glow': True}
            ]
        elif theme == 'underwater':
            objects = [
                {'type': 'coral_formation', 'count': 12, 'animation': 'sway', 'glow': False},
                {'type': 'sea_anemone', 'count': 8, 'animation': 'wave', 'glow': True},
                {'type': 'treasure_chest', 'count': 2, 'animation': 'sparkle', 'glow': True}
            ]
        
        return objects
    
    def _create_lighting_setup(self, theme: str) -> Dict[str, Any]:
        """Create lighting configuration"""
        lighting_setups = {
            'fantasy': {
                'ambient_light': {'color': '#ffd700', 'intensity': 0.6},
                'directional_light': {'color': '#ffffff', 'intensity': 0.8, 'angle': 45},
                'point_lights': [
                    {'color': '#9370db', 'intensity': 0.4, 'position': 'random'},
                    {'color': '#ff69b4', 'intensity': 0.3, 'position': 'random'}
                ]
            },
            'space': {
                'ambient_light': {'color': '#1a1a2e', 'intensity': 0.2},
                'directional_light': {'color': '#ffffff', 'intensity': 1.0, 'angle': 0},
                'point_lights': [
                    {'color': '#00ffff', 'intensity': 0.6, 'position': 'center'},
                    {'color': '#ff00ff', 'intensity': 0.4, 'position': 'random'}
                ]
            },
            'underwater': {
                'ambient_light': {'color': '#87ceeb', 'intensity': 0.5},
                'directional_light': {'color': '#ffffff', 'intensity': 0.6, 'angle': 30},
                'point_lights': [
                    {'color': '#20b2aa', 'intensity': 0.5, 'position': 'top'},
                    {'color': '#00ced1', 'intensity': 0.3, 'position': 'random'}
                ]
            }
        }
        
        return lighting_setups.get(theme, lighting_setups['fantasy'])
    
    def _create_particle_systems(self, theme: str) -> List[Dict[str, Any]]:
        """Create particle effect systems"""
        particle_systems = []
        
        if theme == 'fantasy':
            particle_systems = [
                {
                    'name': 'magical_sparkles',
                    'particle_count': 50,
                    'emission_rate': 10,
                    'lifetime': 3.0,
                    'color': '#ffd700',
                    'size': 2,
                    'movement': 'float_up',
                    'fade': True
                },
                {
                    'name': 'mystical_aura',
                    'particle_count': 20,
                    'emission_rate': 5,
                    'lifetime': 5.0,
                    'color': '#9370db',
                    'size': 4,
                    'movement': 'orbit',
                    'fade': True
                }
            ]
        elif theme == 'space':
            particle_systems = [
                {
                    'name': 'cosmic_dust',
                    'particle_count': 100,
                    'emission_rate': 20,
                    'lifetime': 10.0,
                    'color': '#ffffff',
                    'size': 1,
                    'movement': 'drift',
                    'fade': False
                },
                {
                    'name': 'energy_trails',
                    'particle_count': 30,
                    'emission_rate': 8,
                    'lifetime': 2.0,
                    'color': '#00ffff',
                    'size': 3,
                    'movement': 'streak',
                    'fade': True
                }
            ]
        elif theme == 'underwater':
            particle_systems = [
                {
                    'name': 'bubble_stream',
                    'particle_count': 40,
                    'emission_rate': 12,
                    'lifetime': 4.0,
                    'color': '#87ceeb',
                    'size': 3,
                    'movement': 'rise',
                    'fade': True
                },
                {
                    'name': 'water_sparkles',
                    'particle_count': 25,
                    'emission_rate': 6,
                    'lifetime': 3.0,
                    'color': '#ffffff',
                    'size': 2,
                    'movement': 'shimmer',
                    'fade': True
                }
            ]
        
        return particle_systems
    
    def _create_audio_atmosphere(self, theme: str) -> Dict[str, Any]:
        """Create audio atmosphere specification"""
        audio_atmospheres = {
            'fantasy': {
                'ambient_sounds': ['forest_ambience', 'magical_chimes', 'distant_spells'],
                'music_style': 'orchestral_fantasy',
                'sound_effects': ['magic_sparkle', 'mystical_whoosh', 'fairy_chime'],
                'volume_levels': {'ambient': 0.3, 'music': 0.5, 'effects': 0.7}
            },
            'space': {
                'ambient_sounds': ['space_ambience', 'distant_stars', 'cosmic_hum'],
                'music_style': 'electronic_ambient',
                'sound_effects': ['laser_zap', 'energy_pulse', 'tech_beep'],
                'volume_levels': {'ambient': 0.4, 'music': 0.6, 'effects': 0.8}
            },
            'underwater': {
                'ambient_sounds': ['ocean_depths', 'bubble_streams', 'whale_songs'],
                'music_style': 'flowing_ambient',
                'sound_effects': ['bubble_pop', 'water_splash', 'sonar_ping'],
                'volume_levels': {'ambient': 0.5, 'music': 0.4, 'effects': 0.6}
            }
        }
        
        return audio_atmospheres.get(theme, audio_atmospheres['fantasy'])
    
    def _create_interactive_elements(self, theme: str) -> List[Dict[str, Any]]:
        """Create interactive environmental elements"""
        interactive_elements = []
        
        if theme == 'fantasy':
            interactive_elements = [
                {'type': 'magical_portal', 'effect': 'teleport', 'visual': 'swirling_energy'},
                {'type': 'enchanted_tree', 'effect': 'power_boost', 'visual': 'glowing_leaves'},
                {'type': 'crystal_formation', 'effect': 'score_bonus', 'visual': 'pulsing_light'}
            ]
        elif theme == 'space':
            interactive_elements = [
                {'type': 'wormhole', 'effect': 'teleport', 'visual': 'space_distortion'},
                {'type': 'energy_station', 'effect': 'recharge', 'visual': 'electric_arcs'},
                {'type': 'alien_artifact', 'effect': 'special_ability', 'visual': 'alien_glow'}
            ]
        elif theme == 'underwater':
            interactive_elements = [
                {'type': 'current_stream', 'effect': 'speed_boost', 'visual': 'flowing_water'},
                {'type': 'air_bubble', 'effect': 'life_restore', 'visual': 'rising_bubbles'},
                {'type': 'coral_garden', 'effect': 'hiding_spot', 'visual': 'swaying_coral'}
            ]
        
        return interactive_elements
    
    def _create_responsive_adaptations(self, theme: str) -> Dict[str, Any]:
        """Create responsive design adaptations"""
        return {
            'mobile_optimizations': {
                'reduce_particles': True,
                'simplify_backgrounds': True,
                'larger_touch_targets': True,
                'optimized_animations': True
            },
            'performance_scaling': {
                'low_end_devices': {
                    'particle_count_multiplier': 0.5,
                    'animation_complexity': 'simple',
                    'background_layers': 2
                },
                'high_end_devices': {
                    'particle_count_multiplier': 1.5,
                    'animation_complexity': 'complex',
                    'background_layers': 5
                }
            },
            'accessibility_features': {
                'high_contrast_mode': True,
                'reduced_motion_mode': True,
                'colorblind_friendly_palette': True
            }
        }

# Global instance for easy importing
visual_generator = VisualThemeGenerator()
