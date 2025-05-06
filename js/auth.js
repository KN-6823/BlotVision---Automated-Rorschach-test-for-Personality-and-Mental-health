document.addEventListener("DOMContentLoaded", () => {
  // Function to toggle button visibility based on authentication status
  const updateButtonVisibility = (isLoggedIn, userName) => {
      const signupButton = document.getElementById("signup-button");
      const loginButton = document.getElementById("login-button");
      const logoutButton = document.getElementById("logout-button");
      const usernameDisplay = document.getElementById("username-display");

      if (isLoggedIn) {
          signupButton.style.display = "none";
          loginButton.style.display = "none";
          logoutButton.style.display = "block";
          usernameDisplay.innerText = `Welcome! ${userName}`; // Show username or greeting
          usernameDisplay.style.display = "block";
      } else {
          signupButton.style.display = "block";
          loginButton.style.display = "block";
          logoutButton.style.display = "none";
          usernameDisplay.style.display = "none"; // Hide username or greeting
      }
  };

  // Check if user is logged in (fetch session data from the server)
  const isLoggedIn = !!document.getElementById("username-display").innerText; // Check if username display is filled

  // Call updateButtonVisibility with user name if logged in
  const userName = isLoggedIn ? document.getElementById("username-display").innerText.replace("Welcome! ", "") : null;
  updateButtonVisibility(isLoggedIn, userName);

  // Handle signup form submission
  const signupForm = document.getElementById("signup-form");
  if (signupForm) {
      signupForm.addEventListener("submit", async (e) => {
          e.preventDefault(); // Prevent the default form submission

          const formData = new FormData(signupForm);
          const data = Object.fromEntries(formData.entries());

          try {
              // Show spinner before sending the request
              const spinner = document.getElementById("spinner");
              spinner.style.display = "flex";

              const response = await fetch("/signup", {
                  method: "POST",
                  headers: {
                      "Content-Type": "application/json",
                  },
                  body: JSON.stringify(data),
              });

              // Hide spinner after request completes
              spinner.style.display = "none";

              if (response.redirected) {
                  window.location.href = response.url; // Redirect to home if signup is successful
                  updateButtonVisibility(true, data.name); // User is now logged in
              } else {
                  const message = await response.text();
                  alert(message); // Show any error message
              }
          } catch (error) {
              console.error("Error:", error);
              alert("An error occurred during signup. Please try again.");
              document.getElementById("spinner").style.display = "none"; // Ensure spinner is hidden
          }
      });
  }

  // Handle login form submission
  const loginForm = document.getElementById("login-form");
  if (loginForm) {
      loginForm.addEventListener("submit", async (e) => {
          e.preventDefault(); // Prevent the default form submission

          const formData = new FormData(loginForm);
          const data = Object.fromEntries(formData.entries());

          try {
              // Show spinner before sending the request
              const spinner = document.getElementById("spinner");
              spinner.style.display = "flex";

              const response = await fetch("/login", {
                  method: "POST",
                  headers: {
                      "Content-Type": "application/json",
                  },
                  body: JSON.stringify(data),
              });

              // Hide spinner after request completes
              spinner.style.display = "none";

              if (response.redirected) {
                  window.location.href = response.url; // Redirect to home if login is successful
                  updateButtonVisibility(true, data.email); // Update button visibility and show email as username
              } else {
                  const message = await response.text();
                  alert(message); // Show any error message
              }
          } catch (error) {
              console.error("Error:", error);
              alert("An error occurred during login. Please try again.");
              document.getElementById("spinner").style.display = "none"; // Ensure spinner is hidden
          }
      });
  }

  // Handle logout button click
  const logoutButton = document.getElementById("logout-button");
  if (logoutButton) {
      logoutButton.addEventListener("click", async () => {
          try {
              // Send a request to logout
              const response = await fetch("/logout", {
                  method: "GET",
              });

              if (response.ok) {
                  window.location.href = "/"; // Redirect to home after logout
                  updateButtonVisibility(false); // User is now logged out
              } else {
                  alert("An error occurred during logout. Please try again.");
              }
          } catch (error) {
              console.error("Error:", error);
              alert("An error occurred during logout. Please try again.");
          }
      });
  }
});
