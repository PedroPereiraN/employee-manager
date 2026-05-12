<script setup lang="ts">
const model = defineModel()
</script>

<template>
  <input
    class="w-full px-4 py-2.5 rounded-lg border bg-gray-50 text-gray-900 text-sm placeholder:text-gray-400 transition-all duration-200 focus:outline-none focus:bg-white focus:ring-3"
    v-model="model"
  />
</template>
