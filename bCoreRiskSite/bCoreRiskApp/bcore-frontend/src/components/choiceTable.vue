<template>
  <div v-if="dlgProps.update">
    <v-toolbar flat color="primary">
      <v-toolbar-title>Enum Choices</v-toolbar-title>
      <v-divider
        class="mx-2"
        inset
        vertical
      ></v-divider>
      <v-spacer></v-spacer>
      <v-dialog v-model="dialog" max-width="500px">
        <v-btn
          slot="activator"
          color="accent"
          dark
          class="mb-2">
            Add new choice
        </v-btn>
        <v-form
          ref="choiceCreate"
          v-model="choiceValid"
          @submit.prevent="submitChoice()"
        >
          <v-card>
            <v-card-title>
              <span class="headline">{{ formTitle }}</span>
            </v-card-title>
              <v-container grid-list-xs>
                <v-layout row wrap>
                  <v-flex>
                    <v-text-field
                      v-model="newChoice.choice_text"
                      label="Choice Text"
                      hint="Add an option for this enumerated type"
                      :rules=[rules.required]
                    >
                    </v-text-field>
                  </v-flex>
                </v-layout>
              </v-container>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="accent"
                flat
                @click.native="close()"
              >
                Cancel
              </v-btn>
              <v-btn
                type="submit"
                color="accent"
                flat
              >
                Save
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-form>
      </v-dialog>
    </v-toolbar>
    <v-data-table
      hide-headers
      :items="choices"
      hide-actions
      class="elevation-1"
    >
    <template slot="items" slot-scope="props">
      <td>{{ props.item.choice_text }}</td>
      <td class="justify-center layout px-0">
        <v-icon
          small
          class="mr-2"
          @click="editItem(props.item)"
        >
          edit
        </v-icon>
        <v-icon
          small
          @click="deleteItem(props.item)"
        >
          delete
        </v-icon>
      </td>
    </template>
    </v-data-table>
    <component
      v-bind:is="delChoiceDialog"
      @dialogYes = "dialogYes()"
      @dialogNo = "dialogNo()"
      v-bind:dlgProps="{
        title: 'Really delete ' + currentChoice.choice_text + '?',
        subtitle: 'This action cannot be undone'
      }"
    >
    </component>
  </div>
  <div v-else>
    <v-card-text>
      Create the field before adding enumerated choices.
    </v-card-text>
  </div>
</template>

<script>
import yesNoDialog from './yesNoDialog'
import Vue from 'vue'

Vue.component('yesNoDialog', {
  template: yesNoDialog
})

export default {
  name: 'choiceTable',
  props: ['dlgProps'],
  data () {
    return {
      dialog: false,
      choices: [],
      editedIndex: -1,
      choiceValid: false,
      delChoiceDialog: null,
      newChoice: {
        choice_text: '',
        risk_field: this.dlgProps.rFieldID
      },
      currentChoice: {
        choice_text: '',
        risk_field: this.dlgProps.rFieldID
      },
      rules: {
        required: value => !!value || 'Required.'
      }
    }
  },
  computed: {
    formTitle: function () {
      return this.editedIndex === -1 ? 'New choice' : 'Edit choice'
    }
  },
  watch: {
    dialog (val) {
      val || this.close()
    }
  },
  mounted: function () {
    this.getChoices()
  },
  methods: {
    getChoices: function () {
      this.loading = true
      var rFieldID = this.dlgProps.rFieldID
      this.$http.get(this.baseURL + '/api/choice/')
        .then((response) => {
          this.choices = response.data.filter(function (choice) {
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
    },
    getChoice: function (id) {
      this.loading = true
      this.$http.get(this.baseURL + `/api/choice/${id}/`)
        .then((response) => {
          this.currentChoice = response.data
          this.loading = false
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    },
    addChoice: function () {
      this.loading = true
      this.$http.post(this.baseURL + '/api/choice/', this.newChoice)
        .then((response) => {
          this.loading = false
          this.getChoices()
          this.newChoice.choice_text = ''
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    },
    updateChoice: function () {
      this.loading = true
      this.$http.put(this.baseURL + `/api/choice/${this.currentChoice.id}/`, this.currentChoice)
        .then((response) => {
          this.loading = false
          this.currentChoice = response.data
          this.getChoices()
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    },
    submitChoice: function () {
      // Validate form submission
      if (this.$refs.choiceCreate.validate()) {
        this.currentChoice = Object.assign({}, this.newChoice)
        if (this.editedIndex > -1) {
          // Update Choice
          this.updateChoice()
        } else {
          // Create new Choice
          this.addChoice()
        }
        // Clear
        this.close()
      }
    },
    deleteChoice: function (id) {
      this.loading = true
      this.$http.delete(this.baseURL + `/api/choice/${id}/`)
        .then((response) => {
          this.loading = false
          this.getChoices()
        })
        .catch((err) => {
          this.loading = false
          console.log(err)
        })
    },
    dialogOrNull: function (dialog) {
      if (dialog === 'yesNo') {
        this.delChoiceDialog = yesNoDialog
      } else {
        this.delChoiceDialog = null
        this.createChoiceDialog = null
      }
    },
    dialogYes: function () {
      this.delChoiceDialog = null
      this.deleteChoice(this.currentChoice.id)
    },
    dialogNo: function () {
      this.delChoiceDialog = null
    },
    close: function () {
      this.dialog = false
      setTimeout(() => {
        this.newChoice.choice_text = ''
        this.editedIndex = -1
      }, 300)
    },
    editItem: function (item) {
      this.editedIndex = this.choices.indexOf(item)
      this.newChoice = Object.assign({}, item)
      this.dialog = true
    },
    deleteItem: function (item) {
      this.currentChoice = item
      this.dialogOrNull('yesNo')
    }
  }
}
</script>
