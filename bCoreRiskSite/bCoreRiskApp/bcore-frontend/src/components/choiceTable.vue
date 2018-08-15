<template>
  <div>
    <v-toolbar flat color="primary">
      <v-toolbar-title>Enum Choices</v-toolbar-title>
      <v-divider
        class="mx-2"
        inset
        vertical
      ></v-divider>
      <v-spacer></v-spacer>
      <v-dialog v-model="dialog" max-width="500px">
        <v-btn slot="activator" color="accent" dark class="mb-2">Add new choice</v-btn>
        <v-card>
          <v-card-title>
            <span class="headline">{{ formTitle }}</span>
          </v-card-title>
            <v-container grid-list-xs>
              <v-layout row wrap>
                <v-flex>
                  <v-text-field v-model="newChoice.choice_text" label="Choice Text"></v-text-field>
                </v-flex>
              </v-layout>
            </v-container>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="accent" flat @click.native="close()">Cancel</v-btn>
            <v-btn color="accent" flat @click.native="save()">Save</v-btn>
          </v-card-actions>
        </v-card>
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
  </div>
</template>

<script>
export default {
  name: 'choiceTable',
  props: ['rFieldID'],
  data () {
    return {
      dialog: false,
      choices: [],
      editedIndex: -1,
      newChoice: {
        choice_text: '',
        risk_field: ''
      }
    }
  },
  computed: {
    formTitle () {
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
      var rFieldID = this.rFieldID
      this.$http.get('/api/choice/')
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
      this.$http.get(`/api/choice/${id}/`)
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
      this.$http.post('/api/choice/', this.newChoice)
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
      this.$http.put(`/api/choice/${this.currentChoice.id}/`, this.currentChoice)
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
    submitChoice: function (i) {
      // Capture form submission
      if (this.$refs.rClass[i].validate()) {
        this.currentChoice = this.choices[i]
        this.updateChoice()
      }
    },
    deleteChoice: function (id) {
      this.loading = true
      this.$http.delete(`/api/choice/${id}/`)
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
      } else if (dialog === 'createChoice') {
        this.createChoiceDialog = createChoiceDialog
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
    createChoiceDialogClosed: function () {
      this.createChoiceDialog = null
    },
    dialogCreateChoice: function (userInput) {
      this.createChoiceDialog = null
      this.newChoice.choice_text = userInput
      this.addChoice()
    },
    close: function () {
      this.dialog = false
      setTimeout(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      }, 300)
    },
    save: function () {
      if (this.editedIndex > -1) {
        Object.assign(this.choices[this.editedIndex], this.editedItem)
      } else {
        this.choices.push(this.editedItem)
      }
      this.close()
    },
    editItem: function (item) {
      this.editedIndex = this.choices.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },

    deleteItem: function (item) {
      const index = this.choices.indexOf(item)
      confirm('Are you sure you want to delete this item?') && this.choices.splice(index, 1)
    }
  }
}
</script>
