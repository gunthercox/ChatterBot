// Silktide Consent Manager - https://silktide.com/consent-manager/  

class SilktideCookieBanner {
  constructor(config) {
    this.config = config; // Save config to the instance

    this.wrapper = null;
    this.banner = null;
    this.modal = null;
    this.cookieIcon = null;
    this.backdrop = null;

    this.createWrapper();

    if (this.shouldShowBackdrop()) {
      this.createBackdrop();
    }

    this.createCookieIcon();
    this.createModal();

    if (this.shouldShowBanner()) {
      this.createBanner();
      this.showBackdrop();
    } else {
      this.showCookieIcon();
    }

    this.setupEventListeners();

    if (this.hasSetInitialCookieChoices()) {
      this.loadRequiredCookies();
      this.runAcceptedCookieCallbacks();
    }
  }

  destroyCookieBanner() {
    // Remove all cookie banner elements from the DOM
    if (this.wrapper && this.wrapper.parentNode) {
      this.wrapper.parentNode.removeChild(this.wrapper);
    }

    // Restore scrolling
    this.allowBodyScroll();

    // Clear all references
    this.wrapper = null;
    this.banner = null;
    this.modal = null;
    this.cookieIcon = null;
    this.backdrop = null;
  }

  // ----------------------------------------------------------------
  // Wrapper
  // ----------------------------------------------------------------
  createWrapper() {
    this.wrapper = document.createElement('div');
    this.wrapper.id = 'silktide-wrapper';
    document.body.insertBefore(this.wrapper, document.body.firstChild);
  }

  // ----------------------------------------------------------------
  // Wrapper Child Generator
  // ----------------------------------------------------------------
  createWrapperChild(htmlContent, id) {
    // Create child element
    const child = document.createElement('div');
    child.id = id;
    child.innerHTML = htmlContent;

    // Ensure wrapper exists
    if (!this.wrapper || !document.body.contains(this.wrapper)) {
      this.createWrapper();
    }

    // Append child to wrapper
    this.wrapper.appendChild(child);
    return child;
  }

  // ----------------------------------------------------------------
  // Backdrop
  // ----------------------------------------------------------------
  createBackdrop() {
    this.backdrop = this.createWrapperChild(null, 'silktide-backdrop');
  }

  showBackdrop() {
    if (this.backdrop) {
      this.backdrop.style.display = 'block';
    }
    // Trigger optional onBackdropOpen callback
    if (typeof this.config.onBackdropOpen === 'function') {
      this.config.onBackdropOpen();
    }
  }

  hideBackdrop() {
    if (this.backdrop) {
      this.backdrop.style.display = 'none';
    }

    // Trigger optional onBackdropClose callback
    if (typeof this.config.onBackdropClose === 'function') {
      this.config.onBackdropClose();
    }
  }

  shouldShowBackdrop() {
    return this.config?.background?.showBackground || false;
  }

  // update the checkboxes in the modal with the values from localStorage
  updateCheckboxState(saveToStorage = false) {
    const preferencesSection = this.modal.querySelector('#cookie-preferences');
    const checkboxes = preferencesSection.querySelectorAll('input[type="checkbox"]');

    checkboxes.forEach((checkbox) => {
      const [, cookieId] = checkbox.id.split('cookies-');
      const cookieType = this.config.cookieTypes.find(type => type.id === cookieId);
      
      if (!cookieType) return;

      if (saveToStorage) {
        // Save the current state to localStorage and run callbacks
        const currentState = checkbox.checked;
        
        if (cookieType.required) {
          localStorage.setItem(
            `silktideCookieChoice_${cookieId}${this.getBannerSuffix()}`,
            'true'
          );
        } else {
          localStorage.setItem(
            `silktideCookieChoice_${cookieId}${this.getBannerSuffix()}`,
            currentState.toString()
          );
          
          // Run appropriate callback
          if (currentState && typeof cookieType.onAccept === 'function') {
            cookieType.onAccept();
          } else if (!currentState && typeof cookieType.onReject === 'function') {
            cookieType.onReject();
          }
        }
      } else {
        // When reading values (opening modal)
        if (cookieType.required) {
          checkbox.checked = true;
          checkbox.disabled = true;
        } else {
          const storedValue = localStorage.getItem(
            `silktideCookieChoice_${cookieId}${this.getBannerSuffix()}`
          );
          
          if (storedValue !== null) {
            checkbox.checked = storedValue === 'true';
          } else {
            checkbox.checked = !!cookieType.defaultValue;
          }
        }
      }
    });
  }

