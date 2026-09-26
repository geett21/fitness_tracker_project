(function () {
  "use strict";

  var permissionButton = document.getElementById("enable-water-notifications");
  var permissionMessage = document.getElementById("water-notification-permission");
  var reminderToggle = document.getElementById("id_enabled");
  var storageKey = "fittrack-water-reminder-last-shown";
  var pollTimer = null;

  function askForPermission() {
    if (!("Notification" in window)) {
      if (permissionMessage) permissionMessage.textContent = "This browser does not support notifications.";
      return;
    }
    Notification.requestPermission().then(function (permission) {
      if (permissionMessage) {
        permissionMessage.textContent = permission === "granted"
          ? "Browser notifications are enabled. Save your settings with reminders turned on."
          : "Notifications are blocked. Allow them in your browser site settings to receive reminders.";
      }
      if (permission === "granted") checkWaterReminder();
    });
  }

  if (permissionButton) {
    permissionButton.addEventListener("click", askForPermission);
  }

  if (reminderToggle) {
    reminderToggle.addEventListener("change", function () {
      if (reminderToggle.checked) askForPermission();
    });
  }

  if (permissionMessage && "Notification" in window && Notification.permission === "granted") {
    permissionMessage.textContent = "Browser notifications are allowed on this device.";
  }

  if (!("Notification" in window)) {
    if (permissionMessage) permissionMessage.textContent = "This browser does not support notifications.";
    return;
  }
  if (Notification.permission !== "granted") {
    if (permissionMessage && Notification.permission === "denied") {
      permissionMessage.textContent = "Notifications are blocked. Allow them in your browser site settings to receive reminders.";
    }
    return;
  }

  function localDate() {
    var now = new Date();
    return now.getFullYear() + "-" + String(now.getMonth() + 1).padStart(2, "0") + "-" + String(now.getDate()).padStart(2, "0");
  }

  function timeInMinutes(value) {
    var parts = value.split(":");
    return Number(parts[0]) * 60 + Number(parts[1]);
  }

  function checkWaterReminder() {
    fetch("/water/reminder/status/?date=" + encodeURIComponent(localDate()), {
      credentials: "same-origin",
      headers: { "Accept": "application/json" }
    })
      .then(function (response) {
        if (!response.ok) throw new Error("Reminder status unavailable");
        return response.json();
      })
      .then(function (data) {
        if (!data.enabled) {
          if (pollTimer !== null) {
            window.clearInterval(pollTimer);
            pollTimer = null;
          }
          return;
        }
        if (pollTimer === null) pollTimer = window.setInterval(checkWaterReminder, 60000);

        var now = new Date();
        var minuteOfDay = now.getHours() * 60 + now.getMinutes();
        if (minuteOfDay < timeInMinutes(data.start_time) || minuteOfDay >= timeInMinutes(data.end_time)) return;

        var timestamp = now.getTime();
        var lastShown = Number(localStorage.getItem(storageKey) || 0);
        if (!lastShown) {
          localStorage.setItem(storageKey, String(timestamp));
          return;
        }
        if (timestamp - lastShown < data.interval_minutes * 60 * 1000) return;

        localStorage.setItem(storageKey, String(timestamp));
        if (data.remaining <= 0) return;

        var friendlyMessages = [
          "Hey! It's time to drink some water 💙",
          "Stay hydrated and take a refreshing water break 😊",
          "A little sip can help you stay on track 💧"
        ];
        var messageIndex = Number(localStorage.getItem("fittrack-water-message-index") || 0);
        var body = friendlyMessages[messageIndex % friendlyMessages.length] + " You have " + data.remaining.toFixed(2) + " L left to reach your goal.";
        localStorage.setItem("fittrack-water-message-index", String(messageIndex + 1));
        new Notification("💧 Water Break!", {
          body: body,
          tag: "fittrack-water-goal-reminder",
          renotify: false
        });
      })
      .catch(function () {
        // A temporary network issue should not interrupt the current page.
      });
  }

  checkWaterReminder();
  window.addEventListener("focus", checkWaterReminder);
})();
