import { Navbar } from '@/components/Layout/Navbar'
import { Hero } from '@/components/Home/Hero'
import { Features } from '@/components/Home/Features'
import { Stats } from '@/components/Home/Stats'
import { CTA } from '@/components/Home/CTA'
import { Footer } from '@/components/Layout/Footer'

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gray-50">
      <Navbar />
      <Hero />
      <Features />
      <Stats />
      <CTA />
      <Footer />
    </main>
  )
}