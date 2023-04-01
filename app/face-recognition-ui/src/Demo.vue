<template>
    <div>
      <video ref="video" width="400" height="300"></video>
      <canvas ref="canvas" width="400" height="300"></canvas>
    </div>
  </template>
  
  <script>
  import * as faceapi from "face-api.js";
  import axios from "axios";
  
  export default {
    data() {
      return {
        stream: null,
        faceDetectionIntervalId: null,
      };
    },
    async mounted() {
      await faceapi.loadSsdMobilenetv1Model("/");
      await faceapi.loadFaceLandmarkModel("/");
      await faceapi.loadFaceRecognitionModel("/");
      await faceapi.loadFaceExpressionModel("/");
  
      this.startCamera();
      this.startFaceDetection();
    },
    methods: {
      async startCamera() {
        try {
          this.stream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false,
          });
          this.$refs.video.srcObject = this.stream;
          this.$refs.video.play();
        } catch (error) {
          console.error(error);
        }
      },
      async startFaceDetection() {
        const canvas = this.$refs.canvas;
        const video = this.$refs.video;
        const displaySize = { width: video.width, height: video.height };
        faceapi.matchDimensions(canvas, displaySize);
  
        this.faceDetectionIntervalId = setInterval(async () => {
          const detections = await faceapi
            .detectAllFaces(video)
            .withFaceLandmarks()
            .withFaceExpressions();
  
          if (detections.length > 0) {
            const context = canvas.getContext("2d");
            context.clearRect(0, 0, canvas.width, canvas.height);
            const resizedDetections = faceapi.resizeResults(
              detections,
              displaySize
            );
            faceapi.draw.drawDetections(canvas, resizedDetections);
            faceapi.draw.drawFaceLandmarks(canvas, resizedDetections);
            faceapi.draw.drawFaceExpressions(canvas, resizedDetections);
  
            const imgData = canvas.toDataURL("image/jpeg", 0.8).split(",")[1];
            this.uploadPhoto(imgData);
          }
        }, 500);
      },
      uploadPhoto(imgData) {
        const formData = new FormData();
        formData.append("photo", imgData);
        axios.post("/api/upload", formData).then((response) => {
          console.log(response.data);
        });
      },
    },
    beforeUnmount() {
      clearInterval(this.faceDetectionIntervalId);
  
      if (this.stream) {
        this.stream.getTracks().forEach((track) => track.stop());
      }
    },
  };
  </script>