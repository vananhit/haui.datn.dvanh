import RecognitionHistory from "@/views/recognition-history/RecognitionHistory"
export default[
    {
        path:'/recognition-history',
        name:"RecognitionHistory",
        component:RecognitionHistory,
        meta: { requiresAuth: true ,isMaster:true},
    },
    {
        path:'/account-recognition-history',
        name:"AccountRecognitionHistory",
        component:RecognitionHistory,
        meta: { requiresAuth: true ,isMaster:false},
    }
]