  setInitialCookieChoiceMade() {
    window.localStorage.setItem(`silktideCookieBanner_InitialChoice${this.getBannerSuffix()}`, 1);
  }

  // ----------------------------------------------------------------
  // Consent Handling
  // ----------------------------------------------------------------
  handleCookieChoice(accepted) {
    // We set that an initial choice was made regardless of what it was so we don't show the banner again
    this.setInitialCookieChoiceMade();

    this.removeBanner();
    this.hideBackdrop();
    this.toggleModal(false);
    this.showCookieIcon();

    this.config.cookieTypes.forEach((type) => {
      // Set localStorage and run accept/reject callbacks
      if (type.required == true) {
        localStorage.setItem(`silktideCookieChoice_${type.id}${this.getBannerSuffix()}`, 'true');
        if (typeof type.onAccept === 'function') { type.onAccept() }
      } else {
        localStorage.setItem(
          `silktideCookieChoice_${type.id}${this.getBannerSuffix()}`,
          accepted.toString(),
        );

        if (accepted) {
          if (typeof type.onAccept === 'function') { type.onAccept(); }
        } else {
          if (typeof type.onReject === 'function') { type.onReject(); }
        }
      }
    });

    // Trigger optional onAcceptAll/onRejectAll callbacks
    if (accepted && typeof this.config.onAcceptAll === 'function') {
      if (typeof this.config.onAcceptAll === 'function') { this.config.onAcceptAll(); }
    } else if (typeof this.config.onRejectAll === 'function') {
      if (typeof this.config.onRejectAll === 'function') { this.config.onRejectAll(); }
    }

    // finally update the checkboxes in the modal with the values from localStorage
    this.updateCheckboxState();
  }

  getAcceptedCookies() {
    return (this.config.cookieTypes || []).reduce((acc, cookieType) => {
      acc[cookieType.id] =
        localStorage.getItem(`silktideCookieChoice_${cookieType.id}${this.getBannerSuffix()}`) ===
        'true';
      return acc;
    }, {});
  }

  runAcceptedCookieCallbacks() {
    if (!this.config.cookieTypes) return;

    const acceptedCookies = this.getAcceptedCookies();
    this.config.cookieTypes.forEach((type) => {
      if (type.required) return; // we run required cookies separately in loadRequiredCookies
      if (acceptedCookies[type.id] && typeof type.onAccept === 'function') {
        if (typeof type.onAccept === 'function') { type.onAccept(); }
      }
    });
  }

  runRejectedCookieCallbacks() {
    if (!this.config.cookieTypes) return;

    const rejectedCookies = this.getRejectedCookies();
    this.config.cookieTypes.forEach((type) => {
      if (rejectedCookies[type.id] && typeof type.onReject === 'function') {
        if (typeof type.onReject === 'function') { type.onReject(); }
      }
    });
  }

  /**
   * Run through all of the cookie callbacks based on the current localStorage values
   */
  runStoredCookiePreferenceCallbacks() {
    this.config.cookieTypes.forEach((type) => {
      const accepted =
        localStorage.getItem(`silktideCookieChoice_${type.id}${this.getBannerSuffix()}`) === 'true';
      // Set localStorage and run accept/reject callbacks
      if (accepted) {
        if (typeof type.onAccept === 'function') { type.onAccept(); }
      } else {
        if (typeof type.onReject === 'function') { type.onReject(); }
      }
    });
  }

  loadRequiredCookies() {
    if (!this.config.cookieTypes) return;
    this.config.cookieTypes.forEach((cookie) => {
      if (cookie.required && typeof cookie.onAccept === 'function') {
        if (typeof cookie.onAccept === 'function') { cookie.onAccept(); }
      }
    });
  }

