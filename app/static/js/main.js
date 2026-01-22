/* 
Student ID: 24071105
Student Name: Riya Adhikari
*/

// Main JavaScript for World Hotels

document.addEventListener("DOMContentLoaded", function () {
  console.log("World Hotels JS Loaded");

  // Auto-dismiss alerts after 5 seconds
  const alerts = document.querySelectorAll(".alert-dismissible");
  alerts.forEach((alert) => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });

  // Client-side Date Validation for Search Form
  const searchForm = document.querySelector('form[action*="search"]');
  if (searchForm) {
    const checkInInput = searchForm.querySelector('input[name="check_in"]');
    const checkOutInput = searchForm.querySelector('input[name="check_out"]');

    if (checkInInput && checkOutInput) {
      // Set min check-in date to today
      const today = new Date().toISOString().split("T")[0];
      checkInInput.setAttribute("min", today);

      checkInInput.addEventListener("change", function () {
        // When check-in changes, update check-out min to check-in + 1 day
        checkOutInput.setAttribute("min", this.value);
        if (checkOutInput.value && checkOutInput.value <= this.value) {
          checkOutInput.value = ""; // clear invalid date
        }
      });
    }
  }
});
