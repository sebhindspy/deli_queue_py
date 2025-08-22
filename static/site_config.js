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
        noGuests: "No guests in queue"
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
