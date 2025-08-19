/**
 * Sistema di gestione multilingue per il sito web
 * Supporta italiano (it) e inglese (en)
 */

class I18n {
    constructor() {
        this.currentLanguage = 'it'; // Lingua predefinita
        this.translations = {};
        this.init();
    }

    /**
     * Inizializza il sistema i18n
     */
    async init() {
        // Carica la lingua salvata o usa quella predefinita
        this.currentLanguage = localStorage.getItem('preferred-language') || 'it';
        
        // Carica le traduzioni
        await this.loadTranslations();
        
        // Applica le traduzioni alla pagina
        this.applyTranslations();
        
        // Aggiorna attributo lang del documento
        document.documentElement.lang = this.currentLanguage;
        
        // Inizializza event listeners
        this.initEventListeners();
    }

    /**
     * Carica i file di traduzione
     */
    async loadTranslations() {
        try {
            const response = await fetch(`translations/${this.currentLanguage}.json`);
            this.translations = await response.json();
        } catch (error) {
            console.error('Errore nel caricamento delle traduzioni:', error);
            // Fallback all'italiano se non riesce a caricare
            if (this.currentLanguage !== 'it') {
                this.currentLanguage = 'it';
                await this.loadTranslations();
            }
        }
    }

    /**
     * Applica le traduzioni agli elementi della pagina
     */
    applyTranslations() {
        // Aggiorna il title della pagina
        document.title = this.translations.meta?.title || document.title;

        // Trova tutti gli elementi con data-i18n e applica le traduzioni
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.getTranslation(key);
            
            if (translation) {
                element.textContent = translation;
            }
        });

        // Aggiorna lo stato del language switcher
        this.updateLanguageSwitcher();
    }

    /**
     * Ottiene una traduzione dalla chiave specificata
     * @param {string} key - Chiave della traduzione (es. 'hero.title')
     * @returns {string|null} - Testo tradotto o null se non trovato
     */
    getTranslation(key) {
        const keys = key.split('.');
        let value = this.translations;
        
        for (const k of keys) {
            if (value && typeof value === 'object' && k in value) {
                value = value[k];
            } else {
                return null;
            }
        }
        
        return typeof value === 'string' ? value : null;
    }

    /**
     * Cambia lingua
     * @param {string} language - Codice lingua ('it' o 'en')
     */
    async changeLanguage(language) {
        if (language === this.currentLanguage) return;
        
        this.currentLanguage = language;
        
        // Salva la preferenza
        localStorage.setItem('preferred-language', language);
        
        // Ricarica le traduzioni
        await this.loadTranslations();
        
        // Riapplica le traduzioni
        this.applyTranslations();
        
        // Aggiorna attributo lang del documento
        document.documentElement.lang = language;
    }

    /**
     * Aggiorna lo stato visivo del language switcher
     */
    updateLanguageSwitcher() {
        const switcher = document.querySelector('.language-switcher');
        if (switcher) {
            const buttons = switcher.querySelectorAll('button');
            buttons.forEach(button => {
                const lang = button.getAttribute('data-lang');
                if (lang === this.currentLanguage) {
                    button.classList.add('active');
                } else {
                    button.classList.remove('active');
                }
            });
        }
    }

    /**
     * Inizializza gli event listeners
     */
    initEventListeners() {
        // Event listener per i pulsanti di cambio lingua
        document.addEventListener('click', (event) => {
            if (event.target.matches('[data-lang]')) {
                const language = event.target.getAttribute('data-lang');
                this.changeLanguage(language);
            }
        });
    }
}

// Inizializza il sistema i18n quando il DOM è pronto
document.addEventListener('DOMContentLoaded', () => {
    window.i18n = new I18n();
});