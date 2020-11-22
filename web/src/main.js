import Vue from 'vue'
import App from './App.vue'
Vue.config.productionTip = false


import axios from 'axios';
import VueAxios from 'vue-axios';

Vue.use(VueAxios, axios)

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI)

new Vue({
  render: h => h(App),
}).$mount('#app')
