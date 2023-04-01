
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

export default {
  components: {
    SmileOutlined,
  },
  methods: {
    
    /***
     * lấy ảnh từ đối tượng canvas đưa nó vào trong 1 from data trả về một promise
     */
    getImageFromCanvans(mycanvas, quality = 0.5) {
      return new Promise(function (resolve, reject) {
        mycanvas.toBlob(
          (blob) => {
            try {
              let formData = new FormData();
              formData.append("image", blob, "image.jpg");
              resolve(formData);
            } catch (e) {
              reject(e);
            }
          },
          "image/jpeg",
          quality
        );
      });
    },

    /***
     * Gửi image lên server
     */
    async sendImageToService(canvasElement, quality = 0.5) {
      try {
       
        //Lấy ảnh từ đối tương canvasElement
        let formData = await this.getImageFromCanvans(canvasElement, quality);
        //Upload ảnh lên server
        let ans = await httpClient.post("/faces/upload", formData);
        let data = ans.data
        if(data.face_score>=0.5){
          this.openNotification(data.face_code)
        }
      } catch (e) {
        console.error("Error uploading image:", e);
      }
    },
    /***
     * Mở hộp thoại thông báo
     */
    openNotification(title) {
      notification.open({
        message:title,
        description:
          "This is the content of the notification. This is the content of the notification. This is the content of the notification.",
        icon: h(SmileOutlined, { style: "color: #108ee9" }),
      });
    },

    /***
     * Kiểm tra trình duyệt có hỗ trợ camera hay không
     */
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
    return {
      start:null,
      //Sau bao nhiêu s có khuôn mặt thì gửi lên service
      refreshRate:2000
    };
  },
  created() {},

  mounted() {
    this.testSupport([{ client: "Chrome" }]);
    const videoElement = this.$refs.input_video;
    const canvasElement = this.$refs.output_canvas;
    const controlsElement = this.$refs.control_panel;
    const canvasCtx = canvasElement.getContext("2d");
    const fpsControl = new controls.FPS();
    const spinner = this.$refs.spinner;
    // const sendImage = this.debounce(this.sendImageToService, 500);
    const me= this;
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
      /**
       * Nếu có khuôn mặt trong frame
       */

      if (results.detections.length > 0) {
        //Gửi ảnh lên serve cách 500ms
        // sendImage(canvasElement, 1.0);

        if(!me.start){
          me.start = new Date().getTime();
        }

        let diff = new Date().getTime() - me.start||0;
        if(diff>=me.refreshRate){
          me.sendImageToService(canvasElement,1);
          me.start = null
        }

        //visualize lên màn hình - vẽ bouding box
        drawingUtils.drawRectangle(
          canvasCtx,
          results.detections[0].boundingBox,
          {
            color: "blue",
            lineWidth: 4,
            fillColor: "#00000000",
          }
        );

        //vẽ toạ độ các điểm mắt mũi , tai
        drawingUtils.drawLandmarks(canvasCtx, results.detections[0].landmarks, {
          color: "red",
          radius: 5,
        });
      }else{
        me.start = null;
      }

      canvasCtx.restore();
    }
    const faceDetection = new mpFaceDetection.FaceDetection({
      locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/face_detection@0.4/${file}`;
      },
    });
    faceDetection.onResults(onResults);
    new controls.ControlPanel(controlsElement, {
      selfieMode: true,
      model: "short",
      minDetectionConfidence: 1,
    })
      .add([
        new controls.StaticText({ title: "Bảng điều khiển" }),
        fpsControl,
        new controls.Toggle({ title: "Gương", field: "selfieMode" }),
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
          title: "Ngưỡng chính xác",
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
  beforeUnmount() {},
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