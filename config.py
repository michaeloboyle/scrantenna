"""Configuration management for Scrantenna."""
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class OllamaConfig:
    """Configuration for Ollama extractor."""
    model: str = "phi3:mini"
    temperature: float = 0.1
    max_tokens: int = 300

@dataclass
class ExtractionConfig:
    """Configuration for entity extraction."""
    min_confidence: float = 0.6
    max_entities: int = 10
    max_relationships: int = 15
    preferred_extractor: str = "auto"  # "auto", "ollama", "rule_based"

@dataclass
class ShortsConfig:
    """Configuration for shorts generation."""
    max_shorts: int = 15
    default_duration: int = 8
    auto_distill: bool = True
    
@dataclass
class GraphConfig:
    """Configuration for knowledge graphs."""
    max_nodes: int = 8
    use_circular_layout: bool = True
    show_confidence: bool = False

@dataclass
class Config:
    """Main configuration class."""
    # API Keys
    openai_api_key: Optional[str] = None
    
    # File paths
    data_dir: str = "data"
    daily_dir: str = "data/daily"
    entity_vault_dir: str = "entities"
    
    # Component configs
    ollama: OllamaConfig = None
    extraction: ExtractionConfig = None
    shorts: ShortsConfig = None
    graph: GraphConfig = None
    
    def __post_init__(self):
        """Initialize nested configs if not provided."""
        if self.ollama is None:
            self.ollama = OllamaConfig()
        if self.extraction is None:
            self.extraction = ExtractionConfig()
        if self.shorts is None:
            self.shorts = ShortsConfig()
        if self.graph is None:
            self.graph = GraphConfig()

class ConfigManager:
    """Configuration manager with environment variable and file support."""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or "config.json"
        self._config = None
    
    @property
    def config(self) -> Config:
        """Get configuration, loading if necessary."""
        if self._config is None:
            self._config = self.load_config()
        return self._config
    
    def load_config(self) -> Config:
        """Load configuration from file and environment variables."""
        # Start with defaults
        config_dict = {}
        
        # Load from file if exists
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    file_config = json.load(f)
                config_dict.update(file_config)
            except Exception as e:
                print(f"Warning: Failed to load config file {self.config_file}: {e}")
        
        # Override with environment variables
        env_overrides = self._get_env_overrides()
        config_dict.update(env_overrides)
        
        # Create config object
        return self._dict_to_config(config_dict)
    
    def save_config(self, config: Config) -> None:
        """Save configuration to file."""
        try:
            config_dict = self._config_to_dict(config)
            with open(self.config_file, 'w') as f:
                json.dump(config_dict, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save config to {self.config_file}: {e}")
    
    def _get_env_overrides(self) -> Dict[str, Any]:
        """Get configuration overrides from environment variables."""
        overrides = {}
        
        # API Keys
        if os.getenv('OPENAI_API_KEY'):
            overrides['openai_api_key'] = os.getenv('OPENAI_API_KEY')
        
        # Paths
        if os.getenv('SCRANTENNA_DATA_DIR'):
            overrides['data_dir'] = os.getenv('SCRANTENNA_DATA_DIR')
        
        if os.getenv('SCRANTENNA_ENTITY_VAULT'):
            overrides['entity_vault_dir'] = os.getenv('SCRANTENNA_ENTITY_VAULT')
        
        # Ollama config
        ollama_overrides = {}
        if os.getenv('OLLAMA_MODEL'):
            ollama_overrides['model'] = os.getenv('OLLAMA_MODEL')
        if os.getenv('OLLAMA_TEMPERATURE'):
            try:
                ollama_overrides['temperature'] = float(os.getenv('OLLAMA_TEMPERATURE'))
            except ValueError:
                pass
        
        if ollama_overrides:
            overrides['ollama'] = ollama_overrides
        
        # Extraction config
        extraction_overrides = {}
        if os.getenv('EXTRACTION_MIN_CONFIDENCE'):
            try:
                extraction_overrides['min_confidence'] = float(os.getenv('EXTRACTION_MIN_CONFIDENCE'))
            except ValueError:
                pass
        
        if os.getenv('EXTRACTION_PREFERRED'):
            extraction_overrides['preferred_extractor'] = os.getenv('EXTRACTION_PREFERRED')
        
        if extraction_overrides:
            overrides['extraction'] = extraction_overrides
        
        return overrides
    
    def _dict_to_config(self, config_dict: Dict[str, Any]) -> Config:
        """Convert dictionary to Config object."""
        # Handle nested configs
        if 'ollama' in config_dict and isinstance(config_dict['ollama'], dict):
            config_dict['ollama'] = OllamaConfig(**config_dict['ollama'])
        
        if 'extraction' in config_dict and isinstance(config_dict['extraction'], dict):
            config_dict['extraction'] = ExtractionConfig(**config_dict['extraction'])
        
        if 'shorts' in config_dict and isinstance(config_dict['shorts'], dict):
            config_dict['shorts'] = ShortsConfig(**config_dict['shorts'])
        
        if 'graph' in config_dict and isinstance(config_dict['graph'], dict):
            config_dict['graph'] = GraphConfig(**config_dict['graph'])
        
        return Config(**config_dict)
    
    def _config_to_dict(self, config: Config) -> Dict[str, Any]:
        """Convert Config object to dictionary."""
        config_dict = asdict(config)
        
        # Remove None values
        return {k: v for k, v in config_dict.items() if v is not None}
    
    def get_extractor_config(self) -> Dict[str, Any]:
        """Get configuration dict suitable for extractors."""
        return {
            'model': self.config.ollama.model,
            'temperature': self.config.ollama.temperature,
            'max_tokens': self.config.ollama.max_tokens,
            'min_confidence': self.config.extraction.min_confidence,
            'max_entities': self.config.extraction.max_entities,
            'max_relationships': self.config.extraction.max_relationships,
        }

# Global config manager instance
config_manager = ConfigManager()

def get_config() -> Config:
    """Get the global configuration."""
    return config_manager.config

def get_extractor_config() -> Dict[str, Any]:
    """Get extractor configuration."""
    return config_manager.get_extractor_config()