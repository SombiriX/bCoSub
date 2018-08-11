import '@babel/polyfill'
import Vue from 'vue'
import './plugins/vuetify'
import './plugins/bootstrap-vue'
import './plugins/vue-resource'
import riskApp from './App.vue'
import router from './router'

Vue.config.productionTip = true

new Vue({
  router,
  render: h => h(riskApp),
  delimiters: ['${', '}'],
  data: {
    risks: [],
    loading: false,
    currentRisk: {},
    message: null,
    newRisk: { 'risk_class': null }
  },
  mounted: function () {
    this.getRisks()
  },
  methods: {
    getRisks: function () {
      this.loading = true
      this.$http.get('/api/risk/')
        .then((response) => {
          this.risks = response.data
          this.loading = false
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    },
    getRisk: function (id) {
      this.loading = true
      this.$http.get(`/api/risk/${id}/`)
        .then((response) => {
          this.currentRisk = response.data
          this.loading = false
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    },
    addRisk: function () {
      this.loading = true
      this.$http.post('/api/risk/', this.newRisk)
        .then((response) => {
          this.loading = false
          this.getRisks()
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    },
    updateRisk: function () {
      this.loading = true
      this.$http.put(`/api/risk/${this.currentRisk.risk_id}/`, this.currentRisk)
        .then((response) => {
          this.loading = false
          this.currentRisk = response.data
          this.getRisks()
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    },
    deleteRisk: function (id) {
      this.loading = true
      this.$http.delete(`/api/risk/${id}/`)
        .then((response) => {
          this.loading = false
          this.getRisks()
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    }
  }
}).$mount('#app')
