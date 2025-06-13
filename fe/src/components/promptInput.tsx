type PromptInputProps = {
  loading: boolean
  result?: string
  prompt?: string
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void
  onSubmit: () => void
}

export const PromptInput = ({
  loading,
  prompt,
  onChange,
  onSubmit
}: PromptInputProps) => {
  return (
    <div className='prompt-input mt-10 fixed bottom-0 w-full left-1/2 -translate-x-1/2 max-w-[900px] mx-auto'>
      <p className='mb-2'>Your prompt</p>

      <textarea
        value={prompt}
        onChange={onChange}
        className='h-[120px] text-primary w-full rounded border border-highlight bg-highlight px-2 pt-2 text-sm disabled:cursor-not-allowed disabled:text-disabled enabled:hover:bg-highlight focus:outline-none'
      />
      <button
        type='button'
        onClick={onSubmit}
        className='bg-oddin cursor-pointer font-semibold text-black w-full mt-2 rounded h-[40px]'
        disabled={loading}
      >
        Submit
      </button>
    </div>
  )
}
