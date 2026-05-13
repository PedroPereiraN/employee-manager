<script setup lang="ts">
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import Fieldset from '@/components/ui/Fieldset.vue'
import Input from '@/components/ui/Input.vue'
import Textarea from '@/components/ui/Textarea.vue'
import Separator from '@/components/ui/Separator.vue'
import Button from '@/components/ui/Button.vue'
import Select from '@/components/ui/Select.vue'
import type { SelectOption } from '@/components/ui/Select.vue'
import { useQuery } from '@tanstack/vue-query'
import { createEmployee, editEmployee, getEmployee, getPositions } from '@/services/queries'
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { EMPLOYEES } from '@/utils/paths'
import { EmployeeStatus, EmployeeType, PaymentMethod } from '@/utils/enums'

export type Props = {
  id?: string
}

const router = useRouter()

const { id } = defineProps<Props>()

const { data: employee } = useQuery({
  queryKey: ['employees', id],
  queryFn: () => getEmployee(id!),
  enabled: computed(() => !!id),
})

const { data: positionsData } = useQuery({
  queryKey: ['positions', { page: 1, size: 50 }],
  queryFn: () => getPositions({ page: 1, size: 50 }),
})

const positionOptions = computed<SelectOption[]>(
  () => positionsData.value?.items.map((p) => ({ value: p.id, label: p.name })) ?? [],
)

const statusOptions: SelectOption[] = [
  { value: EmployeeStatus.Active, label: 'Active' },
  { value: EmployeeStatus.Inactive, label: 'Inactive' },
  { value: EmployeeStatus.OnVacation, label: 'On Vacation' },
  { value: EmployeeStatus.SickLeave, label: 'Sick Leave' },
]

const typeOptions: SelectOption[] = [
  { value: EmployeeType.Independent, label: 'Independent' },
  { value: EmployeeType.Employee, label: 'Employee' },
]

const paymentMethodOptions: SelectOption[] = [
  { value: PaymentMethod.Monthly, label: 'Monthly' },
  { value: PaymentMethod.Weekly, label: 'Weekly' },
  { value: PaymentMethod.Daily, label: 'Daily' },
]

const formState = ref<'new' | 'visualize' | 'edit'>('new')

if (id) {
  formState.value = 'visualize'
}

const nullableNumber = z.preprocess(
  (v) => (v === '' || v === undefined || v === null ? null : Number(v)),
  z.number().nullable(),
)

const schema = z.object({
  name: z.string().min(1, 'Name is required'),
  birthday: z.string().nullish(),
  phone: z.string().nullish(),
  email: z.string().nullish(),
  admission_date: z.string().nullish(),
  status: z.nativeEnum(EmployeeStatus, { message: 'Status is required' }),
  type: z.nativeEnum(EmployeeType, { message: 'Type is required' }),
  payment_method: z.nativeEnum(PaymentMethod, { message: 'Payment method is required' }),
  payment_value: z.coerce.number({ invalid_type_error: 'Must be a number' }).min(0),
  hourly_rate: nullableNumber,
  hourly_bonus: nullableNumber,
  observations: z.string().nullish(),
  position_id: z.string().min(1, 'Position is required'),
})

const { handleSubmit, errors, defineField, setValues } = useForm({
  validationSchema: toTypedSchema(schema),
})

watch(employee, (emp) => {
  if (emp) {
    setValues({
      name: emp.name,
      birthday: emp.birthday ?? undefined,
      phone: emp.phone ?? undefined,
      email: emp.email ?? undefined,
      admission_date: emp.admission_date ?? undefined,
      status: emp.status,
      type: emp.type,
      payment_method: emp.payment_method,
      payment_value: emp.payment_value,
      hourly_rate: emp.hourly_rate ?? undefined,
      hourly_bonus: emp.hourly_bonus ?? undefined,
      observations: emp.observations ?? undefined,
      position_id: emp.position.id,
    })
  }
})

const onSubmit = handleSubmit(async (values) => {
  if (formState.value == 'new') {
    createEmployee(values)
      .then(() => {
        router.push(EMPLOYEES)
      })
      .catch((error) => {
        console.error(error)
      })
  } else if (formState.value == 'edit' && id) {
    editEmployee({ ...values, id })
      .then(() => {
        router.push(EMPLOYEES)
      })
      .catch((error) => {
        console.error(error)
      })
  }
})

const [name, nameAttrs] = defineField('name')
const [birthday, birthdayAttrs] = defineField('birthday')
const [phone, phoneAttrs] = defineField('phone')
const [email, emailAttrs] = defineField('email')
const [admissionDate, admissionDateAttrs] = defineField('admission_date')
const [status] = defineField('status')
const [type] = defineField('type')
const [paymentMethod] = defineField('payment_method')
const [paymentValue, paymentValueAttrs] = defineField('payment_value')
const [hourlyRate, hourlyRateAttrs] = defineField('hourly_rate')
const [hourlyBonus, hourlyBonusAttrs] = defineField('hourly_bonus')
const [observations, observationsAttrs] = defineField('observations')
const [positionId] = defineField('position_id')
</script>

