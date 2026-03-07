//Navbar toggle icon
function navbar_toggler() {
  $(".navbar-toggler[data-toggle=collapse]").click(function () {
    if ($(".navbar-toggler[data-bs-toggle=collapse] i").hasClass("fa-bars")) {
    } else {
      $(".navbar-toggler[data-bs-toggle=collapse] i").removeClass("fa-times");
    }
  });
}
navbar_toggler();

// Navbar clone in mobile device
function navClone() {
  $(".js-clone-nav").each(function () {
    var $this = $(this);
    $this
      .clone()
      .attr("class", "navbar-nav ml-auto")
      .appendTo(".d2c_mobile_view_body");
  });

  $(".d2c_mobile_view .nav-link").click(function () {
    $(".nav-link").removeClass("active");
    $(".d2c_mobile_view").removeClass("show");
    $(this).toggleClass("active");
  });
}

navClone();

$(".d2c_certificate_slider").slick({
  dots: false,
  arrows: false,
  infinite: true,
  autoplay: true,
  speed: 1200,
  slidesToShow: 3,
  slidesToScroll: 1,
  responsive: [
    {
      breakpoint: 1400,
      settings: {
        slidesToShow: 2,
      },
    },
    {
      breakpoint: 1200,
      settings: {
        slidesToShow: 2,
      },
    },
    {
      breakpoint: 992,
      settings: {
        slidesToShow: 1,
      },
    },
    {
      breakpoint: 480,
      settings: {
        slidesToShow: 1,
      },
    },
  ],
});

// Form Validation Js
(function () {
  "use strict";

  var forms = document.querySelectorAll(".needs-validation");

  Array.prototype.slice.call(forms).forEach(function (form) {
    form.addEventListener(
      "submit",
      function (event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }

        form.classList.add("was-validated");
      },
      false,
    );
  });
})();

// WOW JS
new WOW().init();

// Preloader JS
window.addEventListener("load", function () {
  var preloader = document.querySelector(".preloader");
  preloader.classList.add("hide");
});

// ScrollBtn JS
window.onscroll = function () {
  scrollFunction();
};

function scrollFunction() {
  var scrollBtn = document.getElementById("scrollBtn");
  if (
    document.body.scrollTop > 100 ||
    document.documentElement.scrollTop > 100
  ) {
    scrollBtn.classList.add("show");
  } else {
    scrollBtn.classList.remove("show");
  }
}

// Counter
$(document).ready(function () {
  var counters = $(".count");
  var countersQuantity = counters.length;
  var counter = [];

  for (i = 0; i < countersQuantity; i++) {
    counter[i] = parseInt(counters[i].innerHTML);
  }

  var count = function (start, value, id) {
    var localStart = start;
    setInterval(function () {
      if (localStart < value) {
        localStart++;
        counters[id].innerHTML = localStart;
      }
    }, 40);
  };

  for (j = 0; j < countersQuantity; j++) {
    count(0, counter[j], j);
  }
});

(function () {
  let sectionElement = document.querySelector("main section");

  function resize() {
    sectionElement.style.height = window.innerHeight + "px";
  }

  document.addEventListener("DOMContentLoaded", resize);
  window.addEventListener("resize", resize);
}).call(this);

(function () {
  let headerElement = document.querySelector("header");
  window.addEventListener("scroll", () => {
    if (window.scrollY > 250) headerElement.classList.add("d3c_navbar");
    else if (window.screenY < 250) headerElement.classList.remove("d3c_navbar");
  });
}).call(this);

(function () {
  function typewriter(
    element,
    deleting_speed = 50,
    writing_speed = 100,
    delay = 1000,
  ) {
    element.style.display = "block";
    element.style.minHeight = element.offsetHeight + "px";

    const words = [element.textContent];
    let i = 0;
    let j = 0;
    let currentWord = "";
    let isDeleting = false;

    function type() {
      currentWord = words[i];

      if (isDeleting) {
        element.textContent = currentWord.substring(0, j--);
      } else {
        element.textContent = currentWord.substring(0, j++);
      }

      if (!isDeleting && j === currentWord.length) {
        setTimeout(() => (isDeleting = true), delay);
      }

      if (isDeleting && j === 0) {
        isDeleting = false;
        i = (i + 1) % words.length;
      }

      setTimeout(
        type,
        !isDeleting && j - 1 === currentWord.length
          ? delay
          : isDeleting
            ? deleting_speed
            : writing_speed,
      );
    }

    type();
  }

  document.querySelectorAll("#typewriter").forEach((element) => {
    deleting_speed = element.dataset.deletingSpeed;
    writing_speed = element.dataset.writingSpeed;
    delay = element.dataset.delay;
    typewriter(element, deleting_speed, writing_speed, delay);
  });
}).call(this);
