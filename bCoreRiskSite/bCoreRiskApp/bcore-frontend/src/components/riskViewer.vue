<template>
  <v-container>
    <v-toolbar color="primary lighten-1" dark>
      <v-toolbar-title>Risk Types</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    <v-list>
      <template v-for="risk in risks">
        <v-list-tile
          :key="risk.id + '-tile'"
          avatar
          @click="
            displayRisk(risk)"
        >
          <v-list-tile-content>
            <v-list-tile-title v-html="risk.risk_class"></v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
        <v-divider :key="risk.id + '-sep'"></v-divider>
      </template>
    </v-list>
    <v-layout row justify-center>
      <v-dialog v-model="rEntryDialog" max-width="400" flat>
        <v-form
          ref="riskForm"
          v-model="rFormValid"
          @submit.prevent="submit()"
        >
          <v-card
            color="secondary"
          >
            <v-toolbar color="primary lighten-1" dark>
              <v-toolbar-title>{{ currentRisk.risk_class }}</v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-layout row wrap justify-center>
              <v-flex xs10>
                <v-card
                  color="secondary lighten-1"
                  v-for="(rf, i) in curRiskFields"
                  :key="i"
                >
                  <risk-field-view
                    v-bind:riskField="Object.assign({}, curRiskFields[i])"
                    v-bind:choices="choices"
                    v-model="curRiskFields[i].field"
                  >
                  </risk-field-view>
                  <v-divider></v-divider>
                </v-card>
              </v-flex>
            </v-layout>
            <v-card>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="accent"
                  flat="flat"
                  @click.native="close()"
                >
                  Cancel
                </v-btn>
                <v-btn
                  type="submit"
                  color="accent"
                  flat="flat"
                >
                  Save
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-card>
        </v-form>
      </v-dialog>
    </v-layout>
  </v-container>
</template>

<script>
import riskFieldView from './riskFieldView'

export default {
  name: 'riskViewer',
  delimiters: ['${', '}'],
  data () {
    return {
      risks: [],
      riskFields: [],
      curRiskFields: [],
      choices: [],
      loading: false,
      currentRisk: {},
      rEntryDialog: false,
      rFormValid: false
    }
  },
  components: {
    'risk-field-view': riskFieldView
  },
  created: function () {
    this.getRisks()
    this.getRFields()
    this.getChoices()
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
    getRFields: function () {
      this.loading = true
      this.$http.get('/api/riskfield/')
        .then((response) => {
          this.riskFields = response.data
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
      this.loading = false
    },
    riskRiskFields: function (risk) {
      return this.riskFields.filter(function (rf) {
        if (rf.risk.id === risk.id) {
          return rf
        }
      })
    },
    getChoices: function () {
      this.loading = true
      // var rFieldID = this.riskField.id
      this.$http.get('/api/choice/')
        .then((response) => {
          this.choices = response.data
          // .filter(function (choice) {
          //   // Set style based on data type
          //   if (choice.risk_field === rFieldID) {
          //     return choice
          //   }
          // })
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
      this.loading = false
    },
    updateRField: function (rField) {
      this.loading = true
      this.$http.put(`/api/riskfield/${rField.id}/`, rField)
        .then((response) => {
          this.loading = false
          // this.rField = response.data
          this.getRFields()
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    },
    displayRisk: function (risk) {
      // Load all risk data and display the dialog
      this.currentRisk = risk
      this.curRiskFields = this.riskRiskFields(risk)
      this.rEntryDialog = true
    },
    close: function () {
      // Clear form and close the dialog
      this.rEntryDialog = false
    },
    submit: function () {
      // Validate form, submit data, and close the dialog
      if (this.$refs.riskForm.validate()) {
        this.rEntryDialog = false
        // Get and submit data
        for (var key in this.curRiskFields) {
          this.updateRField(this.curRiskFields[key])
        }
      }
    }
  }
}
</script>
