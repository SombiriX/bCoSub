<template>
  <div>
    <v-layout row justify-center>
      <v-dialog v-model="dialog" max-width="400">
        <v-form
          ref="rClassCreate"
          v-model="rFieldValid"
          @submit.prevent="submit()"
        >
          <v-card>
            <v-container grid-list-xs>
              <v-text-field
                autofocus
                label="Field Name"
                hint="For example: Height, color, weight, date, etc..."
                :rules=[rules.required]
                v-model="newRField.field_name"
              >
              </v-text-field>
              <v-spacer></v-spacer>
              <v-radio-group
                v-model="newRField.field_type"
                label="Field Type"
                :mandatory="true"
              >
                <v-radio label="Text" value="T"></v-radio>
                <v-radio label="Number" value="N"></v-radio>
                <v-radio label="Date" value="D"></v-radio>
                <v-radio label="Enum" value="E"></v-radio>
              </v-radio-group>
              <!-- Only display the choice table for enum types -->
              <choiceTable
                v-if="newRField.field_type === 'E'"
                v-bind:dlgProps="{
                  rFieldID: dlgProps.updateField.id,
                  update: update
                }"
              >
              </choiceTable>
            </v-container>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="accent"
                flat="flat"
                type="submit"
              >
                {{ update ? 'Update' : 'Create' }}
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-form>
      </v-dialog>
    </v-layout>
  </div>
</template>

<script>
import choiceTable from './choiceTable'

export default {
  name: 'createRFieldDialog',
  components: {
    'choiceTable': choiceTable
  },
  props: ['dlgProps'],
  delimiters: ['${', '}'],
  data () {
    return {
      dialog: true,
      userInput: '',
      rFieldValid: false,
      update: false,
      newRField: { 'field_name': null, 'field_type': 'T', 'risk_id': null },
      rules: {
        required: value => !!value || 'Required.'
      }
    }
  },
  watch: {
    dialog (val) {
      this.clear()
      this.$emit('createRFieldDialogClosed')
    }
  },
  mounted: function () {
    if (this.isUpdate()) {
      this.newRField = this.dlgProps.updateField
      this.update = true
    }
  },
  methods: {
    isUpdate: function () {
      // Check if we're updating or creating
      var updateField = this.dlgProps.updateField
      var objHasNoKeys = (Object.keys(updateField).length === 0)
      var objIsNotObj = !(updateField.constructor === Object)

      var numUndefined = Object.keys(updateField)
        .filter(field => !updateField[field]).length

      return !(objHasNoKeys || objIsNotObj || (numUndefined > 0))
    },
    clear: function () {
      // Clears all form inputs
      this.$refs.rClassCreate.reset()
    },
    emitCreated: function () {
      // Emits event for form creation
      // Along with the user's input data
      this.newRField.risk_id = this.dlgProps.risk_id
      this.$emit('riskFieldCreated', this.newRField)
      this.clear()
    },
    emitUpdated: function () {
      // Emits event for field update
      // Along with the user's input data
      this.newRField.risk_id = this.dlgProps.risk_id
      this.$emit('riskFieldUpdated', this.newRField)
      this.clear()
    },
    emitclosed: function () {
      // Emits event for form closure
      this.clear()
      this.$emit('createRFieldDialogClosed')
    },
    submit: function () {
      // Capture form submission
      if (this.$refs.rClassCreate.validate()) {
        if (this.update) {
          this.emitUpdated()
        } else {
          this.emitCreated()
        }
      }
    }
  }
}

</script>
