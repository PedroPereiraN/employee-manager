<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import Fieldset from '@/components/ui/Fieldset.vue'
import Input from '@/components/ui/Input.vue'
import Separator from '@/components/ui/Separator.vue'
import Button from '@/components/ui/Button.vue'
import Select from '@/components/ui/Select.vue'
import type { SelectOption } from '@/components/ui/Select.vue'
import { useQuery } from '@tanstack/vue-query'
import { createUser, editUser, getUser } from '@/services/queries'
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { USERS } from '@/utils/paths'
import { UserRole } from '@/utils/enums'

export type Props = {
  id?: string
}

const router = useRouter()

const { id } = defineProps<Props>()

const { data: user } = useQuery({
  queryKey: ['users', id],
  queryFn: () => getUser(id!),
  enabled: computed(() => !!id),
})

const formState = ref<'new' | 'visualize' | 'edit'>('new')

if (id) {
  formState.value = 'visualize'
}

const roleOptions: SelectOption[] = [
  { value: UserRole.Admin, label: 'Admin' },
  { value: UserRole.Supervisor, label: 'Supervisor' },
  { value: UserRole.Member, label: 'Member' },
]

const schema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email').min(1, 'Email is required'),
  role: z.nativeEnum(UserRole, { message: 'Role is required' }),
  password: z.string().optional(),
})

const { handleSubmit, errors, defineField, setValues } = useForm({
  validationSchema: toTypedSchema(schema),
})

watch(user, (u) => {
  if (u) {
    setValues({
      name: u.name,
      email: u.email,
      role: u.role,
    })
  }
})

const onSubmit = handleSubmit(async (values) => {
  if (formState.value === 'new') {
    createUser(values)
      .then(() => {
        router.push(USERS)
      })
      .catch((error) => {
        console.error(error)
      })
  } else if (formState.value === 'edit' && id) {
    editUser({ ...values, id })
      .then(() => {
        router.push(USERS)
      })
      .catch((error) => {
        console.error(error)
      })
  }
})

const [name, nameAttrs] = defineField('name')
const [email, emailAttrs] = defineField('email')
const [role] = defineField('role')
const [password, passwordAttrs] = defineField('password')
</script>

<template>
  <div class="p-8">
    <div>
      <h1 class="text-2xl font-bold text-gray-900">
        {{ formState === 'new' ? 'Create user' : formState === 'edit' ? 'Edit user' : 'View user' }}
      </h1>
      <p class="text-sm text-gray-500 mt-1">
        {{ formState === 'new' ? 'Add a new user to your organization.' : 'Manage user details and access.' }}
      </p>
    </div>

    <form @submit.prevent="onSubmit">
      <div class="py-6 flex flex-col gap-5">
        <div class="grid grid-cols-3 gap-4">
          <Fieldset id="name" label="Name" :error="errors.name">
            <Input
              id="name"
              placeholder="e.g. John Doe"
              v-model="name"
              v-bind="nameAttrs"
              :disabled="formState === 'visualize'"
            />
          </Fieldset>
          <Fieldset id="email" label="Email" :error="errors.email">
            <Input
              id="email"
              placeholder="e.g. john@example.com"
              v-model="email"
              v-bind="emailAttrs"
              :disabled="formState === 'visualize'"
            />
          </Fieldset>
          <Fieldset id="role" label="Role" :error="errors.role">
            <Select
              v-model="role as string"
              :options="roleOptions"
              placeholder="Select role…"
              :disabled="formState === 'visualize'"
            />
          </Fieldset>
        </div>

        <Separator />

        <div>
          <h2 class="text-xl font-bold text-gray-900">Password</h2>
          <p class="text-sm text-gray-500 mt-1">
            {{ formState === 'new' ? 'Set a password for this user.' : 'Leave blank to keep the current password.' }}
          </p>
        </div>
        <div class="grid grid-cols-3 gap-4">
          <Fieldset id="password" label="Password" :error="errors.password">
            <Input
              id="password"
              type="password"
              placeholder="••••••••"
              v-model="password"
              v-bind="passwordAttrs"
              :disabled="formState === 'visualize'"
            />
          </Fieldset>
        </div>
      </div>

      <Separator />
      <div class="px-6 py-4 flex justify-end gap-2">
        <Button variant="outline" :to="USERS">Cancel</Button>
        <Button
          type="button"
          icon="lucide:pencil"
          @click="formState = 'edit'"
          v-if="formState === 'visualize'"
          >Edit user</Button
        >
        <Button type="submit" icon="lucide:plus" v-else>{{
          formState === 'new' ? 'Create user' : 'Save changes'
        }}</Button>
      </div>
    </form>
  </div>
</template>
