import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import FreeCourse from '../views/FreeCourse'
import SearchCourse from '../views/SearchCourse'
import CourseDetail from '../views/CourseDetail'

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
    {
        path: '/course/search',
        name: 'search-course',
        component: SearchCourse
    },
    {
        path: '/free/detail/:pk',
        name: 'free-detail',
        component: CourseDetail
    },
];

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
});

export default router
