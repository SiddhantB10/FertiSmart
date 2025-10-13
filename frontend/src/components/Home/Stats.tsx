const stats = [
  {
    number: '98%',
    label: 'Prediction Accuracy',
    description: 'Our ML models achieve high accuracy in crop and fertilizer recommendations'
  },
  {
    number: '7',
    label: 'DMBI Experiments',
    description: 'Complete implementation of all Data Mining and Business Intelligence experiments'
  },
  {
    number: '1000+',
    label: 'Soil Samples',
    description: 'Extensive dataset for training and validation of machine learning models'
  },
  {
    number: '5',
    label: 'ML Algorithms',
    description: 'Decision Tree, Naive Bayes, K-Means, Agglomerative, and DBSCAN clustering'
  }
]

export function Stats() {
  return (
    <section className="py-16 bg-gray-50 dark:bg-gray-900 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4 font-display">
            Trusted by Agricultural Professionals
          </h2>
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Our platform delivers reliable insights backed by advanced data science 
            and comprehensive agricultural research.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {stats.map((stat, index) => (
            <div 
              key={stat.label}
              className="text-center group animate-fade-in"
              style={{ animationDelay: `${index * 0.2}s` }}
            >
              <div className="bg-white dark:bg-gray-800 rounded-2xl p-8 shadow-soft hover:shadow-medium dark:shadow-emerald-500/10 transition-shadow duration-300 border border-gray-100 dark:border-gray-700">
                <div className="text-4xl md:text-5xl font-bold text-emerald-600 dark:text-emerald-400 mb-2 font-display group-hover:scale-110 transition-transform duration-200">
                  {stat.number}
                </div>
                <div className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                  {stat.label}
                </div>
                <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
                  {stat.description}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Additional Metrics */}
        <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-emerald-100 dark:bg-emerald-900/20 rounded-full mb-4">
              <svg className="w-8 h-8 text-emerald-600 dark:text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Data Quality</h3>
            <p className="text-gray-600 dark:text-gray-300">Comprehensive preprocessing ensures clean, reliable data for analysis</p>
          </div>

          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-teal-100 dark:bg-teal-900/20 rounded-full mb-4">
              <svg className="w-8 h-8 text-teal-600 dark:text-teal-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Real-time Analysis</h3>
            <p className="text-gray-600 dark:text-gray-300">Get instant soil analysis and recommendations powered by ML</p>
          </div>

          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 dark:bg-blue-900/20 rounded-full mb-4">
              <svg className="w-8 h-8 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Sustainable Farming</h3>
            <p className="text-gray-600 dark:text-gray-300">Promote eco-friendly agriculture through optimized resource usage</p>
          </div>
        </div>
      </div>
    </section>
  )
}