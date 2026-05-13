<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import Fieldset from '@/components/ui/Fieldset.vue'
import Input from '@/components/ui/Input.vue'
import Textarea from '@/components/ui/Textarea.vue'
import Separator from '@/components/ui/Separator.vue'
import Button from '@/components/ui/Button.vue'

const schema = z.object({
  name: z.string().min(1, 'Name is required'),
  description: z.string().optional(),
})

const { handleSubmit, errors, defineField } = useForm({
  validationSchema: toTypedSchema(schema),
})

const onSubmit = handleSubmit(async (values) => {
  console.log(values)
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
        <Textarea v-model="description" v-bind="descriptionAttrs" />
      </div>
      <Separator />
      <div class="px-6 py-4 flex justify-end gap-2">
        <Button variant="outline" to="/positions">Cancel</Button>
        <Button type="submit" icon="lucide:plus">Create position</Button>
      </div>
    </form>
  </div>
</template>
