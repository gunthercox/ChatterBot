/**
 * Mobile Menu and Responsive Enhancements for ChatterBot Documentation
 * Provides mobile-friendly navigation and touch interactions
 */

(function() {
    'use strict';

    var state = {
        sidebar: null,
        toggleButton: null,
        overlay: null,
        isInitialized: false,
        clickOutsideHandler: null,
        sidebarLinkHandlers: []
    };

    /**
     * Create overlay for mobile menu
     */
    function createOverlay() {
        if (state.overlay) return state.overlay;

        var overlay = document.createElement('div');
        overlay.className = 'mobile-sidebar-overlay';
        overlay.setAttribute('aria-hidden', 'true');
        document.body.appendChild(overlay);

        overlay.addEventListener('click', closeMobileMenu);

        return overlay;
    }

    /**
     * Open mobile menu
     */
    function openMobileMenu() {
        if (!state.sidebar || !state.toggleButton) return;

        state.sidebar.classList.add('mobile-open');
        state.overlay.classList.add('active');
        state.toggleButton.setAttribute('aria-expanded', 'true');
        state.toggleButton.innerHTML = '✕ Close';
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
    }

    /**
     * Close mobile menu
     */
    function closeMobileMenu() {
        if (!state.sidebar || !state.toggleButton) return;

        state.sidebar.classList.remove('mobile-open');
        state.overlay.classList.remove('active');
        state.toggleButton.setAttribute('aria-expanded', 'false');
        state.toggleButton.innerHTML = '☰ Menu';
        document.body.style.overflow = ''; // Restore scrolling
    }

    /**
     * Toggle mobile menu
     */
    function toggleMobileMenu(event) {
        event.preventDefault();
        event.stopPropagation();

        var isOpen = state.sidebar.classList.contains('mobile-open');

        if (isOpen) {
            closeMobileMenu();
        } else {
            openMobileMenu();
        }
    }

    /**
     * Initialize mobile menu functionality
     */
    function initMobileMenu() {
        // Only initialize once
        if (state.isInitialized) return;

        state.sidebar = document.querySelector('div.sphinxsidebar');
        if (!state.sidebar) return;

        // Create overlay
        state.overlay = createOverlay();

        // Create mobile menu toggle button
        state.toggleButton = document.createElement('button');
        state.toggleButton.className = 'mobile-menu-toggle';
        state.toggleButton.innerHTML = '☰ Menu';
        state.toggleButton.setAttribute('aria-label', 'Toggle navigation menu');
        state.toggleButton.setAttribute('aria-expanded', 'false');
        state.toggleButton.setAttribute('type', 'button');
        document.body.appendChild(state.toggleButton);

        // Add click event listener
        state.toggleButton.addEventListener('click', toggleMobileMenu);

        // Close menu when clicking a link inside sidebar
        var sidebarLinks = state.sidebar.querySelectorAll('a');
        sidebarLinks.forEach(function(link) {
            var handler = function(e) {
                // Small delay to allow navigation to start
                setTimeout(closeMobileMenu, 100);
            };
            link.addEventListener('click', handler);
            state.sidebarLinkHandlers.push({ element: link, handler: handler });
        });

        // Handle escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && state.sidebar.classList.contains('mobile-open')) {
                closeMobileMenu();
                state.toggleButton.focus();
            }
        });

        state.isInitialized = true;
    }

    /**
     * Clean up mobile menu
     */
    function cleanupMobileMenu() {
        if (!state.isInitialized) return;

        // Remove toggle button
        if (state.toggleButton && state.toggleButton.parentNode) {
            state.toggleButton.parentNode.removeChild(state.toggleButton);
        }

        // Remove overlay
        if (state.overlay && state.overlay.parentNode) {
            state.overlay.parentNode.removeChild(state.overlay);
        }

        // Remove sidebar classes
        if (state.sidebar) {
            state.sidebar.classList.remove('mobile-open');
        }

        // Remove event listeners from sidebar links
        state.sidebarLinkHandlers.forEach(function(item) {
            item.element.removeEventListener('click', item.handler);
        });

        // Restore body overflow
        document.body.style.overflow = '';

        // Reset state
        state.isInitialized = false;
        state.toggleButton = null;
        state.overlay = null;
        state.sidebarLinkHandlers = [];
    }

    /**
     * Improve table responsiveness
     */
    function makeTablesResponsive() {
        var tables = document.querySelectorAll('table.docutils');

        tables.forEach(function(table) {
            // Skip if already wrapped
            if (table.parentNode.classList.contains('table-wrapper')) {
                return;
            }

            // Create wrapper for horizontal scrolling
            var wrapper = document.createElement('div');
            wrapper.className = 'table-wrapper';
            wrapper.style.overflowX = 'auto';
            wrapper.style.webkitOverflowScrolling = 'touch';
            wrapper.style.marginBottom = '1em';

            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        });
    }

    /**
     * Add touch-friendly behavior to code blocks
     */
    function enhanceCodeBlocks() {
        var codeBlocks = document.querySelectorAll('div.highlight');

        codeBlocks.forEach(function(block) {
            // Add visual indicator for scrollable content
            var pre = block.querySelector('pre');
            if (pre && pre.scrollWidth > pre.clientWidth) {
                block.classList.add('scrollable');
                block.setAttribute('title', 'Swipe to scroll code');
            }
        });
    }

    /**
     * Handle window resize events
     */
    function handleResize() {
        var isMobile = window.innerWidth <= 480;

        if (isMobile && !state.isInitialized) {
            // Mobile view - initialize
            initMobileMenu();
        } else if (!isMobile && state.isInitialized) {
            // Desktop view - cleanup
            cleanupMobileMenu();
        }
    }

    /**
     * Improve accessibility for mobile users
     */
    function improveAccessibility() {
        // Add skip to content link
        var skipLink = document.createElement('a');
        skipLink.href = '#document';
        skipLink.className = 'skip-to-content';
        skipLink.textContent = 'Skip to content';
        skipLink.style.position = 'absolute';
        skipLink.style.top = '-40px';
        skipLink.style.left = '0';
        skipLink.style.background = '#300a24';
        skipLink.style.color = '#e8ffca';
        skipLink.style.padding = '8px';
        skipLink.style.textDecoration = 'none';
        skipLink.style.zIndex = '1001';

        skipLink.addEventListener('focus', function() {
            this.style.top = '0';
        });

        skipLink.addEventListener('blur', function() {
            this.style.top = '-40px';
        });

        document.body.insertBefore(skipLink, document.body.firstChild);
    }

    /**
     * Initialize all mobile enhancements
     */
    function init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                // Check if mobile on initial load (480px breakpoint for actual phones)
                if (window.innerWidth <= 480) {
                    initMobileMenu();
                }
                makeTablesResponsive();
                enhanceCodeBlocks();
                improveAccessibility();
            });
        } else {
            // Check if mobile on initial load (480px breakpoint for actual phones)
            if (window.innerWidth <= 480) {
                initMobileMenu();
            }
            makeTablesResponsive();
            enhanceCodeBlocks();
            improveAccessibility();
        }

        // Handle window resize with debouncing
        var resizeTimer;
        window.addEventListener('resize', function() {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(handleResize, 250);
        });

        // Handle orientation change on mobile devices
        window.addEventListener('orientationchange', function() {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(handleResize, 300);
        });
    }

    // Initialize
    init();

})();
