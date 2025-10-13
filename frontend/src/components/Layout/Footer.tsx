import { 
  EnvelopeIcon
} from '@heroicons/react/24/outline'

export function Footer() {
  return (
    <footer className="bg-gradient-to-br from-gray-900 via-gray-800 to-emerald-900 text-white relative overflow-hidden">
      {/* Animated background pattern */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute inset-0 bg-hero-pattern"></div>
      </div>
      
      {/* Decorative elements */}
      <div className="absolute top-0 left-0 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl"></div>
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl"></div>
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 lg:py-16">
        <div className="grid grid-cols-1 gap-6 sm:gap-8">
          {/* Brand Section */}
          <div className="animate-fade-in text-center">
            <div className="flex items-center justify-center space-x-2 sm:space-x-3 mb-4 sm:mb-6 group">
              <div className="text-3xl sm:text-4xl transform group-hover:scale-110 transition-all duration-300 drop-shadow-lg">
                🌾
              </div>
              <span className="text-2xl sm:text-3xl font-bold font-display gradient-text">FertiSmart</span>
            </div>
            <p className="text-gray-300 mb-4 sm:mb-6 max-w-2xl mx-auto hover:text-gray-100 transition-colors duration-300 text-base sm:text-lg leading-relaxed px-4">
              Revolutionizing agriculture through data-driven soil analysis and intelligent 
              fertilizer recommendations. Empowering farmers with cutting-edge technology 
              for sustainable and profitable farming.
            </p>
            <div className="flex justify-center">
              <div className="flex flex-col sm:flex-row items-center space-y-2 sm:space-y-0 sm:space-x-3 text-gray-300 hover:text-emerald-400 transition-all duration-300 transform hover:scale-105 bg-white/5 px-4 sm:px-6 py-2 sm:py-3 rounded-lg sm:rounded-xl backdrop-blur-sm border border-white/10">
                <EnvelopeIcon className="w-5 sm:w-6 h-5 sm:h-6" />
                <span className="font-medium text-sm sm:text-base">contact@fertismart.com</span>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="border-t border-gray-700/50 mt-8 sm:mt-12 pt-6 sm:pt-8">
          <div className="flex flex-col items-center space-y-4 text-center">
            <p className="text-gray-400 text-sm sm:text-base px-4">
              © 2024 FertiSmart. All rights reserved. Made with 💚 for farmers.
            </p>
            <div className="flex flex-wrap justify-center gap-4 sm:gap-6">
              <a href="#" className="text-gray-400 hover:text-emerald-400 text-sm sm:text-base transition-all duration-300 hover:underline">
                Privacy Policy
              </a>
              <a href="#" className="text-gray-400 hover:text-emerald-400 text-sm sm:text-base transition-all duration-300 hover:underline">
                Terms of Service
              </a>
              <a href="#" className="text-gray-400 hover:text-emerald-400 text-sm sm:text-base transition-all duration-300 hover:underline">
                Contact Us
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}