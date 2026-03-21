(function () {
  const listEl = document.getElementById("notif-list");
  const url = listEl.dataset.fetchNotifications; // data-fetch-notifications

  async function loadNotifications() {
    const res = await fetch(url);
    if (!res.ok) return console.error("Failed to fetch notifications");

    const notifications = await res.json();

    listEl.innerHTML = "";

    if (!notifications.length) {
      listEl.innerHTML = `<li class="text-center text-muted small">No notifications</li>`;
      return;
    }

    notifications.forEach((n) => {
      addNotification(n);
    });
  }

  function addNotification(n) {
    console.log(n);
    const item = `
            <li class="mb-2" data-role="notification">
                <a class="dropdown-item border-radius-md" href="#">
                    <div class="d-flex py-1">
                        <div class="d-flex flex-column justify-content-center">
                            <h6 class="text-sm font-weight-normal mb-1">
                                ${n.message}
                            </h6>
                            <p class="text-xs text-secondary mb-0">
                                <i class="fa fa-clock me-1"></i>
                                ${n.natural_created_at}
                            </p>
                        </div>
                    </div>
                </a>
            </li>
        `;
    listEl.innerHTML += item;
  }

  // Load on page ready
  document.addEventListener("DOMContentLoaded", () => {
    loadNotifications();

    const socket = io();

    socket.on("new_notification", (data) => {
      showDesktopNotification("New Notification", {
        body: data?.message,
        tag: "message-notif",
      });
      addNotification(data);
    });
  });

  // Check if browser supports Notifications
  if ("Notification" in window) {
    if (Notification.permission === "default") {
      Notification.requestPermission().then((permission) => {
        console.log("Notification permission:", permission);
      });
    }
  } else {
    console.log("This browser does not support desktop notifications");
  }

  function showDesktopNotification(title, options = {}) {
    if (Notification.permission === "granted") {
      const notification = new Notification(title, options);

      notification.onclick = () => {
        window.focus();
        notification.close();
      };
    }
  }
}).call(this);
