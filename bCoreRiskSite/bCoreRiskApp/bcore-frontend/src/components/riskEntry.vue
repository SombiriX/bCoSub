<template>
  <v-container>
    <v-flex v-for="risk in risks" :key="risk.id">
      <v-layout row wrap>
        <v-text-field
          name="rClass"
          label="Risk Class"
          id="risk_class_input"
          :placeholder=" risk.risk_class "
        >
        </v-text-field>
        <v-tooltip bottom>
          <v-btn
            flat
            icon
            color="accent"
            slot="activator"
            @click.native.stop="dialogOrNull('yesNo'), currentRisk=risk"
          >
            <v-icon dark>remove_circle_outline</v-icon>
          </v-btn>
            <span>Delete Risk Class</span>
        </v-tooltip>
      </v-layout>
      <v-layout row wrap>
        <risk-field v-bind:risk_id="risk.id"></risk-field>
      </v-layout>
    </v-flex>
    <v-layout row justify-end>
      <v-tooltip bottom>
        <v-btn
          fab
          dark
          color="accent"
          slot="activator"
          @click.native.stop="dialogOrNull('createRisk')">
          <v-icon dark>add</v-icon>
        </v-btn>
        <span>New Risk Class</span>
      </v-tooltip>
    </v-layout>
<!-- User Action Dialogs -->
    <component
      v-bind:is="createRiskDialog"
      @riskCreated = "dialogCreateRisk"
      @createRiskDialogClosed = "createRiskDialogClosed()"
    >
    </component>
    <component
      v-bind:is="delRiskDialog"
      @dialogYes = "dialogYes()"
      @dialogNo = "dialogNo()"
      v-bind:msgProps="{
        title: 'Really delete ' + currentRisk.risk_class + '?',
        subtitle: 'This action cannot be undone'
      }"
    >
    </component>
  </v-container>
</template>

<script>
import riskField from './riskField'
import yesNoDialog from './yesNoDialog'
import createRiskDialog from './createRiskDialog'
import Vue from 'vue'

Vue.component('yesNoDialog', {
  template: yesNoDialog
})

Vue.component('createRiskDialog', {
  template: createRiskDialog
})

export default {
  name: 'riskEntry',
  delimiters: ['${', '}'],
  data () {
    return {
      risks: [],
      loading: false,
      currentRisk: {},
      message: null,
      newRiskClass: {'risk_class': ''},
      createRiskDialog: null,
      delRiskDialog: null
    }
  },
  components: {
    'risk-field': riskField
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
      this.$http.post('/api/risk/', this.newRiskClass)
        .then((response) => {
          this.loading = false
          this.getRisks()
          this.newRiskClass.risk_class = ''
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
    },
    dialogOrNull: function (dialog) {
      if (dialog === 'yesNo') {
        this.delRiskDialog = yesNoDialog
      } else if (dialog === 'createRisk') {
        this.createRiskDialog = createRiskDialog
      } else {
        this.delRiskDialog = null
        this.createRiskDialog = null
      }
    },
    dialogYes: function () {
      this.delRiskDialog = null
      this.deleteRisk(this.currentRisk.id)
    },
    dialogNo: function () {
      this.delRiskDialog = null
    },
    createRiskDialogClosed: function () {
      this.createRiskDialog = null
    },
    dialogCreateRisk: function (userInput) {
      this.createRiskDialog = null
      this.newRiskClass.risk_class = userInput
      this.addRisk()
    }
  }
}

</script>
