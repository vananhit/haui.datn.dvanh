import RecognitionHistory from "@/views/recognition-history/RecognitionHistory"
export default[
    {
        path:'/recognition-history',
        name:"RecognitionHistory",
        component:RecognitionHistory,
        meta: { requiresAuth: true },
    }
]