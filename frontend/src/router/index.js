import { createRouter, createWebHistory } from 'vue-router'
import store from '../store';
import HomeView from '../views/HomeView.vue'
import SignupUser from '../auth/SignupUser.vue'
import LoginUser from '../auth/LoginUser.vue'
import AdminDashboard from '../views/AdminDashboard.vue'
import UserDashboard from '../views/UserDashboard.vue'
import CategoryManage from '@/views/CategoryManage.vue';
import StatPage from '@/views/StatPage.vue';
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/stat',
    name: 'stat',
    component: StatPage
  },
  {
    path: '/category_manage',
    name: 'CategoryManage',
    component: CategoryManage,
    meta:{ requiresAuth:true,roles:['admin']}
  },
  {
    path: '/admin-dashboard',
    name: 'admin',
    component: AdminDashboard,
    meta:{ requiresAuth:true,roles:['admin']}
  },
  {
    path: '/user-dashboard',
    name: 'user',
    component: UserDashboard
  },
  {
    path: '/login',
    name: 'login',
    component: LoginUser
  },
  {
    path: '/signup',
    name: 'Signup',
    component: SignupUser
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// //Navigation Guard
router.beforeEach((to,from,next) =>{
  if (to.meta.requiresAuth){
    if (!store.getters.isAuthenticated){
      next('/login')
    } else {
      console.log(store.getters.userRole);
      const userRole = store.getters.userRole;

      if (to.meta.roles && !to.meta.roles.includes(userRole)){
        next('/login');
      } else {
        next();
      }
    }
  } else {
    next();
  }
});


export default router
