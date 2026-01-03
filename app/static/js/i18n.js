/**
 * Sistema de Internacionalización (i18n) para ViralPost AI
 * Soporta: Español (es), English (en)
 */

const I18n = {
    // Idioma actual
    currentLang: 'es',
    currentCurrency: 'MXN',

    // Tasa de cambio MXN a USD (aproximada, actualizar periódicamente)
    exchangeRate: 17.5,

    // Traducciones
    translations: {
        es: {
            // General
            'app.name': 'ViralPost AI',
            'app.tagline': 'Genera imágenes virales para tus productos',
            'app.description': 'Transforma tus productos en contenido viral con inteligencia artificial',

            // Navegación
            'nav.home': 'Inicio',
            'nav.app': 'Crear',
            'nav.credits': 'Créditos',
            'nav.history': 'Historial',
            'nav.login': 'Iniciar Sesión',
            'nav.register': 'Registrarse',
            'nav.logout': 'Cerrar Sesión',

            // Auth
            'auth.login': 'Iniciar Sesión',
            'auth.register': 'Crear Cuenta',
            'auth.email': 'Correo electrónico',
            'auth.password': 'Contraseña',
            'auth.name': 'Nombre',
            'auth.forgot_password': '¿Olvidaste tu contraseña?',
            'auth.no_account': '¿No tienes cuenta?',
            'auth.have_account': '¿Ya tienes cuenta?',
            'auth.google': 'Continuar con Google',
            'auth.or': 'o',

            // App principal
            'app.product_name': 'Nombre del producto',
            'app.product_name_placeholder': 'Ej: Café Orgánico Premium',
            'app.product_description': 'Descripción del producto',
            'app.product_description_placeholder': 'Describe tu producto, ingredientes, beneficios...',
            'app.brand': 'Marca',
            'app.brand_placeholder': 'Nombre de tu marca',
            'app.price': 'Precio',
            'app.price_placeholder': 'Ej: $299',
            'app.product_image': 'Imagen del producto',
            'app.logo': 'Logo (opcional)',
            'app.select_style': 'Selecciona un estilo',
            'app.generate': 'Generar Imagen',
            'app.generating': 'Generando...',
            'app.credits_remaining': 'créditos disponibles',
            'app.buy_credits': 'Comprar créditos',

            // Estilos
            'style.macro_explosion': 'Explosión Macro',
            'style.liquid_metal': 'Metal Líquido',
            'style.neon_noir': 'Neon Noir',
            'style.botanical_luxury': 'Lujo Botánico',
            'style.zero_gravity': 'Gravedad Cero',
            'style.miniature_world': 'Mundo Miniatura',
            'style.frozen_time': 'Tiempo Congelado',
            'style.dark_luxury': 'Lujo Oscuro',

            // Resultados
            'result.title': 'Tu imagen viral',
            'result.download': 'Descargar',
            'result.share': 'Compartir',
            'result.new': 'Crear otra',
            'result.copy_facebook': 'Copy para Facebook',
            'result.copy_instagram': 'Copy para Instagram',
            'result.copied': '¡Copiado!',

            // Créditos
            'credits.title': 'Comprar Créditos',
            'credits.subtitle': 'Elige el paquete que mejor se adapte a tus necesidades',
            'credits.pack': 'créditos',
            'credits.generations': 'generaciones',
            'credits.popular': 'Popular',
            'credits.best_value': 'Mejor Valor',
            'credits.buy': 'Comprar',
            'credits.per_credit': 'por crédito',

            // Pago
            'payment.success': '¡Pago Exitoso!',
            'payment.credits_added': 'Tus créditos han sido agregados a tu cuenta.',
            'payment.start_creating': 'Ya puedes comenzar a generar imágenes virales.',
            'payment.new_balance': 'Tu nuevo saldo',
            'payment.go_create': 'Ir a Generar',
            'payment.oxxo_title': '¡Voucher OXXO Generado!',
            'payment.oxxo_instructions': 'Tu voucher de pago ha sido generado. Tienes 3 días para realizar el pago en cualquier tienda OXXO.',
            'payment.oxxo_step1': 'Revisa tu correo electrónico para obtener el voucher',
            'payment.oxxo_step2': 'Ve a cualquier tienda OXXO',
            'payment.oxxo_step3': 'Muestra el código de barras al cajero',
            'payment.oxxo_step4': 'Realiza el pago en efectivo',
            'payment.oxxo_note': 'Una vez que pagues, tus créditos se agregarán automáticamente en unos minutos.',
            'payment.back': 'Volver a la App',

            // Historial
            'history.title': 'Historial de Generaciones',
            'history.empty': 'Aún no has generado ninguna imagen',
            'history.start': 'Crear mi primera imagen',

            // Footer
            'footer.terms': 'Términos de Servicio',
            'footer.privacy': 'Política de Privacidad',
            'footer.contact': 'Contacto',
            'footer.rights': 'Todos los derechos reservados',

            // Errores
            'error.generic': 'Ocurrió un error. Por favor intenta de nuevo.',
            'error.no_credits': 'No tienes suficientes créditos',
            'error.invalid_image': 'Por favor sube una imagen válida',
            'error.required_field': 'Este campo es requerido',

            // Moneda
            'currency.symbol': '$',
            'currency.code': 'MXN',
        },

        en: {
            // General
            'app.name': 'ViralPost AI',
            'app.tagline': 'Generate viral images for your products',
            'app.description': 'Transform your products into viral content with artificial intelligence',

            // Navigation
            'nav.home': 'Home',
            'nav.app': 'Create',
            'nav.credits': 'Credits',
            'nav.history': 'History',
            'nav.login': 'Login',
            'nav.register': 'Sign Up',
            'nav.logout': 'Logout',

            // Auth
            'auth.login': 'Login',
            'auth.register': 'Create Account',
            'auth.email': 'Email address',
            'auth.password': 'Password',
            'auth.name': 'Name',
            'auth.forgot_password': 'Forgot your password?',
            'auth.no_account': "Don't have an account?",
            'auth.have_account': 'Already have an account?',
            'auth.google': 'Continue with Google',
            'auth.or': 'or',

            // Main App
            'app.product_name': 'Product name',
            'app.product_name_placeholder': 'Ex: Premium Organic Coffee',
            'app.product_description': 'Product description',
            'app.product_description_placeholder': 'Describe your product, ingredients, benefits...',
            'app.brand': 'Brand',
            'app.brand_placeholder': 'Your brand name',
            'app.price': 'Price',
            'app.price_placeholder': 'Ex: $29.99',
            'app.product_image': 'Product image',
            'app.logo': 'Logo (optional)',
            'app.select_style': 'Select a style',
            'app.generate': 'Generate Image',
            'app.generating': 'Generating...',
            'app.credits_remaining': 'credits remaining',
            'app.buy_credits': 'Buy credits',

            // Styles
            'style.macro_explosion': 'Macro Explosion',
            'style.liquid_metal': 'Liquid Metal',
            'style.neon_noir': 'Neon Noir',
            'style.botanical_luxury': 'Botanical Luxury',
            'style.zero_gravity': 'Zero Gravity',
            'style.miniature_world': 'Miniature World',
            'style.frozen_time': 'Frozen Time',
            'style.dark_luxury': 'Dark Luxury',

            // Results
            'result.title': 'Your viral image',
            'result.download': 'Download',
            'result.share': 'Share',
            'result.new': 'Create another',
            'result.copy_facebook': 'Facebook Copy',
            'result.copy_instagram': 'Instagram Copy',
            'result.copied': 'Copied!',

            // Credits
            'credits.title': 'Buy Credits',
            'credits.subtitle': 'Choose the package that best fits your needs',
            'credits.pack': 'credits',
            'credits.generations': 'generations',
            'credits.popular': 'Popular',
            'credits.best_value': 'Best Value',
            'credits.buy': 'Buy',
            'credits.per_credit': 'per credit',

            // Payment
            'payment.success': 'Payment Successful!',
            'payment.credits_added': 'Your credits have been added to your account.',
            'payment.start_creating': 'You can now start generating viral images.',
            'payment.new_balance': 'Your new balance',
            'payment.go_create': 'Start Creating',
            'payment.oxxo_title': 'OXXO Voucher Generated!',
            'payment.oxxo_instructions': 'Your payment voucher has been generated. You have 3 days to make the payment at any OXXO store.',
            'payment.oxxo_step1': 'Check your email for the voucher',
            'payment.oxxo_step2': 'Go to any OXXO store',
            'payment.oxxo_step3': 'Show the barcode to the cashier',
            'payment.oxxo_step4': 'Pay in cash',
            'payment.oxxo_note': 'Once you pay, your credits will be added automatically within minutes.',
            'payment.back': 'Back to App',

            // History
            'history.title': 'Generation History',
            'history.empty': "You haven't generated any images yet",
            'history.start': 'Create my first image',

            // Footer
            'footer.terms': 'Terms of Service',
            'footer.privacy': 'Privacy Policy',
            'footer.contact': 'Contact',
            'footer.rights': 'All rights reserved',

            // Errors
            'error.generic': 'An error occurred. Please try again.',
            'error.no_credits': "You don't have enough credits",
            'error.invalid_image': 'Please upload a valid image',
            'error.required_field': 'This field is required',

            // Currency
            'currency.symbol': '$',
            'currency.code': 'USD',
        }
    },

    /**
     * Inicializa el sistema de i18n
     */
    init() {
        // Cargar preferencia guardada o detectar automáticamente
        const savedLang = localStorage.getItem('viralpost_lang');
        const savedCurrency = localStorage.getItem('viralpost_currency');

        if (savedLang) {
            this.currentLang = savedLang;
            this.currentCurrency = savedCurrency || (savedLang === 'en' ? 'USD' : 'MXN');
        } else {
            this.detectLanguage();
        }

        // Aplicar traducciones
        this.applyTranslations();

        // Actualizar selector si existe
        this.updateSelector();

        return this;
    },

    /**
     * Detecta el idioma del navegador
     */
    detectLanguage() {
        const browserLang = navigator.language || navigator.userLanguage;

        // Si el idioma contiene 'es', usar español
        if (browserLang.startsWith('es')) {
            this.currentLang = 'es';
            this.currentCurrency = 'MXN';
        } else {
            // Por defecto inglés para otros idiomas
            this.currentLang = 'en';
            this.currentCurrency = 'USD';
        }

        // Guardar preferencia
        this.savePreference();
    },

    /**
     * Cambia el idioma
     */
    setLanguage(lang, currency = null) {
        if (this.translations[lang]) {
            this.currentLang = lang;
            this.currentCurrency = currency || (lang === 'en' ? 'USD' : 'MXN');
            this.savePreference();
            this.applyTranslations();
            this.updateSelector();

            // Disparar evento para que otros componentes se actualicen
            window.dispatchEvent(new CustomEvent('languageChanged', {
                detail: { lang: this.currentLang, currency: this.currentCurrency }
            }));
        }
    },

    /**
     * Guarda la preferencia en localStorage
     */
    savePreference() {
        localStorage.setItem('viralpost_lang', this.currentLang);
        localStorage.setItem('viralpost_currency', this.currentCurrency);
    },

    /**
     * Obtiene una traducción por clave
     */
    t(key, params = {}) {
        const translation = this.translations[this.currentLang]?.[key] ||
                           this.translations['es'][key] ||
                           key;

        // Reemplazar parámetros {{param}}
        return translation.replace(/\{\{(\w+)\}\}/g, (match, param) => {
            return params[param] !== undefined ? params[param] : match;
        });
    },

    /**
     * Convierte precio de MXN a la moneda actual
     */
    convertPrice(priceMXN) {
        if (this.currentCurrency === 'USD') {
            return Math.round(priceMXN / this.exchangeRate * 100) / 100;
        }
        return priceMXN;
    },

    /**
     * Formatea un precio en la moneda actual
     */
    formatPrice(priceMXN) {
        const converted = this.convertPrice(priceMXN);
        const symbol = this.t('currency.symbol');
        const code = this.t('currency.code');

        if (this.currentCurrency === 'USD') {
            return `${symbol}${converted.toFixed(2)} ${code}`;
        }
        return `${symbol}${Math.round(converted).toLocaleString('es-MX')} ${code}`;
    },

    /**
     * Aplica traducciones a elementos con data-i18n
     */
    applyTranslations() {
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            el.textContent = this.t(key);
        });

        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            el.placeholder = this.t(key);
        });

        document.querySelectorAll('[data-i18n-title]').forEach(el => {
            const key = el.getAttribute('data-i18n-title');
            el.title = this.t(key);
        });

        // Actualizar precios
        document.querySelectorAll('[data-price-mxn]').forEach(el => {
            const priceMXN = parseFloat(el.getAttribute('data-price-mxn'));
            el.textContent = this.formatPrice(priceMXN);
        });

        // Actualizar atributo lang del HTML
        document.documentElement.lang = this.currentLang === 'es' ? 'es-MX' : 'en';
    },

    /**
     * Actualiza el selector de idioma en la UI
     */
    updateSelector() {
        const selector = document.getElementById('langSelector');
        if (selector) {
            selector.value = this.currentLang;
        }

        // Actualizar banderas/texto del selector
        const langDisplay = document.getElementById('langDisplay');
        if (langDisplay) {
            langDisplay.textContent = this.currentLang === 'es' ? '🇲🇽 ES' : '🇺🇸 EN';
        }
    },

    /**
     * Obtiene información de la región actual
     */
    getRegionInfo() {
        return {
            lang: this.currentLang,
            currency: this.currentCurrency,
            locale: this.currentLang === 'es' ? 'es-MX' : 'en-US'
        };
    }
};

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    I18n.init();
});

// Exportar para uso global
window.I18n = I18n;
