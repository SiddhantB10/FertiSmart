import type { Metadata, Viewport } from 'next'
import { Inter } from 'next/font/google'
import '../styles/globals.css'
import { Providers } from './providers'
import { ThemeProvider } from '../contexts/ThemeContext'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'FertiSmart - Smart Fertilizer Recommendation System',
  description: 'Data-driven soil analysis and intelligent fertilizer recommendations for modern agriculture',
  keywords: ['agriculture', 'soil analysis', 'fertilizer', 'machine learning', 'farming'],
  authors: [{ name: 'FertiSmart Team' }],
  manifest: '/manifest.json',
  appleWebApp: {
    capable: true,
    statusBarStyle: 'default',
    title: 'FertiSmart',
  },
  formatDetection: {
    telephone: false,
  },
  openGraph: {
    type: 'website',
    siteName: 'FertiSmart',
    title: 'FertiSmart - Smart Fertilizer Recommendation System',
    description: 'Data-driven soil analysis and intelligent fertilizer recommendations',
  },
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
  userScalable: true,
  viewportFit: 'cover',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <head>
        <link rel="icon" href="/favicon.ico" />
        <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <script
          dangerouslySetInnerHTML={{
            __html: `
              try {
                const theme = localStorage.getItem('theme') || 'dark';
                document.documentElement.classList.remove('light', 'dark');
                document.documentElement.classList.add(theme);
              } catch (e) {
                document.documentElement.classList.add('dark');
              }
            `,
          }}
        />
      </head>
      <body className={`${inter.className} bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 antialiased transition-colors duration-300 min-h-screen`} suppressHydrationWarning>
        <ThemeProvider>
          <Providers>
            <div className="relative min-h-screen flex flex-col">
              {children}
            </div>
          </Providers>
        </ThemeProvider>
      </body>
    </html>
  )
}