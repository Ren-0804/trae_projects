declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  type Props = Record<string, unknown>
  type Data = Record<string, unknown>
  const component: DefineComponent<Props, Data, unknown>
  export default component
}

declare module '@/views/*.vue' {
  import type { DefineComponent } from 'vue'
  type Props = Record<string, unknown>
  type Data = Record<string, unknown>
  const component: DefineComponent<Props, Data, unknown>
  export default component
}

declare module '@/views/drivers/*.vue' {
  import type { DefineComponent } from 'vue'
  type Props = Record<string, unknown>
  type Data = Record<string, unknown>
  const component: DefineComponent<Props, Data, unknown>
  export default component
}

declare module '@/views/users/*.vue' {
  import type { DefineComponent } from 'vue'
  type Props = Record<string, unknown>
  type Data = Record<string, unknown>
  const component: DefineComponent<Props, Data, unknown>
  export default component
}
