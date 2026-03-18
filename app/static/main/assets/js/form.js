async function submitForm(form) {
  const formData = new FormData(form);

  let eventInitDict = { bubbles: true };

  try {
    const response = await fetch(form.action, {
      method: form.method,
      body: formData,
    });

    const data = await response.json();

    eventInitDict.detail = data;

    form.querySelectorAll(".errors").forEach((el) => el.remove());

    form
      .querySelectorAll(".is-invalid")
      .forEach((el) => el.classList.remove("is-invalid"));

    if (data.errors) {
      console.log(data.errors);
    } else {
      Swal.fire({
        title: data.title,
        text: data.message,
        icon: data.category,
      }).then(() => {
        if (data?.redirect) window.location.replace(data.redirect);
      });
    }
  } catch (err) {
    console.log(err);
  }

  form.dispatchEvent(new CustomEvent("afterSubmit", eventInitDict));
}

(function () {
  document.addEventListener("submit", (event) => {
    event.preventDefault();

    switch (event.target.tagName) {
      case "FORM":
        submitForm(event.target);

        break;
    }
  });
}).call(this);
