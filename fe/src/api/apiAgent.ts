export async function postStart() {
  const url = 'http://127.0.0.1:8000/start'
  const body = {
    user_query: '/Users/davidzirnsak/Desktop/prace/raiden'
  }

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    console.log('Response:', data)
  } catch (error) {
    console.error('Error:', error)
  }
}

export async function postEnd() {
  const url = 'http://127.0.0.1:8000/end'

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    console.log('Response:', data)
  } catch (error) {
    console.error('Error:', error)
  }
}
export async function postUserQuery(promptState: {
  prompt: string
  paths: string[]
}) {
  const url = 'http://127.0.0.1:8000/chat'
  const body = {
    prompt: promptState.prompt,
    paths: promptState.paths
  }

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    return data // Return the response data
  } catch (error) {
    console.error('Error:', error)
    throw error // Rethrow the error for further handling
  }
}
