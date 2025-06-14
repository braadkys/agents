export type Prompt = {
  prompt: string
  paths: string[]
}

export type HistoryItemType = 'request' | 'result'

export type HistoryItem = { type: HistoryItemType; content: string }
