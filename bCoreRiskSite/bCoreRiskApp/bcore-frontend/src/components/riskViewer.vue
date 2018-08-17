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
                  v-for="(rf, i) in riskFields"
                  :key="i"
                >
                  <risk-field-view
                    v-bind:riskField="rf"
                    v-model="rf.field"
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
      choices: [],
      loading: false,
      currentRisk: {},
      rEntryDialog: false,
      snackBarDisplay: null,
      snackBarTimeout: null,
      rFormValid: false,
      rules: {
        required: value => !!value || 'Required.'
      }
    }
  },
  components: {
    'risk-field-view': riskFieldView
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
    getRFields: function () {
      this.loading = true
      var riskID = this.currentRisk.id
      this.$http.get('/api/riskfield/')
        .then((response) => {
          this.riskFields = response.data.filter(function (rf) {
            // Set style based on data type
            if (rf.risk.id === riskID) {
              // rf.data = ''
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
    updateRField: function (rfield) {
      this.loading = true
      this.$http.put(`/api/riskfield/${rfield.id}/`, rfield)
        .then((response) => {
          this.loading = false
          // this.rfield = response.data
          this.getRFields()
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    },
    clear: function () {
      // Clears all form inputs
      this.$refs.riskForm.reset()
    },
    displayRisk: function (risk) {
      // Load all risk data and display the dialog
      this.currentRisk = risk
      this.getRFields()
      this.rEntryDialog = true
    },
    close: function () {
      // Clear form and close the dialog
      console.log(this.riskFields)
      this.clear()
      this.rEntryDialog = false
    },
    submit: function () {
      // Validate form, submit data, and close the dialog
      if (this.$refs.riskForm.validate()) {
        this.rEntryDialog = false
        // Get and submit data
        for (var key in this.riskFields) {
          this.updateRField(this.riskFields[key])
        }
      }
    }
  }
}
</script>
