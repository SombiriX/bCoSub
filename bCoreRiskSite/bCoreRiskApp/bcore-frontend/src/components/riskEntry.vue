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
            @click.native.stop="dialogOrNull(true), currentRisk=risk"
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
          @click.native.stop="addRiskDialog = true">
          <v-icon dark>add</v-icon>
        </v-btn>
        <span>New Risk Class</span>
      </v-tooltip>
    </v-layout>
<!-- User Action Dialogs -->
    <v-layout row justify-center>
      <v-dialog v-model="addRiskDialog" max-width="400">
        <v-form
          ref="rClassCreate"
          v-model="rClassValid"
          lazy-validation
        >
          <v-card>
            <v-container grid-list-xs>
              <v-text-field
                autofocus
                label="Risk Class"
                id="risk_class_input"
                hint="For example: Car, House, Business, pets, etc..."
                :rules=[rules.required]
                v-model="newRiskClass.risk_class"
              >
              </v-text-field>
            </v-container>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                flat="flat"
                @click.native="addRiskDialog = false, addRisk(), clear()"
                :disabled="!rClassValid"
              >
                Create
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-form>
      </v-dialog>
    </v-layout>
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
import Vue from 'vue'

Vue.component('yesNoDialog', {
  template: yesNoDialog
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
      addRiskDialog: false,
      delRiskDialog: null,
      rClassValid: true,
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
      this.$http.post('/api/risk/', this.newRiskClass, {
        headers: {
          'X-CSRFToken': Vue.cookie.get('csrftoken')
        }
      })
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
    clear: function () {
      this.$refs.rClassCreate.reset()
    },
    dialogOrNull: function (dialog) {
      if (dialog) {
        this.delRiskDialog = yesNoDialog
      } else {
        this.delRiskDialog = null
      }
    },
    dialogYes: function () {
      this.delRiskDialog = null
      this.deleteRisk(this.currentRisk.id)
    },
    dialogNo: function () {
      this.delRiskDialog = null
    }
  }
}

</script>
