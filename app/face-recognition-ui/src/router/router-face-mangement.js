import FaceManagement from "@/views/face-management/FaceManagement"
export default[
    {
        path:'/face-manangement',
        name:'FaceMangement',
        component:FaceManagement,
        meta: { requiresAuth: true },
    }
]