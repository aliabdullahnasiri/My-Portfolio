async function submitForm(form) {
  const formData = new FormData(form);

  let eventInitDict = { bubbles: true };

  try {
    const response = await fetch(form.action, {
      method: form.method,
      body: formData,
    });

    const data = await response.json();

    Swal.fire({
      title: data.title,
      text: data.message,
      icon: data.category,
    }).then(() => {
      if (data?.redirect) {
        window.location.replace(data.redirect);
      }
    });
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