  // ----------------------------------------------------------------
  // Banner
  // ----------------------------------------------------------------
  getBannerContent() {
    const bannerDescription =
      this.config.text?.banner?.description ||
      "<p>We use cookies on our site to enhance your user experience, provide personalized content, and analyze our traffic.</p>";

    // Accept button
    const acceptAllButtonText = this.config.text?.banner?.acceptAllButtonText || 'Accept all';
    const acceptAllButtonLabel = this.config.text?.banner?.acceptAllButtonAccessibleLabel;
    const acceptAllButton = `<button class="accept-all st-button st-button--primary"${
      acceptAllButtonLabel && acceptAllButtonLabel !== acceptAllButtonText 
        ? ` aria-label="${acceptAllButtonLabel}"` 
        : ''
    }>${acceptAllButtonText}</button>`;
    
    // Reject button
    const rejectNonEssentialButtonText = this.config.text?.banner?.rejectNonEssentialButtonText || 'Reject non-essential';
    const rejectNonEssentialButtonLabel = this.config.text?.banner?.rejectNonEssentialButtonAccessibleLabel;
    const rejectNonEssentialButton = `<button class="reject-all st-button st-button--primary"${
      rejectNonEssentialButtonLabel && rejectNonEssentialButtonLabel !== rejectNonEssentialButtonText 
        ? ` aria-label="${rejectNonEssentialButtonLabel}"` 
        : ''
    }>${rejectNonEssentialButtonText}</button>`;

    // Preferences button
    const preferencesButtonText = this.config.text?.banner?.preferencesButtonText || 'Preferences';
    const preferencesButtonLabel = this.config.text?.banner?.preferencesButtonAccessibleLabel;
    const preferencesButton = `<button class="preferences"${
      preferencesButtonLabel && preferencesButtonLabel !== preferencesButtonText 
        ? ` aria-label="${preferencesButtonLabel}"` 
        : ''
    }><span>${preferencesButtonText}</span></button>`;
    

    // Silktide logo link
    const silktideLogo = `
      <a class="silktide-logo" href="https://silktide.com/consent-manager" target="_blank" rel="noreferrer" aria-label="Visit the Silktide Consent Manager page">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="25" viewBox="0 0 24 25" fill="inherit">
          <path fill-rule="evenodd" clip-rule="evenodd" d="M14.1096 16.7745C13.8895 17.2055 13.3537 17.3805 12.9129 17.1653L8.28443 14.9055L2.73192 17.7651L11.1025 21.9814C11.909 22.3876 12.8725 22.3591 13.6524 21.9058L20.4345 17.9645C21.2845 17.4704 21.7797 16.5522 21.7164 15.5872L21.7088 15.4704C21.6487 14.5561 21.0962 13.7419 20.2579 13.3326L15.6793 11.0972L10.2283 13.9045L13.71 15.6043C14.1507 15.8195 14.3297 16.3434 14.1096 16.7745ZM8.2627 12.9448L13.7136 10.1375L10.2889 8.46543C9.84803 8.25021 9.66911 7.72629 9.88916 7.29524C10.1093 6.86417 10.6451 6.68921 11.0859 6.90442L15.6575 9.13647L21.2171 6.27325L12.8808 2.03496C12.0675 1.62147 11.0928 1.65154 10.3078 2.11432L3.54908 6.09869C2.70732 6.59492 2.21846 7.50845 2.28139 8.46761L2.29003 8.59923C2.35002 9.51362 2.9026 10.3278 3.7409 10.7371L8.2627 12.9448ZM6.31884 13.9458L2.94386 12.2981C1.53727 11.6113 0.610092 10.2451 0.509431 8.71094L0.500795 8.57933C0.3952 6.96993 1.21547 5.4371 2.62787 4.60447L9.38662 0.620092C10.7038 -0.156419 12.3392 -0.206861 13.7039 0.486938L23.3799 5.40639C23.4551 5.44459 23.5224 5.4918 23.5811 5.54596C23.7105 5.62499 23.8209 5.73754 23.897 5.87906C24.1266 6.30534 23.9594 6.83293 23.5234 7.05744L17.6231 10.0961L21.0549 11.7716C22.4615 12.4583 23.3887 13.8245 23.4893 15.3587L23.497 15.4755C23.6033 17.0947 22.7724 18.6354 21.346 19.4644L14.5639 23.4057C13.2554 24.1661 11.6386 24.214 10.2854 23.5324L0.621855 18.6649C0.477299 18.592 0.361696 18.4859 0.279794 18.361C0.210188 18.2968 0.150054 18.2204 0.10296 18.133C-0.126635 17.7067 0.0406445 17.1792 0.47659 16.9546L6.31884 13.9458Z" fill="inherit"/>
        </svg>
      </a>
    `;

    const bannerContent = `
      ${bannerDescription}
      <div class="actions">                               
        ${acceptAllButton}
        ${rejectNonEssentialButton}
        <div class="actions-row">
          ${preferencesButton}
          ${silktideLogo}
        </div>
      </div>
    `;

    return bannerContent;
  }

