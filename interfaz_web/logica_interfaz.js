/**
 * CustomMatch — Lógica de la Interfaz (`interfaz_web/logica_interfaz.js`)
 * - Al entrar muestra primero la portada explicativa con fotos reales de maquillaje.
 * - Al iniciar sesión o registrarse muestra el catálogo personalizado sin volver a preguntar.
 * - Incluye botón de Cerrar sesión y botones directos a WhatsApp para Atención Personalizada.
 */

const STORAGE_EMAIL_KEY = "custommatch_logged_email";

let currentUser = null;
let currentCategory = "todos";

function formatMoney(value) {
    const num = Number(value) || 0;
    return "$" + num.toLocaleString("es-CO");
}

function getCheckedValues(containerId) {
    const checkboxes = document.querySelectorAll(`#${containerId} input[type="checkbox"]:checked`);
    const vals = Array.from(checkboxes).map((cb) => cb.value);
    return vals.length > 0 ? vals : ["ninguna"];
}

function setCheckedValues(containerId, activeValues) {
    const set = new Set(activeValues || []);
    const checkboxes = document.querySelectorAll(`#${containerId} input[type="checkbox"]`);
    checkboxes.forEach((cb) => {
        cb.checked = set.has(cb.value);
    });
}

function mostrarVistaBienvenida() {
    currentUser = null;
    localStorage.removeItem(STORAGE_EMAIL_KEY);

    document.getElementById("welcomeLandingView").classList.remove("hidden");
    document.getElementById("catalogoPersonalizadoSection").classList.add("hidden");

    document.getElementById("navGuestActions").classList.remove("hidden");
    document.getElementById("navUserActions").classList.add("hidden");
    document.getElementById("navLinkComoFunciona").classList.remove("hidden");
    document.getElementById("navLinkCatalogo").classList.add("hidden");
}

function activarSesionUsuaria(user) {
    if (!user) return;
    currentUser = user;
    localStorage.setItem(STORAGE_EMAIL_KEY, user.email);

    // Cambiar de la portada de bienvenida al catálogo personalizado
    document.getElementById("welcomeLandingView").classList.add("hidden");
    document.getElementById("catalogoPersonalizadoSection").classList.remove("hidden");

    document.getElementById("navGuestActions").classList.add("hidden");
    document.getElementById("navUserActions").classList.remove("hidden");
    document.getElementById("navLinkComoFunciona").classList.add("hidden");
    document.getElementById("navLinkCatalogo").classList.remove("hidden");

    const sp = user.skin_profile || {
        skin_type: "mixta",
        skin_tone: "media",
        undertone: "oliva",
        conditions: ["acne", "sensibilidad"],
        last_max_price_cop: 190000
    };

    const primerNombre = (user.name || "Usuaria").split(" ")[0];
    document.getElementById("navUserName").textContent = `Hola, ${primerNombre}`;
    document.getElementById("profileStripTitle").textContent = `Recomendaciones para ${user.name}`;
    document.getElementById("savedSkinType").textContent = sp.skin_type;
    document.getElementById("savedSkinTone").textContent = sp.skin_tone;
    document.getElementById("savedUndertone").textContent = sp.undertone;
    document.getElementById("savedConditions").textContent = (sp.conditions || ["ninguna"]).join(", ");

    const slider = document.getElementById("budgetSliderCop");
    if (sp.last_max_price_cop && slider) {
        const val = Math.max(25000, Number(sp.last_max_price_cop));
        slider.value = val;
        document.getElementById("budgetLiveDisplay").textContent = formatMoney(val);
    }

    document.getElementById("editSkinType").value = sp.skin_type || "mixta";
    document.getElementById("editSkinTone").value = sp.skin_tone || "media";
    document.getElementById("editUndertone").value = sp.undertone || "oliva";
    setCheckedValues("editConditionsGroup", sp.conditions || ["ninguna"]);
}

