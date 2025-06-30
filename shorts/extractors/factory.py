"""Factory for creating entity extractors."""
from typing import Dict, Any, Optional
from .base import EntityExtractor
from .ollama_extractor import OllamaExtractor
from .rule_based_extractor import RuleBasedExtractor

class ExtractorFactory:
    """Factory for creating and managing entity extractors."""
    
    EXTRACTORS = {
        'ollama': OllamaExtractor,
        'rule_based': RuleBasedExtractor,
    }
    
    @classmethod
    def create_extractor(cls, extractor_type: str, config: Dict[str, Any] = None) -> EntityExtractor:
        """Create an entity extractor of the specified type.
        
        Args:
            extractor_type: Type of extractor ('ollama', 'rule_based')
            config: Configuration dictionary
            
        Returns:
            EntityExtractor instance
            
        Raises:
            ValueError: If extractor type is not supported
        """
        if extractor_type not in cls.EXTRACTORS:
            raise ValueError(f"Unsupported extractor type: {extractor_type}. "
                           f"Available types: {list(cls.EXTRACTORS.keys())}")
        
        extractor_class = cls.EXTRACTORS[extractor_type]
        return extractor_class(config)
    
    @classmethod
    def get_best_available_extractor(cls, config: Dict[str, Any] = None) -> EntityExtractor:
        """Get the best available extractor based on what's installed.
        
        Priority order: ollama -> rule_based
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Best available EntityExtractor instance
        """
        # Try extractors in order of preference
        for extractor_type in ['ollama', 'rule_based']:
            try:
                extractor = cls.create_extractor(extractor_type, config)
                if extractor.is_available():
                    print(f"Using {extractor_type} extractor")
                    return extractor
            except Exception as e:
                print(f"Failed to create {extractor_type} extractor: {e}")
                continue
        
        # Fallback to rule-based (always available)
        print("Falling back to rule-based extractor")
        return cls.create_extractor('rule_based', config)
    
    @classmethod
    def list_available_extractors(cls, config: Dict[str, Any] = None) -> Dict[str, bool]:
        """List all extractors and their availability status.
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Dictionary mapping extractor names to availability status
        """
        availability = {}
        
        for extractor_type in cls.EXTRACTORS:
            try:
                extractor = cls.create_extractor(extractor_type, config)
                availability[extractor_type] = extractor.is_available()
            except Exception:
                availability[extractor_type] = False
        
        return availability