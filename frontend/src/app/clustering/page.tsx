import { Navbar } from '@/components/Layout/Navbar'
import { Footer } from '@/components/Layout/Footer'

export default function ClusteringPage() {
  return (
    <main className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Soil Clustering Analysis
          </h1>
          <p className="text-lg text-gray-600">
            Discover patterns in your soil data through advanced clustering algorithms.
          </p>
        </div>

        {/* Clustering Dashboard */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Cluster Analysis Results
          </h2>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Cluster Summary */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Identified Clusters
              </h3>
              
              <div className="space-y-4">
                <div className="bg-green-50 rounded-lg p-4 border border-green-200">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-green-900">Cluster 1: High Fertility</h4>
                    <span className="text-sm text-green-700 bg-green-100 px-2 py-1 rounded">
                      32% of samples
                    </span>
                  </div>
                  <p className="text-green-700 text-sm">
                    High NPK levels, optimal pH range (6.5-7.0), excellent organic matter content.
                  </p>
                </div>

                <div className="bg-yellow-50 rounded-lg p-4 border border-yellow-200">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-yellow-900">Cluster 2: Moderate Fertility</h4>
                    <span className="text-sm text-yellow-700 bg-yellow-100 px-2 py-1 rounded">
                      45% of samples
                    </span>
                  </div>
                  <p className="text-yellow-700 text-sm">
                    Moderate nutrient levels, slightly acidic pH, requires balanced fertilization.
                  </p>
                </div>

                <div className="bg-red-50 rounded-lg p-4 border border-red-200">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-semibold text-red-900">Cluster 3: Low Fertility</h4>
                    <span className="text-sm text-red-700 bg-red-100 px-2 py-1 rounded">
                      23% of samples
                    </span>
                  </div>
                  <p className="text-red-700 text-sm">
                    Low nutrient levels, acidic pH, requires intensive soil improvement program.
                  </p>
                </div>
              </div>
            </div>

            {/* Cluster Characteristics */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Cluster Characteristics
              </h3>
              
              <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 rounded-lg">
                <table className="min-w-full divide-y divide-gray-300">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide">
                        Parameter
                      </th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide">
                        Cluster 1
                      </th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide">
                        Cluster 2
                      </th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide">
                        Cluster 3
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    <tr>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900">pH Level</td>
                      <td className="px-4 py-3 text-sm text-gray-500">6.8</td>
                      <td className="px-4 py-3 text-sm text-gray-500">6.2</td>
                      <td className="px-4 py-3 text-sm text-gray-500">5.4</td>
                    </tr>
                    <tr>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900">Nitrogen (N)</td>
                      <td className="px-4 py-3 text-sm text-gray-500">High</td>
                      <td className="px-4 py-3 text-sm text-gray-500">Medium</td>
                      <td className="px-4 py-3 text-sm text-gray-500">Low</td>
                    </tr>
                    <tr>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900">Phosphorus (P)</td>
                      <td className="px-4 py-3 text-sm text-gray-500">High</td>
                      <td className="px-4 py-3 text-sm text-gray-500">Medium</td>
                      <td className="px-4 py-3 text-sm text-gray-500">Low</td>
                    </tr>
                    <tr>
                      <td className="px-4 py-3 text-sm font-medium text-gray-900">Potassium (K)</td>
                      <td className="px-4 py-3 text-sm text-gray-500">High</td>
                      <td className="px-4 py-3 text-sm text-gray-500">Medium</td>
                      <td className="px-4 py-3 text-sm text-gray-500">Low</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </main>
  )
}