'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  Bars3Icon, 
  XMarkIcon,
  BeakerIcon
} from '@heroicons/react/24/outline'
import { ThemeToggle } from '../ui/ThemeToggle'

const navigation = [
  { name: 'Home', href: '/', icon: BeakerIcon },
  { name: 'Crop Recommendation', href: '/crop-recommendation', icon: BeakerIcon }
]

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false)
  const pathname = usePathname()

  return (
    <nav className="bg-white/95 dark:bg-gray-900/95 backdrop-blur-xl shadow-lg dark:shadow-emerald-500/10 sticky top-0 z-50 border-b-2 border-emerald-100 dark:border-gray-700 transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 sm:h-18 lg:h-20">
          {/* Logo and brand */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2 sm:space-x-3 group">
              <div className="text-2xl sm:text-3xl lg:text-4xl transform group-hover:scale-110 transition-all duration-300 drop-shadow-lg">
                🌾
              </div>
              <span className="text-lg sm:text-xl lg:text-2xl font-bold gradient-text font-display dark:text-white">
                FertiSmart
              </span>
            </Link>
          </div>

          {/* Desktop navigation */}
          <div className="hidden md:flex md:items-center md:space-x-2 lg:space-x-3">
            {navigation.map((item, index) => {
              const isActive = pathname === item.href
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`flex items-center space-x-2 px-4 lg:px-6 py-2 lg:py-3 rounded-lg lg:rounded-xl text-sm lg:text-base font-semibold transition-all duration-300 transform hover:scale-105 ${
                    isActive
                      ? 'bg-gradient-to-r from-emerald-500 to-teal-600 dark:from-emerald-400 dark:to-teal-500 text-white shadow-xl shadow-emerald-500/30'
                      : 'text-gray-700 dark:text-gray-300 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-gray-800/70'
                  }`}
                  style={{
                    animationDelay: `${index * 0.05}s`
                  }}
                >
                  <item.icon className={`w-4 lg:w-5 h-4 lg:h-5 ${isActive ? 'animate-bounce-gentle' : ''}`} />
                  <span className="hidden lg:inline">{item.name}</span>
                  <span className="lg:hidden">{item.name.split(' ')[0]}</span>
                </Link>
              )
            })}
          </div>

          {/* Theme Toggle & Mobile menu button */}
          <div className="flex items-center space-x-2 sm:space-x-4">
            <ThemeToggle />
            <div className="md:hidden">
              <button
                onClick={() => setIsOpen(!isOpen)}
                className="inline-flex items-center justify-center p-2 sm:p-3 rounded-lg sm:rounded-xl text-gray-600 dark:text-gray-400 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-emerald-500 dark:focus:ring-emerald-400 transition-all duration-300 transform hover:scale-110">
                {isOpen ? (
                  <XMarkIcon className="w-6 sm:w-7 h-6 sm:h-7 animate-scale-in" />
                ) : (
                  <Bars3Icon className="w-6 sm:w-7 h-6 sm:h-7 animate-scale-in" />
                )}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        <div className="md:hidden border-t-2 border-emerald-100 dark:border-gray-700 bg-white/98 dark:bg-gray-900/98 backdrop-blur-xl animate-slide-up shadow-xl">
          <div className="px-4 pt-4 pb-6 space-y-2">
            {navigation.map((item, index) => {
              const isActive = pathname === item.href
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  onClick={() => setIsOpen(false)}
                  className={`flex items-center space-x-3 px-6 py-4 rounded-xl text-lg font-semibold transition-all duration-300 transform hover:scale-105 ${
                    isActive
                      ? 'bg-gradient-to-r from-emerald-500 to-teal-600 dark:from-emerald-400 dark:to-teal-500 text-white shadow-xl'
                      : 'text-gray-700 dark:text-gray-300 hover:text-emerald-600 dark:hover:text-emerald-400 hover:bg-emerald-50 dark:hover:bg-gray-800/70'
                  }`}
                  style={{
                    animationDelay: `${index * 0.05}s`
                  }}
                >
                  <item.icon className="w-6 h-6" />
                  <span>{item.name}</span>
                </Link>
              )
            })}
          </div>
        </div>
      )}
    </nav>
  )
}