import '@babel/polyfill'
import Vue from 'vue'
import './plugins/vuetify'
import './plugins/bootstrap-vue'
import './plugins/vue-resource'
import './plugins/vue-js-cookie'
import riskApp from './App.vue'
import router from './router'

Vue.config.productionTip = true

new Vue({
  router,
  render: h => h(riskApp),
  delimiters: ['${', '}'],
  data: {}
}).$mount('#app')
