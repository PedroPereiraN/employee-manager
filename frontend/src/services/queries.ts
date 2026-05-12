import { formClient } from '@/lib/axios'

export const auth = async ({ email, password }: { email: string; password: string }) =>
  formClient.post('/auth/login', {
    username: email,
    password,
  })
