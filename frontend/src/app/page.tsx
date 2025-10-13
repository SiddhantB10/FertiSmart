import Link from 'next/link'
import { Button } from '@/components/ui/button'

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-green-50 via-blue-50 to-green-100">
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <div className="text-8xl mb-6">🌾</div>
          <h1 className="text-6xl font-bold text-gray-900 mb-6">
            FertiSmart
          </h1>
          <p className="text-2xl text-gray-600 mb-4 max-w-3xl mx-auto">
            Smart Crop Recommendation System
          </p>
          <p className="text-xl text-gray-500 mb-12 max-w-2xl mx-auto">
            Get AI-powered crop recommendations based on your soil and climate conditions using Random Forest Classification
          </p>
          
          <Link href="/predict">
            <Button className="bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white text-xl px-12 py-6 rounded-full shadow-2xl transform hover:scale-105 transition-all">
              🚀 Get Crop Recommendation
            </Button>
          </Link>
        </div>

        {/* Features */}
        <div className="mt-24 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white rounded-xl shadow-lg p-8 text-center transform hover:scale-105 transition-all">
            <div className="text-5xl mb-4">🤖</div>
            <h3 className="text-2xl font-bold text-gray-900 mb-3">
              Random Forest AI
            </h3>
            <p className="text-gray-600">
              Advanced machine learning algorithm trained on thousands of crop samples for accurate predictions
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-8 text-center transform hover:scale-105 transition-all">
            <div className="text-5xl mb-4">📊</div>
            <h3 className="text-2xl font-bold text-gray-900 mb-3">
              Data-Driven Insights
            </h3>
            <p className="text-gray-600">
              Analyzes soil nutrients (NPK), climate conditions, pH levels, and rainfall patterns
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-8 text-center transform hover:scale-105 transition-all">
            <div className="text-5xl mb-4">🎯</div>
            <h3 className="text-2xl font-bold text-gray-900 mb-3">
              Precise Recommendations
            </h3>
            <p className="text-gray-600">
              Get top crop suggestions with confidence scores and detailed explanations
            </p>
          </div>
        </div>

        {/* How It Works */}
        <div className="mt-24">
          <h2 className="text-4xl font-bold text-center text-gray-900 mb-12">
            How It Works
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="w-16 h-16 bg-green-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                1
              </div>
              <h4 className="text-lg font-semibold text-gray-900 mb-2">Enter Data</h4>
              <p className="text-gray-600">Input your soil nutrients and climate conditions</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                2
              </div>
              <h4 className="text-lg font-semibold text-gray-900 mb-2">AI Analysis</h4>
              <p className="text-gray-600">Random Forest algorithm analyzes your conditions</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                3
              </div>
              <h4 className="text-lg font-semibold text-gray-900 mb-2">Get Results</h4>
              <p className="text-gray-600">Receive top crop recommendations with confidence scores</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-orange-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                4
              </div>
              <h4 className="text-lg font-semibold text-gray-900 mb-2">Make Decision</h4>
              <p className="text-gray-600">Choose the best crop for optimal yield</p>
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="mt-24 bg-white rounded-2xl shadow-2xl p-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div className="text-5xl font-bold text-green-600 mb-2">95%+</div>
              <div className="text-gray-600 text-lg">Model Accuracy</div>
            </div>
            <div>
              <div className="text-5xl font-bold text-blue-600 mb-2">22</div>
              <div className="text-gray-600 text-lg">Crops Supported</div>
            </div>
            <div>
              <div className="text-5xl font-bold text-purple-600 mb-2">7</div>
              <div className="text-gray-600 text-lg">Input Parameters</div>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="mt-24 text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">
            Ready to Find Your Perfect Crop?
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Start making data-driven farming decisions today
          </p>
          <Link href="/predict">
            <Button className="bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white text-xl px-12 py-6 rounded-full shadow-2xl transform hover:scale-105 transition-all">
              Start Now →
            </Button>
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 mt-24">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-gray-400">
            © 2025 FertiSmart - Smart Crop Recommendation System
          </p>
          <p className="text-gray-500 mt-2">
            Powered by Random Forest Classification Algorithm
          </p>
        </div>
      </footer>
    </main>
  )
}