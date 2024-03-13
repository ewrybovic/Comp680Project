const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const context = canvas.getContext("2d");
const captureButton = document.getElementById("capture");
const retakeButton = document.getElementById("retake");
const startButton = document.getElementById("start");
const pauseButton = document.getElementById("pause");
const analyzeButton = document.getElementById("analyze");

let stream = null;

function manageStream(isStarting) {
  if (isStarting) {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then(function (mediaStream) {
        stream = mediaStream;
        video.srcObject = stream;
        video.play();
        video.style.display = "block";
        canvas.style.display = "none";
        captureButton.style.display = "inline-block";
        retakeButton.style.display = "none";
        startButton.style.display = "none";
        pauseButton.style.display = "inline-block";
        analyzeButton.style.display = "none";
      })
      .catch(function (err) {
        console.log("An error occurred: " + err);
      });
  } else {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
    }
    video.style.display = "none";
    captureButton.style.display = "none";
    startButton.style.display = "inline-block";
    pauseButton.style.display = "none";
    retakeButton.style.display = "none"; // Ensure retake button is also managed correctly
    analyzeButton.style.display = "none";
  }
}

// Capture the photo and show it
captureButton.addEventListener("click", function () {
  context.drawImage(video, 0, 0, 640, 480);
  video.style.display = "none";
  canvas.style.display = "block";
  captureButton.style.display = "none";
  retakeButton.style.display = "inline-block";
  startButton.style.display = "none";
  pauseButton.style.display = "none";
  analyzeButton.style.display = "inline-block";
});

// Start the video stream
startButton.addEventListener("click", function () {
  manageStream(true);
});

// Pause the video stream
pauseButton.addEventListener("click", function () {
  manageStream(false);
});

// Retake the photo, showing video stream again
retakeButton.addEventListener("click", function () {
  manageStream(true);
});

// Initialize the page
window.onload = function () {
  startButton.style.display = "inline-block";
  captureButton.style.display = "none";
  retakeButton.style.display = "none";
  pauseButton.style.display = "none";
};

// Handle Analyze Label button click
document.getElementById("analyze").addEventListener("click", function () {
  canvas.toBlob(function (blob) {
    const formData = new FormData();
    formData.append("image", blob, "capture.jpg");
    fetch("/analyze-image/", {
      // Adjust the URL as needed
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.ok) return response.json();
        throw new Error("Network response was not ok.");
      })
      .then((data) => {
        window.location.href = data.redirectURL; // Redirect the user
      })
      .catch((error) => console.error("Error:", error));
  }, "image/jpeg");
});
