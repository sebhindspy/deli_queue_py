/**
 * Shared Configuration Module
 * Handles CSS variable updates across all web apps
 */
(function() {
    'use strict';
    
    // Configuration storage key
    const CONFIG_STORAGE_KEY = 'currentSiteConfig';
    
    /**
     * Update CSS variables based on configuration
     * @param {Object} config - Configuration object with colors
     */
    function updateCSSVariables(config) {
        if (!config || !config.colors) return;
        
        const root = document.documentElement;
        
        // Update all color variables
        Object.entries(config.colors).forEach(([key, value]) => {
            if (value) {
                // Set main color
                root.style.setProperty(`--${key}-color`, value);
                
                // Set hover variant
                const hoverKey = `${key}Hover`;
                if (config.colors[hoverKey]) {
                    root.style.setProperty(`--${key}-hover`, config.colors[hoverKey]);
                }
                
                // Set dark variant
                const darkKey = `${key}Dark`;
                if (config.colors[darkKey]) {
                    root.style.setProperty(`--${key}-dark`, config.colors[darkKey]);
                }
                
                // Set text color for primary and secondary
                if (key === 'primary' || key === 'secondary') {
                    const textKey = `${key}Text`;
                    if (config.colors[textKey]) {
                        root.style.setProperty(`--${key}-text`, config.colors[textKey]);
                    }
                }
            }
        });
        
        console.log('CSS variables updated globally');
    }
    
    /**
     * Load configuration from localStorage and apply it
     */
    function loadAndApplyConfiguration() {
        try {
            const savedConfig = localStorage.getItem(CONFIG_STORAGE_KEY);
            if (savedConfig) {
                const config = JSON.parse(savedConfig);
                updateCSSVariables(config);
                console.log('Applied saved configuration from localStorage');
            }
        } catch (error) {
            console.error('Error loading configuration:', error);
        }
    }
    
    /**
     * Listen for configuration changes from other pages
     */
    function setupConfigurationListener() {
        window.addEventListener('storage', function(event) {
            if (event.key === CONFIG_STORAGE_KEY && event.newValue) {
                try {
                    const config = JSON.parse(event.newValue);
                    updateCSSVariables(config);
                    console.log('Configuration updated via storage event');
                } catch (error) {
                    console.error('Error parsing configuration from storage event:', error);
                }
            }
        });
    }
    
    /**
     * Listen for custom events from CMS
     */
    function setupCustomEventListener() {
        window.addEventListener('configChanged', function(event) {
            if (event.detail && event.detail.config) {
                updateCSSVariables(event.detail.config);
                console.log('Configuration updated via custom event');
            }
        });
    }
    
    /**
     * Initialize the shared configuration system
     */
    function init() {
        // Load any existing configuration
        loadAndApplyConfiguration();
        
        // Setup listeners for configuration changes
        setupConfigurationListener();
        setupCustomEventListener();
        
        console.log('Shared configuration module initialized');
    }
    
    // Auto-initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Expose functions globally for manual use
    window.SharedConfig = {
        updateCSSVariables,
        loadAndApplyConfiguration
    };
})();
