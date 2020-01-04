import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import FreeCourse from '../views/FreeCourse'

Vue.use(VueRouter);

const routes = [
    {
        path: '/',
        name: 'home',
        component: Home
    },
    {
        path: '/free-course',
        name: 'free-course',
        component: FreeCourse
    },
];

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
});

export default router
