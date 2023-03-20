import Webcam from "react-webcam";
import { FaceDetectionAdapter } from "./FacDetection.Adapter";
import './FaceDetection.scss'

const FaceDetection = () => {

    const { webcamRef, canvasRef, faceRef } = FaceDetectionAdapter();


    return <div className="face-detection">
        <canvas ref={faceRef} style={{display:"none"}} ></canvas>
        <Webcam

            mirrored
            className="webcam"
            ref={webcamRef}
        />
        <canvas ref={canvasRef} />

    </div>
}

export default FaceDetection;