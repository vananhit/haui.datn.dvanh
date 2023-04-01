<template>
  <div class="my-image-conatiner">
    <img v-if="!src" :src="placeholder" @click="openCamera" />
    <div class="preview" v-else>
      <img class="btn-del"  @click="deleteFaceEmbedding" :src="require('@/assets/button-close.svg')" />
      <a-image :width="129.38" :height="139" :src="src" />
    </div>
    <div v-if="isCameraOpen" class="camera-conatiner">
      <div class="camera-zone">
        <div class="cancel" @click="cancel">Huỷ</div>
        <div>
          <video class="output-camera" ref="video" autoplay></video>
          <canvas ref="canvas" style="display: none"></canvas>
        </div>
        <img
          class="take-photo"
          src="@/assets/take-photo.svg"
          @click="takephoto"
        />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    src: {
      type: String,
      default: null,
    },
    placeholder: {
      type: String,
      default: require("@/assets/front_1.svg"),
    },
  },
  data() {
    return {
      isCameraOpen: false,
      capturedImage: null,
      stream: null,
    };
  },
  methods: {
    /**
     * Xoá dữ liệu nhận dạng
     */
    deleteFaceEmbedding(){
        this.$emit('delete')
    },
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
    cancel() {
      this.isCameraOpen = false;
      this.closeCamera();
    },
    openCamera() {
      this.isCameraOpen = true;
      window.navigator.mediaDevices
        .getUserMedia({ video: { facingMode: "user" } })
        .then((stream) => {
          const video = this.$refs.video;
          video.srcObject = stream;
          video.play();
          this.stream = stream;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    closeCamera() {
      if (this.stream) {
        this.stream.getTracks().forEach((track) => {
          track.stop();
        });
      }
    },
    async takephoto() {
      const video = this.$refs.video;
      const canvas = this.$refs.canvas;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas
        .getContext("2d")
        .drawImage(video, 0, 0, canvas.width, canvas.height);

      let image = await this.getImageFromCanvans(canvas, 1);
      this.$emit("takePhoto", image);
      this.isCameraOpen = false;
      this.closeCamera();
    },
  },
  mounted() {},
  beforeMount() {
    this.closeCamera();
  },
};
</script>

<style scoped lang="scss">
.my-image-conatiner {
  cursor: pointer;
  .preview {
    position: relative;
    .btn-del {
      position: absolute;
      top: 0;
      right: 0;
      z-index: 100;
      visibility: hidden;
    }
    &:hover {
      .btn-del {
        visibility: visible;
      }
    }
  }
}
.camera-conatiner {
  position: fixed;
  top: 0px;
  bottom: 0px;
  left: 0px;
  right: 0px;
  z-index: 100;
  background-color: rgba(0, 0, 0, 0.2);
  .camera-zone {
    background: #000;
    width: 700px;
    height: 100%;
    margin-left: auto;
    margin-right: auto;
    position: relative;
    cursor: auto;
    .output-camera {
      width: 100%;
      margin-top: 24px;
    }
    .cancel {
      color: #ffffff;
      font-size: 16px;
      padding-top: 8px;
      padding-left: 8px;
      cursor: pointer;
    }
    .take-photo {
      position: absolute;
      bottom: 12px;
      left: calc(50% - 30px);
      cursor: pointer;
    }
  }
}
</style>