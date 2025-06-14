import { useState } from 'react'
import { postUserQuery } from './api/apiAgent.ts'
import { HistoryChat } from './components/historyChat.tsx'
import { PathInit } from './components/pathInit.tsx'
import { Paths } from './components/paths.tsx'
import { PromptInput } from './components/promptInput.tsx'
import { Wrapper } from './components/wrapper.tsx'
import type { HistoryItem, HistoryItemType, Prompt } from './types/types.ts'
import { getPersistedValue, persistValue } from './utils/persistValue.ts'

function App() {
  const [paths, setPaths] = useState<string[]>(
    getPersistedValue<string[]>('paths') || []
  )
  const [loading, setLoading] = useState(false)
  const [currentPath, setCurrentPath] = useState<string>('')
  const [promptState, setPromptState] = useState<Prompt>({
    prompt: '',
    paths: paths
  })

  const [history, setHistory] = useState<HistoryItem[]>([])

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

  const handlePushToHistory = (prompt: string, type: HistoryItemType) => {
    setHistory((prev) => [...prev, { type, content: prompt }])
  }

  const handleDelete = (index: number) => {
    const updatedPaths = paths.filter((_, i) => i !== index)
    setPaths(updatedPaths) // Update paths state
    persistValue('paths', updatedPaths)
  }

  const handlePostUserQuery = async () => {
    if (!promptState.prompt) return
    setLoading(true)
    handlePushToHistory(promptState.prompt, 'request')
    try {
      const response = await postUserQuery(promptState)
      handlePushToHistory(response.result, 'result')
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
            onChange={(e) => setCurrentPath(e.target.value)}
            onDelete={handleDelete}
            onSubmit={handleSubmit}
          />
          <HistoryChat loading={loading} history={history} />
          <PromptInput
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
