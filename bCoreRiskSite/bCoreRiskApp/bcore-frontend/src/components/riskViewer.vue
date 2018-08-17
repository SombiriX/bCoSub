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
                  <v-container>
                    <v-layout row wrap justify-center>
                      <v-flex xs10>
                        <v-textarea
                          v-if="curRiskFields[i].field_type === 'T'"
                          :label="curRiskFields[i].field_name"
                          :rules="[rules.required, rules.textareaLen]"
                          hint="Text"
                          box
                          auto-grow
                          counter=1000
                          v-model="curRiskFields[i].field"
                        >
                        </v-textarea>
                        <v-text-field
                          v-if="curRiskFields[i].field_type === 'N'"
                          :label="curRiskFields[i].field_name"
                          :rules="[rules.required]"
                          hint="Number"
                          type='number'
                          counter=10
                          v-model="curRiskFields[i].field"
                        >
                        </v-text-field>
                        <v-menu
                          v-if="curRiskFields[i].field_type === 'D'"
                          ref="dateMenu"
                          :close-on-content-click="false"
                          v-model="dateMenu"
                          :nudge-right="40"
                          :return-value.sync="curRiskFields[i].field"
                          lazy
                          transition="scale-transition"
                          offset-y
                          full-width
                          min-width="290px"
                        >
                          <v-text-field
                            slot="activator"
                            v-model="curRiskFields[i].field"
                            :label="curRiskFields[i].field_name"
                            prepend-icon="event"
                            readonly
                            :rules="[rules.selectOne]"
                          >
                          </v-text-field>
                          <v-date-picker
                            v-model="curRiskFields[i].field"
                            @input="saveDate(i)"
                          >
                          </v-date-picker>

                        </v-menu>
                        <v-select
                          v-if="enumCheck(curRiskFields[i].field_type)"
                          :items="fieldChoices(curRiskFields[i].id)"
                          item-text="choice_text"
                          item-value="id"
                          :label="curRiskFields[i].field_name"
                          hint="Make a choice"
                          v-model="curRiskFields[i].field"
                          :rules="[rules.selectOne]"
                        >
                        </v-select>
                        <v-card
                          v-if="errorCheck(curRiskFields[i].field_type)"
                          color="error"
                        >
                          <v-card-title primary-title>
                            This field is not properly configured
                          </v-card-title>
                        </v-card>
                      </v-flex>
                    </v-layout>
                  </v-container>
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
      dateMenu: false,
      rEntryDialog: false,
      rFormValid: false,
      rules: {
        required: v => !!v || 'Field required',
        textareaLen: v => (v && (v.length <= 1000)) || 'Maximum Length',
        selectOne: v => !(v === '') || 'A selection is required'
      }
    }
  },
  created: function () {
    this.getRisks()
    this.getRFields()
    this.getChoices()
  },
  computed: {
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
    getCurRiskFields: function () {
      return this.riskRiskFields(this.currentRisk)
    },
    getChoices: function () {
      this.loading = true
      // var rFieldID = this.riskField.id
      this.$http.get('/api/choice/')
        .then((response) => {
          this.choices = response.data
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
      this.curRiskFields = this.getCurRiskFields()
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
    },
    fieldChoices: function (rFieldID) {
      // Filter choices by ID then return a reformatted
      // choice array
      // let rFieldID = this.riskField.id
      return this.choices.filter(function (choice) {
        if (choice.risk_field === rFieldID) {
          return choice
        }
      })
        .map(function (choice) {
          return {
            id: choice.id,
            choice_text: choice.choice_text
          }
        })
    },
    enumCheck: function (fieldType) {
      return (fieldType === 'E') && (this.fieldChoices.length > 0)
    },
    errorCheck: function (fieldType) {
      return (fieldType === 'E') && !(this.enumCheck)
    },
    saveDate: function (i) {
      this.$refs.dateMenu[i].save(this.curRiskFields[i].field)
    }
  }
}
</script>
