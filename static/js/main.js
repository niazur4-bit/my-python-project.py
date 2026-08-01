document.addEventListener("DOMContentLoaded", function () {
  // Bootstrap form validation
  const forms = document.querySelectorAll(".needs-validation");
  Array.from(forms).forEach(function (form) {
    form.addEventListener(
      "submit",
      function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add("was-validated");
      },
      false
    );
  });

  // Animate hero stat counters
  const counters = document.querySelectorAll("[data-counter]");
  counters.forEach(function (el) {
    const target = parseInt(el.dataset.counter, 10);
    if (isNaN(target)) return;
    let current = 0;
    const step = Math.max(1, Math.ceil(target / 60));
    const timer = setInterval(function () {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      el.textContent = current.toLocaleString();
    }, 20);
  });

  // Auto-dismiss alerts after 6 seconds
  document.querySelectorAll(".alert-dismissible").forEach(function (alertEl) {
    setTimeout(function () {
      const alert = bootstrap.Alert.getOrCreateInstance(alertEl);
      alert.close();
    }, 6000);
  });

  // Sticky navbar shadow on scroll
  const navbar = document.querySelector(".navbar-firm");
  if (navbar) {
    window.addEventListener("scroll", function () {
      navbar.classList.toggle("shadow-sm", window.scrollY > 8);
    });
  }

  // Dark mode toggle
  const themeToggle = document.getElementById("themeToggle");
  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      const isDark = document.documentElement.getAttribute("data-theme") === "dark";
      if (isDark) {
        document.documentElement.removeAttribute("data-theme");
        localStorage.setItem("theme", "light");
      } else {
        document.documentElement.setAttribute("data-theme", "dark");
        localStorage.setItem("theme", "dark");
      }
    });
  }
});
