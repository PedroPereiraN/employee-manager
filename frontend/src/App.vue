<script setup lang="ts">
import Sidebar from './components/sidebar/Sidebar.vue'
import { useRoute } from 'vue-router'

const route = useRoute

const viewsWithoutSidebar = ['login']
</script>

<template>
  <main class="flex">
    <Sidebar v-if="!viewsWithoutSidebar.includes(route.name)" />
    <RouterView class="bg-gray-200"> </RouterView>
  </main>
</template>

<style scoped></style>
