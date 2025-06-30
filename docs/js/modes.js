// Mode Management Module for Scrantenna Shorts
export class ModeManager {
    constructor(onModeChange) {
        this.currentMode = 'read';
        this.onModeChange = onModeChange;
        this.autoAdvanceTimer = null;
        this.graphEngaged = false;
    }

    setMode(mode) {
        this.currentMode = mode;
        this.updateModeButtons(mode);
        this.onModeChange(mode);
    }

    updateModeButtons(activeMode) {
        const modes = ['read', 'brief', 'explore'];
        
        modes.forEach(mode => {
            const btn = document.getElementById(`${mode}Btn`);
            if (btn) {
                if (mode === activeMode) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            }
        });
    }

    startAutoAdvance(duration, callback) {
        this.stopAutoAdvance();
        
        if (this.currentMode === 'explore' && !this.graphEngaged) {
            this.autoAdvanceTimer = setTimeout(() => {
                callback();
            }, duration);
        }
    }

    stopAutoAdvance() {
        if (this.autoAdvanceTimer) {
            clearTimeout(this.autoAdvanceTimer);
            this.autoAdvanceTimer = null;
        }
    }

    markGraphEngaged() {
        this.graphEngaged = true;
        this.stopAutoAdvance();
        
        const indicator = document.querySelector('.engagement-indicator.visible');
        if (indicator) {
            indicator.classList.add('visible');
            setTimeout(() => {
                indicator.classList.remove('visible');
            }, 3000);
        }
    }

    resetGraphEngagement() {
        this.graphEngaged = false;
    }
}