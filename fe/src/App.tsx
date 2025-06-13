import { useState } from 'react'
import { postUserQuery } from './api/apiAgent.ts'
import { HistoryChat } from './components/historyChat.tsx'
import { PathInit } from './components/pathInit.tsx'
import { Paths } from './components/paths.tsx'
import { PromptInput } from './components/promptInput.tsx'
import { Wrapper } from './components/wrapper.tsx'
import { getPersistedValue, persistValue } from './utils/persistValue.ts'

function App() {
  const [paths, setPaths] = useState<string[]>(
    getPersistedValue<string[]>('paths') || []
  )
  const [loading, setLoading] = useState(false)
  const [currentPath, setCurrentPath] = useState<string>('')
  const [showForm, setShowForm] = useState(false)
  const [result, setResult] = useState<string | undefined>()
  const [promptState, setPromptState] = useState<{
    prompt: string
    paths: string[]
  }>({ prompt: '', paths: paths })

  const [history, setHistory] = useState<
    { type: 'request' | 'result'; content: string }[]
  >([])

  const handleSubmit = () => {
    if (!currentPath) return
    const updatedPaths = [...paths, currentPath]
    setPaths(updatedPaths) // Update paths state
    setPromptState((prev) => {
      return {
        prompt: prev.prompt,
        paths: updatedPaths
      }
    })
    persistValue('paths', updatedPaths)
    setCurrentPath('')
  }

  const handleDelete = (index: number) => {
    const updatedPaths = paths.filter((_, i) => i !== index)
    setPaths(updatedPaths) // Update paths state
    persistValue('paths', updatedPaths)
  }

  const handlePostUserQuery = async () => {
    if (!promptState.prompt) return
    setLoading(true)
    setHistory((prev) => [
      ...prev,
      { type: 'request', content: JSON.stringify(promptState.prompt) }
    ]) // Add promptState to history
    try {
      const response = await postUserQuery(promptState)
      setResult(response?.result)
      setHistory((prev) => [
        ...prev,
        { type: 'result', content: JSON.stringify(response.result) }
      ]) // Add result to history
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
      setPromptState({ prompt: '', paths }) // Reset the prompt while keeping paths
    }
  }

  return (
    <div className='app-container h-screen flex-1'>
      {paths.length ? (
        <Wrapper>
          <Paths
            paths={paths}
            currentPath={currentPath}
            showForm={showForm}
            onToggleForm={() => setShowForm(!showForm)}
            onChange={(e) => setCurrentPath(e.target.value)}
            onDelete={handleDelete}
            onSubmit={handleSubmit}
          />

          <HistoryChat loading={loading} history={history} />

          <PromptInput
            result={result}
            prompt={promptState.prompt}
            onChange={(e) =>
              setPromptState((prev) => ({
                ...prev,
                prompt: e.target.value
              }))
            }
            onSubmit={handlePostUserQuery}
          />
        </Wrapper>
      ) : (
        <PathInit
          currentPath={currentPath}
          onChange={(e) => setCurrentPath(e.target.value)}
          addPaths={(newPaths) => persistValue('paths', newPaths)}
          paths={paths}
          onSubmit={handleSubmit}
        />
      )}
    </div>
  )
}

export default App
