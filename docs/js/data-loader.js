// Data Loading Module for Scrantenna Shorts
export class DataLoader {
    constructor() {
        this.shorts = [];
        this.fallbackData = this.getDemoData();
    }

    async loadShorts() {
        try {
            // Load optimized shorts data
            const response = await fetch('shorts_data.json');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            this.shorts = data.shorts;
            
            console.log(`Loaded ${this.shorts.length} shorts (${data.total_duration}s total)`);
            return this.shorts;
        } catch (error) {
            console.error('Error loading shorts:', error);
            return this.loadFallbackData();
        }
    }

    async loadFallbackData() {
        try {
            // Fallback to original news data
            const response = await fetch('../data/daily/scranton_news_2025-06-25.json');
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            this.shorts = data.articles.slice(0, 10).map(article => ({
                id: `fallback_${article.title?.slice(0, 20) || 'unknown'}`,
                title: article.title || 'Untitled',
                title_distilled: article.title || 'Untitled',
                description: article.description || '',
                description_distilled: '',
                content: article.content || article.description || '',
                content_distilled: '',
                graph: null,
                duration: 8,
                source: article.source?.name || 'Unknown Source',
                publishedAt: article.publishedAt || new Date().toISOString()
            }));
            
            console.log(`Loaded ${this.shorts.length} fallback shorts`);
            return this.shorts;
        } catch (fallbackError) {
            console.error('Fallback also failed:', fallbackError);
            this.shorts = this.fallbackData;
            console.log(`Using ${this.shorts.length} demo shorts`);
            return this.shorts;
        }
    }

    getShorts() {
        return this.shorts;
    }

    getShort(index) {
        return this.shorts[index] || null;
    }

    getDemoData() {
        return [
            {
                id: "demo_1",
                title: "Welcome to Scrantenna",
                title_distilled: "Welcome to Scrantenna",
                description: "Your TikTok-style news viewer for Scranton updates with knowledge graphs and AI-powered insights.",
                description_distilled: "",
                content: "Explore news in a whole new way with interactive knowledge graphs and distilled content.",
                content_distilled: "Explore news with interactive knowledge graphs.",
                graph: {
                    entities: [
                        { name: "Scrantenna", type: "ORGANIZATION" },
                        { name: "Scranton", type: "LOCATION" },
                        { name: "News Platform", type: "WORK" }
                    ],
                    relationships: [
                        { from: "Scrantenna", to: "Scranton", type: "COVERS" },
                        { from: "Scrantenna", to: "News Platform", type: "IS_A" }
                    ]
                },
                duration: 10,
                source: "Scrantenna",
                publishedAt: new Date().toISOString()
            },
            {
                id: "demo_2", 
                title: "Loading Error",
                title_distilled: "Loading Error",
                description: "Unable to load news data. Please check your connection or try again later.",
                description_distilled: "",
                content: "This is a demo short shown when real data cannot be loaded.",
                content_distilled: "Demo short for loading errors.",
                graph: {
                    entities: [
                        { name: "Loading Error", type: "EVENT" },
                        { name: "Demo Mode", type: "OTHER" }
                    ],
                    relationships: []
                },
                duration: 8,
                source: "System",
                publishedAt: new Date().toISOString()
            }
        ];
    }

    // Validate shorts data structure
    validateShortsData(shorts) {
        const requiredFields = ['id', 'title', 'content', 'source'];
        
        return shorts.every(short => {
            const hasRequiredFields = requiredFields.every(field => 
                short.hasOwnProperty(field) && short[field] !== null
            );
            
            if (!hasRequiredFields) {
                console.warn('Short missing required fields:', short);
                return false;
            }
            
            return true;
        });
    }

    // Process shorts for consistent structure
    processShorts(rawShorts) {
        return rawShorts.map((short, index) => ({
            id: short.id || `short_${index}`,
            title: short.title || 'Untitled',
            title_distilled: short.title_distilled || short.title || 'Untitled',
            description: short.description || '',
            description_distilled: short.description_distilled || '',
            content: short.content || short.description || '',
            content_distilled: short.content_distilled || '',
            graph: short.graph || null,
            duration: short.duration || 8,
            source: short.source || 'Unknown Source',
            publishedAt: short.publishedAt || new Date().toISOString()
        }));
    }
}