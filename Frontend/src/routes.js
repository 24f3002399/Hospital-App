import { createWebHistory ,createRouter } from "vue-router";
import Content from "./components/Content.vue";
import LoginPage from "./components/LoginPage.vue";
import RegisterPage from "./components/RegisterPage.vue";
import AdminDash from "./components/AdminDash.vue";
import AddDoctor from "./components/AddDoctor.vue";
import EditDoct from "./components/EditDoct.vue";
import EditPat from "./components/EditPat.vue";
import Availability from "./components/Availability.vue";
import DoctorDash from "./components/DoctorDash.vue";
import PatientDash from "./components/PatientDash.vue";
import DoctorDt from "./components/DoctorDt.vue";
import Department from "./components/Department.vue";
import Book from "./components/Book.vue";
import Treatment from "./components/Treatment.vue";
import AdminChangeAv from "./components/AdminChangeAv.vue";
import PatientDt from "./components/PatientDt.vue";



const routes = [
    {path: "/", component : Content},
    {path: "/login", component: LoginPage},
    {path: "/register", component: RegisterPage},
    {path: "/addDoctor", component: AddDoctor},
    {path: "/editdoct/:id", component: EditDoct},
    {path: "/editpat/:id", component:EditPat},
    {path: "/availability/:id", component:Availability},
    {path: "/doctordash", component:DoctorDash},
    {path: "/patientdash", component:PatientDash},
    {path:"/doctordt/:id", component:DoctorDt},
    {path: "/department/:name", component: Department},
    {path: "/book/:id", component: Book},
    {path: "/treatment/:id", component: Treatment},
    {path: "/adminchangeav/:id", component: AdminChangeAv},
    {path: "/patientdt/:id", component: PatientDt},
    {path: "/admindash", component: AdminDash
        // [
        // {path: "", component: AdminDash},
        // {path: "/something", component: KoiDash},
        // {path: "/someth", component: KoiDas} 
    // ]
    }
]


export const router = createRouter({
    history: createWebHistory(),
    routes
})