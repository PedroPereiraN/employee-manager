<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import Fieldset from '@/components/ui/Fieldset.vue'
import Input from '@/components/ui/Input.vue'
import Textarea from '@/components/ui/Textarea.vue'
import Separator from '@/components/ui/Separator.vue'
import Button from '@/components/ui/Button.vue'
import { useQuery } from '@tanstack/vue-query'
import { createPosition, editPosition, getPosition } from '@/services/queries'
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { POSITIONS } from '@/utils/paths'

export type Props = {
  id?: string
}

const router = useRouter()

const { id } = defineProps<Props>()

const { data: position } = useQuery({
  queryKey: ['positions', id],
  queryFn: () => getPosition(id!),
  enabled: computed(() => !!id),
})

const formState = ref<'new' | 'visualize' | 'edit'>('new')

if (id) {
  formState.value = 'visualize'
}

const schema = z.object({
  name: z.string().min(1, 'Name is required'),
  description: z.string().nullish(),
})

const { handleSubmit, errors, defineField, setValues } = useForm({
  validationSchema: toTypedSchema(schema),
})

watch(position, (pos) => {
  if (pos) {
    setValues({ name: pos.name, description: pos.description })
  }
})

const onSubmit = handleSubmit(async (values) => {
  if (formState.value == 'new') {
    createPosition(values)
      .then(() => {
        router.push(POSITIONS)
      })
      .catch((error) => {
        console.error(error)
      })
  } else if (formState.value == 'edit' && id) {
    editPosition({ ...values, id })
      .then(() => {
        router.push(POSITIONS)
      })
      .catch((error) => {
        console.error(error)
      })
  }
})

const [name, nameAttrs] = defineField('name')
const [description, descriptionAttrs] = defineField('description')
</script>

<template>
  <div class="p-8">
    <div>
      <h1 class="text-2xl font-bold text-gray-900">Create position</h1>
      <p class="text-sm text-gray-500 mt-1">Add a new job position to your organization.</p>
    </div>

    <form @submit.prevent="onSubmit">
      <div class="py-6 flex flex-col gap-5">
        <div class="grid grid-cols-3 gap-4">
          <Fieldset id="name" label="Name" :error="errors.name">
            <Input
              id="name"
              placeholder="e.g. Senior Software Engineer"
              v-model="name"
              v-bind="nameAttrs"
              :disabled="formState == 'visualize'"
            />
          </Fieldset>
        </div>

        <Separator />

        <div>
          <h2 class="text-xl font-bold text-gray-900">Description</h2>
          <p class="text-sm text-gray-500 mt-1">
            Inform here all the necessary description about this position.
          </p>
        </div>
        <Textarea
          v-model="description"
          v-bind="descriptionAttrs"
          :disabled="formState == 'visualize'"
        />
      </div>
      <Separator />
      <div class="px-6 py-4 flex justify-end gap-2">
        <Button variant="outline" :to="POSITIONS">Cancel</Button>
        <Button
          type="button"
          icon="lucide:plus"
          @click="formState = 'edit'"
          v-if="formState == 'visualize'"
          >Edit position</Button
        >
        <Button type="submit" icon="lucide:plus" v-else>{{
          formState == 'new' ? 'Create position' : 'Edit position'
        }}</Button>
      </div>
    </form>
  </div>
</template>
