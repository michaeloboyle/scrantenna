// Navigation Module for Scrantenna Shorts
export class Navigation {
    constructor(shorts, onNavigate) {
        this.shorts = shorts;
        this.currentShort = 0;
        this.onNavigate = onNavigate;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Touch events for mobile swipe
        let touchStartY = 0;
        let touchStartTime = 0;

        document.addEventListener('touchstart', (e) => {
            touchStartY = e.touches[0].clientY;
            touchStartTime = Date.now();
        }, { passive: true });

        document.addEventListener('touchend', (e) => {
            const touchEndY = e.changedTouches[0].clientY;
            const touchEndTime = Date.now();
            const deltaY = touchStartY - touchEndY;
            const deltaTime = touchEndTime - touchStartTime;
            
            if (deltaTime < 300 && Math.abs(deltaY) > 50) {
                if (deltaY > 0) {
                    this.next();
                } else {
                    this.previous();
                }
            }
        }, { passive: true });

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowDown' || e.key === ' ') {
                e.preventDefault();
                this.next();
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                this.previous();
            }
        });

        // Mouse wheel navigation
        let lastScrollTime = 0;
        document.addEventListener('wheel', (e) => {
            const now = Date.now();
            if (now - lastScrollTime < 500) return; // Throttle scrolling
            
            if (e.deltaY > 0) {
                this.next();
            } else if (e.deltaY < 0) {
                this.previous();
            }
            lastScrollTime = now;
        }, { passive: true });
    }

    next() {
        if (this.currentShort < this.shorts.length - 1) {
            this.currentShort++;
            this.onNavigate(this.currentShort);
        }
    }

    previous() {
        if (this.currentShort > 0) {
            this.currentShort--;
            this.onNavigate(this.currentShort);
        }
    }

    goTo(index) {
        if (index >= 0 && index < this.shorts.length) {
            this.currentShort = index;
            this.onNavigate(this.currentShort);
        }
    }
}