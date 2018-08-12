<template>
  <!-- <v-btn v-on:click="count++" color="success">You clicked me {{ count }} times.</v-btn> -->
  <div>
    <v-btn v-for="risk_field in risk_fields" :key="risk_field.id">
      {{ risk_field.field_name }}
    </v-btn>
  </div>
</template>

<script>
export default {
  name: 'riskField',
  props: ['risk_id'],
  delimiters: ['${', '}'],
  data () {
    return {
      count: 0,
      risk_fields: [],
      loading: false,
      currentRiskField: {},
      message: null,
      newRiskField: { 'field_name': null, 'field_type': null, 'field': null }
    }
  },
  mounted: function () {
    this.getRiskFields()
  },
  methods: {
    getRiskFields: function () {
      this.loading = true
      this.$http.get('/api/riskfield/')
        .then((response) => {
          this.risk_fields = response.data
          this.loading = false
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    },
    getRiskField: function (id) {
      this.loading = true
      this.$http.get(`/api/riskfield/${id}/`)
        .then((response) => {
          this.currentRiskField = response.data
          this.loading = false
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    },
    addRiskField: function () {
      this.loading = true
      this.$http.post('/api/riskfield/', this.newRiskField)
        .then((response) => {
          this.loading = false
          this.getRiskFields()
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    },
    updateRiskField: function () {
      this.loading = true
      this.$http.put(`/api/riskfield/${this.currentRiskField.risk_id}/`, this.currentRiskField)
        .then((response) => {
          this.loading = false
          this.currentRiskField = response.data
          this.getRiskFields()
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    },
    deleteRiskField: function (id) {
      this.loading = true
      this.$http.delete(`/api/riskfield/${id}/`)
        .then((response) => {
          this.loading = false
          this.getRiskFields()
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    }
  }
}

</script>