function renderCatalogProducts(catalogData) {
    const grid = document.getElementById("productsGrid");
    const counterPill = document.getElementById("resultsCounterPill");
    const aiAdviceText = document.getElementById("aiSearchAdviceText");

    const products = (catalogData && catalogData.products) || [];
    const maxBudgetStr = formatMoney(document.getElementById("budgetSliderCop").value);
    counterPill.textContent = `${products.length} productos hasta ${maxBudgetStr}`;

    if (currentUser && currentUser.skin_profile) {
        const sp = currentUser.skin_profile;
        aiAdviceText.textContent = `Productos seleccionados para tu piel ${sp.skin_type} (tono ${sp.skin_tone}, subtono ${sp.undertone}).`;
    }

    if (products.length === 0) {
        grid.innerHTML = `
            <div class="product-card" style="grid-column: 1 / -1; padding: 2.2rem; text-align: center;">
                <h3 class="product-name" style="margin-bottom: 0.5rem;">
                    No encontramos productos hasta ${maxBudgetStr} con ese filtro
                </h3>
                <p class="product-desc">
                    Sube un poco el deslizador de <strong>Precio máximo</strong> o elige otra categoría para ver más opciones.
                </p>
            </div>
        `;
        return;
    }

    grid.innerHTML = products
        .map(
            (item) => `
        <article class="product-card">
            <div class="product-photo-wrap">
                <img
                    src="${item.image_url || `/imagenes_productos/${item.sku}.svg`}"
                    alt="${item.name}"
                    loading="lazy"
                />
                <span class="store-tag-badge">${item.store_name.replace(" Colombia", "")}</span>
            </div>

            <div class="product-info">
                <span class="product-brand">${item.brand}</span>
                <h3 class="product-name">${item.name}</h3>

                <div class="shade-pill">
                    Tono ideal para ti: ${item.recommended_shade}
                </div>

                <p class="product-desc">${item.key_benefit}</p>

                <div class="product-bottom">
                    <span class="product-price">${item.formatted_price_cop}</span>
                    <a
                        href="${item.store_url}"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="btn-product-link"
                    >
                        <span>Ver producto</span>
                        <svg class="icon-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M7 17L17 7"/><path d="M8 7h9v9"/>
                        </svg>
                    </a>
                </div>
            </div>
        </article>
    `
        )
        .join("");
}

function renderAdvisors(advisors) {
    const advisorsGrid = document.getElementById("advisorsGrid");
    if (!advisorsGrid || !advisors) return;

    advisorsGrid.innerHTML = advisors
        .map(
            (adv) => `
        <div class="advisor-card">
            <div>
                <div class="advisor-top">
                    <div class="advisor-avatar" style="background: ${adv.accent_color || "#c95b72"};">
                        ${adv.avatar_initials}
                    </div>
                    <div>
                        <h4 class="advisor-name">${adv.name}</h4>
                        <span class="advisor-city">${adv.city}</span>
                    </div>
                </div>
                <p class="advisor-role" style="margin-top: 0.75rem;">${adv.role}</p>
            </div>

            <a
                href="${adv.whatsapp_url}"
                target="_blank"
                rel="noopener noreferrer"
                class="btn-whatsapp full-width"
            >
                <svg class="icon-wa" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>
                </svg>
                <span>Hablar por WhatsApp</span>
                <svg class="icon-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M7 17L17 7"/><path d="M8 7h9v9"/>
                </svg>
            </a>
        </div>
    `
        )
        .join("");
}

async function loadSupportAdvisors() {
    try {
        const res = await fetch("/api/v1/support/info");
        const data = await res.json();
        if (data.status === "OK") {
            renderAdvisors(data.advisors || []);
        }
    } catch (err) {
        console.error("Error cargando asesoras:", err);
    }
}

async function executeDynamicSearch() {
    const query = document.getElementById("searchInput").value.trim();
    const maxPriceCop = Number(document.getElementById("budgetSliderCop").value) || 190000;
    const storeFilter = document.getElementById("storeSelect").value;
    const sp = (currentUser && currentUser.skin_profile) || {};

    const payload = {
        email: currentUser ? currentUser.email : "valeria@leclat.co",
        query: query,
        category: currentCategory,
        store_filter: storeFilter,
        max_price_cop: maxPriceCop,
        skin_type: sp.skin_type || "mixta",
        skin_tone: sp.skin_tone || "media",
        undertone: sp.undertone || "oliva",
        conditions: sp.conditions || ["acne", "sensibilidad"]
    };

    try {
        const res = await fetch("/api/v1/catalog/search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.status === "OK") {
            renderCatalogProducts(data.catalog);
        }
    } catch (err) {
        console.error("Error buscando en catálogo:", err);
    }
}

