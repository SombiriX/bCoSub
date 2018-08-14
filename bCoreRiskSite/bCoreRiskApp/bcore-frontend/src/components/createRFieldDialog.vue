<template>
  <div>
    <v-layout row justify-center>
      <v-dialog v-model="dialog" max-width="400">
        <v-form
          ref="rClassCreate"
          v-model="rFieldValid"
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
            </v-container>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                flat="flat"
                @click.native="emitCreated()"
                :disabled="!rFieldValid"
              >
                Create
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-form>
      </v-dialog>
    </v-layout>
  </div>
</template>

<script>
export default {
  name: 'createRFieldDialog',
  props: ['dlgProps'],
  delimiters: ['${', '}'],
  data () {
    return {
      dialog: true,
      userInput: '',
      rFieldValid: false,
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
  },
  methods: {
    clear: function () {
      this.$refs.rClassCreate.reset()
    },
    emitCreated: function () {
      this.newRField.risk_id = this.dlgProps.risk_id
      this.$emit('riskFieldCreated', this.newRField)
      this.clear()
    },
    emitclosed: function () {
      this.clear()
      this.$emit('createRFieldDialogClosed')
    }
  }
}

</script>
