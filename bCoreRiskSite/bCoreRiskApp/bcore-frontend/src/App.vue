<template>
  <v-app dark>
    <v-toolbar color="primary">
      <v-toolbar-items>
        <v-btn small color="secondary">Manage Risks</v-btn>
      </v-toolbar-items>
    </v-toolbar>
    <v-btn color="primary" dark>Add Risk</v-btn>
    <v-content>
      <router-view/>
    </v-content>
  </v-app>
</template>

<script>
export default {

}
</script>
