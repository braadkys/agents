import type { ChangeEvent } from 'react'
import { Input } from './input.tsx'
type Props = {
  onSubmit: () => void
  paths: string[]
  currentPath?: string
  onChange: (e: ChangeEvent<HTMLInputElement>) => void
  addPaths: (paths: string[]) => void
}
export const PathInit = (props: Props) => {
  return (
    <div className='w-full absolute top-0 left-0 h-[100vh] flex items-center p-4 justify-center'>
      <div className='bg-foreground rounded-xl w-full font-bold max-w-[400px] p-4'>
        Please enter the url of the project
        <Input
          value={props.currentPath}
          onChange={props.onChange}
          className='mt-2'
          label='path or url'
        />
        <button
          type='button'
          onClick={props.onSubmit}
          className='bg-oddin cursor-pointer font-semibold text-black w-full rounded mt-2 h-[45px]'
        >
          Submit
        </button>
      </div>
    </div>
  )
}
