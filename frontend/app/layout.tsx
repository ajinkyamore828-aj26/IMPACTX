import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import '@/styles/globals.css'

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' })

export const metadata: Metadata = {
  title: 'impactx - Architecture Intelligence',
  description: 'ML-Based Code Change Impact and Unused Code Prediction System',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="bg-bg-page text-text-primary min-h-screen font-sans">{children}</body>
    </html>
  )
}
