<template>
    <p>Admin dashboard</p>
    <button @click="exportcsv">Download Report</button>
    <div>
        <h2>Manager Managing</h2>
        <table v-if="pendingManagers.length>0">
            <thead>
                <tr>
                    <th>username</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="manager in pendingManagers" :key="manager.id">
                    <td>{{ manager.username }}</td>
                    <td>
                        <button @click="confirmApproval(manager)">Approve</button>
                        <button @click="confirmRejection(manager)">Reject</button>
                    </td>
                </tr>
            </tbody>
        </table>
        <p v-else> No new managers</p>

        <div v-if="showConfirmationModel">
            <div>
                <h2>{{ confirmationTitle }}</h2>
                <p>{{ confirmationMessage }}</p>
                <div>
                        <button @click="handleConfirmation(true)">Confirm</button>
                        <button @click="handleConfirmation(false)">Cancel</button>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import axios from 'axios';
export default{
    data(){
        return{
            username:JSON.parse(localStorage.getItem('user')).username,
            user_id : JSON.parse(localStorage.getItem('user')).id,
            pendingManagers:[],
            showConfirmationModel:false,
            confirmationTitle:'',
            pendingManagerToHandle:null,
        }
    },
    created(){
        this.fetchPendingManagers();
        console.log(this.user_id);
    },
    methods:{
        fetchPendingManagers(){
            const accessToken = localStorage.getItem('token');
            axios
                .get('/api/admin/pending_managers',{
                    headers:{
                        Authorization: `Bearer ${accessToken}`
                    },

                })
                .then((response) =>{
                    this.pendingManagers = response.data;
                })
                .catch((error)=>{
                    console.error(error);
                })

        },
        handleManageraction(managerId,status){
            const accessToken = localStorage.getItem('token');
            const data={
                manager_id:managerId,
                status:status,
            };
            axios
                .post('/api/admin/pending_managers',data,{
                    headers:{
                        Authorization: `Bearer ${accessToken}`,
                    },
                })
                .then((response)=>{
                    this.fetchPendingManagers();
                    console.log(response.data);
                })
                .catch((error)=>{
                    console.log(error);
                })
        },
        confirmApproval(manager){
            this.pendingManagerToHandle=manager;
            this.confirmationTitle='Approve Manager';
            this.confirmationMessage = `Approve ${manager.username}'s manager request'`;
            this.showConfirmationModel=true;
        },
        confirmRejection(manager){
            this.pendingManagerToHandle = manager;
            this.confirmationTitle = 'Reject Manager';
            this.confirmationMessage = `Reject ${manager.username}'s manager request'`;
            this.showConfirmationModel = true;
        },
        handleConfirmation(isConfirmed){
            if (isConfirmed){
                if (this.confirmationTitle ==='Approve Manager'){
                    this.handleManageraction(this.pendingManagerToHandle.id,'approve');
                } else if( this.confirmationTitle==='Reject Manager'){
                    this.handleManageraction(this.pendingManagerToHandle.id,'reject'
                    );
                }
            }

            this.showConfirmationModel=false;
            this.confirmationTitle='',
            this.confirmationMessage='',
            this.pendingManagerToHandle=null;
        },
        exportcsv(){
            axios.post('/exportcsv',null,{responseType:'blob'})
            .then(response=> {
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const downloadLink = document.createElement('a');
                downloadLink.href=url;
                downloadLink.setAttribute('download','category_report.csv');
                document.body.appendChild(downloadLink);
                downloadLink.click();
                document.body.removeChild(downloadLink);
            })
            .catch(error => {
                console.error(error);
            })
        }
    }
}
</script>