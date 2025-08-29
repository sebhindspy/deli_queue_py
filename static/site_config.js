// Site Configuration - Customizable for different customers
window.SITE_CONFIG = {
    // Branding
    brand: {
        name: "Deli Queue System",
        logo: "static/deliq_placeholder.png",
        paymentLogo: "static/accessoPay.png"
    },

    // Colors
    colors: {
        primary: "#007bff",
        primaryHover: "#0056b3",
        primaryDark: "#0056b3",
        primaryText: "#ffffff",
        secondary: "#6c757d",
        secondaryHover: "#545b62",
        secondaryDark: "#545b62",
        secondaryText: "#212529",
        success: "#28a745",
        successHover: "#1e7e34",
        successDark: "#1e7e34",
        danger: "#dc3545",
        dangerHover: "#c82333",
        dangerDark: "#c82333",
        warning: "#ffc107",
        warningHover: "#e0a800",
        warningDark: "#e0a800",
        info: "#17a2b8",
        infoHover: "#138496",
        infoDark: "#138496"
    },

    // Text Content
    text: {
        // Guest App
        guestTitle: "Join the Queue!",
        guestSubtitle: "Join the virtual queue and enjoy our other attractions while you wait or upgrade and skip the line!",
        joinButton: "Join Queue",
        leaveButton: "Leave Queue",
        premiumButton: "Skip the Line",
        premiumUnavailable: "Premium unavailable",
        turnMessage: "It's your turn! Please proceed to the attraction.",
        scannedMessage: "You have been scanned out of the queue.",
        paymentComplete: "Payment Complete",
        alreadyPremium: "You are already in the premium queue.",
        premiumPurchased: "You have purchased a One Shot and moved to the front!",
        waitingMessage: "You are in position {position}. Please wait for your turn.",
        
        // Attendant App
        attendantTitle: "Venue Entry App",
        venueStatus: "Venue status:",
        queueStatus: "Queue status:",
        guestCount: "Guests in queue:",
        nextGuest: "Next guest:",
        readyPool: "Ready pool:",
        removeGuest: "Remove guest from queue",
        
        // Attendant App Error Messages
        cameraAccessDenied: "Camera access denied. Please allow camera access and refresh the scanner.",
        noCameraFound: "No camera found. Please connect a camera and refresh the scanner.",
        cameraNotSupported: "Camera not supported. Please try a different device or browser.",
        scannerError: "Scanner error occurred. Please refresh the scanner.",
        cameraError: "Camera error: {error}",
        scannerSetupError: "Error setting up scanner. Please try refreshing the scanner.",
        scannerInitError: "Error initializing QR scanner. Please refresh the page.",
        scannerCreateError: "Error creating QR scanner. Please try refreshing the scanner.",
        
        // Clicker App
        clickerTitle: "Venue Exit Clicker",
        guestsInVenue: "Guests in Venue:",
        
        // Payment Mock
        paymentTitle: "Mock Payment Page",
        paymentComplete: "Mock payment complete",
        
        // Status Dashboard
        dashboardTitle: "Queue Status Dashboard",
        apiBase: "API Base URL:",
        totalGuests: "Total Guests:",
        readyPoolStatus: "Ready Pool:",
        currentQueue: "Current Queue",
        noGuests: "No guests in queue",
        refreshStatus: "Refresh Status",
        openAdmin: "Open Admin Panel",
        openAttendant: "Open Attendant App",
        openGuest: "Open Guest App",
        
        // Admin Control Panel
        adminTitle: "Admin Control Panel",
        premiumLimit: "Premium limit:",
        oneShotPrice: "One Shot price:",
        siteConfigurationLabel: "Site Configuration",
        openCMSBtn: "Open Configuration CMS",
        
        // Unified Control App
        unifiedControlTitle: "Queue Control",
        homeSection: "Home",
        queuesSection: "Queues",
        linksSection: "Links",
        configSection: "Config",
        
        // Section headers
        systemStatus: "System Status",
        queueManagement: "Queue Management",
        applicationLinks: "Application Links",
        siteConfiguration: "Site Configuration",
        
        // Status Items
        guestsInQueue: "Guests in Queue",
        readyPoolLimit: "Ready Pool Limit",
        venueCapacity: "Venue Capacity",
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
        
        // Legacy admin panel
        legacyAdminPanel: "Legacy Admin Panel (Deprecated)",
        legacyAdminDescription: "The old admin control panel is deprecated. All functionality has been moved to this unified control app. You can still access it for reference, but it may not work correctly with the current API.",
        openLegacyAdmin: "Open Legacy Admin Panel",
        
        // Application links
        guestApp: "Guest App",
        attendantApp: "Attendant App",
        clickerApp: "Clicker App",
        openGuestApp: "Open Guest App",
        openAttendantApp: "Open Attendant App",
        openClickerApp: "Open Clicker App",
        
        // Icons
        homeIcon: "🏠",
        queuesIcon: "📋",
        linksIcon: "🔗",
        configIcon: "⚙️",
        
        // Configuration Management
        configurationManagement: "Configuration Management",
        configManagementHelp: "Use the interface below to manage site colors, text, and branding:",
        
        // Placeholders
        qrCodePlaceholder: "QR Code will appear here",
        loadingPlaceholder: "Loading...",
        
        // Alert Messages
        missingGuestEmail: "Missing guest email. Cannot proceed to payment.",
        missingGuestEmailReturn: "Missing guest email. Cannot return to guest app.",
        unableToPurchase: "Unable to purchase One Shot",
        pleaseEnterValidEmail: "Please enter a valid email",
        failedToAdvanceQueue: "Failed to advance queue.",
        networkErrorAdvancing: "Network error occurred while advancing queue.",
        noCamerasFound: "No cameras found",
        errorShowingCameraSelection: "Error showing camera selection. Please try refreshing the scanner.",
        errorUpdatingVenueCount: "Error updating venue count.",
        networkErrorUpdatingVenue: "Network error occurred while updating venue count.",
        failedDailyReset: "Failed to perform daily reset. Please try again."
    },

    // Images
    images: {
        logo: "static/deliq_placeholder.png",
        paymentLogo: "static/accessoPay.png"
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
