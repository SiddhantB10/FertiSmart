'use client'

import { MoonIcon, SunIcon } from '@heroicons/react/24/outline'
import { useTheme } from '../../contexts/ThemeContext'

export function ThemeToggle() {
  const { theme, toggleTheme, mounted } = useTheme()

  // Show a placeholder while hydrating
  if (!mounted) {
    return (
      <div className="h-10 w-10 rounded-lg border border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 animate-pulse" />
    )
  }

  return (
    <button
      onClick={toggleTheme}
      className="relative inline-flex h-10 w-10 items-center justify-center rounded-lg border-2 border-emerald-200 dark:border-emerald-700 bg-white dark:bg-gray-800 text-gray-600 dark:text-emerald-400 transition-all duration-300 hover:bg-emerald-50 dark:hover:bg-emerald-900/50 hover:text-emerald-600 dark:hover:text-emerald-300 hover:shadow-lg hover:scale-110 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-2 dark:focus:ring-emerald-400 dark:focus:ring-offset-gray-900"
      aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
      title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
    >
      <div className="relative">
        {theme === 'light' ? (
          <MoonIcon className="h-5 w-5 transition-all duration-300 hover:rotate-12" />
        ) : (
          <SunIcon className="h-5 w-5 transition-all duration-300 hover:rotate-90" />
        )}
      </div>
    </button>
  )
}