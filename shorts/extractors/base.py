"""Base classes for entity extraction."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class Entity:
    """Represents an extracted entity."""
    name: str
    type: str
    confidence: float = 1.0
    aliases: List[str] = None
    
    def __post_init__(self):
        if self.aliases is None:
            self.aliases = []

@dataclass
class Relationship:
    """Represents a relationship between entities."""
    from_entity: str
    to_entity: str
    type: str
    verb: str = ""
    confidence: float = 1.0

@dataclass
class ExtractionResult:
    """Result of entity extraction."""
    entities: List[Entity]
    relationships: List[Relationship]
    method: str
    confidence: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format for JSON serialization."""
        return {
            "entities": [
                {
                    "name": e.name,
                    "type": e.type,
                    "confidence": e.confidence,
                    "aliases": e.aliases
                }
                for e in self.entities
            ],
            "relationships": [
                {
                    "from": r.from_entity,
                    "to": r.to_entity,
                    "type": r.type,
                    "verb": r.verb,
                    "confidence": r.confidence
                }
                for r in self.relationships
            ],
            "method": self.method,
            "confidence": self.confidence
        }

class EntityExtractor(ABC):
    """Abstract base class for entity extractors."""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.name = self.__class__.__name__
    
    @abstractmethod
    def extract(self, text: str) -> ExtractionResult:
        """Extract entities and relationships from text.
        
        Args:
            text: Input text to process
            
        Returns:
            ExtractionResult containing entities, relationships, and metadata
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if this extractor is available/configured properly."""
        pass
    
    def validate_text(self, text: str) -> bool:
        """Validate input text."""
        return isinstance(text, str) and len(text.strip()) > 0
    
    def filter_entities(self, entities: List[Entity], min_confidence: float = 0.5) -> List[Entity]:
        """Filter entities by confidence threshold."""
        return [e for e in entities if e.confidence >= min_confidence]
    
    def deduplicate_entities(self, entities: List[Entity]) -> List[Entity]:
        """Remove duplicate entities based on name similarity."""
        seen = set()
        unique_entities = []
        
        for entity in entities:
            # Use lowercase name as key for deduplication
            key = entity.name.lower().strip()
            if key not in seen and len(key) > 2:
                seen.add(key)
                unique_entities.append(entity)
        
        return unique_entities
    
    def limit_results(self, entities: List[Entity], relationships: List[Relationship], 
                     max_entities: int = 10, max_relationships: int = 15) -> tuple:
        """Limit the number of results."""
        return entities[:max_entities], relationships[:max_relationships]