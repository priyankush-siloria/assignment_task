<template>
  <v-app>
    <v-main>
      <HeaderComp />
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>
import HeaderComp from './components/HeaderComp.vue';

export default {
  name: 'App',
  comments:{
    HeaderComp
  },

  data: () => ({
    //
  }),
};
</script>
