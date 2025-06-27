#!/usr/bin/env python3
"""
Improved Entity and Relationship Extraction for Scrantenna
Focus on proper NLP-based extraction with verbs as edges
"""

import re
from typing import List, Dict, Tuple
import spacy
from spacy.matcher import Matcher

class ImprovedExtractor:
    """Enhanced entity and relationship extraction using NLP."""
    
    def __init__(self):
        self.nlp = None
        self.matcher = None
        self._init_spacy()
    
    def _init_spacy(self):
        """Initialize spaCy model if available."""
        try:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
            self.matcher = Matcher(self.nlp.vocab)
            self._add_patterns()
            print("✅ spaCy model loaded successfully")
        except (OSError, ImportError):
            print("⚠️  spaCy not available, falling back to regex")
            self.nlp = None
    
    def _add_patterns(self):
        """Add custom patterns for entity recognition."""
        if not self.matcher:
            return
            
        # Pattern for proper names (First Last)
        name_pattern = [{"POS": "PROPN"}, {"POS": "PROPN"}]
        self.matcher.add("PERSON_NAME", [name_pattern])
        
        # Pattern for titles + names
        title_pattern = [
            {"LOWER": {"IN": ["mayor", "judge", "commissioner", "rep", "dr", "president"]}},
            {"POS": "PROPN"},
            {"POS": "PROPN", "OP": "?"}
        ]
        self.matcher.add("TITLED_PERSON", [title_pattern])
        
        # Pattern for organizations
        org_pattern = [
            {"POS": "PROPN", "OP": "+"},
            {"LOWER": {"IN": ["company", "corporation", "inc", "llc", "department", "office", "service"]}}
        ]
        self.matcher.add("ORGANIZATION", [org_pattern])
    
    def extract_entities_and_relationships(self, text: str) -> Tuple[List[Dict], List[Dict]]:
        """Extract both entities and relationships from text."""
        if self.nlp:
            return self._spacy_extract(text)
        else:
            return self._regex_extract(text)
    
    def _spacy_extract(self, text: str) -> Tuple[List[Dict], List[Dict]]:
        """Extract using spaCy NLP."""
        doc = self.nlp(text)
        entities = []
        relationships = []
        seen_entities = set()
        
        # Extract named entities
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG", "GPE", "EVENT", "WORK_OF_ART", "LAW"]:
                clean_name = ent.text.strip()
                if len(clean_name) > 2 and clean_name.lower() not in seen_entities:
                    entity_type = self._map_spacy_type(ent.label_)
                    entities.append({
                        'name': clean_name,
                        'type': entity_type,
                        'start': ent.start,
                        'end': ent.end
                    })
                    seen_entities.add(clean_name.lower())
        
        # Extract relationships using dependency parsing
        relationships = self._extract_verb_relationships(doc, entities)
        
        # Always include Scranton if mentioned
        if 'scranton' in text.lower() and 'scranton' not in seen_entities:
            entities.append({'name': 'Scranton', 'type': 'LOCATION'})
        
        return entities, relationships
    
    def _extract_verb_relationships(self, doc, entities) -> List[Dict]:
        """Extract relationships using verbs as edges."""
        relationships = []
        entity_spans = {(e['start'], e['end']): e for e in entities if 'start' in e}
        
        # Look for Subject-Verb-Object patterns
        for token in doc:
            if token.pos_ == "VERB" and token.dep_ in ["ROOT", "conj"]:
                # Find subject
                subject = None
                for child in token.children:
                    if child.dep_ in ["nsubj", "nsubjpass"]:
                        subject = self._find_entity_for_token(child, entity_spans)
                        break
                
                # Find object
                obj = None
                for child in token.children:
                    if child.dep_ in ["dobj", "pobj", "attr"]:
                        obj = self._find_entity_for_token(child, entity_spans)
                        break
                
                # Create relationship if both subject and object found
                if subject and obj and subject['name'] != obj['name']:
                    rel_type = self._get_relationship_type(token.lemma_)
                    relationships.append({
                        'from': subject['name'],
                        'to': obj['name'],
                        'type': rel_type,
                        'verb': token.lemma_
                    })
        
        return relationships
    
    def _find_entity_for_token(self, token, entity_spans):
        """Find entity that contains this token."""
        for (start, end), entity in entity_spans.items():
            if start <= token.i < end:
                return entity
        return None
    
    def _get_relationship_type(self, verb: str) -> str:
        """Map verbs to relationship types."""
        verb_mapping = {
            'announce': 'ANNOUNCED',
            'say': 'SAID',
            'join': 'JOINED',
            'work': 'WORKS_FOR',
            'live': 'LIVES_IN',
            'locate': 'LOCATED_IN',
            'sue': 'SUED',
            'charge': 'CHARGED',
            'sentence': 'SENTENCED',
            'arrest': 'ARRESTED',
            'lead': 'LEADS',
            'manage': 'MANAGES',
            'own': 'OWNS',
            'visit': 'VISITED',
            'meet': 'MET_WITH',
            'discuss': 'DISCUSSED',
            'create': 'CREATED',
            'build': 'BUILT',
            'destroy': 'DESTROYED'
        }
        return verb_mapping.get(verb.lower(), 'RELATED_TO')
    
    def _map_spacy_type(self, spacy_type: str) -> str:
        """Map spaCy entity types to our schema."""
        mapping = {
            'PERSON': 'PERSON',
            'ORG': 'ORGANIZATION', 
            'GPE': 'LOCATION',  # Geopolitical entity
            'EVENT': 'EVENT',
            'WORK_OF_ART': 'WORK',
            'LAW': 'WORK',
            'FACILITY': 'LOCATION',
            'LOC': 'LOCATION'
        }
        return mapping.get(spacy_type, 'OTHER')
    
    def _regex_extract(self, text: str) -> Tuple[List[Dict], List[Dict]]:
        """Fallback regex extraction with improved patterns."""
        entities = []
        relationships = []
        seen = set()
        
        # Improved person extraction
        person_patterns = [
            # Specific known patterns first
            r'\b(Mayor\s+(?:Paige\s+)?(?:Gebhardt\s+)?Cognetti)\b',
            r'\b(Judge\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
            r'\b(Commissioner\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
            r'\b(Rep\.\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
            # Generic proper names (First Last)
            r'\b([A-Z][a-z]{2,}\s+[A-Z][a-z]{2,})\b',
            # Three part names
            r'\b([A-Z][a-z]+\s+[A-Z]\.\s+[A-Z][a-z]+)\b'
        ]
        
        for pattern in person_patterns:
            for match in re.finditer(pattern, text):
                name = match.group(1)
                # Clean up titles
                clean_name = re.sub(r'^(Mayor|Judge|Commissioner|Rep\.)\s+', '', name)
                
                if (clean_name and len(clean_name) > 3 and 
                    clean_name.lower() not in seen and
                    not self._is_false_positive_person(clean_name)):
                    entities.append({'name': clean_name, 'type': 'PERSON'})
                    seen.add(clean_name.lower())
        
        # Improved location extraction
        location_patterns = [
            r'\b(Scranton)\b',
            r'\b(Pennsylvania)\b',
            r'\b(Lackawanna\s+County)\b',
            r'\b([A-Z][a-z]+\s+(?:Street|Avenue|Road|Boulevard|Drive|Lane))\b',
            r'\b([A-Z][a-z]+\s+(?:Hall|Theater|Theatre|Field|Park|Lake))\b',
            r'\b(Ritz\s+Theater)\b',
            r'\b(Weston\s+Field)\b',
            r'\b(City\s+Hall)\b'
        ]
        
        for pattern in location_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                name = match.group(1)
                if name and name.lower() not in seen:
                    entities.append({'name': name, 'type': 'LOCATION'})
                    seen.add(name.lower())
        
        # Organization extraction
        org_patterns = [
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Department|Office|Service|Company|Corporation|Inc|LLC))\b',
            r'\b(National\s+Weather\s+Service)\b',
            r'\b(Dunder.?Mifflin\s+Paper\s+Company)\b',
            r'\b([A-Z]{2,5})\b'  # Acronyms
        ]
        
        for pattern in org_patterns:
            for match in re.finditer(pattern, text):
                name = match.group(1)
                if (name and len(name) > 2 and 
                    name.lower() not in seen and
                    not self._is_false_positive_org(name)):
                    entities.append({'name': name, 'type': 'ORGANIZATION'})
                    seen.add(name.lower())
        
        # Extract verb-based relationships
        relationships = self._extract_regex_relationships(text, entities)
        
        return entities, relationships
    
    def _extract_regex_relationships(self, text: str, entities: List[Dict]) -> List[Dict]:
        """Extract relationships using verb patterns."""
        relationships = []
        entity_names = [e['name'] for e in entities]
        
        # Verb-based relationship patterns
        verb_patterns = [
            (r'([A-Z][a-z\s]+?)\s+(announced|said|stated|declared)\s+', 'ANNOUNCED'),
            (r'([A-Z][a-z\s]+?)\s+(joined|joins)\s+([A-Z][a-z\s]+)', 'JOINED'),
            (r'([A-Z][a-z\s]+?)\s+(?:sued|filed\s+lawsuit\s+against)\s+([A-Z][a-z\s]+)', 'SUED'),
            (r'([A-Z][a-z\s]+?)\s+(?:sentenced|charged)\s+([A-Z][a-z\s]+)', 'LEGAL_ACTION'),
            (r'([A-Z][a-z\s]+?)\s+(?:works?\s+(?:for|at)|employed\s+by)\s+([A-Z][a-z\s]+)', 'WORKS_FOR'),
            (r'([A-Z][a-z\s]+?)\s+(?:in|at)\s+(Scranton|Pennsylvania)', 'LOCATED_IN'),
            (r'([A-Z][a-z\s]+?)\s+(?:owns?|manages?|leads?)\s+([A-Z][a-z\s]+)', 'MANAGES'),
            (r'([A-Z][a-z\s]+?)\s+(?:met\s+with|discussed\s+with)\s+([A-Z][a-z\s]+)', 'MET_WITH')
        ]
        
        for pattern, rel_type in verb_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                if len(match.groups()) >= 2:
                    subj = match.group(1).strip()
                    obj = match.group(2).strip() if len(match.groups()) > 1 else "Scranton"
                    
                    # Find matching entities
                    subj_entity = self._find_matching_entity_name(subj, entity_names)
                    obj_entity = self._find_matching_entity_name(obj, entity_names)
                    
                    if subj_entity and obj_entity and subj_entity != obj_entity:
                        relationships.append({
                            'from': subj_entity,
                            'to': obj_entity,
                            'type': rel_type
                        })
        
        return relationships
    
    def _find_matching_entity_name(self, text: str, entity_names: List[str]) -> str:
        """Find entity name that matches or contains the text."""
        text_lower = text.lower().strip()
        
        # Exact match
        for name in entity_names:
            if name.lower() == text_lower:
                return name
        
        # Partial match
        for name in entity_names:
            if (text_lower in name.lower() or name.lower() in text_lower) and len(name) > 3:
                return name
        
        return None
    
    def _is_false_positive_person(self, name: str) -> bool:
        """Check if name is likely a false positive."""
        false_positives = [
            'woman to', 'serve four', 'business email', 'hack that', 'final act',
            'paranormal horror', 'the office', 'the paper', 'popeye the',
            'slayer man', 'producer underway', 'with avaryana', 'into sending'
        ]
        return name.lower() in false_positives
    
    def _is_false_positive_org(self, name: str) -> bool:
        """Check if organization name is likely a false positive."""
        false_positives = ['the', 'and', 'for', 'with', 'from', 'but', 'not']
        return name.lower() in false_positives or len(name) < 3