  hasSetInitialCookieChoices() {
    return !!localStorage.getItem(`silktideCookieBanner_InitialChoice${this.getBannerSuffix()}`);
  }

  createBanner() {
    // Create banner element
    this.banner = this.createWrapperChild(this.getBannerContent(), 'silktide-banner');

    // Add positioning class from config
    if (this.banner && this.config.position?.banner) {
      this.banner.classList.add(this.config.position.banner);
    }

    // Trigger optional onBannerOpen callback
    if (this.banner && typeof this.config.onBannerOpen === 'function') {
      this.config.onBannerOpen();
    }
  }

  removeBanner() {
    if (this.banner && this.banner.parentNode) {
      this.banner.parentNode.removeChild(this.banner);
      this.banner = null;

      // Trigger optional onBannerClose callback
      if (typeof this.config.onBannerClose === 'function') {
        this.config.onBannerClose();
      }
    }
  }

  shouldShowBanner() {
    if (this.config.showBanner === false) {
      return false;
    }
    return (
      localStorage.getItem(`silktideCookieBanner_InitialChoice${this.getBannerSuffix()}`) === null
    );
  }

  // ----------------------------------------------------------------
  // Modal
  // ----------------------------------------------------------------
  getModalContent() {
    const preferencesTitle =
      this.config.text?.preferences?.title || 'Customize your cookie preferences';
    
    const preferencesDescription =
      this.config.text?.preferences?.description ||
      "<p>We respect your right to privacy. You can choose not to allow some types of cookies. Your cookie preferences will apply across our website.</p>";
    
    // Preferences button
    const preferencesButtonLabel = this.config.text?.banner?.preferencesButtonAccessibleLabel;

    const closeModalButton = `<button class="modal-close"${preferencesButtonLabel ? ` aria-label="${preferencesButtonLabel}"` : ''}>
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M19.4081 3.41559C20.189 2.6347 20.189 1.36655 19.4081 0.585663C18.6272 -0.195221 17.3591 -0.195221 16.5782 0.585663L10 7.17008L3.41559 0.59191C2.6347 -0.188974 1.36655 -0.188974 0.585663 0.59191C-0.195221 1.37279 -0.195221 2.64095 0.585663 3.42183L7.17008 10L0.59191 16.5844C-0.188974 17.3653 -0.188974 18.6335 0.59191 19.4143C1.37279 20.1952 2.64095 20.1952 3.42183 19.4143L10 12.8299L16.5844 19.4081C17.3653 20.189 18.6335 20.189 19.4143 19.4081C20.1952 18.6272 20.1952 17.3591 19.4143 16.5782L12.8299 10L19.4081 3.41559Z"/>
      </svg>
    </button>`;
    

    const cookieTypes = this.config.cookieTypes || [];
    const acceptedCookieMap = this.getAcceptedCookies();

    // Accept button
    const acceptAllButtonText = this.config.text?.banner?.acceptAllButtonText || 'Accept all';
    const acceptAllButtonLabel = this.config.text?.banner?.acceptAllButtonAccessibleLabel;
    const acceptAllButton = `<button class="preferences-accept-all st-button st-button--primary"${
      acceptAllButtonLabel && acceptAllButtonLabel !== acceptAllButtonText 
        ? ` aria-label="${acceptAllButtonLabel}"` 
        : ''
    }>${acceptAllButtonText}</button>`;
    
    // Reject button
    const rejectNonEssentialButtonText = this.config.text?.banner?.rejectNonEssentialButtonText || 'Reject non-essential';
    const rejectNonEssentialButtonLabel = this.config.text?.banner?.rejectNonEssentialButtonAccessibleLabel;
    const rejectNonEssentialButton = `<button class="preferences-reject-all st-button st-button--primary"${
      rejectNonEssentialButtonLabel && rejectNonEssentialButtonLabel !== rejectNonEssentialButtonText 
        ? ` aria-label="${rejectNonEssentialButtonLabel}"` 
        : ''
    }>${rejectNonEssentialButtonText}</button>`;
    
    // Credit link
    const creditLinkText = this.config.text?.preferences?.creditLinkText || 'Get this banner for free';
    const creditLinkAccessibleLabel = this.config.text?.preferences?.creditLinkAccessibleLabel;
    const creditLink = `<a href="https://silktide.com/consent-manager" target="_blank" rel="noreferrer"${
      creditLinkAccessibleLabel && creditLinkAccessibleLabel !== creditLinkText
        ? ` aria-label="${creditLinkAccessibleLabel}"`
        : ''
    }>${creditLinkText}</a>`;
    
    

    const modalContent = `
      <header>
        <h1>${preferencesTitle}</h1>                    
        ${closeModalButton}
      </header>
      ${preferencesDescription}
      <section id="cookie-preferences">
        ${cookieTypes
          .map((type) => {
            const accepted = acceptedCookieMap[type.id];
            let isChecked = false;

            // if it's accepted then show as checked
            if (accepted) {
              isChecked = true;
            }

            // if nothing has been accepted / rejected yet, then show as checked if the default value is true
            if (!accepted && !this.hasSetInitialCookieChoices()) {
              isChecked = type.defaultValue;
            }

            return `
            <fieldset>
                <legend>${type.name}</legend>
                <div class="cookie-type-content">
                    <div class="cookie-type-description">${type.description}</div>
                    <label class="switch" for="cookies-${type.id}">
                        <input type="checkbox" id="cookies-${type.id}" ${
              type.required ? 'checked disabled' : isChecked ? 'checked' : ''
            } />
                        <span class="switch__pill" aria-hidden="true"></span>
                        <span class="switch__dot" aria-hidden="true"></span>
                        <span class="switch__off" aria-hidden="true">Off</span>
                        <span class="switch__on" aria-hidden="true">On</span>
                    </label>
                </div>
            </fieldset>
        `;
          })
          .join('')}
      </section>
      <footer>
        ${acceptAllButton}
        ${rejectNonEssentialButton}
        ${creditLink}
      </footer>
    `;

    return modalContent;
  }

