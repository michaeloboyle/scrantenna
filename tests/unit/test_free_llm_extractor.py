"""
Unit tests for free LLM entity and relationship extraction.
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from shorts.free_llm_extractor import ProductionFreeLLMExtractor


class TestProductionFreeLLMExtractor:
    """Test suite for ProductionFreeLLMExtractor."""
    
    def test_initialization(self):
        """Test extractor initialization."""
        extractor = ProductionFreeLLMExtractor()
        assert extractor.ollama_model == "llama3.2:3b"
        assert hasattr(extractor, 'ollama_available')
        assert hasattr(extractor, 'hf_available')
    
    @patch('shorts.free_llm_extractor.ollama')
    def test_check_ollama_available(self, mock_ollama):
        """Test Ollama availability check."""
        # Test when Ollama is available
        mock_ollama.show.return_value = {"model": "llama3.2:3b"}
        extractor = ProductionFreeLLMExtractor()
        assert extractor.ollama_available is True
        
        # Test when Ollama is not available
        mock_ollama.show.side_effect = Exception("Model not found")
        extractor = ProductionFreeLLMExtractor()
        assert extractor.ollama_available is False
    
    @patch('shorts.free_llm_extractor.pipeline')
    def test_check_huggingface_available(self, mock_pipeline):
        """Test HuggingFace availability check."""
        # Test when HF is available
        mock_pipeline.return_value = MagicMock()
        extractor = ProductionFreeLLMExtractor()
        assert extractor.hf_available is True
        
        # Test when HF is not available
        mock_pipeline.side_effect = ImportError("transformers not installed")
        extractor = ProductionFreeLLMExtractor()
        assert extractor.hf_available is False
    
    def test_extract_for_article(self, sample_news_article):
        """Test complete article extraction workflow."""
        extractor = ProductionFreeLLMExtractor()
        
        with patch.object(extractor, '_extract_entities_with_fallback') as mock_entities, \
             patch.object(extractor, '_extract_relationships_with_fallback') as mock_relationships, \
             patch.object(extractor, '_generate_svg_graph') as mock_svg:
            
            mock_entities.return_value = [
                {"name": "Paige Cognetti", "type": "PERSON", "confidence": 0.95}
            ]
            mock_relationships.return_value = [
                {"from": "Paige Cognetti", "to": "Scranton", "type": "MAYOR_OF"}
            ]
            mock_svg.return_value = "<svg>test</svg>"
            
            result = extractor.extract_for_article(sample_news_article, 0)
            
            assert "entities" in result
            assert "relationships" in result
            assert "svg" in result
            assert "method" in result
            assert "confidence" in result
            assert len(result["entities"]) == 1
            assert result["entities"][0]["name"] == "Paige Cognetti"
    
    @patch('shorts.free_llm_extractor.ollama')
    def test_ollama_extract_entities(self, mock_ollama):
        """Test entity extraction using Ollama."""
        extractor = ProductionFreeLLMExtractor()
        extractor.ollama_available = True
        
        # Mock successful Ollama response
        mock_ollama.generate.return_value = {
            'response': '[{"name": "Paige Cognetti", "type": "PERSON"}, {"name": "Scranton", "type": "LOCATION"}]'
        }
        
        text = "Mayor Paige Cognetti announced a project in Scranton."
        entities = extractor._ollama_extract_entities(text)
        
        assert len(entities) == 2
        assert entities[0]["name"] == "Paige Cognetti"
        assert entities[0]["type"] == "PERSON"
        assert entities[1]["name"] == "Scranton"
        assert entities[1]["type"] == "LOCATION"
    
    @patch('shorts.free_llm_extractor.ollama')
    def test_ollama_extract_entities_invalid_json(self, mock_ollama):
        """Test handling of invalid JSON from Ollama."""
        extractor = ProductionFreeLLMExtractor()
        extractor.ollama_available = True
        
        # Mock Ollama response with invalid JSON
        mock_ollama.generate.return_value = {
            'response': 'This is not valid JSON'
        }
        
        text = "Test text"
        entities = extractor._ollama_extract_entities(text)
        
        assert entities == []
    
    def test_hf_extract_entities(self, sample_entities):
        """Test HuggingFace entity extraction."""
        extractor = ProductionFreeLLMExtractor()
        extractor.hf_available = True
        extractor.hf_pipeline = Mock()
        
        # Mock HF pipeline response
        extractor.hf_pipeline.return_value = [
            {"word": "Paige Cognetti", "entity_group": "PER", "score": 0.95},
            {"word": "Scranton", "entity_group": "LOC", "score": 0.98}
        ]
        
        text = "Mayor Paige Cognetti announced a project in Scranton."
        entities = extractor._hf_extract_entities(text)
        
        assert len(entities) == 2
        assert entities[0]["name"] == "Paige Cognetti"
        assert entities[0]["type"] == "PERSON"
        assert entities[1]["name"] == "Scranton"
        assert entities[1]["type"] == "LOCATION"
    
    def test_rule_based_entities(self):
        """Test rule-based entity extraction fallback."""
        extractor = ProductionFreeLLMExtractor()
        
        text = "Mayor Paige Cognetti announced a project on Providence Road in Scranton, Pennsylvania."
        entities = extractor._rule_based_entities(text)
        
        # Should find at least some entities
        assert len(entities) > 0
        
        # Check for expected entity types
        entity_names = [e["name"] for e in entities]
        entity_types = [e["type"] for e in entities]
        
        assert "PERSON" in entity_types or "LOCATION" in entity_types
    
    def test_validate_entities(self):
        """Test entity validation."""
        extractor = ProductionFreeLLMExtractor()
        
        # Valid entities
        valid_entities = [
            {"name": "Paige Cognetti", "type": "PERSON"},
            {"name": "Scranton", "type": "LOCATION"}
        ]
        
        # Invalid entities (missing fields, invalid types, short names)
        invalid_entities = [
            {"name": "PC", "type": "PERSON"},  # Too short
            {"name": "Valid Name"},  # Missing type
            {"type": "PERSON"},  # Missing name
            {"name": "Test", "type": "INVALID_TYPE"}  # Invalid type
        ]
        
        # Test valid entities pass validation
        validated = extractor._validate_entities(valid_entities)
        assert len(validated) == 2
        
        # Test invalid entities are filtered out
        validated_invalid = extractor._validate_entities(invalid_entities)
        assert len(validated_invalid) == 0
    
    def test_validate_relationships(self, sample_entities):
        """Test relationship validation."""
        extractor = ProductionFreeLLMExtractor()
        
        entities = [
            {"name": "Paige Cognetti", "type": "PERSON"},
            {"name": "Scranton", "type": "LOCATION"}
        ]
        
        # Valid relationships
        valid_relationships = [
            {"from": "Paige Cognetti", "to": "Scranton", "type": "MAYOR_OF"}
        ]
        
        # Invalid relationships
        invalid_relationships = [
            {"from": "Unknown Person", "to": "Scranton", "type": "UNKNOWN"},  # Unknown entity
            {"from": "Paige Cognetti", "type": "MAYOR_OF"},  # Missing 'to'
            {"to": "Scranton", "type": "MAYOR_OF"}  # Missing 'from'
        ]
        
        # Test valid relationships pass validation
        validated = extractor._validate_relationships(valid_relationships, entities)
        assert len(validated) == 1
        
        # Test invalid relationships are filtered out
        validated_invalid = extractor._validate_relationships(invalid_relationships, entities)
        assert len(validated_invalid) == 0
    
    def test_deduplicate_entities(self):
        """Test entity deduplication."""
        extractor = ProductionFreeLLMExtractor()
        
        entities_with_duplicates = [
            {"name": "Paige Cognetti", "type": "PERSON"},
            {"name": "Scranton", "type": "LOCATION"},
            {"name": "Paige Cognetti", "type": "PERSON"},  # Duplicate
            {"name": "PC", "type": "PERSON"},  # Too short, should be filtered
            {"name": "Different Name", "type": "ORGANIZATION"}
        ]
        
        deduplicated = extractor._deduplicate_entities(entities_with_duplicates)
        
        # Should have 3 unique, valid entities
        assert len(deduplicated) == 3
        names = [e["name"] for e in deduplicated]
        assert "Paige Cognetti" in names
        assert "Scranton" in names
        assert "Different Name" in names
        assert "PC" not in names  # Too short
    
    def test_generate_svg_graph(self, sample_entities, sample_relationships):
        """Test SVG graph generation."""
        extractor = ProductionFreeLLMExtractor()
        
        svg = extractor._generate_svg_graph(sample_entities, sample_relationships, 0)
        
        assert svg.startswith('<svg')
        assert svg.endswith('</svg>')
        assert 'viewBox' in svg
        assert 'circle' in svg  # Should have entity circles
        
    def test_generate_svg_graph_empty(self):
        """Test SVG generation with no entities."""
        extractor = ProductionFreeLLMExtractor()
        
        svg = extractor._generate_svg_graph([], [], 0)
        
        assert 'No entities found' in svg
    
    def test_calculate_confidence(self):
        """Test confidence calculation."""
        extractor = ProductionFreeLLMExtractor()
        
        # Test with entities that have confidence scores
        entities_with_confidence = [
            {"name": "Entity1", "type": "PERSON", "confidence": 0.9},
            {"name": "Entity2", "type": "LOCATION", "confidence": 0.8}
        ]
        
        confidence = extractor._calculate_confidence(entities_with_confidence)
        assert confidence == 0.85  # Average of 0.9 and 0.8
        
        # Test with entities without confidence scores
        entities_without_confidence = [
            {"name": "Entity1", "type": "PERSON"},
            {"name": "Entity2", "type": "LOCATION"}
        ]
        
        confidence = extractor._calculate_confidence(entities_without_confidence)
        assert confidence == 0.5  # Default value
        
        # Test with empty list
        confidence = extractor._calculate_confidence([])
        assert confidence == 0.0
    
    def test_get_method_info(self):
        """Test method information retrieval."""
        extractor = ProductionFreeLLMExtractor()
        
        info = extractor.get_method_info()
        
        assert "ollama_available" in info
        assert "huggingface_available" in info
        assert "active_method" in info
        assert "cost_per_article" in info
        assert "privacy_preserving" in info
        assert info["cost_per_article"] == "$0.00"
    
    def test_extraction_fallback_chain(self, sample_news_article):
        """Test the complete fallback chain for entity extraction."""
        extractor = ProductionFreeLLMExtractor()
        
        # Mock all methods to fail except rule-based
        extractor.ollama_available = False
        extractor.hf_available = False
        
        with patch.object(extractor, '_rule_based_entities') as mock_rule_based:
            mock_rule_based.return_value = [
                {"name": "Test Entity", "type": "PERSON"}
            ]
            
            text = sample_news_article["title"] + " " + sample_news_article["description"]
            entities = extractor._extract_entities_with_fallback(text)
            
            # Should fall back to rule-based extraction
            assert len(entities) == 1
            assert entities[0]["name"] == "Test Entity"
            mock_rule_based.assert_called_once()
    
    def test_map_hf_entity_type(self):
        """Test HuggingFace entity type mapping."""
        extractor = ProductionFreeLLMExtractor()
        
        assert extractor._map_hf_entity_type("PER") == "PERSON"
        assert extractor._map_hf_entity_type("ORG") == "ORGANIZATION"
        assert extractor._map_hf_entity_type("LOC") == "LOCATION"
        assert extractor._map_hf_entity_type("MISC") == "OTHER"
        assert extractor._map_hf_entity_type("UNKNOWN") == "OTHER"