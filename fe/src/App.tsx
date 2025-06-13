import { useState } from 'react'
import { Input } from './components/input.tsx'
import { getPersistedValue, persistValue } from './utils/persistValue.ts'

function App() {
  const [paths, setPaths] = useState<string[]>(
    () => getPersistedValue<string[]>('paths') || []
  )
  const [currentPath, setCurrentPath] = useState<string>('')
  const [showForm, setShowForm] = useState<boolean>(false)

  const handleSubmit = () => {
    if (currentPath) {
      const updatedPaths = [...paths, currentPath]
      setPaths(updatedPaths)
      persistValue('paths', updatedPaths)
      setCurrentPath('') // Clear the input field
    }
  }

  const handleDelete = (index: number) => {
    const updatedPaths = paths.filter((_, i) => i !== index)
    setPaths(updatedPaths)
    persistValue('paths', updatedPaths)
  }

  const toggleForm = () => {
    setShowForm((prev) => !prev)
  }

  return (
    <>
      {paths.length ? (
        <div className='w-full  mx-auto'>
          <div className='bg-foreground py-4 rounded-b-[20px] px-10 '>
            <div className='max-w-[900px] mx-auto'>
              <h3 className='text-[20px] font-bold mb-4'>Saved Paths:</h3>
              <ul className='flex flex-col gap-2'>
                {paths.map((path, index) => (
                  <div className='flex items-center' key={index}>
                    <p className='font-bold flex-1'>
                      Path:
                      <span className='font-bold underline italic'>
                        {' '}
                        {path}
                      </span>
                    </p>
                    <button
                      type='button'
                      onClick={() => handleDelete(index)}
                      className='bg-fail cursor-pointer px-4 ml-10 font-semibold text-white rounded h-[40px]'
                    >
                      Delete
                    </button>
                  </div>
                ))}
              </ul>

              {showForm ? (
                <div className='flex mt-4 gap-2'>
                  <div className='w-full'>
                    <Input
                      value={currentPath}
                      onChange={(e) => setCurrentPath(e.target.value)}
                      className=''
                      label='Add more path or url'
                    />
                  </div>
                  <button
                    disabled={!currentPath}
                    type='button'
                    onClick={handleSubmit}
                    className='bg-oddin cursor-pointer font-semibold text-black w-full rounded h-[40px]'
                  >
                    Add Path
                  </button>
                  <button
                    type='button'
                    onClick={toggleForm}
                    className='bg-red-500 cursor-pointer font-semibold text-white rounded-full min-w-[40px] h-[40px] flex items-center justify-center'
                  >
                    X
                  </button>
                </div>
              ) : (
                <button
                  type='button'
                  onClick={toggleForm}
                  className='bg-green-500 cursor-pointer font-semibold text-white rounded-full min-w-[40px] h-[40px] flex items-center justify-center mt-4'
                >
                  +
                </button>
              )}
            </div>
          </div>
          <div className='max-w-[900px] mx-auto'>
            <p className='my-4'>Write your prompt</p>
            <textarea className='h-[100px] text-primary w-full rounded border border-highlight bg-highlight px-2 pt-2 text-sm disabled:cursor-not-allowed disabled:text-disabled enabled:hover:bg-highlight focus:outline-none' />
            <button
              type='button'
              onClick={() => {}}
              className='bg-oddin cursor-pointer font-semibold text-black w-full rounded mt-2 h-[45px]'
            >
              Submit
            </button>
          </div>{' '}
        </div>
      ) : (
        <div className='w-full absolute top-0 left-0 h-[100vh] flex items-center p-4 justify-center'>
          <div className='bg-foreground rounded-xl w-full font-bold max-w-[400px] p-4'>
            Please enter the url of the project
            <Input
              value={currentPath}
              onChange={(e) => setCurrentPath(e.target.value)}
              className='mt-2'
              label='path or url'
            />
            <button
              type='button'
              onClick={() => {
                handleSubmit()
                setShowForm(false)
              }}
              className='bg-oddin cursor-pointer font-semibold text-black w-full rounded mt-2 h-[45px]'
            >
              Submit
            </button>
          </div>
        </div>
      )}
    </>
  )
}

export default App
