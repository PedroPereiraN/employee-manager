<script setup lang="ts">
import Fieldset from '@/components/ui/Fieldset.vue'
import Input from '@/components/ui/Input.vue'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'

const schema = z.object({
  email: z.email(),
  password: z.string(),
})

const { handleSubmit, errors, defineField } = useForm({
  validationSchema: toTypedSchema(schema),
})

const [email, emailAttrs] = defineField('email')
const [password, passwordAttrs] = defineField('password')

const onSubmit = handleSubmit((values) => {
  console.log(values)
})
</script>

<template>
  <main class="flex h-screen w-screen overflow-hidden">
    <!-- Left branding panel -->
    <section
      class="hidden lg:flex w-3/5 relative bg-gradient-to-br from-blue-700 via-blue-600 to-indigo-700 flex-col justify-between p-12 text-white overflow-hidden"
    >
      <!-- Decorative circles -->
      <div class="absolute -top-24 -left-24 w-96 h-96 rounded-full bg-white/5"></div>
      <div class="absolute top-1/3 -right-16 w-64 h-64 rounded-full bg-white/5"></div>
      <div class="absolute -bottom-20 left-1/4 w-80 h-80 rounded-full bg-white/5"></div>

      <!-- Logo -->
      <div class="relative z-10 flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-white/20 flex items-center justify-center">
          <svg
            class="w-5 h-5 text-white"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0"
            />
          </svg>
        </div>
        <span class="text-lg font-semibold tracking-wide">Employee Manager</span>
      </div>

      <!-- Center content -->
      <div class="relative z-10 space-y-6">
        <h1 class="text-4xl font-bold leading-tight">Manage your team<br />with confidence.</h1>
        <p class="text-blue-100 text-lg leading-relaxed max-w-sm">
          A single platform to track employees, service orders, and team performance — all in one
          place.
        </p>
        <div class="flex items-center gap-4 pt-2">
          <div
            v-for="i in 3"
            :key="i"
            class="flex items-center gap-2 bg-white/10 rounded-full px-4 py-2 text-sm"
          >
            <svg class="w-4 h-4 text-blue-200" fill="currentColor" viewBox="0 0 20 20">
              <path
                fill-rule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clip-rule="evenodd"
              />
            </svg>
            <span>{{ ['Easy to use', 'Secure', 'Fast'][i - 1] }}</span>
          </div>
        </div>
      </div>

      <!-- Footer note -->
      <p class="relative z-10 text-blue-200 text-sm">
        © 2026 Employee Manager. All rights reserved.
      </p>
    </section>

    <!-- Right login panel -->
    <section class="flex-1 flex justify-center items-center bg-gray-50 px-6">
      <div class="w-full max-w-sm space-y-8">
        <!-- Header -->
        <div class="space-y-1">
          <h2 class="text-2xl font-bold text-gray-900">Welcome back</h2>
          <p class="text-sm text-gray-500">Sign in to your account to continue</p>
        </div>

        <!-- Form -->
        <form @submit="onSubmit">
          <Fieldset id="email" label="Email" :error="errors.email">
            <Input
              id="email"
              type="email"
              placeholder="you@example.com"
              v-model="email"
              v-bind="emailAttrs"
            />
          </Fieldset>

          <Fieldset id="password" label="Password" :error="errors.password" class="mt-3">
            <Input
              id="password"
              type="password"
              placeholder="••••••••"
              name="password"
              v-model="password"
              v-bind="passwordAttrs"
            />
          </Fieldset>

          <button
            type="submit"
            class="mt-3 w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white text-sm font-semibold rounded-lg transition-colors duration-200 focus:outline-none focus:ring-3 focus:ring-blue-300 cursor-pointer"
          >
            Sign in
          </button>
        </form>
      </div>
    </section>
  </main>
</template>
