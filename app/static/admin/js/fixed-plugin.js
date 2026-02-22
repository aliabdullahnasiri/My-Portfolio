document.addEventListener("DOMContentLoaded", () => {
  const aside = document.querySelector("aside");
  const fixedPlugin = document.querySelector(".fixed-plugin");

  if (!fixedPlugin || !aside) return;

  const badgeColors = fixedPlugin.querySelector(".badge-colors");
  const sideNavType = fixedPlugin.querySelector(".sidenav-type");
  const darkVersionToggle = fixedPlugin.querySelector("#dark-version");

  const storedColor = localStorage.getItem("side-bar-color") || "dark";
  const storedType = localStorage.getItem("side-nav-type");
  const storedDarkMode = localStorage.getItem("dark-version") === "true";

  // ========================
  // Highlight Active Sidebar Link
  // ========================
  aside.querySelectorAll("a").forEach((link) => {
    const url = new URL(link.href);
    link.classList.toggle("active", url.pathname === location.pathname);
    link.classList.toggle("text-dark", url.pathname !== location.pathname);
  });

  // ========================
  // Apply Stored Sidebar Color
  // ========================
  if (badgeColors) {
    const colorSpan = badgeColors.querySelector(
      `span[data-color="${storedColor}"]`,
    );
    if (colorSpan && typeof sidebarColor === "function") {
      sidebarColor(colorSpan);
    }

    badgeColors.addEventListener("click", (e) => {
      const span = e.target.closest("span[data-color]");
      if (!span) return;

      localStorage.setItem("side-bar-color", span.dataset.color);
      if (typeof sidebarColor === "function") {
        sidebarColor(span);
      }
    });
  }

  // ========================
  // Apply Stored Sidebar Type
  // ========================
  if (sideNavType && storedType) {
    const typeButton = sideNavType.querySelector(
      `button[data-class="${storedType}"]`,
    );

    if (typeButton && typeof sidebarType === "function") {
      sidebarType(typeButton);
    }

    sideNavType.addEventListener("click", (e) => {
      const button = e.target.closest("button[data-class]");
      if (!button) return;

      localStorage.setItem("side-nav-type", button.dataset.class);
      if (typeof sidebarType === "function") {
        sidebarType(button);
      }
    });
  }

  // ========================
  // Dark Mode
  // ========================
  if (darkVersionToggle) {
    darkVersionToggle.checked = storedDarkMode;

    if (storedDarkMode && typeof darkMode === "function") {
      darkMode(darkVersionToggle);
    }

    darkVersionToggle.addEventListener("change", (e) => {
      localStorage.setItem("dark-version", e.target.checked);

      if (typeof darkMode === "function") {
        darkMode(e.target);
      }
    });
  }
});
