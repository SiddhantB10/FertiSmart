import { Navbar } from '@/components/Layout/Navbar'
import { Footer } from '@/components/Layout/Footer'

export default function UploadPage() {
  return (
    <main className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Upload Soil Data
          </h1>
          <p className="text-lg text-gray-600">
            Upload your soil sample data for analysis and personalized fertilizer recommendations.
          </p>
        </div>

        {/* Upload Form */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <form className="space-y-6">
            {/* File Upload */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Soil Data File (CSV, Excel)
              </label>
              <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-lg hover:border-primary-400 transition-colors">
                <div className="space-y-1 text-center">
                  <svg
                    className="mx-auto h-12 w-12 text-gray-400"
                    stroke="currentColor"
                    fill="none"
                    viewBox="0 0 48 48"
                    aria-hidden="true"
                  >
                    <path
                      d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                      strokeWidth={2}
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                  <div className="flex text-sm text-gray-600">
                    <label
                      htmlFor="file-upload"
                      className="relative cursor-pointer bg-white rounded-md font-medium text-primary-600 hover:text-primary-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-primary-500"
                    >
                      <span>Upload a file</span>
                      <input id="file-upload" name="file-upload" type="file" className="sr-only" accept=".csv,.xlsx,.xls" />
                    </label>
                    <p className="pl-1">or drag and drop</p>
                  </div>
                  <p className="text-xs text-gray-500">CSV, Excel up to 10MB</p>
                </div>
              </div>
            </div>

            {/* Sample Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="location" className="block text-sm font-medium text-gray-700">
                  Sample Location
                </label>
                <input
                  type="text"
                  name="location"
                  id="location"
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  placeholder="Enter field location"
                />
              </div>

              <div>
                <label htmlFor="collection-date" className="block text-sm font-medium text-gray-700">
                  Collection Date
                </label>
                <input
                  type="date"
                  name="collection-date"
                  id="collection-date"
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                />
              </div>

              <div>
                <label htmlFor="depth" className="block text-sm font-medium text-gray-700">
                  Sample Depth (cm)
                </label>
                <input
                  type="number"
                  name="depth"
                  id="depth"
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  placeholder="15"
                />
              </div>

              <div>
                <label htmlFor="crop-type" className="block text-sm font-medium text-gray-700">
                  Intended Crop
                </label>
                <select
                  id="crop-type"
                  name="crop-type"
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                >
                  <option value="">Select crop type</option>
                  <option value="wheat">Wheat</option>
                  <option value="rice">Rice</option>
                  <option value="corn">Corn</option>
                  <option value="soybean">Soybean</option>
                  <option value="vegetables">Vegetables</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>

            {/* Additional Notes */}
            <div>
              <label htmlFor="notes" className="block text-sm font-medium text-gray-700">
                Additional Notes
              </label>
              <textarea
                id="notes"
                name="notes"
                rows={3}
                className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                placeholder="Any additional information about the soil sample..."
              />
            </div>

            {/* Submit Button */}
            <div className="flex justify-end">
              <button
                type="submit"
                className="ml-3 inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Upload and Analyze
              </button>
            </div>
          </form>
        </div>

        {/* Sample Data Format */}
        <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Expected Data Format
          </h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Column Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Data Type
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Example
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Description
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">pH</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Decimal</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">6.5</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Soil pH level</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Nitrogen</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Decimal</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">45.2</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Nitrogen content (mg/kg)</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Phosphorus</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Decimal</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">23.8</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Phosphorus content (mg/kg)</td>
                </tr>
                <tr>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">Potassium</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Decimal</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">112.5</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">Potassium content (mg/kg)</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <Footer />
    </main>
  )
}