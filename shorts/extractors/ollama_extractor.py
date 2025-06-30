"""Ollama-based entity extractor."""
import json
import re
from typing import List, Dict, Any
from .base import EntityExtractor, Entity, Relationship, ExtractionResult

class OllamaExtractor(EntityExtractor):
    """Entity extractor using Ollama local LLM."""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.model = self.config.get('model', 'phi3:mini')
        self.temperature = self.config.get('temperature', 0.1)
        self.max_tokens = self.config.get('max_tokens', 300)
        self._ollama = None
    
    def is_available(self) -> bool:
        """Check if Ollama is available."""
        try:
            import ollama
            self._ollama = ollama
            # Test if model is available
            ollama.show(self.model)
            return True
        except Exception:
            return False
    
    def extract(self, text: str) -> ExtractionResult:
        """Extract entities using Ollama."""
        if not self.validate_text(text):
            return ExtractionResult([], [], f"ollama_{self.model}", 0.0)
        
        if not self.is_available():
            raise RuntimeError("Ollama not available")
        
        try:
            # Extract entities
            entities = self._extract_entities(text)
            
            # Extract relationships
            relationships = self._extract_relationships(text, entities)
            
            # Calculate overall confidence
            avg_confidence = self._calculate_confidence(entities, relationships)
            
            return ExtractionResult(
                entities=entities,
                relationships=relationships,
                method=f"ollama_{self.model}",
                confidence=avg_confidence
            )
            
        except Exception as e:
            print(f"Ollama extraction failed: {e}")
            return ExtractionResult([], [], f"ollama_{self.model}", 0.0)
    
    def _extract_entities(self, text: str) -> List[Entity]:
        """Extract entities using Ollama."""
        prompt = f"""Extract named entities from this news text. Return ONLY valid JSON array format with 'name' and 'type' fields.
Entity types: PERSON, ORGANIZATION, LOCATION, WORK (movies/TV/books), EVENT

Text: {text}

Return only a JSON array with objects containing 'name' and 'type' fields. No explanations.

Examples:
- Movies/shows: {{"name": "Final Act", "type": "WORK"}}
- People: {{"name": "Hannah Fierman", "type": "PERSON"}}
- Weather: {{"name": "Flash Flood Warning", "type": "EVENT"}}

JSON:"""

        try:
            response = self._ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            )
            
            response_text = response['response']
            
            # Extract JSON from response
            json_match = re.search(r'\[.*?\]', response_text, re.DOTALL)
            if json_match:
                entities_data = json.loads(json_match.group(0))
                entities = []
                
                for entity_data in entities_data:
                    if 'name' in entity_data and 'type' in entity_data:
                        entities.append(Entity(
                            name=entity_data['name'],
                            type=entity_data['type'],
                            confidence=entity_data.get('confidence', 0.8)
                        ))
                
                return self.deduplicate_entities(entities)
            
        except Exception as e:
            print(f"Entity extraction error: {e}")
        
        return []
    
    def _extract_relationships(self, text: str, entities: List[Entity]) -> List[Relationship]:
        """Extract relationships using Ollama."""
        if not entities:
            return []
        
        entity_names = [e.name for e in entities]
        prompt = f"""Given entities: {entity_names}

Extract ALL verb-based relationships from this text. Every verb between entities should become an edge.
Return ONLY valid JSON array with 'from', 'to', 'type', 'verb' fields.

Examples:
- "Mayor Smith announced the project" → {{"from": "Smith", "to": "project", "type": "ANNOUNCED", "verb": "announced"}}
- "John works for Apple" → {{"from": "John", "to": "Apple", "type": "WORKS_FOR", "verb": "works"}}
- "Company bought building" → {{"from": "Company", "to": "building", "type": "PURCHASED", "verb": "bought"}}

Text: {text}

JSON:"""
        
        try:
            response = self._ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    "temperature": self.temperature,
                    "num_predict": 150
                }
            )
            
            response_text = response['response']
            json_match = re.search(r'\[.*?\]', response_text, re.DOTALL)
            
            if json_match:
                relationships_data = json.loads(json_match.group(0))
                relationships = []
                
                for rel_data in relationships_data:
                    if all(key in rel_data for key in ['from', 'to', 'type']):
                        relationships.append(Relationship(
                            from_entity=rel_data['from'],
                            to_entity=rel_data['to'],
                            type=rel_data['type'],
                            verb=rel_data.get('verb', ''),
                            confidence=rel_data.get('confidence', 0.7)
                        ))
                
                return relationships
                
        except Exception as e:
            print(f"Relationship extraction error: {e}")
        
        return []
    
    def _calculate_confidence(self, entities: List[Entity], relationships: List[Relationship]) -> float:
        """Calculate overall extraction confidence."""
        if not entities:
            return 0.0
        
        entity_confidences = [e.confidence for e in entities]
        relationship_confidences = [r.confidence for r in relationships] if relationships else [0.5]
        
        all_confidences = entity_confidences + relationship_confidences
        return sum(all_confidences) / len(all_confidences)