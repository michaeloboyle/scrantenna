// Main Application Controller for Scrantenna Shorts
import { Navigation } from './navigation.js';
import { ModeManager } from './modes.js';
import { GraphManager } from './graph.js';
import { DataLoader } from './data-loader.js';

class ScrAntennaApp {
    constructor() {
        this.dataLoader = new DataLoader();
        this.modeManager = new ModeManager(this.onModeChange.bind(this));
        this.graphManager = new GraphManager();
        this.navigation = null;
        this.shorts = [];
        this.currentShort = 0;
        
        // Bind methods
        this.showShort = this.showShort.bind(this);
        this.nextShort = this.nextShort.bind(this);
        this.previousShort = this.previousShort.bind(this);
        this.setMode = this.setMode.bind(this);
        
        // Set up graph engagement callback
        this.graphManager.onEntityClick = () => {
            this.modeManager.markGraphEngaged();
        };
    }

    async initialize() {
        try {
            // Load data
            this.shorts = await this.dataLoader.loadShorts();
            
            // Initialize navigation with shorts data
            this.navigation = new Navigation(this.shorts, this.onNavigate.bind(this));
            
            // Create shorts UI
            this.createShorts();
            
            // Show first short
            this.showShort(0);
            
            // Make functions globally available for inline event handlers
            this.setupGlobalFunctions();
            
            console.log('ScrAntenna initialized successfully');
        } catch (error) {
            console.error('Failed to initialize ScrAntenna:', error);
            this.showError('Failed to load application');
        }
    }

    setupGlobalFunctions() {
        // Make functions available globally for onclick handlers
        window.nextShort = this.nextShort;
        window.previousShort = this.previousShort;
        window.setMode = this.setMode;
    }

    onNavigate(index) {
        this.currentShort = index;
        this.showShort(index);
    }

    onModeChange(mode) {
        this.updateShortDisplay(this.currentShort);
    }

    createShorts() {
        const container = document.getElementById('shortsContainer');
        if (!container) {
            console.error('Shorts container not found');
            return;
        }

        container.innerHTML = '';

        this.shorts.forEach((short, index) => {
            const shortDiv = document.createElement('div');
            shortDiv.className = 'short';
            shortDiv.id = `short-${index}`;
            
            shortDiv.innerHTML = `
                <div class="headline ${short.graph?.has_svo ? 'svo' : ''}" id="headline-${index}">
                    ${short.title}
                </div>
                <div class="content" id="content-${index}">
                    ${short.description || short.content}
                </div>
                <div class="metadata">
                    <div class="source">${short.source || 'Unknown Source'}</div>
                    <div class="date">${this.formatDate(short.publishedAt)}</div>
                </div>
                <div class="graph-container" id="graph-container-${index}" style="display: none;">
                    <div class="graph-header">
                        <h3 class="graph-title">${short.title}</h3>
                        <div class="graph-meta">
                            <span>${short.graph?.entities?.length || 0} entities</span>
                            <span>${short.graph?.relationships?.length || 0} relationships</span>
                        </div>
                    </div>
                    <div class="graph-content">
                        <div id="graph-${index}" class="graph-placeholder">
                            <p>Loading knowledge graph...</p>
                        </div>
                        <div class="entity-info" id="entity-info-${index}">
                            <div class="entity-name" id="entity-name-${index}"></div>
                            <div class="entity-type" id="entity-type-${index}"></div>
                        </div>
                    </div>
                    <div class="engagement-indicator" id="engagement-${index}">
                        Graph engaged - auto-advance paused
                    </div>
                </div>
                <div class="progress-bar" style="width: ${((index + 1) / this.shorts.length) * 100}%"></div>
            `;
            
            container.appendChild(shortDiv);
        });
    }

    showShort(index) {
        if (index < 0 || index >= this.shorts.length) return;

        // Update navigation current index
        if (this.navigation) {
            this.navigation.currentShort = index;
        }

        // Hide all shorts
        document.querySelectorAll('.short').forEach((short, i) => {
            short.classList.remove('active', 'prev', 'next');
            if (i < index) {
                short.classList.add('prev');
            } else if (i > index) {
                short.classList.add('next');
            }
        });

        // Show current short
        const currentShortElement = document.getElementById(`short-${index}`);
        if (currentShortElement) {
            currentShortElement.classList.add('active');
        }

        // Update content based on current mode
        this.updateShortDisplay(index);

        // Load graph if in explore mode
        if (this.modeManager.currentMode === 'explore') {
            this.loadGraphForShort(index);
        }

        // Reset graph engagement
        this.modeManager.resetGraphEngagement();

        // Start auto-advance timer
        const short = this.shorts[index];
        if (short && short.duration) {
            this.modeManager.startAutoAdvance(
                short.duration * 1000,
                () => this.nextShort()
            );
        }

        this.currentShort = index;
    }

    updateShortDisplay(index) {
        const short = this.shorts[index];
        if (!short) return;

        const headlineEl = document.getElementById(`headline-${index}`);
        const contentEl = document.getElementById(`content-${index}`);
        const graphContainer = document.getElementById(`graph-container-${index}`);

        if (!headlineEl || !contentEl) return;

        switch (this.modeManager.currentMode) {
            case 'read':
                headlineEl.textContent = short.title;
                contentEl.textContent = short.description || short.content;
                if (graphContainer) graphContainer.style.display = 'none';
                break;

            case 'brief':
                headlineEl.textContent = short.title_distilled || short.title;
                contentEl.textContent = short.content_distilled || short.description_distilled || short.content;
                if (graphContainer) graphContainer.style.display = 'none';
                break;

            case 'explore':
                headlineEl.textContent = short.title;
                contentEl.style.display = 'none';
                if (graphContainer) {
                    graphContainer.style.display = 'block';
                    this.loadGraphForShort(index);
                }
                break;
        }
    }

    loadGraphForShort(index) {
        const short = this.shorts[index];
        if (short) {
            this.graphManager.loadGraphForArticle(index, short);
        }
    }

    nextShort() {
        this.modeManager.stopAutoAdvance();
        if (this.navigation) {
            this.navigation.next();
        }
    }

    previousShort() {
        this.modeManager.stopAutoAdvance();
        if (this.navigation) {
            this.navigation.previous();
        }
    }

    setMode(mode) {
        this.modeManager.setMode(mode);
    }

    formatDate(dateString) {
        if (!dateString) return '';
        
        try {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', {
                month: 'numeric',
                day: 'numeric',
                year: 'numeric'
            });
        } catch (error) {
            return '';
        }
    }

    showError(message) {
        const container = document.getElementById('shortsContainer');
        if (container) {
            container.innerHTML = `
                <div class="short active" style="display: flex; align-items: center; justify-content: center;">
                    <div style="text-align: center;">
                        <h2 style="color: #ff6b6b; margin-bottom: 1rem;">⚠️ Error</h2>
                        <p style="color: white; font-size: 1.2rem;">${message}</p>
                        <button onclick="location.reload()" style="
                            background: rgba(255,255,255,0.2);
                            border: none;
                            color: white;
                            padding: 0.75rem 1.5rem;
                            border-radius: 8px;
                            margin-top: 1rem;
                            cursor: pointer;
                        ">Retry</button>
                    </div>
                </div>
            `;
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const app = new ScrAntennaApp();
    app.initialize();
});

// Export for potential external use
window.ScrAntennaApp = ScrAntennaApp;