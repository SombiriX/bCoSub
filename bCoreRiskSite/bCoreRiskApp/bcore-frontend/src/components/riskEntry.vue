<template>
  <v-container grid-list-xs>
    <v-layout row wrap>
      <v-flex>      
        <v-card color="gray">    
          <v-flex v-for="(risk, i) in risks" :key="risk.id">
            <v-form
              ref="rClass"
              v-model="rClassValid"
              @submit.prevent="submitRisk(i)"
            >
              <v-layout row wrap justify-center>
                <v-flex xs10>
                  
                  <v-text-field
                    :rules=[rules.required]
                    label="Risk Type"
                    id="risk_class_input"
                    hint="Press enter"
                    v-model="risks[i].risk_class"
                  >
                  </v-text-field>
                </v-flex>
                <v-flex xs1>                  
                  <v-tooltip bottom>
                    <v-btn
                      flat
                      icon
                      color="accent"
                      slot="activator"
                      @click.native.stop="
                        currentRisk=risks[i],
                        dialogOrNull('yesNo')"
                    >
                      <v-icon dark>remove_circle_outline</v-icon>
                    </v-btn>
                      <span>Delete Risk Type</span>
                  </v-tooltip>
                </v-flex>
              </v-layout>
            </v-form>
            <v-layout row wrap justify-center>
              <v-flex xs10>                
                <risk-field v-bind:risk_id="risk.id"></risk-field>
              </v-flex>
            </v-layout>
          </v-flex>
          <v-layout row justify-end>
            <v-tooltip bottom>
              <v-btn
                fab
                dark
                ref="rAddButton"
                color="accent"
                slot="activator"
                @click.native.stop="dialogOrNull('createRisk')">
                <v-icon dark>add</v-icon>
              </v-btn>
              <span>New Risk Type</span>
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
            v-bind:dlgProps="{
              title: 'Really delete ' + currentRisk.risk_class + '?',
              subtitle: 'This action cannot be undone'
            }"
          >
          </component>
          <component
            v-bind:is="snackBarDisplay"
            v-bind:snackProps="{
              display: true,
              color: 'success',
              mode: '',
              timeout: 1500,
              text: 'Risk Type Updated'
            }"
            @complete=snackBarComplete()
          >
          </component>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import riskField from './riskField'
import yesNoDialog from './yesNoDialog'
import createRiskDialog from './createRiskDialog'
import infoSnackBar from './infoSnackBar'
import Vue from 'vue'

Vue.component('yesNoDialog', {
  template: yesNoDialog
})

Vue.component('createRiskDialog', {
  template: createRiskDialog
})

Vue.component('infoSnackBar', {
  template: infoSnackBar
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
      delRiskDialog: null,
      snackBarDisplay: null,
      snackBarTimeout: null,
      rClassValid: false,
      rules: {
        required: value => !!value || 'Required.'
      }
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
      this.$http.put(`/api/risk/${this.currentRisk.id}/`, this.currentRisk)
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
    submitRisk: function (i) {
      // Capture form submission
      if (this.$refs.rClass[i].validate()) {
        this.currentRisk = this.risks[i]
        this.updateRisk()
        this.dialogOrNull('snackbar')
      }
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
      } else if (dialog === 'snackbar') {
        this.snackBarDisplay = infoSnackBar
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
    },
    removeSnackBar: function () {
      this.snackBarDisplay = null
      clearTimeout(this.snackBarTimeout)
    },
    snackBarComplete: function () {
      setTimeout(this.removeSnackBar, 100)
    }
  }
}

</script>
