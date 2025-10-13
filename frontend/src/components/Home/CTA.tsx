import Link from 'next/link'

export function CTA() {
  return (
    <section className="py-24 bg-gradient-to-br from-emerald-600 via-emerald-700 to-teal-800 dark:from-emerald-800 dark:via-emerald-900 dark:to-teal-900">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div className="bg-white/10 dark:bg-white/5 backdrop-blur-sm rounded-3xl p-12 border border-white/20 dark:border-white/10">
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-6 font-display">
            Ready to Transform Your Farming?
          </h2>
          
          <p className="text-xl text-emerald-100 dark:text-emerald-200 mb-8 max-w-2xl mx-auto leading-relaxed">
            Join thousands of farmers who are already using FertiSmart to optimize their 
            soil health, increase crop yields, and practice sustainable agriculture.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-8">
            <Link 
              href="/crop-recommendation" 
              className="btn-primary bg-white dark:bg-gray-100 text-emerald-700 dark:text-emerald-800 hover:bg-gray-100 dark:hover:bg-white px-8 py-4 text-lg font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 inline-flex items-center"
            >
              <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014.846 17H9.154a3.374 3.374 0 00-1.849-.547l-.548-.547z" />
              </svg>
              Get Crop Recommendation
            </Link>
            
            <Link 
              href="/crop-recommendation" 
              className="btn-outline border-white/30 dark:border-white/20 text-white hover:bg-white hover:text-emerald-700 dark:hover:text-emerald-800 px-8 py-4 text-lg font-semibold rounded-xl transition-all duration-200 inline-flex items-center backdrop-blur-sm"
            >
              <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              View Demo
            </Link>
          </div>

          {/* Features List */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 text-left">
            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-6 h-6 bg-teal-400 dark:bg-teal-500 rounded-full flex items-center justify-center mt-0.5">
                <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </div>
              <div>
                <h3 className="text-white font-semibold mb-1">Instant Analysis</h3>
                <p className="text-emerald-200 dark:text-emerald-300 text-sm">Get soil analysis results in seconds</p>
              </div>
            </div>

            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-6 h-6 bg-teal-400 dark:bg-teal-500 rounded-full flex items-center justify-center mt-0.5">
                <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </div>
              <div>
                <h3 className="text-white font-semibold mb-1">AI Recommendations</h3>
                <p className="text-emerald-200 dark:text-emerald-300 text-sm">Personalized fertilizer suggestions</p>
              </div>
            </div>

            <div className="flex items-start space-x-3">
              <div className="flex-shrink-0 w-6 h-6 bg-teal-400 dark:bg-teal-500 rounded-full flex items-center justify-center mt-0.5">
                <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
              </div>
              <div>
                <h3 className="text-white font-semibold mb-1">Data Insights</h3>
                <p className="text-emerald-200 dark:text-emerald-300 text-sm">Comprehensive analytics dashboard</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}