  createModal() {
    // Create banner element
    this.modal = this.createWrapperChild(this.getModalContent(), 'silktide-modal');
  }

  toggleModal(show) {
    if (!this.modal) return;

    this.modal.style.display = show ? 'flex' : 'none';

    if (show) {
      this.showBackdrop();
      this.hideCookieIcon();
      this.removeBanner();
      this.preventBodyScroll();

      // Focus the close button
      const modalCloseButton = this.modal.querySelector('.modal-close');
      modalCloseButton.focus();

      // Trigger optional onPreferencesOpen callback
      if (typeof this.config.onPreferencesOpen === 'function') {
        this.config.onPreferencesOpen();
      }

      this.updateCheckboxState(false); // read from storage when opening
    } else {
      // Set that an initial choice was made when closing the modal
      this.setInitialCookieChoiceMade();
      
      // Save current checkbox states to storage
      this.updateCheckboxState(true);

      this.hideBackdrop();
      this.showCookieIcon();
      this.allowBodyScroll();

      // Trigger optional onPreferencesClose callback
      if (typeof this.config.onPreferencesClose === 'function') {
        this.config.onPreferencesClose();
      }
    }
  }

  // ----------------------------------------------------------------
  // Cookie Icon
  // ----------------------------------------------------------------
  getCookieIconContent() {
    return `
      <svg width="38" height="38" viewBox="0 0 38 38" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M19.1172 1.15625C19.0547 0.734374 18.7344 0.390624 18.3125 0.328124C16.5859 0.0859365 14.8281 0.398437 13.2813 1.21875L7.5 4.30469C5.96094 5.125 4.71875 6.41406 3.95313 7.98437L1.08594 13.8906C0.320314 15.4609 0.0703136 17.2422 0.375001 18.9609L1.50781 25.4297C1.8125 27.1562 2.64844 28.7344 3.90625 29.9531L8.61719 34.5156C9.875 35.7344 11.4766 36.5156 13.2031 36.7578L19.6875 37.6719C21.4141 37.9141 23.1719 37.6016 24.7188 36.7812L30.5 33.6953C32.0391 32.875 33.2813 31.5859 34.0469 30.0078L36.9141 24.1094C37.6797 22.5391 37.9297 20.7578 37.625 19.0391C37.5547 18.625 37.2109 18.3125 36.7969 18.25C32.7734 17.6094 29.5469 14.5703 28.6328 10.6406C28.4922 10.0469 28.0078 9.59375 27.4063 9.5C23.1406 8.82031 19.7734 5.4375 19.1094 1.15625H19.1172ZM15.25 10.25C15.913 10.25 16.5489 10.5134 17.0178 10.9822C17.4866 11.4511 17.75 12.087 17.75 12.75C17.75 13.413 17.4866 14.0489 17.0178 14.5178C16.5489 14.9866 15.913 15.25 15.25 15.25C14.587 15.25 13.9511 14.9866 13.4822 14.5178C13.0134 14.0489 12.75 13.413 12.75 12.75C12.75 12.087 13.0134 11.4511 13.4822 10.9822C13.9511 10.5134 14.587 10.25 15.25 10.25ZM10.25 25.25C10.25 24.587 10.5134 23.9511 10.9822 23.4822C11.4511 23.0134 12.087 22.75 12.75 22.75C13.413 22.75 14.0489 23.0134 14.5178 23.4822C14.9866 23.9511 15.25 24.587 15.25 25.25C15.25 25.913 14.9866 26.5489 14.5178 27.0178C14.0489 27.4866 13.413 27.75 12.75 27.75C12.087 27.75 11.4511 27.4866 10.9822 27.0178C10.5134 26.5489 10.25 25.913 10.25 25.25ZM27.75 20.25C28.413 20.25 29.0489 20.5134 29.5178 20.9822C29.9866 21.4511 30.25 22.087 30.25 22.75C30.25 23.413 29.9866 24.0489 29.5178 24.5178C29.0489 24.9866 28.413 25.25 27.75 25.25C27.087 25.25 26.4511 24.9866 25.9822 24.5178C25.5134 24.0489 25.25 23.413 25.25 22.75C25.25 22.087 25.5134 21.4511 25.9822 20.9822C26.4511 20.5134 27.087 20.25 27.75 20.25Z" />
      </svg>
    `;
  }

