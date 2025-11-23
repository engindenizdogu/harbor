(function () {
  'use strict';

  // Client-side navigation to prevent sidebar reload
  // Intercepts internal link clicks, fetches new content, swaps main area only

  var baseUrl = window.location.origin + (typeof siteBaseurl !== 'undefined' ? siteBaseurl : '');
  var mainContent = null;

  function isInternalLink(url) {
    try {
      var link = new URL(url, window.location.href);
      return link.origin === window.location.origin && 
             link.pathname.startsWith(baseUrl.replace(window.location.origin, ''));
    } catch (e) {
      return false;
    }
  }

  function loadPage(url, pushState) {
    if (!mainContent) return;

    fetch(url)
      .then(function (response) {
        if (!response.ok) throw new Error('Failed to load page');
        return response.text();
      })
      .then(function (html) {
        var parser = new DOMParser();
        var doc = parser.parseFromString(html, 'text/html');
        var newContent = doc.querySelector('.main-content');
        
        if (newContent) {
          // Swap content
          mainContent.innerHTML = newContent.innerHTML;
          
          // Update title
          if (doc.title) document.title = doc.title;
          
          // Update URL
          if (pushState) {
            window.history.pushState({ url: url }, '', url);
          }
          
          // Scroll to top
          window.scrollTo(0, 0);
          
          // Re-attach navigation handlers to new links
          attachLinkHandlers();
          
          // Trigger any KaTeX rendering if enabled
          if (typeof renderMath === 'function') {
            renderMath();
          }

          // Re-process wiki links in newly injected content
          if (typeof window.processWikiLinksInContent === 'function') {
            try {
              window.processWikiLinksInContent();
            } catch (err) {
              console.error('Wiki link processing failed:', err);
            }
          }
        }
      })
      .catch(function (err) {
        console.error('Navigation error:', err);
        // Fallback to normal navigation
        window.location.href = url;
      });
  }

  function attachLinkHandlers() {
    if (!mainContent) return;
    
    var links = mainContent.querySelectorAll('a');
    links.forEach(function (link) {
      if (link.dataset.navAttached) return;
      link.dataset.navAttached = 'true';
      
      link.addEventListener('click', function (e) {
        var href = link.getAttribute('href');
        if (!href || href.startsWith('#') || link.target === '_blank') return;
        
        var fullUrl = new URL(href, window.location.href).href;
        
        if (isInternalLink(fullUrl)) {
          e.preventDefault();
          loadPage(fullUrl, true);
        }
      });
    });
    
    // Also attach to sidebar links
    var sidebarLinks = document.querySelectorAll('.sidebar-link');
    sidebarLinks.forEach(function (link) {
      if (link.dataset.navAttached) return;
      link.dataset.navAttached = 'true';
      
      link.addEventListener('click', function (e) {
        var href = link.getAttribute('href');
        if (!href || href.startsWith('#')) return;
        
        var fullUrl = new URL(href, window.location.href).href;
        
        if (isInternalLink(fullUrl)) {
          e.preventDefault();
          loadPage(fullUrl, true);
          
          // Update active state
          document.querySelectorAll('.sidebar-item').forEach(function (item) {
            item.classList.remove('active');
          });
          var parent = link.closest('.sidebar-item');
          if (parent) parent.classList.add('active');
        }
      });
    });
  }

  function init() {
    mainContent = document.querySelector('.main-content');
    if (!mainContent) return;

    // Attach handlers to initial page links
    attachLinkHandlers();

    // Handle browser back/forward
    window.addEventListener('popstate', function (e) {
      if (e.state && e.state.url) {
        loadPage(e.state.url, false);
      } else {
        loadPage(window.location.href, false);
      }
    });

    // Save initial state
    window.history.replaceState({ url: window.location.href }, '', window.location.href);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
