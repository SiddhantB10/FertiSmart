'use client'

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { 
  Bars3Icon, 
  XMarkIcon,
  BeakerIcon,
  ChartBarIcon,
  ClipboardDocumentListIcon,
  CpuChipIcon,
  DocumentChartBarIcon
} from '@heroicons/react/24/outline'
import { ApiStatus } from '../ApiStatus'

const navigation = [
  { name: 'Home', href: '/', icon: BeakerIcon },
  { name: 'Upload Data', href: '/upload', icon: ClipboardDocumentListIcon },
  { name: 'Crop Recommendation', href: '/crop-recommendation', icon: BeakerIcon },
  { name: 'Analytics', href: '/analytics', icon: ChartBarIcon },
  { name: 'Recommendations', href: '/recommendations', icon: CpuChipIcon },
  { name: 'Clustering', href: '/clustering', icon: DocumentChartBarIcon },
  { name: 'Schema', href: '/schema', icon: DocumentChartBarIcon },
]

export function Navbar() {
  const [isOpen, setIsOpen] = useState(false)
  const pathname = usePathname()

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50 backdrop-blur-sm bg-white/95">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo and brand */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-3 group">
              <div className="w-8 h-8 bg-gradient-to-br from-green-500 to-blue-600 rounded-lg flex items-center justify-center transform group-hover:scale-110 group-hover:rotate-12 transition-all duration-300 shadow-lg">
                <BeakerIcon className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold gradient-text font-display">
                FertiSmart
              </span>
            </Link>
          </div>

          {/* Desktop navigation */}
          <div className="hidden md:flex md:items-center md:space-x-2">
            {navigation.map((item, index) => {
              const isActive = pathname === item.href
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 transform hover:scale-105 ${
                    isActive
                      ? 'bg-gradient-to-r from-green-500 to-blue-500 text-white shadow-lg'
                      : 'text-gray-600 hover:text-green-600 hover:bg-green-50'
                  }`}
                  style={{
                    animationDelay: `${index * 0.05}s`
                  }}
                >
                  <item.icon className={`w-4 h-4 ${isActive ? 'animate-bounce-gentle' : ''}`} />
                  <span>{item.name}</span>
                </Link>
              )
            })}
          </div>

          {/* API Status & Mobile menu button */}
          <div className="flex items-center space-x-4">
            <ApiStatus />
            <div className="md:hidden">
              <button
                onClick={() => setIsOpen(!isOpen)}
                className="inline-flex items-center justify-center p-2 rounded-lg text-gray-400 hover:text-gray-500 hover:bg-green-50 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-green-500 transition-all duration-300 transform hover:scale-110"
              >
                {isOpen ? (
                  <XMarkIcon className="w-6 h-6 animate-scale-in" />
                ) : (
                  <Bars3Icon className="w-6 h-6 animate-scale-in" />
                )}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {isOpen && (
        <div className="md:hidden border-t border-gray-200 bg-white/95 backdrop-blur-sm animate-slide-up">
          <div className="px-2 pt-2 pb-3 space-y-1">
            {navigation.map((item, index) => {
              const isActive = pathname === item.href
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  onClick={() => setIsOpen(false)}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-lg text-base font-medium transition-all duration-300 transform hover:scale-105 ${
                    isActive
                      ? 'bg-gradient-to-r from-green-500 to-blue-500 text-white shadow-lg'
                      : 'text-gray-600 hover:text-green-600 hover:bg-green-50'
                  }`}
                  style={{
                    animationDelay: `${index * 0.05}s`
                  }}
                >
                  <item.icon className="w-5 h-5" />
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