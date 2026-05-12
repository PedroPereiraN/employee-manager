<script setup lang="ts">
import Sidebar from './components/sidebar/Sidebar.vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const viewsWithoutSidebar = ['login']
</script>

<template>
  <main class="flex h-screen w-screen">
    <Sidebar v-if="!viewsWithoutSidebar.find((name: string) => name == route.name)" />
    <RouterView class="bg-gray-200 flex-1 min-w-0 overflow-auto"> </RouterView>
  </main>
</template>

<style scoped></style>
