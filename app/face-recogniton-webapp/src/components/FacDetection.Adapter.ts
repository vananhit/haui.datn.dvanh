import { Camera } from "@mediapipe/camera_utils";
import { FaceDetection, Results } from "@mediapipe/face_detection";
import { useEffect, useRef } from "react";
import Webcam from "react-webcam";
import { drawBoundingBox, extractFace, point, writeTex } from "./utils";

const FaceDetectionAdapter = () => {
  const webcamRef = useRef<Webcam>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const faceRef = useRef<HTMLCanvasElement>(null);
  var camera: Camera;

  function onResults(results: Results) {
    const start = new Date();
    let videoWidth = results.image.width;
    let videoHeight = results.image.height;

    if (canvasRef && canvasRef.current) {
      // Set canvas width
      canvasRef.current.width = videoWidth;
      canvasRef.current.height = videoHeight;

      const canvasElement = canvasRef.current;

      const canvasCtx = canvasElement.getContext("2d");
      if (canvasCtx) {
        //draw image
        canvasCtx.save();
        canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
        canvasCtx.drawImage(results.image, 0, 0, videoWidth, videoHeight);

        //visualize
        for (let i = 0; i < results.detections.length; i++) {
          drawBoundingBox(canvasCtx, results.detections[i].boundingBox, {
            width: videoWidth,
            height: videoHeight,
          });

          for (let j = 0; j < results.detections[i].landmarks.length; j++) {
            point(canvasCtx, {
              x: results.detections[i].landmarks[j].x * videoWidth,
              y: results.detections[i].landmarks[j].y * videoHeight,
            });
          }

          // const dataURL = extractFace(
          //   faceRef,
          //   results.image,
          //   results.detections[i].boundingBox
          // );

          //   downloadImageBase64(dataURL);

          const postData = new Promise((resolve, reject) => {
            const url = "facebook.com";
            const request = new XMLHttpRequest();
            request.open("POST", url);

            request.setRequestHeader("Accept", "application/json");
            request.setRequestHeader("Content-Type", "application/json");

            request.onreadystatechange = function () {
              if (request.readyState == 4 && request.status == 200) {
                resolve(request.response);
              } else {
                reject(request.response);
              }
              console.log(request.readyState)
            };

            var data = `{
             "Id": 78912,
             "Customer": "Jason Sweet",
             "Quantity": 1,
             "Price": 18.00
           }`;

            request.send(data);
          });

          postData
            .then((resp) => {
              console.log(resp);
            })
            .catch((e) => {
              console.log(e);
            });
          const fps = Math.round(
            1000.0 / (new Date().valueOf() - start.valueOf())
          );
          writeTex(
            canvasCtx,
            {
              MaSv: "2019601048",
              Tên: "Đặng Văn Anh",
              fps: fps,
            },
            10,
            10
          );

          // pick one face
          break;
        }
      }
    }
  }

  useEffect(() => {
    const faceDetection = new FaceDetection({
      locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/face_detection@0.4/${file}`;
      },
    });

    faceDetection.setOptions({
      selfieMode: true,
      minDetectionConfidence: 0.5,
      model: "short",
    });

    faceDetection.onResults(onResults);

    if (
      typeof webcamRef.current !== "undefined" &&
      webcamRef.current !== null
    ) {
      //@ts-ignore
      camera = new Camera(webcamRef.current.video, {
        onFrame: async () => {
          //@ts-ignore
          await faceDetection.send({ image: webcamRef.current.video });
        },
        width: 640,
        height: 480,
      });
      camera.start();
    }
  }, []);
  return {
    faceRef,
    canvasRef,
    webcamRef,
  };
};

export { FaceDetectionAdapter };
