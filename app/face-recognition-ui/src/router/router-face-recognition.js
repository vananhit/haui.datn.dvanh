import FaceRecognitiom from "@/views/face-recognition/FaceRecognition"
export default [
    {
        path: '/check-in',
        name: 'FaceRecognition',
        component: FaceRecognitiom,
        meta: { requiresAuth: true ,isMaster:true},
    }
]