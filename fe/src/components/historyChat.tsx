import { useCallback, useEffect, useRef } from 'react'
import { cn } from '../utils/cn.ts'

type HistoryItem = {
  type: 'request' | 'result'
  content: string
}

type HistoryChatProps = {
  history: HistoryItem[]
}

export const HistoryChat = ({ history }: HistoryChatProps) => {
  const chatEndRef = useRef<HTMLDivElement>(null) // Explicitly type the ref.

  // Memoize the function with useCallback.
  const scrollToBottom = useCallback(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [])

  // biome-ignore lint/correctness/useExhaustiveDependencies: <explanation>
  useEffect(() => {
    scrollToBottom()
  }, [history])

  return (
    <div className='flex mt-10 overflow-scroll gap-5 h-[calc(100vh-500px)] flex-col'>
      {history.map((item, index) => (
        <div
          key={index}
          className={cn('bg-oddin/40 rounded-[20px] p-4 w-fit max-w-[800px]', {
            'bg-highlight ml-auto': item.type === 'request'
          })}
        >
          <p className={cn('')}>{item.content}</p>
        </div>
      ))}
      <div ref={chatEndRef} /> {/* Ref applied to this div */}
    </div>
  )
}
