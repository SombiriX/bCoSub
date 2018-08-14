<template>
  <div>
    <v-chip
      close
      v-for="(risk_field, i) in risk_fields"
      :key="risk_field.id"
      v-model="risk_fields[i].displayed"
      @input="
        currentRField=risk_fields[i],
        dialogOrNull('yesNo'),
        risk_fields[i].displayed=true"
      @click.native="
        currentRField=risk_fields[i],
        dialogOrNull('createRField')"
    >
      <v-avatar
        :color="risk_field.f_color"
      >
        {{ risk_field.field_type }}
      </v-avatar>
      {{ risk_field.field_name }}
    </v-chip>
    <v-tooltip bottom>
      <v-btn
        flat
        icon
        color="accent"
        slot="activator"
        @click.native.stop="
          dialogOrNull('createRField')"
      >
        <v-icon dark>add_circle_outline</v-icon>
      </v-btn>
      <span>Add new field</span>
    </v-tooltip>
<!-- User Action Dialogs -->
    <component
      v-bind:is="createRFieldDialog"
      @riskFieldCreated = "dialogCreateRField"
      @createRFieldDialogClosed = "createRFieldDialogClosed()"
      v-bind:dlgProps="{
        risk_id: risk_id,
        updateField: currentRField
      }"
    >
    </component>
    <component
      v-bind:is="delRFieldDialog"
      @dialogYes = "dialogYes()"
      @dialogNo = "dialogNo()"
      v-bind:dlgProps="{
        title: 'Really delete ' + currentRField.field_name + '?',
        subtitle: 'This action cannot be undone'
      }"
    >
    </component>
  </div>
</template>

<script>
import yesNoDialog from './yesNoDialog'
import createRFieldDialog from './createRFieldDialog'
import Vue from 'vue'

Vue.component('yesNoDialog', {
  template: yesNoDialog
})

Vue.component('createRFieldDialog', {
  template: createRFieldDialog
})

export default {
  name: 'riskField',
  props: ['risk_id'],
  delimiters: ['${', '}'],
  data () {
    return {
      risk_fields: [],
      loading: false,
      currentRField: {},
      message: null,
      createRFieldDialog: null,
      delRFieldDialog: null,
      rFieldValid: true,
      newRField: {},
      rules: {
        required: value => !!value || 'Required.'
      }
    }
  },
  mounted: function () {
    this.getRFields()
  },
  methods: {
    getRFields: function () {
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
    getRField: function (id) {
      this.loading = true
      this.$http.get(`/api/riskfield/${id}/`)
        .then((response) => {
          this.currentRField = response.data
          this.loading = false
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    },
    addRField: function () {
      this.loading = true
      this.$http.post('/api/riskfield/', this.newRField)
        .then((response) => {
          this.loading = false
          this.getRFields()
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    },
    updateRField: function () {
      this.loading = true
      this.$http.put(`/api/riskfield/${this.currentRField.risk_id}/`, this.currentRField)
        .then((response) => {
          this.loading = false
          this.currentRField = response.data
          this.getRFields()
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    },
    deleteRField: function (id) {
      this.loading = true
      this.$http.delete(`/api/riskfield/${id}/`)
        .then((response) => {
          this.loading = false
          this.getRFields()
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    },
    dialogOrNull: function (dialog) {
      if (dialog === 'yesNo') {
        this.delRFieldDialog = yesNoDialog
      } else if (dialog === 'createRField') {
        this.createRFieldDialog = createRFieldDialog
      } else {
        this.delRFieldDialog = null
        this.createRFieldDialog = null
      }
    },
    dialogYes: function () {
      this.delRFieldDialog = null
      this.deleteRField(this.currentRField.id)
    },
    dialogNo: function () {
      this.delRFieldDialog = null
    },
    createRFieldDialogClosed: function () {
      this.createRFieldDialog = null
    },
    dialogCreateRField: function (newRField) {
      this.createRFieldDialog = null
      this.newRField = newRField
      this.addRField()
    }
  }
}

</script>
