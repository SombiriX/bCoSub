import '@babel/polyfill'
import Vue from 'vue'
import './plugins/vuetify'
import './plugins/bootstrap-vue'
import './plugins/vue-resource'
import './plugins/vue-js-cookie'
import riskApp from './App.vue'

Vue.config.productionTip = true

// Set the CSRF Token on all modification requests
Vue.http.interceptors.push((request, next) => {
  // Get the CSRF Token
  var csrftoken = Vue.cookie.get('csrftoken')
  var method = request.method
  // Check the request type
  if ((method === 'POST') || (method === 'DELETE') || (method === 'PUT')) {
    // modify headers
    request.headers.set('X-CSRF-TOKEN', csrftoken)
    request.headers.set('X-CSRFToken', csrftoken)
  }
  // continue to next interceptor
  next()
})

new Vue({
  render: h => h(riskApp),
  delimiters: ['${', '}'],
  data: {}
}).$mount('#app')
