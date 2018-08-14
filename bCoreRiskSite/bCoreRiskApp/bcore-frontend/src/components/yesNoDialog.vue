<template>
  <div>
    <v-layout row justify-center>
      <v-dialog v-model="dialog" max-width="400">
        <v-card>
          <v-container grid-list-xs>
            <v-card-title class="headline">
              {{ msgProps.title }}
            </v-card-title>
            <v-card-text>{{ msgProps.subtitle }}</v-card-text>
          </v-container>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              color="success"
              flat="flat"
              @click.native="dialog = false, emitNo()"
            >
                NO
            </v-btn>
            <v-btn
              color="error"
              flat="flat"
              @click.native="dialog = false, emitYes()"
            >
                YES
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-layout>
  </div>
</template>

<script>
export default {
  name: 'yesNoDialog',
  props: ['msgProps'],
  delimiters: ['${', '}'],
  data () {
    return {
      risk_fields: [],
      loading: false,
      dialog: true,
      rules: {
        required: value => !!value || 'Required.'
      }
    }
  },
  watch: {
    dialog (val) {
      this.$emit('dialogNo')
    }
  },
  mounted: function () {
  },
  methods: {
    emitYes: function () {
      this.$emit('dialogYes')
    },
    emitNo: function () {
      this.$emit('dialogNo')
    }
  }
}

</script>
