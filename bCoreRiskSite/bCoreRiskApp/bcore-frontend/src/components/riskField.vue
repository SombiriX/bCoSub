<template>
  <div>
    <v-chip
      close
      v-for="(risk_field, i) in risk_fields"
      :key="risk_field.id"
      v-model="risk_fields[i].displayed"
      @input="
        currentRiskField=risk_fields[i],
        dialogOrNull(true),
        risk_fields[i].displayed=true"
    >
      <v-avatar :color="risk_field.f_color">{{ risk_field.field_type }}</v-avatar>
      {{ risk_field.field_name }}
    </v-chip>
    <v-tooltip bottom>
      <v-btn flat icon color="accent" slot="activator">
        <v-icon dark>add_circle_outline</v-icon>
      </v-btn>
      <span>Add new field</span>
    </v-tooltip>
    <component
      v-bind:is="delRFieldDialog"
      @dialogYes = "dialogYes()"
      @dialogNo = "dialogNo()"
      v-bind:msgProps="{
        title: 'Really delete ' + currentRiskField.field_name + '?',
        subtitle: 'This action cannot be undone'
      }"
    >
    </component>
  </div>
</template>

<script>
import yesNoDialog from './yesNoDialog'
import Vue from 'vue'

Vue.component('yesNoDialog', {
  template: yesNoDialog
})

export default {
  name: 'riskField',
  props: ['risk_id'],
  delimiters: ['${', '}'],
  data () {
    return {
      risk_fields: [],
      loading: false,
      currentRiskField: {},
      message: null,
      newRiskField: { 'field_name': null, 'field_type': null, 'field': null },
      addRFieldDialog: false,
      delRFieldDialog: null,
      rFieldValid: true,
      rules: {
        required: value => !!value || 'Required.'
      }
    }
  },
  mounted: function () {
    this.getRiskFields()
  },
  methods: {
    getRiskFields: function () {
      this.loading = true
      var riskID = this.risk_id
      this.$http.get('/api/riskfield/')
        .then((response) => {
          this.risk_fields = response.data.filter(function (rf) {
            // Set style based on data type
            if (rf.risk.id === riskID) {
              if (rf.field_type === 'T') {
                rf.f_color = 'pink darken-2'
              } else if (rf.field_type === 'N') {
                rf.f_color = 'lime'
              } else if (rf.field_type === 'D') {
                rf.f_color = 'light-green'
              } else if (rf.field_type === 'E') {
                rf.f_color = 'purple darken-2'
              } else { rf.f_color = 'white' }
              // Add display data
              rf.displayed = true
              return rf
            }
          })
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
      this.loading = false
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
    },
    dialogOrNull: function (dialog) {
      if (dialog) {
        this.delRFieldDialog = yesNoDialog
      } else {
        this.delRFieldDialog = null
      }
    },
    dialogYes: function () {
      this.delRFieldDialog = null
      this.deleteRiskField(this.currentRiskField.id)
    },
    dialogNo: function () {
      this.delRFieldDialog = null
    }
  }
}

</script>
