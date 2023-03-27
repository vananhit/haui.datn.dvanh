
<template>
  <div>
    <div v-if="isLoadingModel">Loading model...</div>
    <video ref="video" autoplay @loadedmetadata="onVideoLoaded"></video>
    <canvas ref="canvas"></canvas>
    <button @click="sendImage">Send image</button>
  </div>
</template>

<script>
import * as mp from "@mediapipe/pose"; //import MediaPipe
//import * as cv from "opencv.js"; //import OpenCV
import * as tf from "@tensorflow/tfjs"; //import TensorFlow
//import * as tfjsWasm from "@tensorflow/tfjs-backend-wasm"; //import TensorFlow WASM backend

export default {
  name: "FaceDetection",
  data() {
    return {
      video: null,
      canvas: null,
      ctx: null,
      model: null,
      currentDetection: null,
      isLoadingModel: true,
    };
  },
  methods: {
    async sendImage() {
      const dataUrl = this.canvas.toDataURL(); // lấy dữ liệu của canvas dưới dạng base64
      try {
        const response = await fetch("/server-endpoint", {
          method: "POST",
          body: JSON.stringify({ dataUrl }),
          headers: {
            "Content-Type": "application/json",
          },
        });
        const result = await response.json();
        console.log(result);
      } catch (error) {
        console.error(error);
      }
    },
    async loadModel() {
      
      this.model = await mp.Pose();
      console.log(mp)
      await this.model.load();
      this.isLoadingModel = false;
    },
    onVideoLoaded() {
      this.canvas.width = this.video.videoWidth;
      this.canvas.height = this.video.videoHeight;
      this.ctx.fillStyle = "#32EEDB";
      this.ctx.strokeStyle = "#32EEDB";
      this.ctx.lineWidth = 2;
      this.detectFace();
    },
    async detectFace() {
      requestAnimationFrame(() => {
        this.detectFace();
      });
      this.ctx.drawImage(
        this.video,
        0,
        0,
        this.canvas.width,
        this.canvas.height
      );
      const imgData = this.ctx.getImageData(
        0,
        0,
        this.canvas.width,
        this.canvas.height
      );
      const tensor = tf.browser.fromPixels(imgData).toFloat();
      const pose = await this.model.estimateSinglePose(tensor, {
        flipHorizontal: false,
      });
      this.currentDetection = pose;
      this.drawDetection();
    },
    drawDetection() {
      if (this.currentDetection) {
        const keypoints = this.currentDetection.keypoints;
        for (let i = 0; i < keypoints.length; i++) {
          const keypoint = keypoints[i];
          this.ctx.beginPath();
          this.ctx.arc(
            keypoint.position.x,
            keypoint.position.y,
            5,
            0,
            2 * Math.PI
          );
          this.ctx.fill();
          this.ctx.stroke();
        }
      }
    },
  },
  mounted() {
    this.video = this.$refs.video;
    this.canvas = this.$refs.canvas;
    this.ctx = this.canvas.getContext("2d");
    this.loadModel();
  },
};
</script>

<style>
canvas {
  display: none;
}
video {
  width: 100%;
  height: auto;
  max-width: 640px;
  margin-bottom: 1rem;
}
</style>
