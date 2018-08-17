<template>
  <v-container>
    <v-layout row wrap justify-center>
      <v-flex xs10>
        <v-textarea
          v-if="fieldType === 'T'"
          :label="riskField.field_name"
          :rules="[rules.required, rules.textareaLen]"
          hint="Text"
          box
          auto-grow
          counter=1000
          v-model="input.txt"
          @input="emitInput('txt')"
        >
        </v-textarea>
        <v-text-field
          v-if="fieldType === 'N'"
          :label="riskField.field_name"
          :rules="[rules.required]"
          hint="Number"
          type='number'
          counter=10
          v-model="input.num"
          @input="emitInput('num')"
        >
        </v-text-field>
        <v-menu
          v-if="fieldType === 'D'"
          ref="dateMenu"
          :close-on-content-click="false"
          v-model="dateMenu"
          :nudge-right="40"
          :return-value.sync="input.dat"
          lazy
          transition="scale-transition"
          offset-y
          full-width
          min-width="290px"
        >
          <v-text-field
            slot="activator"
            v-model="input.dat"
            :label="riskField.field_name"
            prepend-icon="event"
            readonly
            :rules="[rules.selectOne]"
          >
          </v-text-field>
          <v-date-picker
            v-model="input.dat"
            @input="
              $refs.dateMenu.save(input.dat),
              emitInput('dat')"
          >
          </v-date-picker>

        </v-menu>
        <v-select
          v-if="enumCheck"
          :items="fieldChoices"
          item-text="choice_text"
          item-value="id"
          :label="riskField.field_name"
          hint="Make a choice"
          v-model="input.enm"
          @input="emitInput('enm')"
          :rules="[rules.selectOne]"
        >
        </v-select>
        <v-card
          v-if="errorCheck"
          color="error"
        >
          <v-card-title primary-title>
            This field is not properly configured
          </v-card-title>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'riskFieldView',
  props: ['riskField', 'choices', 'value'],
  data () {
    return {
      rules: {
        required: v => !!v || 'Field required',
        textareaLen: v => (v && (v.length <= 1000)) || 'Maximum Length',
        selectOne: v => !(v === '') || 'A selection is required'
      },
      dateMenu: false,
      input: {
        txt: this.value,
        num: this.value,
        dat: this.value,
        enm: this.value
      }
    }
  },
  created: function () {
  },
  methods: {
    emitInput: function (fType) {
      switch (fType) {
        case 'txt':
          this.$emit('input', this.input.txt)
          break
        case 'num':
          this.$emit('input', this.input.num)
          break
        case 'dat':
          this.$emit('input', this.input.dat)
          break
        case 'enm':
          this.$emit('input', this.input.enm)
          break
        default:
          console.log('Error in form entry')
      }
    }
  },
  computed: {
    fieldType: function () {
      return this.riskField.field_type
    },
    fieldChoices: function () {
      // Filter choices by ID then return a reformatted
      // choice array
      var rFieldID = this.riskField.id
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
    enumCheck: function () {
      return (this.fieldType === 'E') && (this.fieldChoices.length > 0)
    },
    errorCheck: function () {
      return (this.fieldType === 'E') && !(this.enumCheck)
    }
  }
}
</script>
