type Props = {
  path: string
  index: number
  onDelete: (index: number) => void
}
export const PathItem = (props: Props) => {
  return (
    <div className='flex items-center'>
      <p className='font-bold flex-1'>
        Path:
        <span className='font-medium underline italic'> {props.path}</span>
      </p>
      <button
        type='button'
        onClick={() => props.onDelete(props.index)}
        className='border-fail border bg-fail-mild text-sm cursor-pointer px-4 ml-10 font-semibold text-white rounded h-[40px]'
      >
        Delete
      </button>
    </div>
  )
}
