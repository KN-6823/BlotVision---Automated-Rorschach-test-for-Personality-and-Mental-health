// document.addEventListener('DOMContentLoaded', function () {
//   const image = document.getElementById('rotate-image');
//   let rotationAngle = 0;
//   let images = [];
//   let currentIndex = 0;

//   // Fetch images from the server when the page loads
//   async function fetchImages() {
//       try {
//           const response = await fetch('/get-images');
//           images = await response.json(); // Store images in the array
//           if (images.length > 0) {
//               image.src = images[0].url; // Set the first image source
//           }
//       } catch (error) {
//           console.error("Failed to fetch images:", error);
//       }
//   }

//   // Rotate image left
//   document.getElementById('rotate-left').addEventListener('click', function () {
//       rotationAngle -= 90;
//       image.style.transform = `rotate(${rotationAngle}deg)`; // Rotate image
//   });

//   // Rotate image right
//   document.getElementById('rotate-right').addEventListener('click', function () {
//       rotationAngle += 90;
//       image.style.transform = `rotate(${rotationAngle}deg)`; // Rotate image
//   });

//   // Next image button click handler
//   document.getElementById('next-button').addEventListener('click', function () {
//       if (images.length > 0) {
//           currentIndex = (currentIndex + 1) % images.length; // Cycle through images
//           image.src = images[currentIndex].url; // Update image source
//       }
//   });

//   fetchImages(); // Fetch images on page load
// });


