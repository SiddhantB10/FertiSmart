import { 
  CpuChipIcon,
  ChartBarIcon,
  BeakerIcon,
  ClipboardDocumentListIcon,
  CloudIcon,
  ShieldCheckIcon
} from '@heroicons/react/24/outline'

const features = [
  {
    title: 'Smart Soil Analysis',
    description: 'Advanced machine learning algorithms analyze your soil composition including NPK levels, pH, temperature, humidity, and rainfall patterns.',
    icon: BeakerIcon,
    color: 'bg-primary-500'
  },
  {
    title: 'AI-Powered Recommendations',
    description: 'Get personalized fertilizer recommendations using Decision Tree and Naive Bayes classification models trained on extensive agricultural data.',
    icon: CpuChipIcon,
    color: 'bg-secondary-500'
  },
  {
    title: 'Interactive Dashboard',
    description: 'Visualize your data through comprehensive charts, correlations, and trends. Explore EDA insights and business intelligence reports.',
    icon: ChartBarIcon,
    color: 'bg-accent-500'
  },
  {
    title: 'Clustering Analysis',
    description: 'Discover soil patterns using K-Means, Agglomerative, and DBSCAN clustering to identify distinct soil types and fertility zones.',
    icon: CloudIcon,
    color: 'bg-purple-500'
  },
  {
    title: 'Data Preprocessing',
    description: 'Automated data cleaning, normalization, and quality assessment ensures accurate analysis and reliable recommendations.',
    icon: ClipboardDocumentListIcon,
    color: 'bg-green-500'
  },
  {
    title: 'Enterprise Ready',
    description: 'Built with robust data warehouse design using Star and Snowflake schemas. Scalable architecture for agricultural enterprises.',
    icon: ShieldCheckIcon,
    color: 'bg-indigo-500'
  }
]

export function Features() {
  return (
    <section className="py-24 bg-white dark:bg-gray-900 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white mb-4 font-display">
            Powerful Features for Modern Agriculture
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Comprehensive suite of tools combining data science, machine learning, 
            and agricultural expertise to revolutionize farming decisions.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div 
              key={feature.title}
              className="group relative bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-8 hover:border-emerald-200 dark:hover:border-emerald-500/50 hover:shadow-lg dark:hover:shadow-emerald-500/10 transition-all duration-300 animate-fade-in"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              {/* Icon */}
              <div className={`inline-flex items-center justify-center w-12 h-12 rounded-lg ${feature.color} mb-6 group-hover:scale-110 transition-transform duration-200`}>
                <feature.icon className="w-6 h-6 text-white" />
              </div>

              {/* Content */}
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 group-hover:text-emerald-600 dark:group-hover:text-emerald-400 transition-colors">
                {feature.title}
              </h3>
              
              <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                {feature.description}
              </p>

              {/* Hover Effect */}
              <div className="absolute inset-0 bg-gradient-to-br from-emerald-50 dark:from-emerald-900/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-xl pointer-events-none"></div>
            </div>
          ))}
        </div>

        {/* Call to Action */}
        <div className="mt-16 text-center">
          <div className="inline-flex items-center space-x-4 p-6 bg-gradient-to-r from-emerald-50 to-teal-50 dark:from-emerald-900/20 dark:to-teal-900/20 rounded-2xl border border-emerald-100 dark:border-emerald-800">
            <div className="flex-shrink-0">
              <div className="w-16 h-16 bg-emerald-600 dark:bg-emerald-500 rounded-full flex items-center justify-center">
                <BeakerIcon className="w-8 h-8 text-white" />
              </div>
            </div>
            <div className="text-left">
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-1">
                Ready to optimize your farming?
              </h3>
              <p className="text-gray-600 dark:text-gray-300">
                Start analyzing your soil data and get personalized recommendations.
              </p>
            </div>
            <div className="flex-shrink-0">
              <a 
                href="/upload" 
                className="btn-primary px-8 py-3 font-semibold hover:shadow-lg transform hover:scale-105 transition-all duration-200"
              >
                Get Started
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}