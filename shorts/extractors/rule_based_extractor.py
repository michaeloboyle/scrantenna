"""Rule-based entity extractor."""
import re
from typing import List, Dict, Any, Set
from .base import EntityExtractor, Entity, Relationship, ExtractionResult

class RuleBasedExtractor(EntityExtractor):
    """Entity extractor using regex patterns and rules."""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        self.patterns = self._load_patterns()
        self.malformed_indicators = [
            'announces', 'announced', 'says', 'said', 'states', 'stated',
            'issues', 'issued', 'releases', 'released'
        ]
    
    def is_available(self) -> bool:
        """Rule-based extractor is always available."""
        return True
    
    def extract(self, text: str) -> ExtractionResult:
        """Extract entities using regex patterns."""
        if not self.validate_text(text):
            return ExtractionResult([], [], "rule_based", 0.0)
        
        entities = self._extract_entities(text)
        relationships = self._extract_relationships(text, entities)
        
        # Filter and deduplicate
        entities = self.deduplicate_entities(entities)
        entities = self.filter_entities(entities, min_confidence=0.6)
        
        # Limit results
        entities, relationships = self.limit_results(entities, relationships)
        
        confidence = 0.7 if entities else 0.0
        
        return ExtractionResult(
            entities=entities,
            relationships=relationships,
            method="rule_based",
            confidence=confidence
        )
    
    def _load_patterns(self) -> Dict[str, List[Dict]]:
        """Load entity extraction patterns."""
        return {
            'WORK': [
                {'pattern': r'\b(Final Act|V/H/S|Teen Wolf|The Walking Dead|The Caretaker)\b', 'confidence': 0.9},
                {'pattern': r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:\(film\)|\(movie\)|\(TV series\)|\(book\))\b', 'confidence': 0.8},
                {'pattern': r'\bindependent film ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', 'confidence': 0.8},
                {'pattern': r'\bmovie ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', 'confidence': 0.7},
                {'pattern': r'\bTV series ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', 'confidence': 0.7},
                {'pattern': r'\bhorror-thriller ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', 'confidence': 0.8},
            ],
            'PERSON': [
                {'pattern': r'\b(?:Mayor|Judge|Commissioner|Rep\.|Representative|Senator|Dr\.|President)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', 'confidence': 0.9},
                {'pattern': r'\b([A-Z][a-z]+\s+[A-Z][a-z]+)\s+(?:announced|said|stated|declared)\b', 'confidence': 0.8},
                {'pattern': r'\bActress\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', 'confidence': 0.8},
                {'pattern': r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})\s+\([^)]*(?:actor|actress|director|producer)[^)]*\)', 'confidence': 0.9},
                {'pattern': r'\b([A-Z][a-z]+\s+[A-Z][a-z]+)\b(?!\s+(?:Department|Office|Service|Agency|Theater|Theatre|Hall|Park|Road|Street|Avenue))', 'confidence': 0.6},
            ],
            'LOCATION': [
                {'pattern': r'\b(Scranton)\b', 'confidence': 0.9},
                {'pattern': r'\b(Pennsylvania|PA)\b', 'confidence': 0.8},
                {'pattern': r'\b(Lackawanna County)\b', 'confidence': 0.9},
                {'pattern': r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}\s+(?:Road|Street|Avenue|Drive|Lane|Boulevard|Highway))\b', 'confidence': 0.8},
                {'pattern': r'\b(Ritz Theater|City Hall)\b', 'confidence': 0.9},
                {'pattern': r'\b([A-Z][a-z]+\s+(?:Theater|Theatre|Hall|Park|Lake|River))\b(?!\s+and)', 'confidence': 0.7},
                {'pattern': r'\bfilming at the ([A-Z][a-z]+\s+(?:Theater|Theatre|Hall))\b', 'confidence': 0.8},
            ],
            'ORGANIZATION': [
                {'pattern': r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Department|Office|Service|Agency|Bureau|Administration))\b', 'confidence': 0.8},
                {'pattern': r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Company|Corporation|Inc\.|LLC|Corp\.))\b', 'confidence': 0.8},
                {'pattern': r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:University|College|School))\b', 'confidence': 0.8},
                {'pattern': r'\b(CNN|NBC|ABC|CBS|FOX|NPR|WBRE|WYOU)\b', 'confidence': 0.9},
                {'pattern': r'\b(National Weather Service|NWS)\b', 'confidence': 0.9},
                {'pattern': r'\b(FBI|CIA|NSA|EPA|FDA)\b', 'confidence': 0.9},
            ],
            'EVENT': [
                {'pattern': r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Festival|Celebration|Conference|Summit|Game|Tournament))\b', 'confidence': 0.8},
                {'pattern': r'\b(Pride Month|Memorial Day|Labor Day|Independence Day)\b', 'confidence': 0.9},
                {'pattern': r'\b(Flash Flood Warning|Flash Flood)\b', 'confidence': 0.9},
                {'pattern': r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Warning|Alert|Advisory|Emergency))\b', 'confidence': 0.8},
                {'pattern': r'\b(Weather Warning|Storm Warning|Heat Advisory)\b', 'confidence': 0.8},
            ]
        }
    
    def _extract_entities(self, text: str) -> List[Entity]:
        """Extract entities using regex patterns."""
        entities = []
        seen: Set[str] = set()
        
        # Extract quoted works first (highest priority)
        quoted_works = re.findall(r'[\'"]([^\'\"]+)[\'"]', text)
        for work in quoted_works:
            if 2 < len(work) < 50 and work.lower() not in seen and not self._is_malformed_entity(work):
                entities.append(Entity(name=work, type='WORK', confidence=0.8))
                seen.add(work.lower())
        
        # Extract parenthetical works
        paren_works = re.findall(r'\(([^)]+)\)', text)
        for work in paren_works:
            work = work.strip()
            if (2 < len(work) < 50 and 
                work.lower() not in seen and 
                not self._is_malformed_entity(work) and
                not any(word in work.lower() for word in ['wbre', 'wyou', 'news', 'weather'])):
                entities.append(Entity(name=work, type='WORK', confidence=0.7))
                seen.add(work.lower())
        
        # Apply patterns for each entity type
        for entity_type, pattern_list in self.patterns.items():
            for pattern_info in pattern_list:
                pattern = pattern_info['pattern']
                confidence = pattern_info['confidence']
                
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    name = match.group(1) if len(match.groups()) > 0 else match.group(0)
                    name = name.strip()
                    
                    if self._is_valid_entity(name, entity_type, seen):
                        entities.append(Entity(name=name, type=entity_type, confidence=confidence))
                        seen.add(name.lower())
        
        # Always include Scranton if mentioned and not present
        if 'scranton' not in seen and 'Scranton' in text:
            entities.append(Entity(name='Scranton', type='LOCATION', confidence=0.9))
        
        return entities
    
    def _extract_relationships(self, text: str, entities: List[Entity]) -> List[Relationship]:
        """Extract relationships using pattern matching."""
        relationships = []
        entity_lookup = {e.name.lower(): e for e in entities}
        
        # Relationship patterns
        patterns = [
            (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:announced|declared|stated|said)', 'ANNOUNCED'),
            (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:from|of)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'MEMBER_OF'),
            (r'(?:in|at|located\s+in|based\s+in)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'LOCATED_IN'),
            (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:in|at)\s+(Scranton|Pennsylvania)', 'LOCATED_IN'),
            (r'(filming|shooting|recorded)\s+(?:in|at)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'OCCURS_AT'),
            (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:joined|stars\s+in|appears\s+in|cast\s+in)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'PARTICIPATES_IN'),
            (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:directed|produced|created)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'CREATED'),
            (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:issued|released)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'ISSUED'),
        ]
        
        for pattern, rel_type in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                if len(match.groups()) >= 2:
                    from_name = match.group(1).strip()
                    to_name = match.group(2).strip()
                    
                    # Check if both entities exist
                    if (from_name.lower() in entity_lookup and 
                        to_name.lower() in entity_lookup):
                        relationships.append(Relationship(
                            from_entity=from_name,
                            to_entity=to_name,
                            type=rel_type,
                            confidence=0.7
                        ))
        
        return relationships[:10]  # Limit relationships
    
    def _is_valid_entity(self, name: str, entity_type: str, seen: Set[str]) -> bool:
        """Check if entity is valid for extraction."""
        if not name or len(name) < 3 or name.lower() in seen:
            return False
        
        if self._is_malformed_entity(name):
            return False
        
        # Type-specific filters
        if entity_type == 'PERSON':
            invalid_words = [
                'service', 'county', 'office', 'department', 'road', 'street',
                'announces', 'announced', 'underway', 'producer', 'actress',
                'horror', 'filming', 'project', 'infrastructure', 'paranormal'
            ]
            if any(word in name.lower() for word in invalid_words):
                return False
        
        elif entity_type == 'LOCATION':
            if (len(name.split()) > 6 or 
                any(word in name.lower() for word in ['million', 'project', 'improvement', 'targeting'])):
                return False
        
        return True
    
    def _is_malformed_entity(self, name: str) -> bool:
        """Check if an entity name looks malformed or like a concatenated phrase."""
        return any(verb in name.lower() for verb in self.malformed_indicators)