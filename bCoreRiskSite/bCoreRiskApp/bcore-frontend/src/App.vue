<template>
  <v-app dark>
    <v-content>
      <v-toolbar color="primary">
        <v-toolbar-title>Risk Manager</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon>
          <v-icon>search</v-icon>
        </v-btn>
        <v-btn icon>
          <v-icon>apps</v-icon>
        </v-btn>
        <v-btn icon>
          <v-icon>refresh</v-icon>
        </v-btn>
        <v-btn icon>
          <v-icon>more_vert</v-icon>
        </v-btn>
      </v-toolbar>
      <v-container>
        <v-flex v-for="risk in risks" :key="risk.id">
          <v-layout row wrap>
            <v-text-field
              name="name"
              label="Risk Class"
              id="risk_class_input"
              :placeholder=" risk.risk_class "
            >
            </v-text-field>
            <v-btn flat icon color="accent">
              <v-icon dark>remove_circle_outline</v-icon>
            </v-btn>
          </v-layout>
          <v-layout row wrap>
            <risk-field v-bind:risk_id="risk.id"></risk-field>
          </v-layout>
        </v-flex>
        <v-layout row wrap>
          <v-btn fab dark color="accent">
            <v-icon dark>add</v-icon>
          </v-btn>          
        </v-layout>
      </v-container>
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
