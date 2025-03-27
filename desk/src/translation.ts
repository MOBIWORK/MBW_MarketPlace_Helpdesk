import { createResource } from 'frappe-ui'

interface TranslatedMessages {
  [key: string]: string
}

declare global {
  interface Window {
    translatedMessages?: TranslatedMessages
    __?: typeof translate
  }
}

export default function translationPlugin(app: any): void {
  app.config.globalProperties.__ = translate
  window.__ = translate
  if (!window.translatedMessages) fetchTranslations()
}

function format(message: string, replace: string[]): string {
  return message.replace(/{(\d+)}/g, function (match, number) {
    return typeof replace[number] !== 'undefined' ? replace[number] : match
  })
}

function translate(message: string, replace: string[] = [], context: string | null = null): string {
  const translatedMessages: TranslatedMessages = window.translatedMessages || {}
  let translatedMessage = ''

  if (context) {
    const key = `${message}:${context}`
    if (translatedMessages[key]) {
      translatedMessage = translatedMessages[key]
    }
  }

  if (!translatedMessage) {
    translatedMessage = translatedMessages[message] || message
  }

  const hasPlaceholders = /{\d+}/.test(message)
  if (!hasPlaceholders) {
    return translatedMessage
  }

  return format(translatedMessage, replace)
}

function fetchTranslations(lang?: string): void {
  createResource({
    url: 'helpdesk.api.get_translations',
    cache: 'translations',
    auto: true,
    transform: (data: TranslatedMessages) => {
      window.translatedMessages = data
    },
  })
}