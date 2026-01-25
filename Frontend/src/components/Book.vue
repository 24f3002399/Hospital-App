<script>
import axios from 'axios';

export default {
    data(){
        return {
            mess: "",
            slot_detail: "",
            patient_id: ""
        }
    },
    mounted(){
        this.Slot()
        this.loadUser()
    },
    methods: {
        loadUser: function() {
            const response = axios.get("http://127.0.0.1:5000/api/dashboard", {
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem("token")}` 
                }
            })
            response
            .then(res => {
                   this.patient_id = res.data.patient_id
            }).catch(err => this.error = err.response.data.message)
        },
        Slot: function() {
            const response = axios.get(`http://127.0.0.1:5000/api/slot_dt/${this.$route.params.id}`,{
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            })
            response
            .then(res => {
                    this.slot_detail = res.data.slot_detail
            }).catch(err => this.error = err.response.data.message)

        },
        Book: function(date, id , slot) { 
                const response = axios.post(`http://127.0.0.1:5000/api/book/${this.$route.params.id}/${this.patient_id}/${id}/${slot}/${date}`,{},{
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            })
            response
            .then(res => {
                    this.Slot()
            }).catch(err => this.error = err.response.data.message)
        },
        Ask_book: function(date, id , slot) {
            const result = confirm("Are you want to book this slot");
            if (result) {
                this.Book(date, id , slot)                
            } else {
                console.log("Denied Booking")
            }
        },        
    }
}
</script>

<template>
    <div style="width: 60%; margin: auto;">
    <div id="head"><h2>Book Slot</h2></div>
    <ul class="list-group list-group-flush">
        <li v-for="slot in slot_detail" style="text-align: center; padding: 10px;" class="list-group-item">
            <span class="date"><b>{{ new Date(slot.date).toLocaleDateString('en-GB')}}</b></span>
            <span v-if="slot.slot1 == `available`" class="slot">
                <button  @click="Ask_book(slot.date, slot.id, 1)" type="button" class="btn btn-outline-success" >8 AM - 11 AM</button>
            </span>
            <span v-else class="slot">
                <button type="button" class="btn btn-outline-danger" disabled>8 AM - 11 AM</button>
            </span>
            <span v-if="slot.slot2 == `available`" class="slot">
                <button @click="Ask_book(slot.date, slot.id, 2)" type="button" class="btn btn-outline-success" >1 PM - 4 PM</button>
            </span>
            <span v-else class="slot">
                <button type="button" class="btn btn-outline-danger" disabled>1 PM - 4 PM</button>
            </span>
            <span v-if="slot.slot3 == `available`" class="slot">
                <button @click="Ask_book(slot.date, slot.id, 3)" type="button" class="btn btn-outline-success" >6 PM - 9 PM</button>
            </span>
            <span v-else class="slot">
                <button type="button" class="btn btn-outline-danger" disabled>6 PM - 9 PM</button>
            </span>
        </li> 
    </ul>
    <div style="text-align: center; margin-top: 10px;">
        <button @click="$router.go(-1)" class="btn btn-info">Go Back</button>
    </div>
    </div>
</template>

<style scoped>
    #head{
            text-align: center; 
            color:mediumvioletred; 
            border: 2px solid black; 
            width: 60% ; 
            margin: auto; 
            margin-bottom: 20px;
            border-radius: 15px;
    }
    .slot{
        padding: 20px;
    }
    .date{
        padding: 20px;
    }
    .alert {
        padding: 15px;
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
        border-radius: 4px;
        text-align: center;
    }
</style>