  createCookieIcon() {
    this.cookieIcon = document.createElement('button');
    this.cookieIcon.id = 'silktide-cookie-icon';
    this.cookieIcon.title = 'Manage your cookie preferences for this site';
    this.cookieIcon.innerHTML = this.getCookieIconContent();

    if (this.config.text?.banner?.preferencesButtonAccessibleLabel) {
      this.cookieIcon.ariaLabel = this.config.text?.banner?.preferencesButtonAccessibleLabel;
    }

    // Ensure wrapper exists
    if (!this.wrapper || !document.body.contains(this.wrapper)) {
      this.createWrapper();
    }

    // Append child to wrapper
    this.wrapper.appendChild(this.cookieIcon);

    // Add positioning class from config
    if (this.cookieIcon && this.config.cookieIcon?.position) {
      this.cookieIcon.classList.add(this.config.cookieIcon.position);
    }

    // Add color scheme class from config
    if (this.cookieIcon && this.config.cookieIcon?.colorScheme) {
      this.cookieIcon.classList.add(this.config.cookieIcon.colorScheme);
    }
  }

  showCookieIcon() {
    if (this.cookieIcon) {
      this.cookieIcon.style.display = 'flex';
    }
  }

  hideCookieIcon() {
    if (this.cookieIcon) {
      this.cookieIcon.style.display = 'none';
    }
  }

