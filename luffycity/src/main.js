import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

Vue.config.productionTip = false;

// 全局css
require('@/assets/css/global.css');

// 全局js配置
import settings from '@/assets/js/settings'
Vue.prototype.$settings = settings;

// axios
import axios from 'axios'
Vue.prototype.$axios = axios;

// cookies
import cookies from 'vue-cookies'
Vue.prototype.$cookies = cookies;
/*
this.$cookies.set(key, value, exp)
this.$cookies.get(key)
this.$cookies.remove(key)
*/

// element-ui
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(ElementUI);

// bootstrap + jquery
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'


new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app');
