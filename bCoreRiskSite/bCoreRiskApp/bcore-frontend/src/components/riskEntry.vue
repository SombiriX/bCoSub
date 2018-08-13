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
          <v-btn flat icon color="accent" slot="activator">
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
          @click.native.stop="dialog = true">
          <v-icon dark>add</v-icon>
        </v-btn>
        <span>New Risk Class</span>
      </v-tooltip>
    </v-layout>
    <v-layout row justify-center>
      <v-dialog v-model="dialog" max-width="400">
        <v-card>
          <v-container grid-list-xs>
            <v-text-field
              name="rClassCreate"
              label="Risk Class"
              id="risk_class_input"
              hint="For example: Car, House, Business, pets, etc..."
              :rules=[rules.required]
              v-model="newRiskClass.risk_class"
              @keydown.enter="dialog = false, addRisk()"
            >
            </v-text-field>
          </v-container>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              flat="flat"
              @click.native="dialog = false, addRisk()"
            >
              Create
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>
  </v-container>
</template>

<script>
import riskField from './riskField'
import Vue from 'vue'

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
      dialog: false,
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
    }
  }
}

</script>
