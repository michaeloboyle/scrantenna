#!/usr/bin/env python3
"""
Free LLM Entity and Relationship Extractor for Scrantenna
Provides cost-effective alternatives to OpenAI for knowledge graph generation.
"""

import json
import re
import os
from typing import List, Dict, Optional


class ProductionFreeLLMExtractor:
    """Production-ready free LLM entity/relationship extractor."""
    
    def __init__(self, ollama_model: str = "llama3.2:3b"):
        self.ollama_model = ollama_model
        self.ollama_available = self._check_ollama()
        self.hf_available = self._check_huggingface()
        self.hf_pipeline = None
        
        # Initialize HF pipeline if available
        if self.hf_available:
            self._init_hf_pipeline()
    
    def _check_ollama(self) -> bool:
        """Check if Ollama is available and model exists."""
        try:
            import ollama
            ollama.show(self.ollama_model)
            return True
        except Exception:
            return False
    
    def _check_huggingface(self) -> bool:
        """Check if HuggingFace transformers is available."""
        try:
            from transformers import pipeline
            return True
        except ImportError:
            return False
    
    def _init_hf_pipeline(self):
        """Initialize HuggingFace NER pipeline."""
        try:
            from transformers import pipeline
            self.hf_pipeline = pipeline(
                "ner",
                model="dbmdz/bert-large-cased-finetuned-conll03-english",
                aggregation_strategy="simple"
            )
        except Exception as e:
            print(f"Failed to initialize HF pipeline: {e}")
            self.hf_available = False
    
    def extract_for_article(self, article: Dict, index: int = 0) -> Dict:
        """Extract entities and relationships for a news article."""
        text = f"{article.get('title', '')} {article.get('description', '')}"
        
        # Extract entities with fallback chain
        entities = self._extract_entities_with_fallback(text)
        
        # Extract relationships with fallback chain
        relationships = self._extract_relationships_with_fallback(text, entities)
        
        # Generate SVG visualization
        svg_graph = self._generate_svg_graph(entities, relationships, index)
        
        return {
            "entities": entities,
            "relationships": relationships,
            "svg": svg_graph,
            "method": self._get_active_method(),
            "confidence": self._calculate_confidence(entities)
        }
    
    def _extract_entities_with_fallback(self, text: str) -> List[Dict]:
        """Extract entities using best available method."""
        
        # Try Ollama first (best for structured output)
        if self.ollama_available:
            try:
                entities = self._ollama_extract_entities(text)
                if entities:
                    return entities
            except Exception as e:
                print(f"Ollama extraction failed: {e}")
        
        # Try HuggingFace NER (good accuracy)
        if self.hf_available and self.hf_pipeline:
            try:
                entities = self._hf_extract_entities(text)
                if entities:
                    return entities
            except Exception as e:
                print(f"HuggingFace extraction failed: {e}")
        
        # Fallback to rule-based extraction
        return self._rule_based_entities(text)
    
    def _ollama_extract_entities(self, text: str) -> List[Dict]:
        """Extract entities using Ollama."""
        import ollama
        
        prompt = f"""Extract named entities from this news text. Return ONLY valid JSON array format with 'name' and 'type' fields.
Entity types: PERSON, ORGANIZATION, LOCATION, DATE, EVENT

Text: {text}

JSON:"""
        
        response = ollama.generate(
            model=self.ollama_model,
            prompt=prompt,
            options={
                "temperature": 0.1,
                "top_p": 0.9,
                "num_predict": 200
            }
        )
        
        # Extract JSON from response
        response_text = response['response']
        json_match = re.search(r'\[.*?\]', response_text, re.DOTALL)
        
        if json_match:
            try:
                entities = json.loads(json_match.group(0))
                # Filter and validate entities
                return self._validate_entities(entities)
            except json.JSONDecodeError:
                return []
        
        return []
    
    def _hf_extract_entities(self, text: str) -> List[Dict]:
        """Extract entities using HuggingFace NER."""
        if not self.hf_pipeline:
            return []
        
        ner_results = self.hf_pipeline(text)
        entities = []
        
        for result in ner_results:
            if result['score'] > 0.7:  # High confidence only
                entity_type = self._map_hf_entity_type(result['entity_group'])
                entities.append({
                    'name': result['word'].replace('##', ''),
                    'type': entity_type,
                    'confidence': result['score']
                })
        
        # Remove duplicates and clean
        return self._deduplicate_entities(entities)
    
    def _map_hf_entity_type(self, hf_type: str) -> str:
        """Map HuggingFace entity types to our schema."""
        mapping = {
            'PER': 'PERSON',
            'ORG': 'ORGANIZATION',
            'LOC': 'LOCATION',
            'MISC': 'OTHER'
        }
        return mapping.get(hf_type, 'OTHER')
    
    def _rule_based_entities(self, text: str) -> List[Dict]:
        """Enhanced fallback rule-based entity extraction."""
        entities = []
        seen = set()
        
        # Extract quoted works/titles first (movies, shows, etc)
        quoted_works = re.findall(r'[\'"]([^\'\"]+)[\'"]', text)
        for work in quoted_works:
            if 2 < len(work) < 50 and work not in seen:
                entities.append({'name': work, 'type': 'WORK'})
                seen.add(work.lower())
        
        # Person patterns - more specific
        person_patterns = [
            # Full names with optional middle initial
            r'\b([A-Z][a-z]+(?:\s+[A-Z]\.)?(?:\s+[A-Z][a-z]+)+)\b',
            # Titles with names
            r'\b(?:Mayor|Judge|Commissioner|Rep\.|Representative|Senator|Dr\.|President)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b',
        ]
        
        for pattern in person_patterns:
            for match in re.finditer(pattern, text):
                name = match.group(1) if match.lastindex else match.group(0)
                # Clean up titles
                name = re.sub(r'^(Mayor|Judge|Commissioner|Rep\.|Representative|Senator|Dr\.|President)\s+', '', name)
                
                # Filter out common false positives
                if (name and len(name) > 3 and 
                    name.lower() not in seen and
                    not any(word in name.lower() for word in ['service', 'county', 'office', 'department', 'road', 'street'])):
                    entities.append({'name': name, 'type': 'PERSON'})
                    seen.add(name.lower())
        
        # Location patterns
        location_patterns = [
            r'\b(Scranton)\b',
            r'\b(Pennsylvania|PA)\b',
            r'\b(Lackawanna County)\b',
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Road|Street|Avenue|Drive|Lane|Boulevard|Highway))\b',
            r'\b([A-Z][a-z]+\s+(?:Lake|River|Park|Field|Theater|Theatre|Hall))\b',
            r'\b(City Hall)\b',
        ]
        
        for pattern in location_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                name = match.group(1)
                if name and name.lower() not in seen:
                    # Normalize Pennsylvania/PA
                    if name.upper() == 'PA':
                        name = 'Pennsylvania'
                    entities.append({'name': name, 'type': 'LOCATION'})
                    seen.add(name.lower())
        
        # Organization patterns
        org_patterns = [
            # Government agencies
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Department|Office|Service|Agency|Bureau|Administration))\b',
            # Companies
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Company|Corporation|Inc\.|LLC|Corp\.))\b',
            # Universities/Schools
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:University|College|School))\b',
            # News organizations
            r'\b(CNN|NBC|ABC|CBS|FOX|NPR|WBRE|WYOU)\b',
            # Specific organizations
            r'\b(National Weather Service|NWS)\b',
            r'\b(FBI|CIA|NSA|EPA|FDA)\b',
        ]
        
        for pattern in org_patterns:
            for match in re.finditer(pattern, text):
                name = match.group(1)
                if name and name.lower() not in seen and len(name) > 2:
                    entities.append({'name': name, 'type': 'ORGANIZATION'})
                    seen.add(name.lower())
        
        # Event patterns
        event_patterns = [
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Festival|Celebration|Conference|Summit|Game|Tournament))\b',
            r'\b(Pride Month|Memorial Day|Labor Day|Independence Day)\b',
            r'\b(Flash Flood Warning)\b',
        ]
        
        for pattern in event_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                name = match.group(1)
                if name and name.lower() not in seen:
                    entities.append({'name': name, 'type': 'EVENT'})
                    seen.add(name.lower())
        
        # Always include Scranton if not present
        if 'scranton' not in seen and 'Scranton' in text:
            entities.append({'name': 'Scranton', 'type': 'LOCATION'})
        
        return entities[:10]  # Limit to 10
    
    def _extract_relationships_with_fallback(self, text: str, entities: List[Dict]) -> List[Dict]:
        """Extract relationships using best available method."""
        
        # Try Ollama for relationship extraction
        if self.ollama_available and entities:
            try:
                relationships = self._ollama_extract_relationships(text, entities)
                if relationships:
                    return relationships
            except Exception as e:
                print(f"Ollama relationship extraction failed: {e}")
        
        # Fallback to rule-based relationships
        return self._rule_based_relationships(text, entities)
    
    def _ollama_extract_relationships(self, text: str, entities: List[Dict]) -> List[Dict]:
        """Extract relationships using Ollama."""
        import ollama
        
        entity_names = [e['name'] for e in entities]
        prompt = f"""Given entities: {entity_names}

Extract ALL verb-based relationships from this text. Every verb between entities should become an edge.
Return ONLY valid JSON array with 'from', 'to', 'type', 'verb' fields.

Examples:
- "Mayor Smith announced the project" → {{"from": "Smith", "to": "project", "type": "ANNOUNCED", "verb": "announced"}}
- "John works for Apple" → {{"from": "John", "to": "Apple", "type": "WORKS_FOR", "verb": "works"}}
- "Company bought building" → {{"from": "Company", "to": "building", "type": "PURCHASED", "verb": "bought"}}

Text: {text}

JSON:"""
        
        response = ollama.generate(
            model=self.ollama_model,
            prompt=prompt,
            options={"temperature": 0.1, "num_predict": 150}
        )
        
        response_text = response['response']
        json_match = re.search(r'\[.*?\]', response_text, re.DOTALL)
        
        if json_match:
            try:
                relationships = json.loads(json_match.group(0))
                return self._validate_relationships(relationships, entities)
            except json.JSONDecodeError:
                return []
        
        return []
    
    def _rule_based_relationships(self, text: str, entities: List[Dict]) -> List[Dict]:
        """Enhanced rule-based relationship extraction using comprehensive verb patterns."""
        relationships = []
        entity_lookup = {}
        
        # Create flexible entity lookup (partial matching)
        for entity in entities:
            name = entity['name']
            entity_lookup[name.lower()] = entity
            # Also add individual words for partial matching
            words = name.split()
            if len(words) > 1:
                for word in words:
                    if len(word) > 3:  # Only meaningful words
                        entity_lookup[word.lower()] = entity
        
        # First, extract ALL verb-based relationships
        relationships.extend(self._extract_all_verb_relationships(text, entities, entity_lookup))
        
        # Enhanced relationship patterns with more comprehensive coverage
        patterns = [
            # Professional relationships
            (r'(Mayor|Judge|Commissioner|Rep\.|Representative|Senator|Dr\.|President)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'HAS_TITLE'),
            (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:announced|declared|stated|said)', 'ANNOUNCED'),
            (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:from|of)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'MEMBER_OF'),
            
            # Location relationships
            (r'(?:in|at|located\s+in|based\s+in)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'LOCATED_IN'),
            (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:in|at)\s+(Scranton|Pennsylvania)', 'LOCATED_IN'),
            (r'(filming|shooting|recorded)\s+(?:in|at)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'OCCURS_AT'),
            
            # Work/participation relationships
            (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:joined|stars\s+in|appears\s+in|cast\s+in)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'PARTICIPATES_IN'),
            (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:directed|produced|created)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'CREATED'),
            (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:plays|portrays|acts\s+as)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'PORTRAYS'),
            
            # Event relationships
            (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:during|for)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'OCCURS_DURING'),
            (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:issued|released)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'ISSUED'),
            
            # Legal/administrative relationships
            (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:sentenced|charged|arrested)', 'LEGAL_ACTION'),
            (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:sued|filed\s+lawsuit\s+against)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'LEGAL_DISPUTE'),
            
            # Educational/sports relationships
            (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:chooses|commits\s+to|signed\s+with)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'COMMITTED_TO'),
            (r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:named\s+to|selected\s+for)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', 'SELECTED_FOR'),
        ]
        
        for pattern, rel_type in patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                groups = match.groups()
                if len(groups) >= 2:
                    subj_text = groups[0].strip()
                    obj_text = groups[1].strip()
                    
                    # Find matching entities (exact or partial)
                    subj_entity = self._find_matching_entity(subj_text, entity_lookup)
                    obj_entity = self._find_matching_entity(obj_text, entity_lookup)
                    
                    if subj_entity and obj_entity and subj_entity['name'] != obj_entity['name']:
                        relationships.append({
                            'from': subj_entity['name'],
                            'to': obj_entity['name'],
                            'type': rel_type
                        })
                
                # Handle single-group patterns (like ANNOUNCED)
                elif len(groups) == 1 and rel_type in ['ANNOUNCED', 'LEGAL_ACTION']:
                    subj_text = groups[0].strip()
                    subj_entity = self._find_matching_entity(subj_text, entity_lookup)
                    
                    # Connect to Scranton for local context
                    scranton_entity = next((e for e in entities if e['name'] == 'Scranton'), None)
                    if subj_entity and scranton_entity and subj_entity['name'] != 'Scranton':
                        relationships.append({
                            'from': subj_entity['name'],
                            'to': 'Scranton',
                            'type': 'RELATES_TO'
                        })
        
        # Add geographic relationships
        for entity in entities:
            if entity['type'] == 'LOCATION' and entity['name'] != 'Scranton':
                scranton_entity = next((e for e in entities if e['name'] == 'Scranton'), None)
                if scranton_entity:
                    relationships.append({
                        'from': entity['name'],
                        'to': 'Scranton',
                        'type': 'LOCATED_NEAR'
                    })
        
        # Add organizational relationships to Scranton
        for entity in entities:
            if entity['type'] == 'ORGANIZATION' and 'scranton' in text.lower():
                scranton_entity = next((e for e in entities if e['name'] == 'Scranton'), None)
                if scranton_entity and entity['name'] != 'Scranton':
                    relationships.append({
                        'from': entity['name'],
                        'to': 'Scranton',
                        'type': 'OPERATES_IN'
                    })
        
        # Remove duplicates
        unique_relationships = []
        seen = set()
        for rel in relationships:
            key = (rel['from'], rel['to'], rel['type'])
            if key not in seen:
                seen.add(key)
                unique_relationships.append(rel)
        
        return unique_relationships[:8]  # Limit for readability
    
    def _extract_all_verb_relationships(self, text: str, entities: List[Dict], entity_lookup: Dict) -> List[Dict]:
        """Extract relationships using ALL verbs as potential edges."""
        relationships = []
        
        # Common English verbs that indicate relationships
        relationship_verbs = {
            # Action verbs
            'announced', 'said', 'stated', 'declared', 'reported', 'confirmed', 'revealed',
            'joined', 'left', 'quit', 'hired', 'fired', 'promoted', 'demoted',
            'created', 'built', 'designed', 'developed', 'launched', 'started', 'founded',
            'bought', 'sold', 'acquired', 'purchased', 'invested', 'funded', 'sponsored',
            'opened', 'closed', 'moved', 'relocated', 'expanded', 'reduced', 'increased',
            'won', 'lost', 'defeated', 'beat', 'competed', 'participated', 'attended',
            'married', 'divorced', 'dated', 'met', 'knew', 'befriended', 'partnered',
            'sued', 'charged', 'arrested', 'sentenced', 'convicted', 'accused', 'blamed',
            'elected', 'appointed', 'nominated', 'selected', 'chosen', 'picked',
            'visited', 'traveled', 'went', 'came', 'arrived', 'departed', 'returned',
            'supports', 'opposes', 'endorses', 'backs', 'promotes', 'advocates',
            'leads', 'manages', 'directs', 'supervises', 'oversees', 'heads',
            'owns', 'operates', 'runs', 'controls', 'manages', 'administers',
            'teaches', 'learns', 'studies', 'graduates', 'enrolls', 'attends',
            'works', 'serves', 'volunteers', 'helps', 'assists', 'aids',
            'lives', 'resides', 'stays', 'inhabits', 'occupies', 'dwells',
            'plays', 'performs', 'acts', 'stars', 'appears', 'features',
            'writes', 'authors', 'publishes', 'edits', 'reviews', 'critiques',
            'produces', 'directs', 'films', 'shoots', 'records', 'broadcasts'
        }
        
        # Pattern: Entity + Verb + Entity
        entity_names = [e['name'] for e in entities]
        for i, entity1 in enumerate(entities):
            for j, entity2 in enumerate(entities):
                if i >= j:  # Avoid duplicates and self-references
                    continue
                
                # Look for patterns: Entity1 verb Entity2
                for verb in relationship_verbs:
                    patterns = [
                        # Direct patterns
                        rf'\b{re.escape(entity1["name"])}\b[^.!?]*?\b{verb}s?\b[^.!?]*?\b{re.escape(entity2["name"])}\b',
                        rf'\b{re.escape(entity2["name"])}\b[^.!?]*?\b{verb}s?\b[^.!?]*?\b{re.escape(entity1["name"])}\b',
                        # Passive patterns  
                        rf'\b{re.escape(entity1["name"])}\b[^.!?]*?\bwas {verb}[ed|n]?\b[^.!?]*?\b{re.escape(entity2["name"])}\b',
                        rf'\b{re.escape(entity2["name"])}\b[^.!?]*?\bwas {verb}[ed|n]?\b[^.!?]*?\b{re.escape(entity1["name"])}\b',
                    ]
                    
                    for pattern in patterns:
                        if re.search(pattern, text, re.IGNORECASE):
                            # Determine direction based on pattern match
                            if re.search(rf'\b{re.escape(entity1["name"])}\b[^.!?]*?\b{verb}', text, re.IGNORECASE):
                                from_entity, to_entity = entity1['name'], entity2['name']
                            else:
                                from_entity, to_entity = entity2['name'], entity1['name']
                            
                            rel_type = self._normalize_verb_to_relationship(verb)
                            relationships.append({
                                'from': from_entity,
                                'to': to_entity,
                                'type': rel_type,
                                'verb': verb
                            })
                            break  # Found relationship, move to next verb
        
        return relationships
    
    def _normalize_verb_to_relationship(self, verb: str) -> str:
        """Convert verbs to normalized relationship types."""
        verb_mappings = {
            # Communication
            'announced': 'ANNOUNCED', 'said': 'SAID', 'stated': 'STATED', 'declared': 'DECLARED',
            'reported': 'REPORTED', 'confirmed': 'CONFIRMED', 'revealed': 'REVEALED',
            
            # Employment/Organization  
            'joined': 'JOINED', 'left': 'LEFT', 'hired': 'HIRED', 'fired': 'FIRED',
            'works': 'WORKS_FOR', 'serves': 'SERVES', 'leads': 'LEADS', 'manages': 'MANAGES',
            
            # Creation/Development
            'created': 'CREATED', 'built': 'BUILT', 'designed': 'DESIGNED', 'founded': 'FOUNDED',
            'developed': 'DEVELOPED', 'launched': 'LAUNCHED', 'started': 'STARTED',
            
            # Business/Finance
            'bought': 'PURCHASED', 'sold': 'SOLD', 'acquired': 'ACQUIRED', 'invested': 'INVESTED',
            'funded': 'FUNDED', 'sponsored': 'SPONSORED', 'owns': 'OWNS',
            
            # Location/Movement
            'moved': 'MOVED_TO', 'relocated': 'RELOCATED_TO', 'visited': 'VISITED',
            'lives': 'LIVES_IN', 'resides': 'RESIDES_IN', 'traveled': 'TRAVELED_TO',
            
            # Legal/Government
            'sued': 'SUED', 'charged': 'CHARGED', 'arrested': 'ARRESTED', 'elected': 'ELECTED',
            'appointed': 'APPOINTED', 'nominated': 'NOMINATED', 'sentenced': 'SENTENCED',
            
            # Social/Personal
            'married': 'MARRIED', 'met': 'MET', 'knew': 'KNEW', 'befriended': 'BEFRIENDED',
            'supports': 'SUPPORTS', 'opposes': 'OPPOSES', 'endorses': 'ENDORSES',
            
            # Performance/Arts
            'plays': 'PLAYS', 'performs': 'PERFORMS', 'stars': 'STARS_IN', 'appears': 'APPEARS_IN',
            'wrote': 'WROTE', 'produced': 'PRODUCED', 'directed': 'DIRECTED',
            
            # Competition/Achievement
            'won': 'WON', 'defeated': 'DEFEATED', 'competed': 'COMPETED_AGAINST',
            'participated': 'PARTICIPATED_IN', 'graduated': 'GRADUATED_FROM'
        }
        
        return verb_mappings.get(verb.lower(), verb.upper().replace(' ', '_'))
    
    def _find_matching_entity(self, text: str, entity_lookup: Dict) -> Optional[Dict]:
        """Find matching entity using exact or partial matching."""
        text_lower = text.lower()
        
        # Try exact match first
        if text_lower in entity_lookup:
            return entity_lookup[text_lower]
        
        # Try partial matching - find entity that contains this text or vice versa
        for key, entity in entity_lookup.items():
            if (text_lower in key or key in text_lower) and len(key) > 3:
                return entity
        
        return None
    
    def _validate_entities(self, entities: List[Dict]) -> List[Dict]:
        """Validate and clean entities."""
        valid_entities = []
        valid_types = {'PERSON', 'ORGANIZATION', 'LOCATION', 'DATE', 'EVENT', 'WORK', 'OTHER'}
        
        for entity in entities:
            if (isinstance(entity, dict) and 
                'name' in entity and 
                'type' in entity and
                entity['type'] in valid_types and
                len(entity['name']) > 2):
                valid_entities.append(entity)
        
        return self._deduplicate_entities(valid_entities)
    
    def _validate_relationships(self, relationships: List[Dict], entities: List[Dict]) -> List[Dict]:
        """Validate relationships against entities."""
        entity_names = {e['name'] for e in entities}
        valid_relationships = []
        
        for rel in relationships:
            if (isinstance(rel, dict) and 
                'from' in rel and 
                'to' in rel and 
                'type' in rel and
                rel['from'] in entity_names and
                rel['to'] in entity_names):
                valid_relationships.append(rel)
        
        return valid_relationships
    
    def _deduplicate_entities(self, entities: List[Dict]) -> List[Dict]:
        """Remove duplicate entities."""
        seen_names = set()
        unique_entities = []
        
        for entity in entities:
            name = entity['name']
            if name not in seen_names and len(name) > 2:
                unique_entities.append(entity)
                seen_names.add(name)
        
        return unique_entities
    
    def _generate_svg_graph(self, entities: List[Dict], relationships: List[Dict], index: int) -> str:
        """Generate SVG visualization of the knowledge graph."""
        if not entities:
            return '<svg width="300" height="200"><text x="150" y="100" text-anchor="middle" fill="white">No entities found</text></svg>'
        
        colors = {
            'PERSON': '#FF6B6B',
            'ORGANIZATION': '#4ECDC4',
            'LOCATION': '#45B7D1',
            'DATE': '#FFA726',
            'EVENT': '#AB47BC',
            'WORK': '#9C27B0',
            'OTHER': '#78909C'
        }
        
        svg = '<svg width="300" height="200" viewBox="0 0 300 200" class="graph-svg">'
        
        # Draw entities as circles
        for i, entity in enumerate(entities[:6]):  # Limit to 6 for layout
            x = 50 + (i % 3) * 100
            y = 50 + (i // 3) * 60
            color = colors.get(entity['type'], '#888')
            
            svg += f'<circle cx="{x}" cy="{y}" r="20" fill="{color}" stroke="white" stroke-width="2"/>'
            svg += f'<text x="{x}" y="{y-25}" text-anchor="middle" fill="white" font-size="10" font-weight="bold">{entity["name"][:8]}</text>'
            svg += f'<text x="{x}" y="{y+35}" text-anchor="middle" fill="white" font-size="8">{entity["type"]}</text>'
        
        # Draw relationships as lines
        for rel in relationships:
            from_entity = next((e for e in entities if e['name'] == rel['from']), None)
            to_entity = next((e for e in entities if e['name'] == rel['to']), None)
            
            if from_entity and to_entity:
                from_index = entities.index(from_entity)
                to_index = entities.index(to_entity)
                
                if from_index < 6 and to_index < 6:  # Only draw if both visible
                    x1 = 50 + (from_index % 3) * 100
                    y1 = 50 + (from_index // 3) * 60
                    x2 = 50 + (to_index % 3) * 100
                    y2 = 50 + (to_index // 3) * 60
                    
                    svg += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="white" stroke-width="1" opacity="0.7"/>'
                    
                    # Add relationship label
                    mid_x = (x1 + x2) // 2
                    mid_y = (y1 + y2) // 2
                    svg += f'<text x="{mid_x}" y="{mid_y}" text-anchor="middle" fill="white" font-size="8">{rel["type"]}</text>'
        
        svg += '</svg>'
        return svg
    
    def _calculate_confidence(self, entities: List[Dict]) -> float:
        """Calculate overall confidence score."""
        if not entities:
            return 0.0
        
        confidences = [e.get('confidence', 0.5) for e in entities]
        return sum(confidences) / len(confidences)
    
    def _get_active_method(self) -> str:
        """Get the active extraction method."""
        if self.ollama_available:
            return f"ollama_{self.ollama_model}"
        elif self.hf_available:
            return "huggingface_bert"
        else:
            return "rule_based"
    
    def get_method_info(self) -> Dict:
        """Get information about available methods."""
        return {
            "ollama_available": self.ollama_available,
            "ollama_model": self.ollama_model if self.ollama_available else None,
            "huggingface_available": self.hf_available,
            "active_method": self._get_active_method(),
            "cost_per_article": "$0.00",  # Free!
            "privacy_preserving": self.ollama_available or self.hf_available
        }


# Integration function for generate_shorts.py
def create_free_llm_graph_data(article: Dict, index: int = 0) -> Dict:
    """
    Drop-in replacement for generate_article_graph() in generate_shorts.py
    """
    extractor = ProductionFreeLLMExtractor()
    return extractor.extract_for_article(article, index)


if __name__ == "__main__":
    # Test the extractor with verb-heavy content
    test_article = {
        "title": "Mayor Cognetti Announces New Infrastructure Project in Scranton",
        "description": "Scranton Mayor Paige Cognetti announced a $2 million infrastructure improvement project targeting Providence Road. The Department of Public Works will manage the project. Commissioner Johnson supports the initiative. Local residents attended the meeting where Cognetti revealed the timeline."
    }
    
    extractor = ProductionFreeLLMExtractor()
    result = extractor.extract_for_article(test_article)
    
    print("🔬 Free LLM Extractor Test Results (Verb-Enhanced):")
    print(f"Method: {result['method']}")
    print(f"Entities ({len(result['entities'])}):")
    for entity in result['entities']:
        print(f"  - {entity['name']} ({entity['type']})")
    
    print(f"\nVerb-based Relationships ({len(result['relationships'])}):")
    for rel in result['relationships']:
        verb_info = f" [verb: {rel['verb']}]" if 'verb' in rel else ""
        print(f"  - {rel['from']} → {rel['to']} ({rel['type']}){verb_info}")
    
    print(f"\nConfidence: {result['confidence']:.2f}")
    print(f"Method Info: {extractor.get_method_info()}")
    print("\n✅ All verbs should now appear as graph edges!")