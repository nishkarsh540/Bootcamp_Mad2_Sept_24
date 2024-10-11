<template>
    <div>
        <h2>
            Category Management
        </h2>

        <input 
            type="text"
            v-model="searchQuery"
            placeholder="search categories"
            @input="filterCategories"
        />

        <form @submit.prevent="addCategory">
            <input type="text" v-model="newCategoryName" placeholder="Enter Category Name" required>
            <button type="submit">Add Category</button>
        </form>

        <table v-if="filteredCategories.length>0">
            <thead>
                <tr>
                    <th>Id</th>
                    <th>Name</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="category in filteredCategories" :key="category.id">
                    <td>{{ category.id }}</td>
                    <td>
                        <input type="text" v-model="category.name" :disabled="category.id !== editingCategoryId">
                    </td>

                    <td>
                        <button v-if="category.id !== editingCategoryId" @click="startEditing(category)">Edit</button>
                        <button v-if="category.id == editingCategoryId" @click="saveCategory(category)">Save</button>
                        <button v-if="category.id == editingCategoryId" @click="cancelCategory()">Cancel</button>
                        <button v-if="category.id !== editingCategoryId" @click="deleteCategory(category)">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>

        <div v-else>
            <p>No categories found.</p>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default{
    data(){
        return {
            categories:[],
            newCategoryName:'',
            editingCategoryId:null,
            filteredCategories:[],
            searchQuery:'',
        };
    },
    mounted() {
        this.loadCategories();
    },
    methods:{
        async loadCategories(){
            try{
                const response = await axios.get('http://127.0.0.1:5000/api/category');
                this.categories = response.data;
                this.filteredCategories = this.categories;
            } catch(error){
                console.error('Error loading categories',error);
            }
        },
        async addCategory(){
            try{
                const response = await axios.post('http://127.0.0.1:5000/api/category',{
                    name:this.newCategoryName
                });
                console.log('Category added',response.data);
                this.newCategoryName='';
                this.loadCategories();
            } catch(error){
                console.error(
                    'Error adding category',error
                )
            }
        },
        async deleteCategory(category){
            try {
                const response = await axios.delete('http://127.0.0.1:5000/api/category', {
                    data: { id:category.id }
                });
                console.log('Category Deleted');
                console.log(response.data);
                this.loadCategories();
            } catch (error) {
                console.error(
                    'Error deleting category', error
                )
            }
        },
        async saveCategory(category){
            try{
                const response = await axios.put('http://127.0.0.1:5000/api/category',{
                    id:category.id,
                    name:category.name
                });
                console.log('Category updated', response.data);
                this.editingCategoryId = null;
                this.loadCategories();
            } catch(error){
                console.error('Error updating category',error);
            }
        },

        startEditing(category){
            this.editingCategoryId = category.id;
        },
        cancelCategory(){
            this.editingCategoryId = null;
        },
        filterCategories(){
            const query = this.searchQuery.toLowerCase();
            this.filteredCategories = this.categories.filter(category => category.name.toLowerCase().includes(query))
            console.log(this.filteredCategories)
        }
    }
}

</script>