  /**
   * This runs if the user closes the modal without making a choice for the first time
   * We apply the default values and the necessary values as default
   */
  handleClosedWithNoChoice() {
    this.config.cookieTypes.forEach((type) => {
      let accepted = true;
      // Set localStorage and run accept/reject callbacks
      if (type.required == true || type.defaultValue) {
        localStorage.setItem(
          `silktideCookieChoice_${type.id}${this.getBannerSuffix()}`,
          accepted.toString(),
        );
      } else {
        accepted = false;
        localStorage.setItem(
          `silktideCookieChoice_${type.id}${this.getBannerSuffix()}`,
          accepted.toString(),
        );
      }

      if (accepted) {
        if (typeof type.onAccept === 'function') { type.onAccept(); }
      } else {
        if (typeof type.onReject === 'function') { type.onReject(); }
      }
      // set the flag to say that the cookie choice has been made
      this.setInitialCookieChoiceMade();
      this.updateCheckboxState();
    });
  }

  // ----------------------------------------------------------------
  // Focusable Elements
  // ----------------------------------------------------------------
  getFocusableElements(element) {
    return element.querySelectorAll(
      'button, a[href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
    );
  }

  // ----------------------------------------------------------------
  // Event Listeners
  // ----------------------------------------------------------------
  setupEventListeners() {
    // Check Banner exists before trying to add event listeners
    if (this.banner) {
      // Get the buttons
      const acceptButton = this.banner.querySelector('.accept-all');
      const rejectButton = this.banner.querySelector('.reject-all');
      const preferencesButton = this.banner.querySelector('.preferences');

      // Add event listeners to the buttons
      acceptButton?.addEventListener('click', () => this.handleCookieChoice(true));
      rejectButton?.addEventListener('click', () => this.handleCookieChoice(false));
      preferencesButton?.addEventListener('click', () => {
        this.showBackdrop();
        this.toggleModal(true);
      });

      // Focus Trap
      const focusableElements = this.getFocusableElements(this.banner);
      const firstFocusableEl = focusableElements[0];
      const lastFocusableEl = focusableElements[focusableElements.length - 1];

      // Add keydown event listener to handle tab navigation
      this.banner.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
          if (e.shiftKey) {
            if (document.activeElement === firstFocusableEl) {
              lastFocusableEl.focus();
              e.preventDefault();
            }
          } else {
            if (document.activeElement === lastFocusableEl) {
              firstFocusableEl.focus();
              e.preventDefault();
            }
          }
        }
      });

      // Set initial focus
      if (this.config.mode !== 'wizard') {
        acceptButton?.focus();
      }
    }

    // Check Modal exists before trying to add event listeners
    if (this.modal) {
      const closeButton = this.modal.querySelector('.modal-close');
      const acceptAllButton = this.modal.querySelector('.preferences-accept-all');
      const rejectAllButton = this.modal.querySelector('.preferences-reject-all');

      closeButton?.addEventListener('click', () => {
        this.toggleModal(false);

        const hasMadeFirstChoice = this.hasSetInitialCookieChoices();

        if (hasMadeFirstChoice) {
          // run through the callbacks based on the current localStorage state
          this.runStoredCookiePreferenceCallbacks();
        } else {
          // handle the case where the user closes without making a choice for the first time
          this.handleClosedWithNoChoice();
        }
      });
      acceptAllButton?.addEventListener('click', () => this.handleCookieChoice(true));
      rejectAllButton?.addEventListener('click', () => this.handleCookieChoice(false));

      // Banner Focus Trap
      const focusableElements = this.getFocusableElements(this.modal);
      const firstFocusableEl = focusableElements[0];
      const lastFocusableEl = focusableElements[focusableElements.length - 1];

      this.modal.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
          if (e.shiftKey) {
            if (document.activeElement === firstFocusableEl) {
              lastFocusableEl.focus();
              e.preventDefault();
            }
          } else {
            if (document.activeElement === lastFocusableEl) {
              firstFocusableEl.focus();
              e.preventDefault();
            }
          }
        }
        if (e.key === 'Escape') {
          this.toggleModal(false);
        }
      });

      closeButton?.focus();

      // Update the checkbox event listeners
      const preferencesSection = this.modal.querySelector('#cookie-preferences');
      const checkboxes = preferencesSection.querySelectorAll('input[type="checkbox"]');
      
      checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', (event) => {
          const [, cookieId] = event.target.id.split('cookies-');
          const isAccepted = event.target.checked;
          const previousValue = localStorage.getItem(
            `silktideCookieChoice_${cookieId}${this.getBannerSuffix()}`
          ) === 'true';
          
          // Only proceed if the value has actually changed
          if (isAccepted !== previousValue) {
            // Find the corresponding cookie type
            const cookieType = this.config.cookieTypes.find(type => type.id === cookieId);
            
            if (cookieType) {
              // Update localStorage
              localStorage.setItem(
                `silktideCookieChoice_${cookieId}${this.getBannerSuffix()}`,
                isAccepted.toString()
              );
              
              // Run the appropriate callback only if the value changed
              if (isAccepted && typeof cookieType.onAccept === 'function') {
                cookieType.onAccept();
              } else if (!isAccepted && typeof cookieType.onReject === 'function') {
                cookieType.onReject();
              }
            }
          }
        });
      });
    }

    // Check Cookie Icon exists before trying to add event listeners
    if (this.cookieIcon) {

      this.cookieIcon.addEventListener('click', () => {
        // If modal is not found, create it
        if (!this.modal) {
          this.createModal();
          this.toggleModal(true);
          this.hideCookieIcon();
        }
        // If modal is hidden, show it
        else if (this.modal.style.display === 'none' || this.modal.style.display === '') {
          this.toggleModal(true);
          this.hideCookieIcon();
        }
        // If modal is visible, hide it
        else {
          this.toggleModal(false);
        }
      });
    }
  }

  getBannerSuffix() {
    if (this.config.bannerSuffix) {
      return '_' + this.config.bannerSuffix;
    }
    return '';
  }

  preventBodyScroll() {
    document.body.style.overflow = 'hidden';
    // Prevent iOS Safari scrolling
    document.body.style.position = 'fixed';
    document.body.style.width = '100%';
  }

  allowBodyScroll() {
    document.body.style.overflow = '';
    document.body.style.position = '';
    document.body.style.width = '';
  }
}

