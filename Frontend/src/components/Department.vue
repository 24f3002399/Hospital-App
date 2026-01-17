<script>
import axios from 'axios';

export default {
    data(){
        return {
            doctors: "" ,
            search_doc_for: "",
            message: "",
            dept_dt: {
                'Cardiology': `Cardiology unit is dedicated to the prevention, diagnosis, and 
                                treatment of heart-related ailments. Our expert Cardiologists manage conditions 
                                such as coronary artery disease, heart failure, and heart valve problems. 
                                We provide advanced diagnostic services like ECG, TMT (Stress Test), and 
                                Echocardiography to ensure your heart is in safe hands.`,
                'Pediatrics': `We offer specialized care for our youngest patients, from newborns to 
                                teenagers. Our Pediatricians focus on physical, emotional, and social health. Services 
                                include routine check-ups, mandatory vaccinations, nutritional guidance, and treatment 
                                for childhood infections, asthma, and developmental milestones.`,
                'Gynecology': `Our center provides comprehensive care for women at every stage of life. 
                                Our Gynecologists handle reproductive health, menstrual disorders, and menopause 
                                management. Our Obstetricians offer world-class maternity services, including prenatal 
                                care, painless delivery, and post-natal support for both mother and child.`,
                'Orthopedics': `We specialize in the health of your bones, joints, and muscles. 
                                Our Orthopedic Surgeons treat everything from simple fractures and ligament tears to 
                                complex spine disorders. We are experts in joint replacement surgeries (Knee and Hip), 
                                sports medicine, and advanced physiotherapy for long-term mobility.`,
                'Dermatology': `Our Dermatologists treat over 3,000 conditions affecting the skin, hair, 
                                and nails. Whether it is managing chronic conditions like psoriasis and eczema, treating 
                                severe acne, or performing cosmetic procedures for skin rejuvenation and hair restoration,
                                we provide clinical and aesthetic excellence.`,
                'Neurology': `The Neurology department offers specialized care for disorders of the brain,
                                spinal cord, and nerves. Our Neurologists provide expert diagnosis and long-term 
                                management for chronic headaches, migraines, epilepsy (seizures), Parkinson’s disease, 
                                and stroke rehabilitation, focusing on improving the patient's quality of life.`,
                                'Ophthalmology': 'Ophthalmologist',
                'ENT': `Our ENT Specialists provide medical and surgical treatment for disorders of the 
                                head and neck. This includes treating hearing loss and ear infections, chronic sinusitis 
                                and nasal allergies, tonsillitis, and speech or swallowing disorders using modern 
                                endoscopic techniques.`,
                'Dentistry': `We are committed to providing a healthy and beautiful smile. Our Dentists 
                                offer a wide range of services including preventive cleaning, painless root canal 
                                treatments (RCT), dental implants, braces, and professional teeth whitening in a 
                                hygienic and comfortable environment.`,
                'General Medicine': `As the foundation of our hospital, the General Medicine department 
                                manages adult health holistically. Our General Physicians diagnose and treat various 
                                viral fevers, respiratory infections, and chronic lifestyle diseases such as Diabetes, 
                                Thyroid disorders, and Hypertension.`
            }
        }
    },
    mounted(){
        this.loadData()
    },
    methods: {
    loadData: function() {
            const response = axios.get(`http://127.0.0.1:5000/api/dept_doctor/${this.$route.params.name}`, {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem("token")}` 
                }
            })
            response
            .then(res => {
                   this.doctors = res.data.doct_detail
            }).catch(err => this.error = err.response.data.message)
        },
    },
    computed: {
        doct(){
            if (!this.doctors) {
                    return []; 
                }

            return this.doctors.filter(doctor => {
                return doctor.name.toLowerCase().includes(this.search_doc_for.toLowerCase())                   
            })
        },
        about(){
            return this.dept_dt[this.$route.params.name] || this.$route.params.name
        }
    }
}
</script>

<template>
    <div class="dash">
        <div style="color:chocolate;">
            <h1><b>Department of {{ this.$route.params.name }}</b></h1>
        </div>
        <div style="margin-top: 30px; color:mediumvioletred;">
            <h2 style="color:darkgreen;">Overview</h2>
            <h4>{{ about }}</h4>
        </div>
        <div class="row" style="margin-top: 30px;">
            <div class="col-auto me-auto"><h2> Doctors ( {{ doct.length }} )</h2></div>
            <div class="col-auto">
                <input type="text" style="border-radius: 10px" v-model="search_doc_for" :placeholder="`search for...`">
            </div>
        </div>
        <table class="table table-bordered" style="text-align: center;">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Action</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="doctor in doct" :key="doctor.user_id">
                    <td>{{ doctor.id }}</td>
                    <td>{{ doctor.name }}</td>
                    <td><div class="row justify-content-evenly">
                        <div class="col-4">
                            <RouterLink :to="'/book/' + doctor.id">
                                <button class="btn btn-success">Check Availability</button>
                            </RouterLink>
                        </div>
                        </div>
                    </td>
                    <td>
                        <RouterLink :to="'/doctordt/' + doctor.user_id" >
                            <button class="btn btn-warning">View</button>
                        </RouterLink>
                    </td>
                    
                </tr>
            </tbody>
        </table>
        <div style="text-align: center; margin-top: 10px;">
            <button @click="$router.go(-1)" class="btn btn-info">Go Back</button>
        </div>
    </div>
</template>

<style scoped>
    .dash{
        margin-left: 20px;
        margin-right: 20px;
    }
</style>