# Integration function for generate_shorts.py
def create_improved_graph_data(article: Dict, index: int = 0) -> Dict:
    """
    Drop-in replacement using improved extraction
    """
    extractor = ImprovedExtractor()
    text = f"{article.get('title', '')} {article.get('description', '')}"
    
    entities, relationships = extractor.extract_entities_and_relationships(text)
    
    return {
        "entities": entities,
        "relationships": relationships,
        "method": "improved_nlp" if extractor.nlp else "improved_regex",
        "confidence": 0.8 if extractor.nlp else 0.6
    }


if __name__ == "__main__":
    # Test the improved extractor
    test_text = """
    Mayor Paige Cognetti announced a new infrastructure project in Scranton. 
    Bob Bolus sued Commissioner Bill Gaughan over the vacancy. 
    The project will be managed by the Department of Public Works.
    """
    
    extractor = ImprovedExtractor()
    entities, relationships = extractor.extract_entities_and_relationships(test_text)
    
    print("🔬 Improved Extractor Test Results:")
    print(f"\nEntities ({len(entities)}):")
    for entity in entities:
        print(f"  - {entity['name']} ({entity['type']})")
    
    print(f"\nRelationships ({len(relationships)}):")
    for rel in relationships:
        print(f"  - {rel['from']} → {rel['to']} ({rel['type']})")