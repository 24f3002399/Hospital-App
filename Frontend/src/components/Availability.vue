<script>
import axios from 'axios';

export default {
    data(){
        return {
            mess: "",
            slot_detail: "",
            doctor_id: null
        }
    },
    mounted(){
        this.Slot()
    },
    methods: {
        Slot: function() {
            const response = axios.post(`http://127.0.0.1:5000/api/provide_av/${this.$route.params.id}`,{},{
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
        Change: function(id , slot) { 
                const response = axios.post(`http://127.0.0.1:5000/api/change/${this.$route.params.id}/${id}/${slot}`,{},{
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`
                }
            })
            response
            .then(res => {
                    null
            }).catch(err => this.error = err.response.data.message)
        },
        Save: function() {
            this.Slot()
            this.mess = "Availability Provide Successfully"
        }
        
    }
}
</script>

<template>
    <div style="width: 60%; margin: auto;">
    <div id="head"><h2>Provide Availability</h2></div>
    <ul class="list-group list-group-flush">
        <li v-for="slot in slot_detail" style="text-align: center; padding: 10px;" class="list-group-item">
            <span class="date"><b>{{ new Date(slot.date).toLocaleDateString('en-GB')}}</b></span>
            <span v-if="slot.slot1 == `available`" class="slot">
                <button  @click="Change(slot.id, 1)" type="button" class="btn btn-outline-success" data-bs-toggle="button">8AM - 11 AM</button>
            </span>
            <span v-else-if="slot.slot1 == `booked`" class="slot">
                <button @click="Change(slot.id, 1)" type="button" class="btn btn-outline-danger" disabled>8 AM - 11 AM</button>
            </span>
            <span v-else class="slot">
                <button @click="Change(slot.id, 1)" type="button" class="btn btn-outline-danger" data-bs-toggle="button">8 AM - 11 AM</button>
            </span>
            <span v-if="slot.slot2 == `available`" class="slot">
                <button @click="Change(slot.id, 2)" type="button" class="btn btn-outline-success" data-bs-toggle="button">1 PM - 4 PM</button>
            </span>
            <span v-else-if="slot.slot2 == `booked`" class="slot">
                <button @click="Change(slot.id, 2)" type="button" class="btn btn-outline-danger" disabled>1 PM - 4 PM</button>
            </span>
            <span v-else class="slot">
                <button @click="Change(slot.id, 2)" type="button" class="btn btn-outline-danger" data-bs-toggle="button">1 PM - 4 PM</button>
            </span>
            <span v-if="slot.slot3 == `available`" class="slot">
                <button @click="Change(slot.id, 3)" type="button" class="btn btn-outline-success" data-bs-toggle="button">6 PM - 9 PM</button>
            </span>
            <span v-else-if="slot.slot3 == `booked`" class="slot">
                <button @click="Change(slot.id, 3)" type="button" class="btn btn-outline-danger" disabled>6 PM - 9 PM</button>
            </span>
            <span v-else class="slot">
                <button @click="Change(slot.id, 3)" type="button" class="btn btn-outline-danger" data-bs-toggle="button">6 PM - 9 PM</button>
            </span>
        </li> 
    </ul>
    <div style="text-align: center;">
        <button @click="Save" class="btn btn-success" style="margin-right: 10px;">Save</button> 
        <RouterLink to="/doctordash" >
            <button class="btn btn-info">Go Back</button>
        </RouterLink>
    </div>
    </div>
    <div v-if="mess" class="alert" >
        {{ mess }}
    </div>
</template>

<style scoped>
    #head{
            text-align: center; 
            color:mediumvioletred; 
            border: 2px solid black; 
            width: 60% ; 
            margin: auto; 
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