// Site Configuration - Customizable for different customers
window.SITE_CONFIG = {
    // Branding
    brand: {
        name: "Deli Queue",
        logo: "static/deliq_placeholder.png",
        favicon: "static/deliq_placeholder.png"
    },

    // Colors
    colors: {
        primary: "#007bff",
        secondary: "#6c757d",
        success: "#28a745",
        danger: "#dc3545",
        warning: "#ffc107",
        info: "#17a2b8",
        light: "#f8f9fa",
        dark: "#343a40",
        background: "#ffffff",
        text: "#212529",
        border: "#dee2e6"
    },

    // Text Content
    text: {
        // Guest App
        guestTitle: "Join the Queue!",
        guestSubtitle: "Join the virtual queue and enjoy our other attractions while you wait or upgrade and skip the line!",
        joinButton: "Join queue",
        leaveButton: "Leave Queue",
        premiumButton: "Skip the Line",
        premiumUnavailable: "Premium unavailable",
        turnMessage: "It's your turn! Please proceed to the attraction.",
        scannedMessage: "You have been scanned out of the queue.",
        
        // Admin Panel
        adminTitle: "Admin Control Panel",
        queueStatus: "Queue status:",
        guestCount: "Guests in queue:",
        venueStatus: "Guests in venue:",
        premiumLimit: "Premium limit:",
        oneShotPrice: "One Shot price:",
        readyPool: "Ready pool:",
        
        // Attendant App
        attendantTitle: "Venue Entry App",
        venueStatus: "Venue status:",
        queueStatus: "Queue status:",
        nextGuest: "Next guest:",
        removeGuest: "Remove guest from queue",
        
        // Payment
        paymentTitle: "Mock Payment Page",
        paymentComplete: "Mock payment complete",
        
        // Status Dashboard
        dashboardTitle: "Queue Status Dashboard",
        apiBase: "API Base URL:",
        totalGuests: "Total Guests:",
        readyPoolStatus: "Ready Pool:",
        venueStatus: "Venue Status:",
        guestsInVenue: "Guests in Venue:",
        currentQueue: "Current Queue",
        noGuests: "No guests in queue",
        refreshStatus: "Refresh Status",
        openAdmin: "Open Admin Panel",
        openAttendant: "Open Attendant App",
        openGuest: "Open Guest App",
        
        // Clicker App
        clickerTitle: "Venue Exit Clicker",
        guestLeft: "Guest Left Venue",
        
        // Admin Panel Additional
        siteConfigurationLabel: "Site Configuration",
        openCMSBtn: "Open Configuration CMS",
        
        // Unified Control App
        unifiedControlTitle: "Queue Control",
        homeSection: "Home",
        queuesSection: "Queues",
        linksSection: "Links",
        configSection: "Config",
        systemStatus: "System Status",
        queueManagement: "Queue Management",
        applicationLinks: "Application Links",
        siteConfiguration: "Site Configuration",
        
        // Status Items
        queueStatus: "Queue Status",
        guestsInQueue: "Guests in Queue",
        readyPool: "Ready Pool",
        readyPoolLimit: "Ready Pool Limit",
        guestsInVenue: "Guests in Venue",
        venueCapacity: "Venue Capacity",
        currentQueue: "Current Queue",
        noGuestsInQueue: "No guests in queue",
        
        // Queue Controls
        queueControls: "Queue Controls",
        openQueue: "Open Queue",
        closeQueue: "Close Queue",
        resetQueue: "Reset Queue",
        
        // Demo Mode
        demoMode: "Demo Mode",
        mockGuestsLabel: "Number of mock guests:",
        insertMockGuests: "Insert Mock Guests",
        resetCounter: "Reset Counter",
        mockGuestsHelp: "Mock guests get unique names (mock0, mock1, mock2...). Use \"Reset Counter\" to start over from 0.",
        
        // Premium Access
        premiumAccess: "Premium Access",
        enablePremiumAccess: "Enable Premium Access",
        premiumLimitLabel: "Premium Limit:",
        updatePremiumLimit: "Update Premium Limit",
        oneShotPriceLabel: "One Shot Price ($):",
        updateOneShotPrice: "Update One Shot Price",
        premiumAccessHelp: "Premium access must be enabled AND premium limit must be >0 for the upgrade button to appear in the guest app.",
        
        // Venue Management
        venueManagement: "Venue Management",
        enableVenueMode: "Enable Venue Mode",
        venueCapacityLabel: "Venue Capacity:",
        updateVenueCapacity: "Update Venue Capacity",
        removeGuestFromVenue: "Remove Guest from Venue",
        removeGuestHelp: "Use this when a guest leaves the venue",
        
        // Ready Pool Configuration
        readyPoolConfiguration: "Ready Pool Configuration",
        readyPoolSizeLabel: "Ready Pool Size:",
        setReadyPool: "Set",
        readyPoolHelp: "Set to 0 to disable ready pool. When enabled, the first N guests in the queue are considered \"ready\" and can be scanned in any order.",
        
        // Daily Operations
        dailyOperations: "Daily Operations",
        dailyResetQueue: "Daily Reset Queue",
        dailyResetHelp: "Clears all guests from queue while preserving configuration. Use at start of business day.",
        
        // Links Section
        legacyAdminPanel: "Legacy Admin Panel (Deprecated)",
        legacyAdminDescription: "The old admin control panel is deprecated. All functionality has been moved to this unified control app. You can still access it for reference, but it may not work correctly with the current API.",
        openLegacyAdmin: "Open Legacy Admin Panel",
        guestApp: "Guest App",
        attendantApp: "Attendant App",
        clickerApp: "Clicker App",
        openGuestApp: "Open Guest App",
        openAttendantApp: "Open Attendant App",
        openClickerApp: "Open Clicker App",
        qrCodePlaceholder: "QR Code will appear here",
        loadingPlaceholder: "Loading...",
        
        // Configuration Management
        configurationManagement: "Configuration Management",
        configManagementHelp: "Use the interface below to manage site colors, text, and branding:",
        
        // Navigation Icons
        homeIcon: "🏠",
        queuesIcon: "📋",
        linksIcon: "🔗",
        configIcon: "⚙️"
    },

    // Features
    features: {
        readyPool: false,
        premiumQueue: false,
        venueMode: false,
        qrCodes: false,
        paymentIntegration: false
    },

    // Defaults
    defaults: {
        premiumLimit: 0,
        oneShotPrice: 5,
        readyPoolLimit: 0,
        venueCapacity: 0
    },

    // Images
    images: {
        logo: "static/deliq_placeholder.png",
        paymentLogo: "static/accessoPay.png",
        qrPlaceholder: "static/deliq_placeholder.png"
    },

    // Styling
    styling: {
        borderRadius: "16px",
        buttonPadding: "10px 20px",
        containerMaxWidth: "800px",
        fontSize: "16px",
        fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
    }
};

// Helper function to get config values with fallbacks
window.getConfig = function(path, defaultValue = '') {
    const keys = path.split('.');
    let value = window.SITE_CONFIG;
    
    for (const key of keys) {
        if (value && typeof value === 'object' && key in value) {
            value = value[key];
        } else {
            return defaultValue;
        }
    }
    
    return value;
};