(function () {
  window.silktideCookieBannerManager = {};

  let config = {};
  let cookieBanner;

  function updateCookieBannerConfig(userConfig = {}) {
    config = {...config, ...userConfig};

    // If cookie banner exists, destroy and recreate it with new config
    if (cookieBanner) {
      cookieBanner.destroyCookieBanner(); // We'll need to add this method
      cookieBanner = null;
    }

    // Only initialize if document.body exists
    if (document.body) {
      initCookieBanner();
    } else {
      // Wait for DOM to be ready
      document.addEventListener('DOMContentLoaded', initCookieBanner, {once: true});
    }
  }

  function initCookieBanner() {
    if (!cookieBanner) {
      cookieBanner = new SilktideCookieBanner(config); // Pass config to the CookieBanner instance
    }
  }

  function injectScript(url, loadOption) {
    // Check if script with this URL already exists
    const existingScript = document.querySelector(`script[src="${url}"]`);
    if (existingScript) {
      return; // Script already exists, don't add it again
    }

    const script = document.createElement('script');
    script.src = url;

    // Apply the async or defer attribute based on the loadOption parameter
    if (loadOption === 'async') {
      script.async = true;
    } else if (loadOption === 'defer') {
      script.defer = true;
    }

    document.head.appendChild(script);
  }

  window.silktideCookieBannerManager.initCookieBanner = initCookieBanner;
  window.silktideCookieBannerManager.updateCookieBannerConfig = updateCookieBannerConfig;
  window.silktideCookieBannerManager.injectScript = injectScript;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCookieBanner, {once: true});
  } else {
    initCookieBanner();
  }
})();