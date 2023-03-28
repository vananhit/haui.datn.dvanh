
<template>
  <div class="face-detector-container">
    <!-- partial:index.partial.html -->
    <div class="container">
      <video ref="input_video" class="input_video"></video>
      <div class="canvas-container">
        <canvas
          ref="output_canvas"
          class="output_canvas"
          width="320"
          height="180"
        >
        </canvas>
      </div>
      <div ref="spinner" class="loading">
        <div class="spinner"></div>
        <div class="message">Loading</div>
      </div>
    </div>
    <div ref="control_panel" class="control-panel"></div>
    <!-- partial -->
  </div>
</template>

<script>
import DeviceDetector from "device-detector-js";
import * as controls from "@mediapipe/control_utils";
import * as mpFaceDetection from "@mediapipe/face_detection";
import * as drawingUtils from "@mediapipe/drawing_utils";
import { httpClient } from "@/apis/httpclient";
import { notification } from "ant-design-vue";
import { SmileOutlined } from "@ant-design/icons-vue";
import { h } from "vue";
import {socket} from "@/socket"
export default {
  components: {
    SmileOutlined,
  },
  methods: {
    openNotification() {
      notification.open({
        message: "Notification Title",
        description:
          "This is the content of the notification. This is the content of the notification. This is the content of the notification.",
        icon: h(SmileOutlined, { style: "color: #108ee9" }),
      });
    },
    testSupport(supportedDevices) {
      const deviceDetector = new DeviceDetector();
      const detectedDevice = deviceDetector.parse(navigator.userAgent);
      let isSupported = false;
      for (const device of supportedDevices) {
        if (device.client !== undefined) {
          const re = new RegExp(`^${device.client}$`);
          if (!re.test(detectedDevice.client.name)) {
            continue;
          }
        }
        if (device.os !== undefined) {
          const re = new RegExp(`^${device.os}$`);
          if (!re.test(detectedDevice.os.name)) {
            continue;
          }
        }
        isSupported = true;
        break;
      }
      if (!isSupported) {
        alert(
          `This demo, running on ${detectedDevice.client.name}/${detectedDevice.os.name}, ` +
            `is not well supported at this time, continue at your own risk.`
        );
      }
    },
  },
  data() {
    return {};
  },
  created() {
    this.$socket.connect()
  },
 
  mounted() {
    const me = this;
    // Client and os are regular expressions.
    // See: https://cdn.jsdelivr.net/npm/device-detector-js@2.2.10/README.md for
    // legal values for client and os
    this.testSupport([{ client: "Chrome" }]);
    const videoElement = this.$refs.input_video;
    const canvasElement = this.$refs.output_canvas;
    const controlsElement = this.$refs.control_panel;
    const canvasCtx = canvasElement.getContext("2d");
    const fpsControl = new controls.FPS();
    const spinner = this.$refs.spinner;
    spinner.ontransitionend = () => {
      spinner.style.display = "none";
    };
    function onResults(results) {
      document.body.classList.add("loaded");
      fpsControl.tick();
      canvasCtx.save();
      canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
      canvasCtx.drawImage(
        results.image,
        0,
        0,
        canvasElement.width,
        canvasElement.height
      );
      if (results.detections.length > 0) {
        // canvasElement.toBlob(
        //   async (blob) => {
        //     const formData = new FormData();
        //     formData.append("image", blob, "image.jpg");

           

        //     // await httpClient
        //     //   .post("/faces/upload", formData)
        //     //   .then((response) => {
        //     //     // Handle the server response
        //     //     console.log(response.data);
        //     //   })
        //     //   .catch((error) => {
        //     //     console.error("Error uploading image:", error);
        //     //   });
        //     // const xhr = new XMLHttpRequest();
        //     // xhr.open("POST", "http://127.0.0.1:8000/api/v1/faces/upload");
        //     // // Define a function to handle the response when it's received
        //     // xhr.onload = function () {
        //     //   // Check the status code of the response
        //     //   if (xhr.status === 200) {
        //     //     // Access the response data
        //     //     var responseData = xhr.response;
        //     //     console.log(responseData);
        //     //   } else {
        //     //     console.log(
        //     //       "Request failed.  Returned status of " + xhr.status
        //     //     );
        //     //   }
        //     // };

        //     // xhr.send(formData);
        //   },
        //   "image/jpeg",
        //   0.5
        // ); // Set the JPEG compression level to 50%
        // socket.on("connect", () => {
              // console.log("Connected to server");
              // const FPS = 22;
              // emit an event to the server
              // setInterval(() => {
              //   var type = "image/png";
              //   var data = canvasElement.toDataURL(type);
              //   data = data.replace("data:" + type + ";base64,", ""); //split off junk
              //   // at the beginning
              //   socket.emit("stream", data);
              // }, 10000 / FPS);
            // });
        drawingUtils.drawRectangle(
          canvasCtx,
          results.detections[0].boundingBox,
          {
            color: "blue",
            lineWidth: 4,
            fillColor: "#00000000",
          }
        );
        drawingUtils.drawLandmarks(canvasCtx, results.detections[0].landmarks, {
          color: "red",
          radius: 5,
        });
      }
      canvasCtx.restore();
    }
    const faceDetection = new mpFaceDetection.FaceDetection({
      locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/face_detection@0.4/${file}`;
      },
    });
    faceDetection.onResults(onResults);
    let control = new controls.ControlPanel(controlsElement, {
      selfieMode: true,
      model: "short",
      minDetectionConfidence: 0.5,
    })
      .add([
        new controls.StaticText({ title: "MediaPipe Face Detection" }),
        fpsControl,
        new controls.Toggle({ title: "Selfie Mode", field: "selfieMode" }),
        new controls.SourcePicker({
          onSourceChanged: () => {
            faceDetection.reset();
          },
          onFrame: async (input, size) => {
            const aspect = size.height / size.width;
            let width, height;
            if (window.innerWidth > window.innerHeight) {
              height = window.innerHeight;
              width = height / aspect;
            } else {
              width = window.innerWidth;
              height = width * aspect;
            }
            canvasElement.width = width;
            canvasElement.height = height;
            await faceDetection.send({ image: input });
          },
          examples: {
            images: [],
            videos: [],
          },
        }),
        new controls.Slider({
          title: "Model Selection",
          field: "model",
          discrete: { short: "Short-Range", full: "Full-Range" },
        }),
        new controls.Slider({
          title: "Min Detection Confidence",
          field: "minDetectionConfidence",
          range: [0, 1],
          step: 0.01,
        }),
      ])
      .on((x) => {
        const options = x;
        videoElement.classList.toggle("selfie", options.selfieMode);
        faceDetection.setOptions(options);
      });
  },
  beforeUnmount() {
    // this.$socket.disconnect()
  },
};
</script>



<style lang="scss">
@import "./control_utils.css";

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

.abs {
  position: absolute;
}

.face-detector-container {
  position: relative;
}

.container {
  position: absolute;
  background-color: #596e73;
  width: 100%;
  max-height: 100%;
}

.input_video {
  display: none;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;

  &.selfie {
    transform: scale(-1, 1);
  }
}

.input_image {
  position: absolute;
}

.canvas-container {
  display: flex;
  height: 100%;
  width: 100%;
  justify-content: center;
  align-items: center;
}

.output_canvas {
  max-width: 100%;
  display: block;
  position: relative;
  left: 0;
  top: 0;
}

.control-panel {
  position: absolute;
  left: 10px;
  top: 10px;
}

.loading {
  display: flex;
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  align-items: center;
  backface-visibility: hidden;
  justify-content: center;
  opacity: 1;
  transition: opacity 1s;

  .message {
    font-size: x-large;
  }

  .spinner {
    position: absolute;
    width: 120px;
    height: 120px;
    animation: spin 1s linear infinite;
    border: 32px solid #bebebe;
    border-top: 32px solid #3498db;
    border-radius: 50%;
  }
}

.loaded .loading {
  opacity: 0;
}
</style>