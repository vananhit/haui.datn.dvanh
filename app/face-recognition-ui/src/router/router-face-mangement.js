import FaceManagement from "@/views/face-management/FaceManagement";
import FaceManagementDetail from "@/views/face-management/FaceMangementDetail";
export default[
    {
        path:'/face-manangement',
        name:'FaceMangement',
        component:FaceManagement,
        meta: { requiresAuth: true },
    
    },
    {
        // when //face-manangement/detail is matched
        name:"FaceMangementDetatil",
        path: '/face-manangement/detail',
        component: FaceManagementDetail,
        meta: { requiresAuth: true },

      },
]