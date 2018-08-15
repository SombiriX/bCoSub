<template>
  <div>
    <v-layout row justify-center>
      <v-dialog v-model="dialog" max-width="400">
        <v-form
          ref="rClassCreate"
          v-model="rClassValid"
          @submit.prevent="submit()"
        >
          <v-card>
            <v-container grid-list-xs>
              <v-text-field
                autofocus
                label="Risk Class"
                id="risk_class_input"
                hint="For example: Car, House, Business, pets, etc..."
                :rules=[rules.required]
                v-model="userInput"
              >
              </v-text-field>
            </v-container>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                flat="flat"
                type="submit"
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
  name: 'createRiskDialog',
  props: ['msgProps'],
  delimiters: ['${', '}'],
  data () {
    return {
      dialog: true,
      userInput: '',
      rClassValid: false,
      rules: {
        required: value => !!value || 'Required.'
      }
    }
  },
  watch: {
    dialog (val) {
      this.clear()
      this.$emit('createRiskDialogClosed')
    }
  },
  mounted: function () {
  },
  methods: {
    clear: function () {
      this.$refs.rClassCreate.reset()
    },
    emitCreated: function () {
      this.$emit('riskCreated', this.userInput)
      this.clear()
    },
    emitclosed: function () {
      this.clear()
      this.$emit('createRiskDialogClosed')
    },
    submit: function () {
      // Capture form submission
      if (this.$refs.rClassCreate.validate()) {
        this.emitCreated()
      }
    }
  }
}

</script>
