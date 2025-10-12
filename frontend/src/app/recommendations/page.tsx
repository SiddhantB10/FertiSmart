import { Navbar } from '@/components/Layout/Navbar'
import { Footer } from '@/components/Layout/Footer'

export default function RecommendationsPage() {
  return (
    <main className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Fertilizer Recommendations
          </h1>
          <p className="text-lg text-gray-600">
            Get personalized fertilizer recommendations based on your soil analysis data.
          </p>
        </div>

        {/* Recommendations Dashboard */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Smart Recommendations
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Sample recommendation cards */}
            <div className="bg-primary-50 rounded-lg p-4 border border-primary-200">
              <h3 className="font-semibold text-primary-900 mb-2">NPK Fertilizer</h3>
              <p className="text-primary-700 text-sm mb-2">
                Recommended for balanced nutrition
              </p>
              <div className="text-primary-600 text-sm">
                Application: 25 kg/hectare
              </div>
            </div>

            <div className="bg-secondary-50 rounded-lg p-4 border border-secondary-200">
              <h3 className="font-semibold text-secondary-900 mb-2">Organic Compost</h3>
              <p className="text-secondary-700 text-sm mb-2">
                Improves soil structure and fertility
              </p>
              <div className="text-secondary-600 text-sm">
                Application: 2-3 tons/hectare
              </div>
            </div>

            <div className="bg-accent-50 rounded-lg p-4 border border-accent-200">
              <h3 className="font-semibold text-accent-900 mb-2">Micronutrient Mix</h3>
              <p className="text-accent-700 text-sm mb-2">
                Essential trace elements for growth
              </p>
              <div className="text-accent-600 text-sm">
                Application: 5 kg/hectare
              </div>
            </div>
          </div>

          <div className="mt-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Recommendation Details
            </h3>
            <div className="prose max-w-none">
              <p className="text-gray-600">
                Based on your soil analysis, we recommend a balanced approach combining synthetic 
                and organic fertilizers. The soil shows moderate nitrogen levels but requires 
                phosphorus supplementation for optimal crop yield.
              </p>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </main>
  )
}