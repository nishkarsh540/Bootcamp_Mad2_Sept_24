<template>
    <div class="signup-container">
        <form @submit.prevent="loginuser">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" required>
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required>
            </div>
            <button type="submit">Login</button>
        </form>
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
</template>

<script>
import axios from 'axios';

export default{
    data(){
        return{
            username:'',
            password:'',
            errorMessage:'',
        }
    },
    methods:{
        async loginuser(){
            try{
                const response = await axios.post('http://127.0.0.1:5000/api/login',{
                    username:this.username,
                    password:this.password
                });

                console.log(response);
                const {access_token,user} = response.data;
                localStorage.setItem('user',JSON.stringify(user));
                this.$store.dispatch('login',{token:access_token,user});

                if (user.role === 'admin'){
                    this.$router.push('/admin-dashboard')
                } else if (user.role === "store-manager"){
                    this.$router.push('/store-dashboard')
                } else {
                    this.$router.push('/user-dashboard')
                }
            } catch(error){
                console.log(error);
                this.errorMessage = error.response ? error.response.data.message:'Invalid'
            }
        }
    }

}

</script>