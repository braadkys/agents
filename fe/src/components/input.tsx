import type { ChangeEvent, InputHTMLAttributes } from 'react'
import { cn } from '../utils/cn.ts'

export type InputProps = Omit<
  InputHTMLAttributes<HTMLInputElement>,
  'onChange'
> & {
  label: string
  tooltip?: string
  errorMessage?: string
  disabledTooltip?: string
  onChange: (e: ChangeEvent<HTMLInputElement>) => void
}

export const Input = (props: InputProps) => {
  const { ...restProps } = props
  const component = (
    <div className={cn('group relative h-[50px] font-normal', props.className)}>
      <label
        htmlFor={props.name}
        className={cn(
          'absolute top-1/2 m-auto flex h-auto -translate-y-[15px] px-2 text-sm text-secondary transition-all ',
          {
            'group-focus-within:top-0.5 group-focus-within:translate-y-[0px] group-focus-within:text-[10px]':
              !props.readOnly,
            'top-0.5 translate-y-1/2 text-[10px]': !!props.value,
            'text-disabled': props.disabled,
            'cursor-text': !(props.readOnly || props.disabled)
          }
        )}
      >
        {props.label}
      </label>
      <input
        id={props.name}
        {...restProps}
        className={cn(
          'h-[40px] text-primary w-full rounded border border-highlight bg-highlight px-2 pt-2 text-sm disabled:cursor-not-allowed disabled:text-disabled enabled:hover:bg-highlight focus:outline-none',
          {
            '!border-fail': props.errorMessage
          },
          props.className
        )}
        type={props.type ?? 'text'}
        step={props.type === 'time' ? '1' : 'any'}
      />
    </div>
  )

  return <div className='w-full'>{component}</div>
}
