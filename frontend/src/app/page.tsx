import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Navbar } from '@/components/Layout/Navbar'
import { Footer } from '@/components/Layout/Footer'

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-green-50 dark:from-gray-900 dark:via-slate-900 dark:to-gray-900 transition-colors duration-500">
      <Navbar />
      
      {/* Hero Section with Enhanced Design */}
      <div className="relative overflow-hidden">
        {/* Decorative background elements */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-20 left-10 w-72 h-72 bg-emerald-200 dark:bg-emerald-900 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-3xl opacity-30 animate-pulse"></div>
          <div className="absolute top-40 right-10 w-96 h-96 bg-teal-200 dark:bg-teal-900 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-3xl opacity-30 animate-pulse" style={{animationDelay: '2s'}}></div>
          <div className="absolute bottom-20 left-1/2 w-80 h-80 bg-green-200 dark:bg-green-900 rounded-full mix-blend-multiply dark:mix-blend-soft-light filter blur-3xl opacity-30 animate-pulse" style={{animationDelay: '4s'}}></div>
        </div>

        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 lg:py-20">
          <div className="text-center">
            <div className="text-6xl sm:text-7xl md:text-8xl mb-4 sm:mb-6 animate-bounce-in drop-shadow-lg">🌾</div>
            <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 dark:text-white mb-4 sm:mb-6 animate-fade-in px-2">
              <span className="gradient-text">FertiSmart</span>
            </h1>
            <p className="text-lg sm:text-xl md:text-2xl lg:text-3xl font-semibold text-gray-700 dark:text-gray-200 mb-3 sm:mb-4 max-w-3xl mx-auto animate-slide-up px-4" style={{animationDelay: '0.1s'}}>
              Smart Crop Recommendation System
            </p>
            <p className="text-base sm:text-lg md:text-xl text-gray-600 dark:text-gray-400 mb-8 sm:mb-10 lg:mb-12 max-w-2xl mx-auto animate-slide-up leading-relaxed px-4" style={{animationDelay: '0.2s'}}>
              Harness the power of AI to get intelligent crop recommendations based on your soil and climate conditions using advanced Random Forest Classification
            </p>
            
            <Link href="/crop-recommendation" className="inline-block animate-scale-in px-4" style={{animationDelay: '0.3s'}}>
              <Button className="bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 dark:from-emerald-500 dark:to-teal-500 dark:hover:from-emerald-600 dark:hover:to-teal-600 text-white text-lg sm:text-xl font-semibold px-8 sm:px-12 py-5 sm:py-7 rounded-full shadow-2xl transform hover:scale-110 transition-all duration-300 hover:shadow-emerald-500/50 dark:hover:shadow-emerald-400/50 animate-glow w-full sm:w-auto">
                🚀 Get Crop Recommendation Now
              </Button>
            </Link>
          </div>

          {/* Features Section with Enhanced Cards */}
          <div className="mt-16 sm:mt-20 lg:mt-28 grid grid-cols-1 lg:grid-cols-3 gap-6 sm:gap-8 px-4 sm:px-0">
            <div className="group bg-white/80 dark:bg-gray-800/80 backdrop-blur-lg rounded-2xl sm:rounded-3xl shadow-xl dark:shadow-emerald-500/10 p-6 sm:p-8 lg:p-10 text-center transform hover:scale-105 transition-all duration-500 hover:shadow-2xl dark:hover:shadow-emerald-500/30 animate-slide-in-left border-2 border-emerald-100 dark:border-gray-700/50 hover:border-emerald-300 dark:hover:border-emerald-600" style={{animationDelay: '0.4s'}}>
              <div className="text-5xl sm:text-6xl mb-4 sm:mb-6 transform group-hover:scale-125 group-hover:rotate-12 transition-all duration-500">🤖</div>
              <h3 className="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white mb-3 sm:mb-4 gradient-text">
                Random Forest AI
              </h3>
              <p className="text-sm sm:text-base text-gray-600 dark:text-gray-300 leading-relaxed">
                Advanced machine learning algorithm trained on thousands of crop samples for highly accurate predictions
              </p>
            </div>

            <div className="group bg-white/80 dark:bg-gray-800/80 backdrop-blur-lg rounded-2xl sm:rounded-3xl shadow-xl dark:shadow-emerald-500/10 p-6 sm:p-8 lg:p-10 text-center transform hover:scale-105 transition-all duration-500 hover:shadow-2xl dark:hover:shadow-emerald-500/30 animate-slide-up border-2 border-teal-100 dark:border-gray-700/50 hover:border-teal-300 dark:hover:border-teal-600" style={{animationDelay: '0.5s'}}>
              <div className="text-5xl sm:text-6xl mb-4 sm:mb-6 transform group-hover:scale-125 group-hover:rotate-12 transition-all duration-500">📊</div>
              <h3 className="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white mb-3 sm:mb-4 gradient-text">
                Data-Driven Insights
              </h3>
              <p className="text-sm sm:text-base text-gray-600 dark:text-gray-300 leading-relaxed">
                Comprehensive analysis of soil nutrients (NPK), climate conditions, pH levels, and rainfall patterns
              </p>
            </div>

            <div className="group bg-white/80 dark:bg-gray-800/80 backdrop-blur-lg rounded-2xl sm:rounded-3xl shadow-xl dark:shadow-emerald-500/10 p-6 sm:p-8 lg:p-10 text-center transform hover:scale-105 transition-all duration-500 hover:shadow-2xl dark:hover:shadow-emerald-500/30 animate-slide-in-right border-2 border-green-100 dark:border-gray-700/50 hover:border-green-300 dark:hover:border-green-600" style={{animationDelay: '0.6s'}}>
              <div className="text-5xl sm:text-6xl mb-4 sm:mb-6 transform group-hover:scale-125 group-hover:rotate-12 transition-all duration-500">🎯</div>
              <h3 className="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white mb-3 sm:mb-4 gradient-text">
                Precise Recommendations
              </h3>
              <p className="text-sm sm:text-base text-gray-600 dark:text-gray-300 leading-relaxed">
                Get top crop suggestions with detailed confidence scores and comprehensive explanations
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* How It Works Section with Timeline Design */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 lg:py-20">
        <div className="animate-fade-in" style={{animationDelay: '0.7s'}}>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-center text-gray-900 dark:text-white mb-3 sm:mb-4 gradient-text px-4">
            How It Works
          </h2>
          <p className="text-center text-gray-600 dark:text-gray-400 mb-10 sm:mb-12 lg:mb-16 text-base sm:text-lg max-w-2xl mx-auto px-4">
            Simple, fast, and intelligent - get your crop recommendations in 4 easy steps
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8">
            <div className="text-center group animate-slide-up relative" style={{animationDelay: '0.8s'}}>
              <div className="w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-emerald-500 to-emerald-700 text-white rounded-xl sm:rounded-2xl flex items-center justify-center text-2xl sm:text-3xl font-bold mx-auto mb-4 sm:mb-6 shadow-2xl transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-500">
                1
              </div>
              <h4 className="text-lg sm:text-xl font-bold text-gray-900 dark:text-white mb-2 sm:mb-3">Enter Data</h4>
              <p className="text-sm sm:text-base text-gray-600 dark:text-gray-400 leading-relaxed px-2">Input your soil nutrients and climate conditions</p>
            </div>
            
            <div className="text-center group animate-slide-up relative" style={{animationDelay: '0.9s'}}>
              <div className="w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-blue-500 to-blue-700 text-white rounded-xl sm:rounded-2xl flex items-center justify-center text-2xl sm:text-3xl font-bold mx-auto mb-4 sm:mb-6 shadow-2xl transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-500">
                2
              </div>
              <h4 className="text-lg sm:text-xl font-bold text-gray-900 dark:text-white mb-2 sm:mb-3">AI Analysis</h4>
              <p className="text-sm sm:text-base text-gray-600 dark:text-gray-400 leading-relaxed px-2">Random Forest algorithm analyzes your conditions</p>
            </div>
            
            <div className="text-center group animate-slide-up relative" style={{animationDelay: '1s'}}>
              <div className="w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-purple-500 to-purple-700 text-white rounded-xl sm:rounded-2xl flex items-center justify-center text-2xl sm:text-3xl font-bold mx-auto mb-4 sm:mb-6 shadow-2xl transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-500">
                3
              </div>
              <h4 className="text-lg sm:text-xl font-bold text-gray-900 dark:text-white mb-2 sm:mb-3">Get Results</h4>
              <p className="text-sm sm:text-base text-gray-600 dark:text-gray-400 leading-relaxed px-2">Receive top crop recommendations with confidence scores</p>
            </div>
            
            <div className="text-center group animate-slide-up relative" style={{animationDelay: '1.1s'}}>
              <div className="w-16 h-16 sm:w-20 sm:h-20 bg-gradient-to-br from-orange-500 to-orange-700 text-white rounded-xl sm:rounded-2xl flex items-center justify-center text-2xl sm:text-3xl font-bold mx-auto mb-4 sm:mb-6 shadow-2xl transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-500">
                4
              </div>
              <h4 className="text-lg sm:text-xl font-bold text-gray-900 dark:text-white mb-2 sm:mb-3">Make Decision</h4>
              <p className="text-sm sm:text-base text-gray-600 dark:text-gray-400 leading-relaxed px-2">Choose the best crop for optimal yield</p>
            </div>
          </div>
        </div>

        {/* Enhanced Stats Section */}
        <div className="mt-16 sm:mt-20 lg:mt-28 bg-gradient-to-br from-white to-emerald-50 dark:from-gray-800 dark:to-gray-900 rounded-2xl sm:rounded-3xl shadow-2xl p-6 sm:p-8 lg:p-12 border-2 border-emerald-100 dark:border-gray-700 mx-4 sm:mx-0">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 sm:gap-12 text-center">
            <div className="transform hover:scale-110 transition-all duration-500">
              <div className="text-4xl sm:text-5xl lg:text-6xl font-bold bg-gradient-to-r from-emerald-600 to-teal-600 dark:from-emerald-400 dark:to-teal-400 bg-clip-text text-transparent mb-2 sm:mb-3">95%+</div>
              <div className="text-gray-700 dark:text-gray-300 text-base sm:text-lg font-semibold">Model Accuracy</div>
              <div className="text-gray-500 dark:text-gray-400 text-sm mt-1 sm:mt-2">Highly reliable predictions</div>
            </div>
            <div className="transform hover:scale-110 transition-all duration-500">
              <div className="text-4xl sm:text-5xl lg:text-6xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-400 dark:to-indigo-400 bg-clip-text text-transparent mb-2 sm:mb-3">22</div>
              <div className="text-gray-700 dark:text-gray-300 text-base sm:text-lg font-semibold">Crops Supported</div>
              <div className="text-gray-500 dark:text-gray-400 text-sm mt-1 sm:mt-2">Diverse crop options</div>
            </div>
            <div className="transform hover:scale-110 transition-all duration-500">
              <div className="text-4xl sm:text-5xl lg:text-6xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 dark:from-purple-400 dark:to-pink-400 bg-clip-text text-transparent mb-2 sm:mb-3">7</div>
              <div className="text-gray-700 dark:text-gray-300 text-base sm:text-lg font-semibold">Input Parameters</div>
              <div className="text-gray-500 dark:text-gray-400 text-sm mt-1 sm:mt-2">Comprehensive analysis</div>
            </div>
          </div>
        </div>

        {/* Enhanced CTA Section */}
        <div className="mt-16 sm:mt-20 lg:mt-28 text-center bg-gradient-to-r from-emerald-600 to-teal-600 dark:from-emerald-700 dark:to-teal-700 rounded-2xl sm:rounded-3xl p-8 sm:p-12 lg:p-16 shadow-2xl relative overflow-hidden mx-4 sm:mx-0">
          {/* Decorative elements */}
          <div className="absolute top-0 right-0 w-32 h-32 sm:w-64 sm:h-64 bg-white/10 rounded-full -mr-16 sm:-mr-32 -mt-16 sm:-mt-32"></div>
          <div className="absolute bottom-0 left-0 w-32 h-32 sm:w-64 sm:h-64 bg-white/10 rounded-full -ml-16 sm:-ml-32 -mb-16 sm:-mb-32"></div>
          
          <div className="relative z-10">
            <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-4 sm:mb-6 px-4">
              Ready to Find Your Perfect Crop?
            </h2>
            <p className="text-base sm:text-lg lg:text-xl text-emerald-50 mb-6 sm:mb-8 lg:mb-10 max-w-2xl mx-auto px-4">
              Start making data-driven farming decisions today and maximize your yield potential
            </p>
            <Link href="/crop-recommendation">
              <Button className="bg-emerald-100 hover:bg-emerald-200 text-emerald-800 hover:text-emerald-900 text-lg sm:text-xl font-bold px-10 sm:px-14 py-5 sm:py-7 rounded-full shadow-2xl transform hover:scale-105 transition-all duration-300 border-2 border-emerald-300 hover:border-emerald-400 w-full sm:w-auto">
                Start Now →
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Footer */}
      <Footer />
    </main>
  )
}