import Vue from 'vue'
import App from './App.vue'
import router from "./router";
import store from "./store"
import ElenmentUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';

import 'xe-utils'
import VXETable from 'vxe-table'
import 'vxe-table/lib/style.css'

Vue.use(VXETable)

Vue.use(ElenmentUI);
Vue.config.productionTip = false

new Vue({
	router,
	store,
	render: h => h(App),
}).$mount('#app')
