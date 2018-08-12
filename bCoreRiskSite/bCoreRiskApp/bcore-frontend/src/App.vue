<template>
  <v-app dark>
    <v-content>
      <v-toolbar color="primary">
        <v-toolbar-items>
          <v-btn small color="secondary">Manage Risks</v-btn>
        </v-toolbar-items>
      </v-toolbar>
      <div v-for="risk in risks" v-bind:risk_id="risk.id":key="risk.id">          
        <v-text-field
          name="name"
          label="Risk Class"
          id="risk_class_input"          
          :placeholder=" risk.risk_class "
        >
        </v-text-field>
        <risk-field></risk-field>
      </div>
      <v-btn color="primary">Add Field</v-btn>
      <v-btn color="success" dark>Submit Risk</v-btn>
    </v-content>
  </v-app>
</template>

<script>
import riskField from './components/riskField'

export default {
  name: 'riskApp',
  delimiters: ['${', '}'],
  data () {
    return {
      risks: [],
      loading: false,
      currentRisk: {},
      message: null,
      newRisk: { 'risk_class': null }
    }
  },
  components: {
    riskField
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
}

</script>
