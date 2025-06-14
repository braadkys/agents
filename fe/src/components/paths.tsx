import { type ChangeEvent, useState } from 'react'
import { cn } from '../utils/cn.ts'
import { Input } from './input.tsx'
import { PathItem } from './pathItem.tsx'

type Props = {
  onSubmit: () => void
  paths: string[]
  currentPath?: string
  onChange: (e: ChangeEvent<HTMLInputElement>) => void
  onDelete: (index: number) => void
}
export const Paths = (props: Props) => {
  const [showForm, setShowForm] = useState(false)
  const [showSection, setShowSection] = useState(false)
  const handleToggleForm = () => {
    setShowForm(!showForm)
  }

  return (
    <div
      className={cn(
        'bg-foreground fixed top-0 transition-all duration-150 left-1/2 -translate-x-1/2 max-w-[1000px] py-4 w-full rounded-b-[20px] px-10 ',
        { '-translate-y-4/5': !showSection }
      )}
    >
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

        {showForm ? (
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
                handleToggleForm()
              }}
              className='bg-highlight border-highlight border text-white cursor-pointer text-sm font-semibold text-black w-full rounded h-[40px]'
            >
              Add Path
            </button>
            <button
              type='button'
              onClick={handleToggleForm}
              className='border-fail border bg-fail-mild cursor-pointer font-semibold text-white rounded-full min-w-[40px] h-[40px] flex items-center justify-center'
            >
              X
            </button>
          </div>
        ) : (
          <div
            className={cn('flex justify-between', { 'flex-end': !showSection })}
          >
            {showSection && (
              <button
                type='button'
                onClick={handleToggleForm}
                className='border-success border bg-success-mild cursor-pointer font-semibold text-white rounded-full min-w-[40px] h-[40px] flex items-center justify-center mt-4'
              >
                +
              </button>
            )}

            <button
              type='button'
              onClick={() => setShowSection(!showSection)}
              className='px-4 ml-auto border-highlight border bg-highlight cursor-pointer font-semibold text-white rounded-full min-w-[40px] h-[40px] flex items-center justify-center mt-4'
            >
              {!showSection ? 'Show paths' : 'Hide Paths'}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
