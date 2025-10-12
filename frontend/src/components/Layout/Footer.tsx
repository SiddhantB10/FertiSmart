import Link from 'next/link'
import { 
  BeakerIcon,
  EnvelopeIcon,
  MapPinIcon,
  PhoneIcon
} from '@heroicons/react/24/outline'

export function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand Section */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
                <BeakerIcon className="w-5 h-5 text-white" />
              </div>
              <span className="text-xl font-bold font-display">FertiSmart</span>
            </div>
            <p className="text-gray-300 mb-6 max-w-md">
              Revolutionizing agriculture through data-driven soil analysis and intelligent 
              fertilizer recommendations. Empowering farmers with cutting-edge technology 
              for sustainable farming.
            </p>
            <div className="flex space-x-4">
              <div className="flex items-center space-x-2 text-gray-300">
                <EnvelopeIcon className="w-5 h-5" />
                <span>contact@fertismart.com</span>
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/analytics" className="text-gray-300 hover:text-primary-400 transition-colors">
                  Analytics Dashboard
                </Link>
              </li>
              <li>
                <Link href="/recommendations" className="text-gray-300 hover:text-primary-400 transition-colors">
                  Get Recommendations
                </Link>
              </li>
              <li>
                <Link href="/clustering" className="text-gray-300 hover:text-primary-400 transition-colors">
                  Soil Clustering
                </Link>
              </li>
              <li>
                <Link href="/schema" className="text-gray-300 hover:text-primary-400 transition-colors">
                  Database Schema
                </Link>
              </li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Resources</h3>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-gray-300 hover:text-primary-400 transition-colors">
                  Documentation
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-300 hover:text-primary-400 transition-colors">
                  API Reference
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-300 hover:text-primary-400 transition-colors">
                  User Guide
                </a>
              </li>
              <li>
                <a href="#" className="text-gray-300 hover:text-primary-400 transition-colors">
                  Support
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-gray-800 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 text-sm">
              © 2024 FertiSmart. All rights reserved.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a href="#" className="text-gray-400 hover:text-primary-400 text-sm transition-colors">
                Privacy Policy
              </a>
              <a href="#" className="text-gray-400 hover:text-primary-400 text-sm transition-colors">
                Terms of Service
              </a>
              <a href="#" className="text-gray-400 hover:text-primary-400 text-sm transition-colors">
                Contact
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}