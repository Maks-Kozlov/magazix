/* Project specific Javascript goes here. */

document.addEventListener("ajax:before", (event) => {
  // Глобальная логика перед AJAX запросом (например, лоадер)
  console.log("AJAX request starting...", event.detail.url);
});

document.addEventListener("ajax:error", (event) => {
  // Глобальная обработка ошибок AJAX
  console.error("AJAX request failed:", event.detail.error);
  // Здесь можно добавить уведомление пользователю через Alpine Message Middleware
});
