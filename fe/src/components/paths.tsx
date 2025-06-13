import type { ChangeEvent } from 'react'
import { Input } from './input.tsx'
import { PathItem } from './pathItem.tsx'

type Props = {
  onSubmit: () => void
  paths: string[]
  currentPath?: string
  onChange: (e: ChangeEvent<HTMLInputElement>) => void
  onDelete: (index: number) => void
  showForm: boolean
  onToggleForm: () => void
}
export const Paths = (props: Props) => {
  return (
    <div className='bg-foreground py-4 rounded-b-[20px] px-10 '>
      <div className='max-w-[900px] mx-auto'>
        <h3 className='text-[20px] font-bold mb-4'>Saved Paths:</h3>
        <ul className='flex flex-col gap-2'>
          {props.paths.map((path, index) => (
            <PathItem
              key={index}
              path={path}
              index={index}
              onDelete={props.onDelete}
            />
          ))}
        </ul>

        {props.showForm ? (
          <div className='flex mt-4 gap-2'>
            <div className='w-full'>
              <Input
                value={props.currentPath}
                onChange={props.onChange}
                className=''
                label='Add more path or url'
              />
            </div>
            <button
              disabled={!props.currentPath}
              type='button'
              onClick={() => {
                props.onSubmit()
                props.onToggleForm()
              }}
              className='bg-highlight border-highlight border text-white cursor-pointer text-sm font-semibold text-black w-full rounded h-[40px]'
            >
              Add Path
            </button>
            <button
              type='button'
              onClick={props.onToggleForm}
              className='border-fail border bg-fail-mild cursor-pointer font-semibold text-white rounded-full min-w-[40px] h-[40px] flex items-center justify-center'
            >
              X
            </button>
          </div>
        ) : (
          <button
            type='button'
            onClick={props.onToggleForm}
            className='border-success border bg-success-mild cursor-pointer font-semibold text-white rounded-full min-w-[40px] h-[40px] flex items-center justify-center mt-4'
          >
            +
          </button>
        )}
      </div>
    </div>
  )
}
