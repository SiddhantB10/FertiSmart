import Link from 'next/link'
import { 
  ChartBarIcon,
  CpuChipIcon,
  BeakerIcon
} from '@heroicons/react/24/outline'

export function Hero() {
  return (
    <div className="relative bg-gradient-to-br from-primary-600 via-primary-700 to-primary-800 overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-hero-pattern opacity-10"></div>
      
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 sm:py-32">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Content */}
          <div className="text-center lg:text-left">
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6 font-display">
              Smart
              <span className="block text-secondary-400">Fertilizer</span>
              <span className="block">Recommendations</span>
            </h1>
            
            <p className="text-xl text-primary-100 mb-8 max-w-2xl">
              Harness the power of data science and machine learning to optimize your 
              soil health and crop yields. Get personalized fertilizer recommendations 
              based on comprehensive soil analysis.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <Link 
                href="/upload" 
                className="btn-primary inline-flex items-center justify-center px-8 py-4 text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
              >
                <BeakerIcon className="w-6 h-6 mr-2" />
                Analyze Soil Now
              </Link>
              
              <Link 
                href="/analytics" 
                className="btn-outline bg-white/10 backdrop-blur-sm border-white/20 text-white hover:bg-white hover:text-primary-700 inline-flex items-center justify-center px-8 py-4 text-lg font-semibold rounded-xl transition-all duration-200"
              >
                <ChartBarIcon className="w-6 h-6 mr-2" />
                View Dashboard
              </Link>
            </div>

            {/* Stats */}
            <div className="mt-12 grid grid-cols-3 gap-6 text-center">
              <div>
                <div className="text-2xl font-bold text-white">98%</div>
                <div className="text-primary-200 text-sm">Accuracy</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-white">7</div>
                <div className="text-primary-200 text-sm">ML Algorithms</div>
              </div>
              <div>
                <div className="text-2xl font-bold text-white">1000+</div>
                <div className="text-primary-200 text-sm">Soil Samples</div>
              </div>
            </div>
          </div>

          {/* Visual */}
          <div className="relative">
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 border border-white/20">
              {/* Mockup Dashboard */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-white font-semibold">Soil Analysis</h3>
                  <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                </div>
                
                {/* NPK Levels */}
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-primary-100 text-sm">Nitrogen (N)</span>
                    <span className="text-white font-medium">75 ppm</span>
                  </div>
                  <div className="w-full bg-white/20 rounded-full h-2">
                    <div className="bg-secondary-400 h-2 rounded-full w-3/4"></div>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-primary-100 text-sm">Phosphorus (P)</span>
                    <span className="text-white font-medium">42 ppm</span>
                  </div>
                  <div className="w-full bg-white/20 rounded-full h-2">
                    <div className="bg-secondary-400 h-2 rounded-full w-1/2"></div>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-primary-100 text-sm">Potassium (K)</span>
                    <span className="text-white font-medium">58 ppm</span>
                  </div>
                  <div className="w-full bg-white/20 rounded-full h-2">
                    <div className="bg-secondary-400 h-2 rounded-full w-2/3"></div>
                  </div>
                </div>

                {/* Recommendation */}
                <div className="mt-6 p-4 bg-white/20 rounded-lg border border-white/30">
                  <div className="flex items-center space-x-2 mb-2">
                    <CpuChipIcon className="w-4 h-4 text-secondary-400" />
                    <span className="text-white font-medium text-sm">AI Recommendation</span>
                  </div>
                  <p className="text-primary-100 text-sm">
                    Apply NPK 10:26:26 at 120 kg/ha for optimal rice cultivation
                  </p>
                </div>
              </div>
            </div>
            
            {/* Floating Elements */}
            <div className="absolute -top-4 -right-4 w-24 h-24 bg-secondary-400/20 rounded-full blur-xl animate-pulse-slow"></div>
            <div className="absolute -bottom-4 -left-4 w-32 h-32 bg-accent-400/20 rounded-full blur-xl animate-pulse-slow"></div>
          </div>
        </div>
      </div>
    </div>
  )
}