<template>
  <div class="p-8">
    <div>
      <h1 class="text-2xl font-bold text-gray-900">Create employee</h1>
      <p class="text-sm text-gray-500 mt-1">Add a new employee to your organization.</p>
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
              :disabled="formState == 'visualize'"
            />
          </Fieldset>
          <Fieldset id="phone" label="Phone" :error="errors.phone">
            <Input
              id="phone"
              placeholder="e.g. +1 555 000 0000"
              v-model="phone"
              v-bind="phoneAttrs"
              :disabled="formState == 'visualize'"
            />
          </Fieldset>
          <Fieldset id="email" label="Email" :error="errors.email">
            <Input
              id="email"
              placeholder="e.g. john@example.com"
              v-model="email"
              v-bind="emailAttrs"
              :disabled="formState == 'visualize'"
            />
          </Fieldset>
          <Fieldset id="birthday" label="Birthday" :error="errors.birthday">
            <Input
              id="birthday"
              type="date"
              v-model="birthday"
              v-bind="birthdayAttrs"
              :disabled="formState == 'visualize'"
            />
          </Fieldset>
          <Fieldset id="admission_date" label="Admission Date" :error="errors.admission_date">
            <Input
              id="admission_date"
              type="date"
              v-model="admissionDate"
              v-bind="admissionDateAttrs"
              :disabled="formState == 'visualize'"
            />
          </Fieldset>
        </div>

        <Separator />

        <div>
          <h2 class="text-xl font-bold text-gray-900">Employment Details</h2>
          <p class="text-sm text-gray-500 mt-1">Status, type and position in the organization.</p>
        </div>
        <div class="grid grid-cols-3 gap-4">
          <Fieldset id="status" label="Status" :error="errors.status">
            <Select
              v-model="status as string"
              :options="statusOptions"
              placeholder="Select status…"
              :disabled="formState == 'visualize'"
            />
          </Fieldset>
          <Fieldset id="type" label="Type" :error="errors.type">
            <Select
              v-model="type as string"
              :options="typeOptions"
              placeholder="Select type…"
              :disabled="formState == 'visualize'"
            />
          </Fieldset>
          <Fieldset id="position_id" label="Position" :error="errors.position_id">
            <Select
              v-model="positionId as string"
              :options="positionOptions"
              placeholder="Select position…"
              :disabled="formState == 'visualize'"
            />
          </Fieldset>
        </div>

        <Separator />

        <div>
          <h2 class="text-xl font-bold text-gray-900">Payment</h2>
          <p class="text-sm text-gray-500 mt-1">Payment method and compensation details.</p>
        </div>
        <div class="grid grid-cols-4 gap-4">
          <Fieldset id="payment_method" label="Payment Method" :error="errors.payment_method">
            <Select
              v-model="paymentMethod as string"
              :options="paymentMethodOptions"
              placeholder="Select method…"
              :disabled="formState == 'visualize'"
            />
          </Fieldset>
          <Fieldset id="payment_value" label="Payment Value" :error="errors.payment_value">
            <Input
              id="payment_value"
              type="number"
              placeholder="0.00"
              v-model="paymentValue"
              v-bind="paymentValueAttrs"
              :disabled="formState == 'visualize'"
            />
          </Fieldset>
          <Fieldset id="hourly_rate" label="Hourly Rate" :error="errors.hourly_rate">
            <Input
              id="hourly_rate"
              type="number"
              placeholder="0.00"
              v-model="hourlyRate"
              v-bind="hourlyRateAttrs"
              :disabled="formState == 'visualize'"
            />
          </Fieldset>
          <Fieldset id="hourly_bonus" label="Hourly Bonus" :error="errors.hourly_bonus">
            <Input
              id="hourly_bonus"
              type="number"
              placeholder="0.00"
              v-model="hourlyBonus"
              v-bind="hourlyBonusAttrs"
              :disabled="formState == 'visualize'"
            />
          </Fieldset>
        </div>

        <Separator />

        <div>
          <h2 class="text-xl font-bold text-gray-900">Observations</h2>
          <p class="text-sm text-gray-500 mt-1">Any additional notes about this employee.</p>
        </div>
        <Textarea
          v-model="observations"
          v-bind="observationsAttrs"
          :disabled="formState == 'visualize'"
        />
      </div>
      <Separator />
      <div class="px-6 py-4 flex justify-end gap-2">
        <Button variant="outline" :to="EMPLOYEES">Cancel</Button>
        <Button
          type="button"
          icon="lucide:pencil"
          @click="formState = 'edit'"
          v-if="formState == 'visualize'"
          >Edit employee</Button
        >
        <Button type="submit" icon="lucide:plus" v-else>{{
          formState == 'new' ? 'Create employee' : 'Edit employee'
        }}</Button>
      </div>
    </form>
  </div>
</template>
