#!/usr/bin/env python3
"""
Obsidian Entity Manager for Scrantenna
Integrates entity extraction with Obsidian vault for knowledge accumulation.
"""

import json
import os
import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from difflib import SequenceMatcher


class ObsidianEntityManager:
    """Manages entity knowledge base using Obsidian vault structure."""
    
    def __init__(self, vault_path: str = "../entities"):
        self.vault_path = Path(vault_path)
        self.templates_path = self.vault_path / "templates"
        self.known_entities = self._load_known_entities()
        
    def _load_known_entities(self) -> Dict[str, Dict]:
        """Load all known entities from vault for resolution."""
        known_entities = {}
        
        for entity_file in self.vault_path.rglob("*.md"):
            # Skip template and meta files
            if "templates" in str(entity_file) or "meta" in str(entity_file) or "dashboards" in str(entity_file):
                continue
                
            try:
                metadata = self._parse_front_matter(entity_file)
                if metadata and 'name' in metadata:
                    known_entities[metadata['name'].lower()] = {
                        'file_path': entity_file,
                        'metadata': metadata,
                        'canonical_name': metadata['name'],
                        'aliases': metadata.get('aliases', []),
                        'search_patterns': metadata.get('search_patterns', []),
                        'entity_type': metadata.get('entity_type', 'UNKNOWN')
                    }
                    
                    # Add aliases to lookup
                    for alias in metadata.get('aliases', []):
                        known_entities[alias.lower()] = known_entities[metadata['name'].lower()]
                        
            except Exception as e:
                print(f"Error loading entity {entity_file}: {e}")
                
        return known_entities
    
    def _parse_front_matter(self, file_path: Path) -> Optional[Dict]:
        """Parse YAML front matter from markdown file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if content.startswith('---'):
                # Find the end of front matter
                end_marker = content.find('---', 3)
                if end_marker != -1:
                    front_matter = content[3:end_marker].strip()
                    return yaml.safe_load(front_matter)
        except Exception as e:
            print(f"Error parsing front matter from {file_path}: {e}")
        
        return None
    
    def resolve_entities(self, extracted_entities: List[Dict]) -> List[Dict]:
        """Resolve extracted entities against known entity vault."""
        resolved_entities = []
        
        for entity in extracted_entities:
            entity_name = entity.get('name', '').strip()
            entity_type = entity.get('type', 'UNKNOWN')
            
            if not entity_name:
                continue
                
            # Try to match against known entities
            resolved_entity = self._match_known_entity(entity_name, entity_type)
            
            if resolved_entity:
                # Update existing entity
                self._update_entity_file(resolved_entity['file_path'], entity)
                resolved_entities.append({
                    'name': resolved_entity['canonical_name'],
                    'type': resolved_entity['entity_type'],
                    'confidence': entity.get('confidence', 0.8),
                    'file_path': str(resolved_entity['file_path']),
                    'matched_alias': entity_name if entity_name != resolved_entity['canonical_name'] else None,
                    'resolution_method': 'known_entity'
                })
            else:
                # Create new entity
                new_entity_path = self._create_new_entity(entity_name, entity_type, entity)
                if new_entity_path:
                    resolved_entities.append({
                        'name': entity_name,
                        'type': entity_type,
                        'confidence': entity.get('confidence', 0.5),
                        'file_path': str(new_entity_path),
                        'resolution_method': 'new_entity'
                    })
        
        return resolved_entities
    
    def _match_known_entity(self, entity_name: str, entity_type: str) -> Optional[Dict]:
        """Match entity against known entities using various strategies."""
        entity_lower = entity_name.lower()
        
        # Strategy 1: Exact match
        if entity_lower in self.known_entities:
            known = self.known_entities[entity_lower]
            if known['entity_type'] == entity_type or entity_type == 'UNKNOWN':
                return known
        
        # Strategy 2: Pattern matching
        for known_name, known_data in self.known_entities.items():
            if known_data['entity_type'] != entity_type and entity_type != 'UNKNOWN':
                continue
                
            # Check search patterns
            for pattern in known_data.get('search_patterns', []):
                if re.search(pattern, entity_name, re.IGNORECASE):
                    return known_data
        
        # Strategy 3: Fuzzy matching
        best_match = None
        best_score = 0.8  # Minimum similarity threshold
        
        for known_name, known_data in self.known_entities.items():
            if known_data['entity_type'] != entity_type and entity_type != 'UNKNOWN':
                continue
                
            # Check against canonical name and aliases
            candidates = [known_data['canonical_name']] + known_data.get('aliases', [])
            
            for candidate in candidates:
                similarity = SequenceMatcher(None, entity_lower, candidate.lower()).ratio()
                if similarity > best_score:
                    best_score = similarity
                    best_match = known_data
        
        return best_match
    
    def _update_entity_file(self, file_path: Path, new_entity_data: Dict):
        """Update existing entity file with new mention data."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse front matter
            if content.startswith('---'):
                end_marker = content.find('---', 3)
                if end_marker != -1:
                    front_matter_text = content[3:end_marker].strip()
                    front_matter = yaml.safe_load(front_matter_text)
                    body = content[end_marker + 3:]
                    
                    # Update metadata
                    front_matter['mention_count'] = front_matter.get('mention_count', 0) + 1
                    front_matter['last_mentioned'] = datetime.now().strftime('%Y-%m-%d')
                    
                    # Add new alias if different
                    new_name = new_entity_data.get('name', '')
                    if (new_name and 
                        new_name != front_matter.get('name') and 
                        new_name not in front_matter.get('aliases', [])):
                        aliases = front_matter.get('aliases', [])
                        aliases.append(new_name)
                        front_matter['aliases'] = aliases
                    
                    # Update confidence if higher
                    new_confidence = new_entity_data.get('confidence', 0.5)
                    if new_confidence > front_matter.get('confidence', 0.5):
                        front_matter['confidence'] = new_confidence
                    
                    # Write updated file
                    new_content = "---\n" + yaml.dump(front_matter, default_flow_style=False) + "---" + body
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                        
        except Exception as e:
            print(f"Error updating entity file {file_path}: {e}")
    
    def _create_new_entity(self, entity_name: str, entity_type: str, entity_data: Dict) -> Optional[Path]:
        """Create new entity file from template."""
        try:
            # Determine entity category and template
            template_name, subfolder = self._get_template_and_folder(entity_type)
            template_path = self.templates_path / template_name
            
            if not template_path.exists():
                print(f"Template not found: {template_path}")
                return None
            
            # Load template
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Prepare template variables
            template_vars = {
                'entity_name': entity_name,
                'entity_type': entity_type,
                'confidence_score': entity_data.get('confidence', 0.5),
                'first_mentioned_date': datetime.now().strftime('%Y-%m-%d'),
                'last_mentioned_date': datetime.now().strftime('%Y-%m-%d'),
                'mention_count': 1,
                'last_updated_date': datetime.now().strftime('%Y-%m-%d'),
                'current_month': datetime.now().strftime('%B'),
                'current_year': datetime.now().strftime('%Y'),
                # Default values for template placeholders
                'entity_category': self._get_entity_category(entity_type),
                'official_title': '',
                'primary_location': 'Scranton',
                'primary_organization': '',
                'bio_summary': '',
                'relationship_target': '',
                'relationship_type': '',
                'relationship_confidence': 0.5,
                'source_url': '',
                'article_title': '',
                'article_date': datetime.now().strftime('%Y-%m-%d'),
                'article_mentions': 1,
                'recent_date': datetime.now().strftime('%Y-%m-%d'),
                'recent_activity_description': f"First mentioned in news article",
                'project_name': '',
                'project_description': '',
            }
            
            # Replace template variables
            content = template_content
            for var, value in template_vars.items():
                content = content.replace('{{' + var + '}}', str(value))
            
            # Create file path
            file_name = self._slugify(entity_name) + '.md'
            entity_path = self.vault_path / subfolder / file_name
            
            # Ensure directory exists
            entity_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(entity_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Created new entity: {entity_path}")
            return entity_path
            
        except Exception as e:
            print(f"Error creating new entity {entity_name}: {e}")
            return None
    
    def _get_template_and_folder(self, entity_type: str) -> Tuple[str, str]:
        """Get template filename and subfolder for entity type."""
        type_mapping = {
            'PERSON': ('person-template.md', 'people'),
            'LOCATION': ('location-template.md', 'locations'),
            'ORGANIZATION': ('organization-template.md', 'organizations'),
            'WORK': ('work-template.md', 'works/movies'),
            'EVENT': ('work-template.md', 'events'),  # Reuse work template for events
        }
        
        return type_mapping.get(entity_type, ('person-template.md', 'people'))
    
    def _get_entity_category(self, entity_type: str) -> str:
        """Get category tag for entity type."""
        category_mapping = {
            'PERSON': 'person',
            'LOCATION': 'location', 
            'ORGANIZATION': 'organization',
            'WORK': 'work',
            'EVENT': 'event'
        }
        
        return category_mapping.get(entity_type, 'unknown')
    
    def _slugify(self, text: str) -> str:
        """Convert text to filename-safe slug."""
        # Convert to lowercase and replace spaces/special chars with hyphens
        slug = re.sub(r'[^\w\s-]', '', text.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    def create_entity_relationships(self, relationships: List[Dict], entity_map: Dict[str, str]):
        """Add relationships between entities in the vault."""
        for rel in relationships:
            from_entity = rel.get('from')
            to_entity = rel.get('to')
            rel_type = rel.get('type', 'RELATED_TO')
            confidence = rel.get('confidence', 0.5)
            
            if from_entity in entity_map and to_entity in entity_map:
                from_file = Path(entity_map[from_entity])
                to_file = Path(entity_map[to_entity])
                
                # Add relationship to both entities
                self._add_relationship_to_file(from_file, to_entity, rel_type, confidence)
                
                # Add reverse relationship (if appropriate)
                reverse_rel = self._get_reverse_relationship(rel_type)
                if reverse_rel:
                    self._add_relationship_to_file(to_file, from_entity, reverse_rel, confidence)
    
    def _add_relationship_to_file(self, file_path: Path, target_entity: str, rel_type: str, confidence: float):
        """Add a relationship to an entity file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if content.startswith('---'):
                end_marker = content.find('---', 3)
                if end_marker != -1:
                    front_matter_text = content[3:end_marker].strip()
                    front_matter = yaml.safe_load(front_matter_text)
                    body = content[end_marker + 3:]
                    
                    # Add relationship
                    relationships = front_matter.get('relationships', [])
                    
                    # Check if relationship already exists
                    existing = False
                    for rel in relationships:
                        if (rel.get('target') == f"[[{target_entity}]]" and 
                            rel.get('type') == rel_type):
                            existing = True
                            break
                    
                    if not existing:
                        relationships.append({
                            'target': f"[[{target_entity}]]",
                            'type': rel_type,
                            'confidence': confidence
                        })
                        front_matter['relationships'] = relationships
                        
                        # Write updated file
                        new_content = "---\n" + yaml.dump(front_matter, default_flow_style=False) + "---" + body
                        
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                            
        except Exception as e:
            print(f"Error adding relationship to {file_path}: {e}")
    
    def _get_reverse_relationship(self, rel_type: str) -> Optional[str]:
        """Get reverse relationship type if applicable."""
        reverse_mapping = {
            'MAYOR_OF': 'HAS_MAYOR',
            'COMMISSIONER_OF': 'HAS_COMMISSIONER',
            'WORKS_FOR': 'EMPLOYS',
            'LEADS': 'LED_BY',
            'OVERSEES': 'OVERSEEN_BY',
            'LOCATED_IN': 'CONTAINS',
            'STARS_IN': 'FEATURES',
            'APPEARS_IN': 'FEATURES',
            'FILMED_AT': 'FILMING_LOCATION_FOR',
        }
        
        return reverse_mapping.get(rel_type)
    
    def get_entity_statistics(self) -> Dict:
        """Get statistics about the entity vault."""
        stats = {
            'total_entities': len(self.known_entities),
            'by_type': {},
            'high_confidence': 0,
            'low_confidence': 0,
            'total_relationships': 0
        }
        
        for entity_data in self.known_entities.values():
            if 'canonical_name' in entity_data:  # Avoid counting aliases
                entity_type = entity_data['entity_type']
                stats['by_type'][entity_type] = stats['by_type'].get(entity_type, 0) + 1
                
                confidence = entity_data['metadata'].get('confidence', 0.5)
                if confidence >= 0.8:
                    stats['high_confidence'] += 1
                elif confidence < 0.6:
                    stats['low_confidence'] += 1
                
                relationships = entity_data['metadata'].get('relationships', [])
                stats['total_relationships'] += len(relationships)
        
        return stats


# Integration function for use with existing pipeline
def integrate_with_obsidian(extracted_entities: List[Dict], extracted_relationships: List[Dict]) -> Dict:
    """
    Integrate extracted entities and relationships with Obsidian vault.
    
    Args:
        extracted_entities: List of entities from extraction pipeline
        extracted_relationships: List of relationships from extraction pipeline
    
    Returns:
        Dictionary with resolved entities and statistics
    """
    manager = ObsidianEntityManager()
    
    # Resolve entities against known vault
    resolved_entities = manager.resolve_entities(extracted_entities)
    
    # Create entity name to file path mapping
    entity_map = {entity['name']: entity['file_path'] for entity in resolved_entities}
    
    # Add relationships between entities
    manager.create_entity_relationships(extracted_relationships, entity_map)
    
    # Get vault statistics
    stats = manager.get_entity_statistics()
    
    return {
        'resolved_entities': resolved_entities,
        'vault_statistics': stats,
        'entity_files': entity_map
    }


if __name__ == "__main__":
    # Test the entity manager
    manager = ObsidianEntityManager()
    
    # Test entity resolution
    test_entities = [
        {'name': 'Mayor Cognetti', 'type': 'PERSON', 'confidence': 0.9},
        {'name': 'Ritz Theater', 'type': 'LOCATION', 'confidence': 0.8},
        {'name': 'Final Act', 'type': 'WORK', 'confidence': 0.85},
        {'name': 'New Test Person', 'type': 'PERSON', 'confidence': 0.6}
    ]
    
    resolved = manager.resolve_entities(test_entities)
    
    print("🏛️ Obsidian Entity Manager Test Results:")
    print(f"Known entities loaded: {len(manager.known_entities)}")
    print(f"Resolved entities: {len(resolved)}")
    
    for entity in resolved:
        print(f"  - {entity['name']} ({entity['type']}) - {entity['resolution_method']}")
    
    # Get vault statistics
    stats = manager.get_entity_statistics()
    print(f"\nVault Statistics: {stats}")