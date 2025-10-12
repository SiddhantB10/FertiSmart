import { Navbar } from '@/components/Layout/Navbar'
import { Footer } from '@/components/Layout/Footer'

export default function SchemaPage() {
  return (
    <main className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Database Schema
          </h1>
          <p className="text-lg text-gray-600">
            Explore the FertiSmart database structure and relationships.
          </p>
        </div>

        {/* Schema Overview */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Schema Overview
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Tables */}
            <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
              <h3 className="font-semibold text-blue-900 mb-3">Core Tables</h3>
              <ul className="space-y-2 text-sm text-blue-800">
                <li>• soil_samples</li>
                <li>• soil_analysis</li>
                <li>• fertilizer_recommendations</li>
                <li>• crop_data</li>
              </ul>
            </div>

            <div className="bg-green-50 rounded-lg p-4 border border-green-200">
              <h3 className="font-semibold text-green-900 mb-3">Fact Tables</h3>
              <ul className="space-y-2 text-sm text-green-800">
                <li>• fact_soil_analysis</li>
                <li>• fact_recommendations</li>
                <li>• fact_yield_performance</li>
              </ul>
            </div>

            <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
              <h3 className="font-semibold text-purple-900 mb-3">Dimension Tables</h3>
              <ul className="space-y-2 text-sm text-purple-800">
                <li>• dim_location</li>
                <li>• dim_time</li>
                <li>• dim_fertilizer_type</li>
                <li>• dim_crop_variety</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Schema Details */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Table Relationships
          </h2>
          
          <div className="space-y-6">
            {/* Soil Samples Table */}
            <div className="border border-gray-200 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">soil_samples</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Primary Key</h4>
                  <p className="text-sm text-gray-600">sample_id (INTEGER)</p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Key Attributes</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• location_coordinates</li>
                    <li>• collection_date</li>
                    <li>• sample_depth</li>
                    <li>• field_conditions</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Soil Analysis Table */}
            <div className="border border-gray-200 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">soil_analysis</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Foreign Key</h4>
                  <p className="text-sm text-gray-600">sample_id → soil_samples.sample_id</p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Analysis Parameters</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• ph_level (DECIMAL)</li>
                    <li>• nitrogen_content (DECIMAL)</li>
                    <li>• phosphorus_content (DECIMAL)</li>
                    <li>• potassium_content (DECIMAL)</li>
                    <li>• organic_matter (DECIMAL)</li>
                    <li>• moisture_level (DECIMAL)</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Recommendations Table */}
            <div className="border border-gray-200 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">fertilizer_recommendations</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Foreign Key</h4>
                  <p className="text-sm text-gray-600">sample_id → soil_samples.sample_id</p>
                </div>
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Recommendation Data</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• fertilizer_type (VARCHAR)</li>
                    <li>• application_rate (DECIMAL)</li>
                    <li>• application_method (VARCHAR)</li>
                    <li>• timing_recommendation (VARCHAR)</li>
                    <li>• expected_yield_improvement (DECIMAL)</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </main>
  )
}