async function restoreSessionIfLogged() {
    const savedEmail = localStorage.getItem(STORAGE_EMAIL_KEY);
    if (!savedEmail) {
        // Si no ha iniciado sesión, mostrar la pantalla de bienvenida explicativa
        mostrarVistaBienvenida();
        return;
    }

    try {
        const res = await fetch("/api/v1/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: savedEmail, password: "" })
        });
        const data = await res.json();
        if (data.status === "OK") {
            activarSesionUsuaria(data.user);
            executeDynamicSearch();
            return;
        }
    } catch (e) {
        console.error("Error restaurando sesión:", e);
    }
    mostrarVistaBienvenida();
}

function showRegisterWizardStep(stepNumber) {
    const s1 = document.getElementById("regStep1Explanation");
    const s2 = document.getElementById("regStep2Account");
    const s3 = document.getElementById("regStep3SkinQuiz");

    const ind1 = document.getElementById("wizIndicator1");
    const ind2 = document.getElementById("wizIndicator2");
    const ind3 = document.getElementById("wizIndicator3");

    s1.classList.add("hidden");
    s2.classList.add("hidden");
    s3.classList.add("hidden");
    ind1.classList.remove("active");
    ind2.classList.remove("active");
    ind3.classList.remove("active");

    if (stepNumber === 1) {
        s1.classList.remove("hidden");
        ind1.classList.add("active");
    } else if (stepNumber === 2) {
        s2.classList.remove("hidden");
        ind2.classList.add("active");
    } else {
        s3.classList.remove("hidden");
        ind3.classList.add("active");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    loadSupportAdvisors();
    restoreSessionIfLogged();

    // Deslizador de Precio Máximo
    const budgetSlider = document.getElementById("budgetSliderCop");
    const budgetDisplay = document.getElementById("budgetLiveDisplay");
    budgetSlider.addEventListener("input", () => {
        budgetDisplay.textContent = formatMoney(budgetSlider.value);
    });
    budgetSlider.addEventListener("change", () => {
        executeDynamicSearch();
    });

    document.getElementById("storeSelect").addEventListener("change", () => {
        executeDynamicSearch();
    });

    document.getElementById("dynamicSearchForm").addEventListener("submit", (e) => {
        e.preventDefault();
        executeDynamicSearch();
    });

    document.getElementById("btnClearSearch").addEventListener("click", () => {
        document.getElementById("searchInput").value = "";
        currentCategory = "todos";
        document.querySelectorAll(".cat-chip").forEach((c) => c.classList.remove("active"));
        document.querySelector('.cat-chip[data-category="todos"]').classList.add("active");
        executeDynamicSearch();
    });

    document.querySelectorAll(".cat-chip").forEach((chip) => {
        chip.addEventListener("click", () => {
            document.querySelectorAll(".cat-chip").forEach((c) => c.classList.remove("active"));
            chip.classList.add("active");
            currentCategory = chip.getAttribute("data-category") || "todos";
            const q = chip.getAttribute("data-query") || "";
            document.getElementById("searchInput").value = q;
            executeDynamicSearch();
        });
    });

    // Botón Cerrar sesión
    document.getElementById("btnLogout").addEventListener("click", () => {
        mostrarVistaBienvenida();
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    // Modales de Inicio de Sesión y Registro
    const authModal = document.getElementById("authModalBackdrop");
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const tabLoginBtn = document.getElementById("tabLoginBtn");
    const tabRegisterBtn = document.getElementById("tabRegisterBtn");

    function openRegisterModal() {
        tabRegisterBtn.classList.add("active");
        tabLoginBtn.classList.remove("active");
        registerForm.classList.remove("hidden");
        loginForm.classList.add("hidden");
        showRegisterWizardStep(1);
        authModal.classList.remove("hidden");
    }

    function openLoginModal() {
        tabLoginBtn.classList.add("active");
        tabRegisterBtn.classList.remove("active");
        loginForm.classList.remove("hidden");
        registerForm.classList.add("hidden");
        authModal.classList.remove("hidden");
    }

    document.getElementById("btnOpenRegister").addEventListener("click", openRegisterModal);
    document.getElementById("btnHeroStartRegister").addEventListener("click", openRegisterModal);
    document.getElementById("btnOpenLogin").addEventListener("click", openLoginModal);
    document.getElementById("btnHeroLogin").addEventListener("click", openLoginModal);
    document.getElementById("btnCloseAuthModal").addEventListener("click", () => {
        authModal.classList.add("hidden");
    });

    tabLoginBtn.addEventListener("click", openLoginModal);
    tabRegisterBtn.addEventListener("click", openRegisterModal);

    // Pasos del Registro
    document.getElementById("btnStep1ToStep2").addEventListener("click", () => {
        showRegisterWizardStep(2);
    });
    document.getElementById("btnBackToStep1").addEventListener("click", () => {
        showRegisterWizardStep(1);
    });
    document.getElementById("btnStep2ToStep3").addEventListener("click", () => {
        const name = document.getElementById("regName").value.trim();
        const email = document.getElementById("regEmail").value.trim();
        const msgBox = document.getElementById("step2ValidationMsg");
        if (!name || !email) {
            msgBox.textContent = "Por favor completa tu nombre y correo.";
            msgBox.classList.remove("hidden");
            return;
        }
        msgBox.classList.add("hidden");
        showRegisterWizardStep(3);
    });
    document.getElementById("btnBackToStep2").addEventListener("click", () => {
        showRegisterWizardStep(2);
    });

    // Enviar Login
    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const errBox = document.getElementById("loginErrorMsg");
        errBox.classList.add("hidden");

        const email = document.getElementById("loginEmail").value.trim();
        const password = document.getElementById("loginPassword").value;

        try {
            const res = await fetch("/api/v1/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });
            const data = await res.json();
            if (data.status !== "OK") {
                errBox.textContent = data.message || "Error al iniciar sesión.";
                errBox.classList.remove("hidden");
                return;
            }
            activarSesionUsuaria(data.user);
            renderCatalogProducts(data.catalog);
            authModal.classList.add("hidden");
            window.scrollTo({ top: 0, behavior: "smooth" });
        } catch (err) {
            errBox.textContent = "Error de conexión.";
            errBox.classList.remove("hidden");
        }
    });

    // Enviar Registro
    registerForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const errBox = document.getElementById("registerErrorMsg");
        errBox.classList.add("hidden");

        const payload = {
            name: document.getElementById("regName").value.trim(),
            city: document.getElementById("regCity").value.trim(),
            email: document.getElementById("regEmail").value.trim(),
            password: document.getElementById("regPassword").value,
            skin_type: document.getElementById("regSkinType").value,
            skin_tone: document.getElementById("regSkinTone").value,
            undertone: document.getElementById("regUndertone").value,
            conditions: getCheckedValues("regConditionsGroup"),
            max_price_cop: Number(document.getElementById("regMaxPrice").value) || 160000
        };

        try {
            const res = await fetch("/api/v1/auth/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (data.status !== "OK") {
                errBox.textContent = data.message || "No se pudo completar el registro.";
                errBox.classList.remove("hidden");
                return;
            }
            activarSesionUsuaria(data.user);
            renderCatalogProducts(data.catalog);
            authModal.classList.add("hidden");
            window.scrollTo({ top: 0, behavior: "smooth" });
        } catch (err) {
            errBox.textContent = "Error al crear la cuenta.";
            errBox.classList.remove("hidden");
        }
    });

    // Modal Editar Piel
    const editSkinModal = document.getElementById("editSkinModalBackdrop");
    document.getElementById("btnEditSkin").addEventListener("click", () => {
        editSkinModal.classList.remove("hidden");
    });
    document.getElementById("btnQuickEditSkin").addEventListener("click", () => {
        editSkinModal.classList.remove("hidden");
    });
    document.getElementById("btnCloseEditSkinModal").addEventListener("click", () => {
        editSkinModal.classList.add("hidden");
    });

    document.getElementById("updateSkinForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        const payload = {
            email: currentUser ? currentUser.email : "valeria@leclat.co",
            skin_type: document.getElementById("editSkinType").value,
            skin_tone: document.getElementById("editSkinTone").value,
            undertone: document.getElementById("editUndertone").value,
            conditions: getCheckedValues("editConditionsGroup"),
            max_price_cop: Number(document.getElementById("budgetSliderCop").value) || 190000,
            query: document.getElementById("searchInput").value.trim(),
            category: currentCategory
        };

        const res = await fetch("/api/v1/profile/update-skin", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.status === "OK") {
            activarSesionUsuaria(data.user);
            renderCatalogProducts(data.catalog);
            editSkinModal.classList.add("hidden");
        }
    });
});
