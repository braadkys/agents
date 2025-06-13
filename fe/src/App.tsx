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
    () => getPersistedValue<string[]>('paths') || []
  )
  const [loading, setLoading] = useState(false)
  const [currentPath, setCurrentPath] = useState<string>('')
  const [showForm, setShowForm] = useState(false)
  const [result, setResult] = useState<string | undefined>()
  const [prompt, setPrompt] = useState<string | undefined>()
  const [history, setHistory] = useState<
    { type: 'request' | 'result'; content: string }[]
  >([])

  const handleSubmit = () => {
    if (!currentPath) return
    const updatedPaths = [...paths, currentPath]
    setPaths(updatedPaths)
    persistValue('paths', updatedPaths)
    setCurrentPath('')
  }

  const handleDelete = (index: number) => {
    const updatedPaths = paths.filter((_, i) => i !== index)
    setPaths(updatedPaths)
    persistValue('paths', updatedPaths)
  }

  const handlePostUserQuery = async () => {
    if (!prompt) return
    setLoading(true)
    setHistory((prev) => [...prev, { type: 'request', content: prompt }]) // Add prompt to history
    try {
      const response = await postUserQuery(prompt)
      setResult(response?.result)
      setHistory((prev) => [
        ...prev,
        { type: 'result', content: JSON.stringify(response.result) }
      ]) // Add request to history
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setLoading(false)
      setPrompt('') // Reset the prompt value
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

          <HistoryChat history={history} />

          <PromptInput
            loading={loading}
            result={result}
            prompt={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onSubmit={handlePostUserQuery}
          />
        </Wrapper>
      ) : (
        <PathInit
          currentPath={currentPath}
          onChange={(e) => setCurrentPath(e.target.value)}
          addPaths={setPaths}
          paths={paths}
          onSubmit={handleSubmit}
        />
      )}
    </div>
  )
}

export default App
