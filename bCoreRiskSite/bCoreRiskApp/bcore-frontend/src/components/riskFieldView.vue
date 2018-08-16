<template>
  <v-container>
    <v-layout row wrap justify-center>
      <v-flex xs10>
        <v-textarea
          v-if="fieldType === 'T'"
          :label="riskField.field_name"
          :rules=[rules.required]
          hint="Text"
          box
          auto-grow
          counter=1000
        >
        </v-textarea>
        <v-text-field
          v-else-if="fieldType === 'N'"
          :label="riskField.field_name"
          mask="################"
          :rules="[rules.required, rules.textareaLen]"
          hint="Number"
          counter=16
        >
        </v-text-field>
        <v-menu
          v-else-if="fieldType === 'D'"
          ref="dateMenu"
          :close-on-content-click="false"
          v-model="dateMenu"
          :nudge-right="40"
          :return-value.sync="date"
          lazy
          transition="scale-transition"
          offset-y
          full-width
          min-width="290px"
        >
          <v-text-field
            slot="activator"
            v-model="date"
            :label="riskField.field_name"
            prepend-icon="event"
            readonly
          ></v-text-field>
          <v-date-picker
            v-model="date"
            @input="$refs.dateMenu.save(date)"
          ></v-date-picker>

        </v-menu>
        <v-select
          v-else-if="fieldType === 'E'"
          :items="choices"
          item-text="choice_text"
          item-value="id"
          :label="riskField.field_name"
          hint="Make a choice"
        ></v-select>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
export default {
  name: 'riskFieldView',
  props: ['riskField'],
  data () {
    return {
      choicesArr: [],
      rules: {
        required: v => !!v || 'Field required',
        textareaLen: v => v.length <= 1000 || 'Maximum Length'
      },
      date: null,
      dateMenu: false,
      loading: false
    }
  },
  mounted: function () {
    this.getChoices()
  },
  methods: {
    getChoices: function () {
      this.loading = true
      var rFieldID = this.riskField.id
      this.$http.get('/api/choice/')
        .then((response) => {
          this.choicesArr = response.data.filter(function (choice) {
            // Set style based on data type
            if (choice.risk_field === rFieldID) {
              return choice
            }
          })
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
      this.loading = false
    }
  },
  computed: {
    fieldType: function () {
      return this.riskField.field_type
    },
    choices: function () {
      var choiceList = []
      for (var choice in this.choicesArr) {
        choiceList.push({
          id: this.choicesArr[choice].id,
          choice_text: this.choicesArr[choice].choice_text
        })
      }
      return choiceList
    }
  }
}
</script>
